import json
from pathlib import Path
from typing import Any, Dict


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(value, hi))


def load_json_file(path: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
  
    try:
        with Path(path).open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except (OSError, json.JSONDecodeError):
        pass
    return fallback
