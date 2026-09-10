"""Generic reusable JSON file read/write utility (task.md section 59).

All functions are rooted at app/data/. Do not duplicate read/write logic
elsewhere — every route/service that needs JSON-file persistence should go
through this module.

Writes are atomic: data is written to a temp file in the same directory and
then swapped into place with os.replace, so a crash mid-write cannot corrupt
the target file.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Union

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _resolve(filename: str) -> Path:
    """Resolve a filename (e.g. 'materials.json') to its absolute path
    under app/data/. Accepts a bare filename or a relative path already
    rooted at app/data/."""
    path = Path(filename)
    if not path.is_absolute():
        path = DATA_DIR / path
    return path


def read_json(filename: str) -> Union[list, dict]:
    """Read a JSON file from app/data/. Returns [] if the file's top-level
    value looks list-like by convention (i.e. missing file returns []
    unless a default is more appropriate) -- to keep behavior predictable,
    a missing or empty file returns [] . Use read_json_dict() when a dict
    default is required."""
    path = _resolve(filename)
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    return json.loads(text)


def read_json_dict(filename: str) -> dict:
    """Read a JSON file expected to contain an object. Returns {} if the
    file is missing or empty."""
    path = _resolve(filename)
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {}
    data = json.loads(text)
    return data if isinstance(data, dict) else {}


def write_json(filename: str, data: Any) -> None:
    """Atomically write data as JSON to app/data/<filename>."""
    path = _resolve(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(
        dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp_file:
            json.dump(data, tmp_file, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def append_json(filename: str, item: Any) -> None:
    """Append an item to a JSON file that stores a list. If the file does
    not exist or is empty, it is created with a single-item list."""
    data = read_json(filename)
    if not isinstance(data, list):
        raise ValueError(f"{filename} does not contain a JSON list; cannot append.")
    data.append(item)
    write_json(filename, data)
