from .clientes import router as clientes_router
from .productos import router as productos_router
from .pedidos import router as pedidos_router
from .mensajes import router as mensajes_router
from .dashboard import router as dashboard_router
from .categorias import router as categorias_router

__all__ = [
    "clientes_router", "productos_router", "pedidos_router",
    "mensajes_router", "dashboard_router", "categorias_router",
]
