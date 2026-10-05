# 🚀 DS-OJ 部署指南

本项目提供两种互补的公网部署方式，可**同时使用**：

| 方式 | 提供的能力 | 有无后端 | 适用场景 |
|---|---|---|---|
| **GitHub Pages** | 静态题库站：题面、样例、分类浏览 | 无 | 让学生随时查阅题目，零成本、零维护 |
| **Streamlit** | 完整判题：在线编辑、编译、运行、提交 | 需要服务器 | 真实判题（需 C++ 编译器与可执行权限） |

> **核心矛盾**：判题必须**编译并运行**用户提交的 C++ 代码。
> 这要求运行环境具备 C++ 编译器、可写入的临时目录，以及执行子进程的权限。
> 因此纯静态托管（GitHub Pages）只能承载「题面浏览」，无法判题。

---

## 一、GitHub Pages（静态题库站）

### 原理

`scripts/build_static.py` 把 `oj/data/problems/**` 中的题库渲染为静态站点：

```
static/
├── index.html          题目列表（按知识点分类、可搜索）
├── problems/<id>.html  每道题独立页面（题面 + 样例）
├── problems.json       原始题库数据（供前端检索 / 二次开发）
├── style.css
└── .nojekyll           阻止 GitHub Pages 的 Jekyll 处理
```

渲染器为**零第三方依赖**的轻量 Markdown 实现，因此 CI 中无需 `pip install` 任何包。

### 本地预览

```bash
python scripts/build_static.py
# 然后打开 static/index.html
```

### 自动部署（推荐）

> ### ⚠️ 第一步必须先做：启用 Pages 并选择 "GitHub Actions"
>
> **这是最容易踩的坑。** 若跳过此步，工作流会「构建成功、部署失败」——
> `build` 任务全绿，`deploy` 任务报 `Failed to create deployment (status: 404)`，
> 站点始终 404。原因不是代码问题，而是**仓库还没启用 Pages**。
>
> 操作路径（一次性，约 10 秒）：
>
> 1. 打开 `https://github.com/<用户名>/<仓库名>/settings/pages`
> 2. **Build and deployment → Source** → 选择 **GitHub Actions**
>    （**不要**选 "Deploy from a branch"，那会与内置工作流冲突）
> 3. 保存后，到 **Actions** 页面 → 选 **Build and Deploy Static Site to GitHub Pages**
>    → **Re-run all jobs**（或点 **Run workflow** 手动触发）
>
> 验证是否已启用：`GET /repos/<用户名>/<仓库名>/pages` 返回 200（而非 404）。

仓库已内置工作流 `.github/workflows/pages.yml`，触发条件：

- `main` 分支上 `oj/**`（题库、数据模型、站点配置）、构建脚本或工作流本身有改动
- 手动触发（Actions 页面 → **Run workflow**）

部署步骤：

1. 把仓库推送到 GitHub。
2. **按上方 ⚠️ 提示启用 Pages 并选择 GitHub Actions。**
3. 推送到 `main` 分支，或在 Actions 页面手动运行工作流。
4. 稍候片刻，站点发布在
   `https://<用户名>.github.io/<仓库名>/`。

> **提示**：工作流自带一步「预检 — 确认 Pages 已启用」。
> 若检测到未启用，会在日志里给出 `::warning::` 明确提示，而不只是抛出一句难懂的报错。

### 自定义站点信息

站点名称与标语在 `oj/config.py` 中：

```python
SITE_NAME = "DS-OJ"
SITE_SLOGAN = "..."
```

> 改动 `oj/config.py` 后推送到 `main` 会自动触发重新构建
> （`paths` 已放宽为 `oj/**`，覆盖 `config.py`）。

---

## 二、Streamlit（完整判题）

Streamlit 版提供完整 UI：题库筛选、Monaco 代码编辑、运行调试、提交判题、提交记录。

### 方式 A：本地 / 内网服务器（最可靠）

在具备 C++ 编译器的机器上：

```bash
pip install -r requirements.txt
python scripts/validate_problems.py   # 确认编译器就绪、题库正确
streamlit run app.py
```

默认监听 `http://localhost:8501`。如需局域网访问：

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

> 本项目的判题沙箱是**教学/本地开发级**的（子进程隔离 + 超时 kill + 内存采样），
> **不是**对抗恶意代码的安全沙箱。**请勿**直接把这种模式暴露在完全开放的公网。
> 若必须公网提供判题，请按下文 Docker 方案，并配合容器级隔离。

### 方式 B：Streamlit Community Cloud

Streamlit Cloud 免费、部署简单，但有两点**必须注意**：

1. **不保证提供 C++ 编译器。** 其基础镜像通常没有 `g++` / `cl`。
   若检测不到编译器，界面会提示「未找到 C++ 编译器」，只能浏览题目、无法判题。
