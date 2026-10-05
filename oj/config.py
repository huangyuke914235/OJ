"""全局配置。

所有路径与判题参数集中在此，frontend / judge / scripts 共用，避免散落。
"""
from __future__ import annotations

import os
from pathlib import Path

# ---------------------------------------------------------------- 路径

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "oj" / "data"
PROBLEMS_DIR = DATA_DIR / "problems"
# 知识点总结（每个分类一份，含题型清单与方法总结）
KNOWLEDGE_DIR = DATA_DIR / "knowledge"
SUBMISSIONS_DB = DATA_DIR / "submissions.json"
STATIC_DIR = PROJECT_ROOT / "static"
DEPLOY_DIR = PROJECT_ROOT / "deploy"

# ---------------------------------------------------------------- 判题参数

# 单测试点默认时间限制（秒），题目可单独覆盖
DEFAULT_TIME_LIMIT = 2.0
# 单测试点默认内存限制（MB）
DEFAULT_MEMORY_LIMIT = 256
# 编译/解释器启动的额外宽限（秒），不计入题目时间限制
COMPILE_GRACE = 5.0
# 允许提交的语言
LANGS = {
    "python3": {
        "ext": ".py",
        "display": "Python 3",
        "monaco": "python",
    },
}
# 默认语言
DEFAULT_LANG = "python3"

# ---------------------------------------------------------------- 沙箱

# 提交代码可使用的最大源文件字节数
MAX_SOURCE_BYTES = 512 * 1024
# 判题时工作目录前缀（每份提交一个临时目录）
WORK_DIR_PREFIX = "dsoj_run_"

# ---------------------------------------------------------------- 站点

SITE_NAME = "DS-OJ 数据结构判题系统"
SITE_SLOGAN = "在线运行 · 即时判题 · 覆盖链表/栈/树/堆/图/排序"
# 提交记录最多保留条数（本地 JSON 存储）
MAX_SUBMISSIONS = 2000


def env_flag(name: str, default: bool = False) -> bool:
    """读取布尔型环境变量，接受 1/true/yes/on。"""
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}
