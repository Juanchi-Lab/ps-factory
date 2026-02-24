import html
from typing import Any, Dict


def _e(s: Any) -> str:
    return html.escape(str(s or ""), quote=False)


def render_post_html(post_id: str, version: int, post: Dict[str, Any]) -> str:
    # Título / encabezado
    title = post.get("title") or post.get("topic") or post_id

    hook = post.get("hook", "")
    explain = post.get("explain_simple", "")
    btc = post.get("bitcoin_anchor", "")
    insight = post.get("insight", "")
    risk = post.get("risk", "")
    caption = post.get("caption", "")
    visual = post.get("visual_prompt", "")

    qa = post.get("qa") or []
    qa_lines = "\n".join([f"• {_e(x)}" for x in qa]) if qa else "• (sin checklist)"

    # Estilo: emojis + labels en negrita, con saltos claros (como antes)
    return (
        f"🟠 <b>POST DEL DÍA</b> — <code>{_e(post_id)}</code> · v{version}\n\n"
        f"🎯 <b>Hook</b>\n{_e(hook)}\n\n"
        f"🧠 <b>Explicación simple</b>\n{_e(explain)}\n\n"
        f"⚡️ <b>Bitcoin Anchor</b>\n{_e(btc)}\n\n"
        f"📈 <b>Insight</b>\n{_e(insight)}\n\n"
        f"⚠️ <b>Riesgos / matices</b>\n{_e(risk)}\n\n"
        f"📝 <b>Caption sugerido (IG/TikTok/X)</b>\n{_e(caption)}\n\n"
        f"🖼 <b>Prompt visual (4:5)</b>\n{_e(visual)}\n\n"
        f"✅ <b>Checklist QA</b>\n{qa_lines}"
    )
