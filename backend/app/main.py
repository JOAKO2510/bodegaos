"""BodegaOS — Punto de entrada principal de FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_tables
from app.routes import (
    clientes_router, productos_router, pedidos_router,
    mensajes_router, dashboard_router, categorias_router,
)
from app.utils.seed_productos import seed_data
from app.database import SessionLocal

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema de gestión para bodega con venta por WhatsApp y chatbot.",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categorias_router, prefix="/api")
app.include_router(clientes_router,   prefix="/api")
app.include_router(productos_router,  prefix="/api")
app.include_router(pedidos_router,    prefix="/api")
app.include_router(mensajes_router,   prefix="/api")
app.include_router(dashboard_router,  prefix="/api")


@app.on_event("startup")
def on_startup():
    create_tables()
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


@app.get("/", tags=["Root"])
def root():
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}
