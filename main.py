from fastapi.middleware.cors import CORSMiddleware

from backend.api.routers import create_app
from backend.services.loader_service import loader_service
from backend.services.vector_service import vector_service

app = create_app()


@app.on_event("startup")
async def startup():
    doc = await loader_service.document_loader(1)
    await vector_service.generate_embedding(doc)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
