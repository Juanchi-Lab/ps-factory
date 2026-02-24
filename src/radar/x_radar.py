from typing import Dict, List, Optional, Any, Tuple
from radar.x_client import XClient


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def normalize_list_tweets(payload: Dict[str, Any], source: str) -> List[Dict[str, Any]]:
    data = payload.get("data") or []
    users = payload.get("includes", {}).get("users") or []
    user_by_id = {u.get("id"): u for u in users if u.get("id")}

    out: List[Dict[str, Any]] = []
    for t in data:
        author_id = t.get("author_id")
        u = user_by_id.get(author_id, {}) if author_id else {}

        metrics = t.get("public_metrics") or {}
        out.append(
            {
                "id": str(t.get("id")),
                "text": (t.get("text") or "").strip(),
                "created_at": t.get("created_at"),
                "author": {
                    "id": str(author_id) if author_id else None,
                    "username": u.get("username"),
                    "name": u.get("name"),
                },
                "metrics": {
                    "like_count": _safe_int(metrics.get("like_count")),
                    "retweet_count": _safe_int(metrics.get("retweet_count")),
                    "reply_count": _safe_int(metrics.get("reply_count")),
                    "quote_count": _safe_int(metrics.get("quote_count")),
                },
                "source": source,
            }
        )
    return out


def fetch_list_tweets(
    client: XClient,
    list_id: str,
    *,
    pagination_token: Optional[str] = None,
    max_results: int = 50,
    source: str = "x_list",
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Fetch tweets from a List using cursor pagination.
    NOTE: /2/lists/:id/tweets does NOT support since_id nor start_time.
    Returns (tweets, next_token).
    """
    params: Dict[str, Any] = {
        "max_results": max(5, min(100, int(max_results))),
        "tweet.fields": "created_at,public_metrics,author_id,lang",
        "expansions": "author_id",
        "user.fields": "username,name",
    }

    if pagination_token:
        params["pagination_token"] = str(pagination_token)

    payload = client.get(f"/lists/{list_id}/tweets", params=params)

    tweets = normalize_list_tweets(payload, source=source)

    meta = payload.get("meta") or {}
    next_token = meta.get("next_token")
    if next_token is not None:
        next_token = str(next_token)

    return tweets, next_token
