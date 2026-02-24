import json
import os
import time
from typing import Any, Dict

STATE_PATH_DEFAULT = "/opt/ps_factory/outputs/state.json"


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def load_state(path: str = STATE_PATH_DEFAULT) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "meta": {"created_at": int(time.time())},
            "posts": {},              # post_id -> post payload
            "candidates": {},         # cand_id -> candidate payload
            "last_draft_msg_id": None,
        }


def save_state(state: Dict[str, Any], path: str = STATE_PATH_DEFAULT) -> None:
    _ensure_dir(path)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)
