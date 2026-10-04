"""受限执行器：带时间/内存限制地运行选手程序。

Windows 上不引入 Job Object 等复杂机制，采用：
  - 独立子进程 + 独立工作目录
  - 超时 kill（超时判定 TLE）
  - 通过 psutil 采样峰值内存（无 psutil 时退化为仅时间判限）
  - 输出截断，防止海量输出打爆内存

这是**教学/本地开发级**沙箱，不是对抗恶意代码的安全沙箱。
公网部署时应改用容器/隔离环境（见 README 的安全说明）。
"""
from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

IS_WINDOWS = os.name == "nt"

try:  # 可选依赖
    import psutil  # type: ignore
    _HAS_PSUTIL = True
except ImportError:  # pragma: no cover
    psutil = None  # type: ignore
    _HAS_PSUTIL = False

# 输出上限：超过即截断（同时视为输出超限）
MAX_OUTPUT_BYTES = 16 * 1024 * 1024

# ---------------------------------------------------------------- Windows 崩溃抑制
# 程序因访问违例等异常崩溃时，Windows 会启动 Windows 错误报告（WER / WerFault.exe）
# 去检查并收集崩溃转储。WER 会**持有崩溃进程的句柄**，导致父进程的 poll() 迟迟不返回，
# 我们的监控循环便会误判为「超时」（TLE），把本该是 RE 的提交错判成 TLE。
# 关闭错误对话框后，崩溃进程会立即以异常退出码结束，正确落入 RE 分支。
if IS_WINDOWS:
    try:
        import ctypes

        # SEM_FAILCRITICALERRORS(1) | SEM_NOGPFAULTERRORBOX(2) | SEM_NOALIGNMENTFAULTEXCEPT(4)
        _SEM_FLAGS = 0x0001 | 0x0002 | 0x0004
        # 该设置由当前进程及其子进程继承，因此对判题子进程同样生效
        ctypes.windll.kernel32.SetErrorMode(_SEM_FLAGS)
        # 关闭「弹出调试器」的默认行为，避免挂起
        _prev = ctypes.c_int(0)
        ctypes.windll.kernel32.SetThreadErrorMode(_SEM_FLAGS, ctypes.byref(_prev))
    except Exception:  # pragma: no cover - 非致命，失败时退化为原行为
        pass

    # 子进程不弹控制台窗口，减少句柄与启动开销
    _CREATE_NO_WINDOW = 0x08000000
else:  # pragma: no cover
    _CREATE_NO_WINDOW = 0


@dataclass
class RunResult:
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    time: float = 0.0          # 墙钟时间（秒）
    memory_kb: int = 0         # 峰值内存（KB），无 psutil 时为 0
    timed_out: bool = False
    oom: bool = False
    output_truncated: bool = False
    error: str = ""


def _kill_tree(proc: "subprocess.Popen") -> None:
    """杀掉进程及其子进程。"""
    try:
        if _HAS_PSUTIL:
            parent = psutil.Process(proc.pid)
            for child in parent.children(recursive=True):
                try:
                    child.kill()
                except Exception:
                    pass
            parent.kill()
        else:
            proc.kill()
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def run_program(
    exe: Path,
    stdin_data: str,
    work_dir: Path,
    time_limit: float = 2.0,
    memory_limit_mb: int = 256,
    env: Optional[dict] = None,
    fast_fail: bool = False,
) -> RunResult:
    """运行可执行文件，喂入 stdin，收集 stdout/stderr 与资源占用。

    :param fast_fail: 为 True 时不做超时复核（用于「仅测样例」等追求速度的场景）。
    """
    work_dir.mkdir(parents=True, exist_ok=True)

    run_env = dict(os.environ)
    # 清理可能干扰判题的环境变量
    run_env.pop("PYTHONPATH", None)
    if env:
        run_env.update(env)

    # ---------------------------------------------------------------- 说明
    # 超时判定采用「一次判定 + 一次复核」策略：
    # 判题机负载较高时，正常程序也可能因调度延迟而短暂超出时限，
    # 造成偶发的 TLE 误判。因此在首次超时后等待片刻重跑一次，
    # 若再次超时（或复核时同样超时）才最终判定 TLE。
    # 复核开销只发生在「疑似超时」的少数提交上，对正常提交无影响。
    attempts = 0
    max_attempts = 1 if fast_fail else 2

    while True:
        attempts += 1
        res = _run_once(
            exe, stdin_data, work_dir, time_limit, run_env,
            memory_limit_mb=memory_limit_mb,
        )

        # 只有「疑似超时」才需要复核；其余情况直接返回
        if not res.timed_out or attempts >= max_attempts:
            return res

        # 疑似超时：清理后短暂等待，再跑一次
        time.sleep(0.15)


