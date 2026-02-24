from aiohttp import web
import os
import traceback

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


def _generate_metrics_bytes() -> bytes:
    """
    Genera métricas. Soporta multiprocess si PROMETHEUS_MULTIPROC_DIR está seteado.
    """
    mp_dir = os.getenv("PROMETHEUS_MULTIPROC_DIR", "").strip()
    if mp_dir:
        from prometheus_client import CollectorRegistry
        from prometheus_client import multiprocess

        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        return generate_latest(registry)

    return generate_latest()


def make_app(store):
    async def healthz(_req):
        try:
            await store.ping()
            return web.json_response({"ok": True})
        except Exception as e:
            return web.json_response({"ok": False, "error": str(e)}, status=500)

    async def metrics(_req):
        try:
            body = _generate_metrics_bytes()
            # aiohttp no permite charset dentro de content_type=...
            return web.Response(body=body, headers={"Content-Type": CONTENT_TYPE_LATEST})
        except Exception as e:
            return web.json_response(
                {
                    "ok": False,
                    "error": str(e),
                    "traceback": traceback.format_exc()[-3500:],
                    "prometheus_multiproc_dir": os.getenv("PROMETHEUS_MULTIPROC_DIR", ""),
                },
                status=500,
            )

    app = web.Application()
    app.add_routes(
        [
            web.get("/healthz", healthz),
            web.get("/metrics", metrics),
        ]
    )
    return app


async def start_http_server(store, host: str = "127.0.0.1", port: int = 18790):
    app = make_app(store)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    return runner


async def stop_http_server(runner):
    if runner:
        await runner.cleanup()
