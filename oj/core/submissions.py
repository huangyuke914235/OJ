"""提交记录存储（本地 JSON 文件，单机单进程使用）。

公网部署时（Streamlit Community Cloud）文件系统是临时的，记录不保证持久；
该实现面向本地开发与演示。若需持久化，可替换为 SQLite / 云数据库。
"""
from __future__ import annotations

import json
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from oj.config import MAX_SUBMISSIONS, SUBMISSIONS_DB

_LOCK = threading.Lock()


def _read_all(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def _write_all(path: Path, records: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(records[-MAX_SUBMISSIONS:], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    tmp.replace(path)


def new_submission_id() -> str:
    return uuid.uuid4().hex[:12]


def save_submission(record: Dict[str, Any], path: Path = SUBMISSIONS_DB) -> Dict[str, Any]:
    """追加一条提交记录，返回带 id/时间戳的完整记录。"""
    record = dict(record)
    record.setdefault("id", new_submission_id())
    record.setdefault("time", time.time())
    with _LOCK:
        records = _read_all(path)
        records.append(record)
        _write_all(path, records)
    return record


def list_submissions(
    path: Path = SUBMISSIONS_DB,
    problem_id: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """按时间倒序返回提交记录。"""
    records = _read_all(path)
    if problem_id:
        records = [r for r in records if r.get("problem_id") == problem_id]
    records.reverse()
    return records[:limit]


def get_submission(sub_id: str, path: Path = SUBMISSIONS_DB) -> Optional[Dict[str, Any]]:
    for r in _read_all(path):
        if r.get("id") == sub_id:
            return r
    return None


def clear_submissions(path: Path = SUBMISSIONS_DB) -> None:
    with _LOCK:
        _write_all(path, [])
