from typing import Any, Dict, Optional
from threading import Lock
from datetime import datetime

_lock = Lock()
_last_run: Optional[Dict[str, Any]] = None

def save_last_run(state: Dict[str, Any]) -> None:
    # Add a timestamp to make the demo nicer
    state_with_meta = dict(state)
    state_with_meta["_debug_saved_at"] = datetime.utcnow().isoformat() + "Z"
    global _last_run
    with _lock:
        _last_run = state_with_meta

def get_last_run() -> Optional[Dict[str, Any]]:
    with _lock:
        return _last_run