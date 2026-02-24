from typing import Dict, Any


def render_post_text(post: Dict[str, Any]) -> str:
    # Todo en español, estilo Panamá Soberano
    parts = []
    parts.append(f"🟠 *POST DEL DÍA* — `{post.get('post_id','')}`")
    parts.append("")
    parts.append(f"🎣 *Hook:* {post.get('hook','')}")
    parts.append("")
    parts.append(f"🧠 *Explicación simple:* {post.get('explain_simple','')}")
    parts.append("")
    parts.append(f"⚡️ *Bitcoin Anchor:* {post.get('bitcoin_anchor','')}")
    parts.append("")
    parts.append(f"📈 *Insight estratégico:* {post.get('insight','')}")
    parts.append("")
    parts.append(f"⚠️ *Riesgos / matices:* {post.get('risk','')}")
    parts.append("")
    parts.append("📝 *Caption sugerido (IG/TikTok/X):*")
    parts.append(post.get("caption",""))
    parts.append("")
    parts.append("🖼️ *Prompt visual (4:5):*")
    parts.append(f"`{post.get('visual_prompt','')}`")
    parts.append("")
    parts.append("✅ *Checklist QA:*")
    for item in post.get("qa", []):
        parts.append(f"• {item}")
    return "\n".join(parts)