def _run_once(
    exe: Path,
    stdin_data: str,
    work_dir: Path,
    time_limit: float,
    run_env: dict,
    memory_limit_mb: int = 256,
) -> RunResult:
    """执行一次程序，返回运行结果。"""
    try:
        proc = subprocess.Popen(
            [str(exe)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(work_dir),
            env=run_env,
            creationflags=_CREATE_NO_WINDOW,
        )
    except OSError as exc:
        return RunResult(error=f"无法启动程序：{exc}", exit_code=None)

    start = time.perf_counter()
    peak_kb = 0
    timed_out = False
    oom = False

    # 写入 stdin（可能阻塞，用线程避免死锁）
    import threading

    def _write_input() -> None:
        try:
            assert proc.stdin is not None
            proc.stdin.write(stdin_data.encode("utf-8", errors="replace"))
            proc.stdin.close()
        except Exception:
            pass

    writer = threading.Thread(target=_write_input, daemon=True)
    writer.start()

    # 采集 stdout/stderr（同样用线程）
    out_chunks: list[bytes] = []
    err_chunks: list[bytes] = []
    out_len = 0
    truncated = False

    def _reader(pipe, chunks, limit_flag: list) -> None:
        nonlocal out_len, truncated
        try:
            for chunk in iter(lambda: pipe.read(65536), b""):
                if chunks is out_chunks:
                    out_len += len(chunk)
                    if out_len > MAX_OUTPUT_BYTES:
                        truncated = True
                        break
                chunks.append(chunk)
        except Exception:
            pass
        finally:
            try:
                pipe.close()
            except Exception:
                pass

    t_out = threading.Thread(target=_reader, args=(proc.stdout, out_chunks, []), daemon=True)
    t_err = threading.Thread(target=_reader, args=(proc.stderr, err_chunks, []), daemon=True)
    t_out.start()
    t_err.start()

    # 监控循环
    deadline = start + time_limit
    poll_interval = 0.005

    while True:
        rc = proc.poll()
        if rc is not None:
            break

        now = time.perf_counter()
        if now - start > time_limit:
            # 超时前的「宽限检查」：负载较高时，崩溃进程的退出码可能姗姗来迟。
            # 先给系统一点时间回收，若进程其实已经结束，就直接采用其退出码，
            # 避免把 RE（崩溃）错判成 TLE（超时）。
            for _ in range(10):  # 最多再等 ~100ms
                if proc.poll() is not None:
                    break
                time.sleep(0.01)

            if proc.poll() is None:
                timed_out = True
                _kill_tree(proc)
                proc.wait(timeout=5)
            break

        if _HAS_PSUTIL:
            try:
                p = psutil.Process(proc.pid)
                mem_kb = p.memory_info().rss // 1024
                # 计入子进程
                for child in p.children(recursive=True):
                    try:
                        mem_kb += child.memory_info().rss // 1024
                    except Exception:
                        pass
                peak_kb = max(peak_kb, mem_kb)
                if memory_limit_mb and mem_kb > memory_limit_mb * 1024:
                    oom = True
                    _kill_tree(proc)
                    proc.wait(timeout=5)
                    break
            except Exception:
                pass

        # 自适应轮询：前 50ms 密集，之后放宽，降低 CPU 占用
        elapsed = now - start
        time.sleep(poll_interval if elapsed < 0.05 else 0.002)

    wall = time.perf_counter() - start
    t_out.join(timeout=3)
    t_err.join(timeout=3)
    writer.join(timeout=1)

    stdout = b"".join(out_chunks).decode("utf-8", errors="replace")
    stderr = b"".join(err_chunks).decode("utf-8", errors="replace")
    if truncated:
        stdout += "\n…（输出超过 16MB 已截断）"

    return RunResult(
        exit_code=proc.returncode,
        stdout=stdout,
        stderr=stderr,
        time=wall,
        memory_kb=peak_kb,
        timed_out=timed_out,
        oom=oom,
        output_truncated=truncated,
    )


def has_memory_tracking() -> bool:
    return _HAS_PSUTIL
