from prometheus_client import Counter, Histogram, Gauge

# Eventos de alto nivel
events_total = Counter(
    "psf_events_total",
    "Total events by type",
    ["event_type"],
)

# Errores por tipo
errors_total = Counter(
    "psf_errors_total",
    "Total errors by kind",
    ["kind"],
)

# Latencia OpenClaw (gen/regen)
openclaw_latency_seconds = Histogram(
    "psf_openclaw_latency_seconds",
    "Latency for OpenClaw calls",
    ["stage"],
)

# Estado de cola (desde SQLite snapshot)
posts_total = Gauge("psf_posts_total", "Total posts in DB")
posts_draft_total = Gauge("psf_posts_draft_total", "Total draft posts")
posts_approved_total = Gauge("psf_posts_approved_total", "Total approved posts")
events_db_total = Gauge("psf_events_db_total", "Total events rows in DB (2C)")
errors_db_total = Gauge("psf_errors_db_total", "Total ERROR events rows in DB (2C)")

# Control flags
pipeline_paused = Gauge("psf_pipeline_paused", "1 if pipeline_paused=1 else 0")
cooldown_active = Gauge("psf_cooldown_active", "1 if cooldown_until in future else 0")
fail_streak = Gauge("psf_fail_streak", "Current fail_streak flag value (int)")
