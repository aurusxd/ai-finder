from hashlib import sha256

from fastapi import FastAPI

from .routes.document import router as doc_router
from .routes.message import router as msg_router
from .routes.user import router as user_router


def hash_password(raw_password: str) -> str:
    return sha256(raw_password.encode("utf-8")).hexdigest()


def create_app() -> FastAPI:
    app = FastAPI(
        title="DocumentAI API",
    )
    app.include_router(doc_router)
    app.include_router(user_router)
    app.include_router(msg_router)
    return app
