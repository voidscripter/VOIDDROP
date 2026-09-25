"""FastAPI application and HTTP endpoints."""

from __future__ import annotations

from pathlib import Path
import secrets
import time
import os

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .config import Config
from .files import confined_path, delete_file, list_files, safe_filename
from .qr import qr_png
from .security import PinAuth
from .transfers import Transfer


def create_app(config: Config, advertised_host: str | None = None) -> FastAPI:
    app = FastAPI(title="VOIDDROP", docs_url=None, redoc_url=None)
    auth = PinAuth(config.pin)
    active_clients: dict[str, float] = {}
    app.state.transfers = {}
    app.state.advertised_host = advertised_host

    def authenticated(request: Request) -> bool:
        return auth.verify_token(request.cookies.get("voiddrop_session"))

    @app.middleware("http")
    async def pin_gate(request: Request, call_next):
        if request.url.path == "/api/login" and request.method == "POST":
            return await call_next(request)
        if request.url.path in {"/health", "/", "/static/index.html", "/static/style.css", "/static/app.js"} or request.url.path.startswith("/static/"):
            return await call_next(request)
        if not authenticated(request):
            if request.url.path.startswith("/api/"):
                return Response(status_code=401)
            return HTMLResponse('<!doctype html><title>VOIDDROP</title><p>PIN required. Open the VOIDDROP page again to sign in.</p>', status_code=401)
        remote = request.client.host if request.client else "unknown"
        active_clients[remote] = time.monotonic()
        now = time.monotonic()
        for host, seen in list(active_clients.items()):
            if now - seen > 300:
                active_clients.pop(host, None)
        return await call_next(request)

    web_dir = Path(__file__).resolve().parent / "web"
    if not web_dir.exists():
        web_dir = Path(__file__).resolve().parents[2] / "web"
    app.mount("/static", StaticFiles(directory=web_dir), name="static")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/")
    async def index() -> FileResponse:
        return FileResponse(web_dir / "index.html")

    @app.get("/api/status")
    async def status(request: Request) -> dict[str, int | bool]:
        return {"pin_required": auth.enabled, "connected_devices": max(1, len(active_clients)),
                "active_transfers": len(app.state.transfers)}

    @app.post("/api/login")
    async def login(request: Request, response: Response):
        try:
            payload = await request.json()
        except Exception as exc:
            raise HTTPException(400, "Malformed request") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("pin"), str) or not auth.verify_pin(payload["pin"]):
            raise HTTPException(401, "Incorrect PIN")
        response.set_cookie("voiddrop_session", auth.token, httponly=True, samesite="strict", secure=False, max_age=86400)
        return {"ok": True}

    @app.get("/api/files")
    async def files():
        return {"files": list_files(config.directory)}

    @app.get("/api/transfers")
    async def transfers():
        return {"transfers": [{"name": item.name, "received": item.received,
                "speed": int(item.speed)} for item in app.state.transfers.values()]}

    @app.put("/api/files/{filename}")
    async def upload(filename: str, request: Request):
        try:
            name = safe_filename(filename)
            destination = confined_path(config.directory, name)
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from exc
        if destination.exists():
            raise HTTPException(409, "A file with that name already exists")
        temp = config.directory / f".voiddrop-{secrets.token_hex(12)}.part"
        transfer = Transfer(name=name, started=time.monotonic())
        key = secrets.token_urlsafe(12)
        app.state.transfers[key] = transfer
        try:
            with temp.open("xb") as output:
                async for chunk in request.stream():
                    if chunk:
                        output.write(chunk)
                        transfer.received += len(chunk)
            if not temp.exists():
                raise HTTPException(400, "Upload was interrupted")
            try:
                os.link(temp, destination)
                temp.unlink()
            except FileExistsError as exc:
                raise HTTPException(409, "A file with that name already exists") from exc
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(400, "Upload failed; incomplete data was discarded") from exc
        finally:
            app.state.transfers.pop(key, None)
            try:
                temp.unlink(missing_ok=True)
            except OSError:
                pass
        return {"name": name, "size": transfer.received}

    @app.get("/api/files/{filename}")
    async def download(filename: str):
        try:
            path = confined_path(config.directory, filename)
        except ValueError as exc:
            raise HTTPException(400, "Invalid filename") from exc
        if path.is_symlink() or not path.is_file():
            raise HTTPException(404, "File not found")
        return FileResponse(path, filename=path.name, media_type="application/octet-stream")

    @app.delete("/api/files/{filename}")
    async def remove(filename: str):
        try:
            delete_file(config.directory, filename)
        except ValueError as exc:
            raise HTTPException(400, "Invalid filename") from exc
        except FileNotFoundError as exc:
            raise HTTPException(404, "File not found") from exc
        return {"deleted": True}

    @app.get("/api/qr.png")
    async def qr(request: Request):
        host = app.state.advertised_host or request.url.hostname or "localhost"
        url = f"http://{host}:{request.url.port or config.port}"
        return Response(qr_png(url), media_type="image/png", headers={"Cache-Control": "no-store"})

    @app.get("/api/info")
    async def info(request: Request):
        host = app.state.advertised_host or request.url.hostname or "localhost"
        return {"url": f"http://{host}:{request.url.port or config.port}", "directory": str(config.directory), "port": config.port}

    return app
