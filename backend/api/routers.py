from fastapi import FastAPI

from .routes.ai import router as ai_router
from .routes.chat import router as chat_router
from .routes.document import router as doc_router
from .routes.message import router as msg_router
from .routes.user import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DocumentAI API",
    )
    app.include_router(doc_router)
    app.include_router(user_router)
    app.include_router(msg_router)
    app.include_router(ai_router)
    app.include_router(chat_router)
    return app
