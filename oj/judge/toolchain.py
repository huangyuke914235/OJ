"""编译器/运行时探测与调用。

设计目标
--------
1. **零外部依赖**：不要求用户额外安装 MinGW / TDM-GCC。
2. **自动探测**：优先使用系统已装的 g++ / clang++，其次回退到
   Visual Studio 自带的 MSVC（Windows 上最常见的可用编译器）。
3. **统一接口**：对外只暴露 ``compile(source, exe) -> CompileResult``。

由于 MSVC 的 ``cl.exe`` 需要 vcvars 环境（PATH/INCLUDE/LIB），
而 Windows SDK 的自动探测依赖注册表（可能不可用），
本模块通过显式构造环境变量来调用 ``cl.exe``，不依赖 ``vcvars64.bat``。
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

IS_WINDOWS = sys.platform.startswith("win")

# MSVC / Windows SDK 常见安装位置
_VS_ROOTS = [
    r"C:\Program Files\Microsoft Visual Studio\2022",
    r"C:\Program Files (x86)\Microsoft Visual Studio\2022",
    r"C:\Program Files\Microsoft Visual Studio\2019",
    r"C:\Program Files (x86)\Microsoft Visual Studio\2019",
]
_SDK_ROOT = r"C:\Program Files (x86)\Windows Kits\10"


@dataclass
class Toolchain:
    """一个可用的编译工具链。"""

    name: str                 # 展示名，如 "GCC 13.2" / "MSVC 19.44"
    kind: str                 # "gcc" | "clang" | "msvc"
    compiler: str             # 编译器可执行文件绝对路径
    env: Dict[str, str] = field(default_factory=dict)  # 额外环境变量

    @property
    def display(self) -> str:
        return self.name


@dataclass
class CompileResult:
    ok: bool
    exe: Optional[Path] = None
    stdout: str = ""
    stderr: str = ""
    command: List[str] = field(default_factory=list)
    duration: float = 0.0

    @property
    def message(self) -> str:
        return (self.stderr or self.stdout or "").strip()


# ---------------------------------------------------------------- 探测

def _probe_gcc_style(exe: str, kind: str) -> Optional[Toolchain]:
    """探测 g++/clang++，返回版本信息。"""
    try:
        out = subprocess.run(
            [exe, "--version"],
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    first = (out.stdout or "").splitlines()[0] if out.stdout else kind
    return Toolchain(name=f"{first.strip()}", kind=kind, compiler=exe)


def _probe_msvc() -> Optional[Toolchain]:
    """探测 MSVC cl.exe 及其所需的环境变量。"""
    cl = _find_cl_exe()
    if not cl:
        return None

    # cl.exe 位于 .../VC/Tools/MSVC/<ver>/bin/Hostx64/x64/cl.exe
    msvc_ver_dir = cl.parent.parent.parent.parent
    inc = msvc_ver_dir / "include"
    lib = msvc_ver_dir / "lib" / "x64"
    if not inc.exists() or not lib.exists():
        return None

    sdk_inc, sdk_lib = _find_sdk_paths()
    if not sdk_inc or not sdk_lib:
        return None

    include = ";".join(
        [
            str(inc),
            str(msvc_ver_dir / "ATLMFC" / "include"),
            str(sdk_inc / "ucrt"),
            str(sdk_inc / "um"),
            str(sdk_inc / "shared"),
            str(sdk_inc / "winrt"),
            str(sdk_inc / "cppwinrt"),
        ]
    )
    libs = ";".join(
        [
            str(lib),
            str(sdk_lib / "ucrt" / "x64"),
            str(sdk_lib / "um" / "x64"),
        ]
    )

    # cl.exe 自身依赖 PATH 中的 dll（mspdbcore.dll 等）
    extra_path = [
        str(cl.parent),
        str(msvc_ver_dir / "bin" / "Hostx64" / "x64"),
    ]
    env = {
        "INCLUDE": include,
        "LIB": libs,
        "PATH": ";".join(extra_path + [os.environ.get("PATH", "")]),
    }

    ver = msvc_ver_dir.name
    return Toolchain(
        name=f"MSVC {ver} (cl.exe)",
        kind="msvc",
        compiler=str(cl),
        env=env,
    )


def _find_cl_exe() -> Optional[Path]:
    for root in _VS_ROOTS:
        root_path = Path(root)
        if not root_path.exists():
            continue
        # 可能形如 2022/Community、2022/BuildTools、2022/Professional
        for edition in sorted(root_path.iterdir()):
            tools = edition / "VC" / "Tools" / "MSVC"
            if not tools.is_dir():
                continue
            for ver in sorted(tools.iterdir(), reverse=True):
                cl = ver / "bin" / "Hostx64" / "x64" / "cl.exe"
                if cl.exists():
                    return cl
    # 也可能通过 PATH 直接可用
    found = shutil.which("cl")
    return Path(found) if found else None


def _find_sdk_paths() -> tuple[Optional[Path], Optional[Path]]:
    sdk = Path(_SDK_ROOT)
    inc_root = sdk / "Include"
    lib_root = sdk / "Lib"
    if not inc_root.is_dir() or not lib_root.is_dir():
        return None, None
    # 取版本号最高的 SDK
    inc_vers = sorted(
        [p for p in inc_root.iterdir() if (p / "ucrt").is_dir()],
        key=lambda p: p.name,
        reverse=True,
    )
    lib_vers = {p.name for p in lib_root.iterdir() if (p / "ucrt").is_dir()}
    for iv in inc_vers:
        if iv.name in lib_vers:
            return iv, lib_root / iv.name
    return None, None


_TOOLCHAIN_CACHE: Optional[Toolchain] = None
_PROBE_DONE = False


def detect_toolchain(force: bool = False) -> Optional[Toolchain]:
    """探测并缓存可用编译工具链。优先 g++ / clang++，回退 MSVC。"""
    global _TOOLCHAIN_CACHE, _PROBE_DONE
    if _PROBE_DONE and not force:
        return _TOOLCHAIN_CACHE
    _PROBE_DONE = True

    # 允许用户通过环境变量强制指定
    forced = os.environ.get("DSOJ_CXX")
    if forced and Path(forced).exists():
        tc = _probe_gcc_style(forced, "gcc") or _probe_msvc()
        _TOOLCHAIN_CACHE = tc
        return tc

    for exe, kind in (("g++", "gcc"), ("clang++", "clang"), ("c++", "gcc")):
        found = shutil.which(exe)
        if found:
            tc = _probe_gcc_style(found, kind)
            if tc:
                _TOOLCHAIN_CACHE = tc
                return tc

    tc = _probe_msvc()
    _TOOLCHAIN_CACHE = tc
    return tc


def toolchain_info() -> Dict[str, object]:
    """供前端展示的工具链状态。"""
    tc = detect_toolchain()
    if not tc:
        return {
            "available": False,
            "name": "未检测到 C++ 编译器",
            "hint": (
                "请安装以下任一编译器后重启应用：\n"
                "  • MinGW-w64 / TDM-GCC（推荐，安装后把 bin 目录加入 PATH）\n"
                "  • Visual Studio 2022 的「使用 C++ 的桌面开发」工作负载\n"
                "  • LLVM/Clang (clang++)"
            ),
        }
    return {"available": True, "name": tc.name, "kind": tc.kind}


# ---------------------------------------------------------------- 编译

def compile_cpp(
    source_path: Path,
    work_dir: Path,
    toolchain: Optional[Toolchain] = None,
    timeout: float = 60.0,
    standard: str = "c++17",
) -> CompileResult:
    """把 C++ 源码编译为可执行文件。

    gcc/clang: ``-O2 -std=c++17 -o exe source``
    msvc:      ``/O2 /EHsc /std:c++17 source /Fe:exe``
    """
    import time

    tc = toolchain or detect_toolchain()
    if tc is None:
        return CompileResult(
            ok=False,
            stderr="未检测到可用的 C++ 编译器。请先安装 MinGW-w64 或 Visual Studio (C++ 工作负载)。",
        )

    work_dir.mkdir(parents=True, exist_ok=True)
    exe = work_dir / ("main.exe" if IS_WINDOWS else "main.out")

    std_flag = f"-std={standard}" if tc.kind != "msvc" else f"/std:{standard}"

    if tc.kind == "msvc":
        cmd = [
            tc.compiler,
            "/nologo",
            "/O2",
            "/EHsc",
            std_flag,
            str(source_path),
            f"/Fe:{exe}",
        ]
    else:
        cmd = [
            tc.compiler,
            "-O2",
            std_flag,
            "-static",           # 静态链接，避免运行时缺 dll
            "-o",
            str(exe),
            str(source_path),
        ]

    env = dict(os.environ)
    env.update(tc.env)

    start = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired:
        return CompileResult(
            ok=False,
            stderr=f"编译超时（>{timeout:.0f}s）",
            command=cmd,
            duration=time.perf_counter() - start,
        )
    except OSError as exc:
        return CompileResult(ok=False, stderr=f"无法启动编译器：{exc}", command=cmd)

    duration = time.perf_counter() - start
    ok = proc.returncode == 0 and exe.exists()
    return CompileResult(
        ok=ok,
        exe=exe if ok else None,
        stdout=proc.stdout or "",
        stderr=proc.stderr or "",
        command=cmd,
        duration=duration,
    )


def self_test() -> CompileResult:
    """编译运行一个最小程序，验证工具链端到端可用。"""
    tc = detect_toolchain()
    if tc is None:
        return CompileResult(ok=False, stderr="未检测到编译器")

    with tempfile.TemporaryDirectory(prefix="dsoj_selftest_") as tmp:
        tmp_path = Path(tmp)
        src = tmp_path / "selftest.cpp"
        src.write_text(
            "#include <cstdio>\n"
            "int main(){int a,b;if(scanf(\"%d %d\",&a,&b)!=2)return 1;"
            "printf(\"%d\\n\",a+b);return 0;}\n",
            encoding="utf-8",
        )
        res = compile_cpp(src, tmp_path, toolchain=tc)
        if not res.ok:
            return res
        try:
            run = subprocess.run(
                [str(res.exe)],
                input="2 3\n",
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
        except (OSError, subprocess.SubprocessError) as exc:
            return CompileResult(ok=False, stderr=f"运行失败：{exc}")
        if run.stdout.strip() != "5":
            return CompileResult(
                ok=False, stderr=f"自检输出异常：{run.stdout!r}"
            )
        return CompileResult(ok=True, exe=res.exe, stdout="5", stderr="")
