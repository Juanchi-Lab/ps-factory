import os, requests
from dotenv import load_dotenv
load_dotenv("/opt/ps_factory/config/.env", override=True)

BEARER = os.getenv("X_BEARER_TOKEN","").strip()
LIST_ID = os.getenv("X_LIST_PANAMA","").strip() or "2025235677516878257"

assert BEARER, "Missing X_BEARER_TOKEN"
url = f"https://api.x.com/2/lists/{LIST_ID}/tweets"
# si api.x.com no te funciona, cambia a api.twitter.com
# url = f"https://api.twitter.com/2/lists/{LIST_ID}/tweets"

params = {
  "max_results": 10,
  "tweet.fields": "created_at,author_id,public_metrics,lang",
}
r = requests.get(url, headers={"Authorization": f"Bearer {BEARER}"}, params=params, timeout=30)
print("STATUS:", r.status_code)
print(r.text[:2000])
