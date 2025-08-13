import os
from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from common.constants import VERSION, PROJECT_NAME, PROJECT_DESCRIPTION
from common.settings import settings
from common.security import validate_static_file_path

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    try:
        # Yield control to FastAPI
        print(f"Starting {PROJECT_NAME} v{VERSION}...")
        yield
    finally:
        # Shutdown background token usage processor
        print(f"Shutting down {PROJECT_NAME} v{VERSION}...")

def register_app() -> FastAPI:
    app = FastAPI(
        title=PROJECT_NAME,
        version=VERSION,
        description=PROJECT_DESCRIPTION,
        lifespan=lifespan,
    )

    register_middleware(app)
    register_router(app)
    register_static_files(app)

    return app

def register_middleware(app: FastAPI) -> None:

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def register_router(app: FastAPI) -> None:
    from app.router import router
    app.include_router(router)

def register_static_files(app: FastAPI) -> None:
    # Register static files for serving frontend assets
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
    app.mount("/i18n", StaticFiles(directory="static/i18n"), name="i18n")

    @app.get("/{full_path:path}")
    async def serve_index(full_path: str) -> FileResponse:
        # Serve index.html for all paths except API and static files
        if (full_path.startswith("api/") or
            full_path.startswith("docs") or
            full_path.startswith("redoc")):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not found")

        # Check if it's a valid static file
        static_file_path = validate_static_file_path(full_path)
        if static_file_path:
            return FileResponse(static_file_path)

        # Fallback to serving index.html for SPA
        index_path = os.path.join("static", "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path, media_type="text/html")
        else:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Frontend not found")    