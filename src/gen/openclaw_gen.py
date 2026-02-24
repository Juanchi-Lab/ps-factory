import os
import requests
from dotenv import load_dotenv

load_dotenv("/opt/ps_factory/config/.env", override=True)

def _get(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip()

def _require(name: str) -> str:
    v = _get(name)
    if not v or len(v) < 20:
        raise RuntimeError(f"{name} missing/invalid in /opt/ps_factory/config/.env")
    return v

def openclaw_chat(prompt: str) -> str:
    base_url = _get("OPENCLAW_URL", "http://127.0.0.1:18789").rstrip("/")
    token = _require("OPENCLAW_GATEWAY_TOKEN")
    agent_id = _get("OPENCLAW_AGENT_ID", "main")

    url = f"{base_url}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-openclaw-agent-id": agent_id,
    }
    payload = {
        "model": "openclaw",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }

    r = requests.post(url, headers=headers, json=payload, timeout=180)
    if r.status_code == 401:
        raise RuntimeError(f"401 from {url}. Check OPENCLAW_GATEWAY_TOKEN / agent_id / endpoint.")
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]

def openclaw_gen(prompt: str) -> str:
    gateway = _get("OPENCLAW_GATEWAY", "http://127.0.0.1:18789").rstrip("/")
    endpoint = _get("OPENCLAW_ENDPOINT", "/gen")
    token = _require("OPENCLAW_TOKEN")

    url = f"{gateway}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/plain;q=0.9, */*;q=0.8",
    }

    # ✅ /gen en tu gateway es GET (POST da 405)
    r = requests.get(url, headers=headers, params={"prompt": prompt}, timeout=180)

    if r.status_code == 401:
        raise RuntimeError(f"401 from {url}. Token mismatch (OPENCLAW_TOKEN).")
    r.raise_for_status()

    # Puede venir texto plano o JSON
    ct = (r.headers.get("content-type") or "").lower()
    if "application/json" in ct:
        data = r.json()
        if isinstance(data, dict) and "text" in data:
            return data["text"]
        if isinstance(data, dict) and "output" in data:
            return data["output"]
        return str(data)

    return r.text.strip()