2. **文件系统是临时的。** 每次重启/重新部署，写入的数据都会丢失，
   提交记录（`oj/data/submissions/`）无法持久化。

若坚持使用，可在仓库根目录添加 `packages.txt` 让 Cloud 安装系统包：

```
g++
```

但即便装上 `g++`，临时文件系统与资源限制仍可能让判题不稳定。
**更推荐方式 A 或方式 C。**

### 方式 C：Docker 部署（公网判题推荐）

在容器内固定编译器版本与隔离边界，再对外提供服务。

`Dockerfile` 示例：

```dockerfile
FROM python:3.11-slim

# 安装 C++ 编译器
RUN apt-get update \
    && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 判题临时目录
RUN mkdir -p /app/.oj_work

EXPOSE 8501
HEALTHCHECK CMD curl -f http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.address=0.0.0.0", "--server.port=8501"]
```

构建与运行：

```bash
docker build -t ds-oj .
docker run -d --name ds-oj \
  -p 8501:8501 \
  --memory=2g --cpus=2 \
  --pids-limit=256 \
  ds-oj
```

进一步收紧隔离（生产环境建议）：

- `--read-only` 配合 `--tmpfs /tmp`，让容器根文件系统不可写；
- `--security-opt no-new-privileges`；
- 限制 `--memory` / `--cpus` / `--pids-limit`，防止 fork 炸弹与内存耗尽；
- 用反向代理（Nginx / Caddy）加 HTTPS 与访问控制。

---

## 三、编译环境说明

判题时程序自动探测本机 C++ 编译器，优先级为 **MSVC → GCC → Clang**，无需手动配置。

| 平台 | 推荐编译器 | 安装要点 |
|---|---|---|
| Windows | MinGW-w64 / TDM-GCC | 安装后将 `bin` 加入 `PATH` |
| Windows | Visual Studio 2022 | 勾选「使用 C++ 的桌面开发」工作负载 |
| Linux | GCC（`g++`） | `apt install g++` / `yum install gcc-c++` |
| macOS | Clang（`clang++`） | 安装 Xcode Command Line Tools |

### Visual Studio / MSVC 的特别说明

MSVC 的 `cl.exe` 需要 `INCLUDE` / `LIB` / `PATH` 环境变量才能找到标准库头文件。
本项目**不依赖** `vcvars64.bat`（该脚本在缺少 Windows SDK 的机器上会失败），
而是直接定位 MSVC 与 Windows SDK 目录，自行拼装编译环境。

验证编译器是否就绪：

```bash
python -c "from oj.judge.toolchain import toolchain_info, self_test; print(toolchain_info()); print('ok=', self_test())"
```

预期输出形如：

```
{'name': 'MSVC 14.44.35207 (cl.exe)', ...}
ok= True
```

> **Windows 崩溃抑制**：判题器会关闭 Windows 错误报告（WER）。
> 否则崩溃的提交会被 `WerFault.exe` 挂住、迟迟不返回退出码，
> 导致 RE（运行时错误）被误判为 TLE（超时）。

---

## 四、判题安全边界（务必阅读）

当前实现的安全措施：

- 独立子进程 + 独立工作目录
- 墙钟超时 kill（含进程树）
- 内存上限采样（需 `psutil`；未安装则仅测时间）
- 输出截断（16MB），防止海量输出打爆内存

**未**提供（公网部署需自行补齐）：

- 系统调用过滤（seccomp / AppArmor）
- 网络隔离
- 文件系统隔离（chroot / 容器）
- 用户权限降级

因此：

- **本地 / 教学 / 内网**：当前实现足够。
- **开放公网**：必须使用容器（方式 C）或更严格的沙箱，
  切勿把裸的 Streamlit 进程直接暴露出去。

---

## 五、常见问题

**Q: GitHub Pages 上能判题吗？**
不能。Pages 只托管静态文件，没有后端、没有编译器。判题需要 Streamlit（方式 A/C）。

**Q: Streamlit Cloud 上编译器检测失败？**
在仓库根目录添加 `packages.txt`（内容 `g++`）后重新部署；
若仍失败，改用 Docker 方案。

**Q: 提交记录会丢吗？**
会。提交记录存于 `oj/data/submissions/`（JSON 文件）。
Streamlit Cloud 的文件系统是临时的，重启即丢失。
需要持久化请用 Docker + 挂载卷：

```bash
docker run -d -v ds_oj_data:/app/oj/data --name ds-oj -p 8501:8501 ds-oj
```

**Q: 为什么崩溃的提交有时被判成超时？**
已修复。原因是 Windows 错误报告（WER）挂住了崩溃进程。
判题器现已关闭 WER，并对疑似超时做宽限检查，确保 RE 被正确识别。

**Q: 静态站点样式/题目没更新？**
工作流的触发路径有限定（见 `pages.yml` 的 `paths`）。
改动不在列出的路径内时不会自动构建，可在 Actions 页面手动 **Run workflow**。
