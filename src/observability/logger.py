import json
import logging
import os
import sys
from datetime import datetime, timezone


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": _iso(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        # Extras opcionales
        for k in ("event_type", "content_id", "run_id", "actor"):
            v = getattr(record, k, None)
            if v is not None:
                payload[k] = v

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


def setup_logging() -> None:
    level = os.getenv("PSF_LOG_LEVEL", "INFO").upper()
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root.handlers.clear()
    root.addHandler(handler)
