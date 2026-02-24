import os
import requests
from typing import Any, Dict, Optional


class XClient:
    def __init__(self, bearer_token: Optional[str] = None, timeout: int = 25):
        self.bearer_token = bearer_token or os.getenv("X_BEARER_TOKEN", "").strip()
        if not self.bearer_token:
            raise RuntimeError("Missing X_BEARER_TOKEN in env")
        self.timeout = timeout
        self.base = "https://api.x.com/2"  # X API v2

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.bearer_token}"}

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self.base + path
        r = requests.get(url, headers=self._headers(), params=params or {}, timeout=self.timeout)
        if r.status_code >= 400:
            raise RuntimeError(f"X API error {r.status_code}: {r.text[:400]}")
        return r.json()
