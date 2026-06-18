from hashlib import sha256

from fastapi import FastAPI

from .routes.document import router


def hash_password(raw_password: str) -> str:
    return sha256(raw_password.encode("utf-8")).hexdigest()





def create_app() -> FastAPI:
    app = FastAPI(
        title="DocumentAI API",
    )
    app.include_router(router)
    return app
