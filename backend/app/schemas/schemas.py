"""Schemas Pydantic v2 — BodegaOS."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# ── CATEGORIAS ────────────────────────────────────────────────
class CategoriaBase(BaseModel):
    nombre: str
    emoji: Optional[str] = "📦"
    activo: bool = True

class CategoriaCreate(CategoriaBase): pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    emoji:  Optional[str] = None
    activo: Optional[bool] = None

class CategoriaOut(CategoriaBase):
    id: int
    fecha_creacion: datetime
    model_config = {"from_attributes": True}


# ── CLIENTES ──────────────────────────────────────────────────
class ClienteBase(BaseModel):
    nombre:       str
    telefono:     Optional[str] = None
    correo:       Optional[str] = None
    direccion:    Optional[str] = None
    tipo_cliente: str = "minorista"
    activo:       bool = True

class ClienteCreate(ClienteBase): pass

class ClienteUpdate(BaseModel):
    nombre:       Optional[str]  = None
    telefono:     Optional[str]  = None
    correo:       Optional[str]  = None
    direccion:    Optional[str]  = None
    tipo_cliente: Optional[str]  = None
    activo:       Optional[bool] = None

class ClienteOut(ClienteBase):
    id: int
    fecha_creacion: datetime
    model_config = {"from_attributes": True}


# ── PRODUCTOS ─────────────────────────────────────────────────
class ProductoBase(BaseModel):
    codigo:           str
    nombre:           str
    descripcion:      Optional[str] = None
    categoria_id:     Optional[int] = None
    precio_compra:    float = 0.0          # ← NUEVO
    precio_minorista: float = 0.0
    precio_mayorista: float = 0.0
    stock:            int   = 0
    stock_minimo:     int   = 5
    activo:           bool  = True

class ProductoCreate(ProductoBase): pass

class ProductoUpdate(BaseModel):
    nombre:           Optional[str]   = None
    descripcion:      Optional[str]   = None
    categoria_id:     Optional[int]   = None
    precio_compra:    Optional[float] = None   # ← NUEVO
    precio_minorista: Optional[float] = None
    precio_mayorista: Optional[float] = None
    stock:            Optional[int]   = None
    stock_minimo:     Optional[int]   = None
    activo:           Optional[bool]  = None

class ProductoOut(ProductoBase):
    id: int
    fecha_creacion: datetime
    categoria_rel:  Optional[CategoriaOut] = None
    # Utilidad calculada (no viene de BD, se calcula en el endpoint)
    utilidad_minorista: Optional[float] = None
    utilidad_mayorista: Optional[float] = None
    model_config = {"from_attributes": True}


# ── DETALLE PEDIDO ────────────────────────────────────────────
class DetalleBase(BaseModel):
    producto_id:    int
    cantidad:       int
    precio_unitario: float

class DetalleCreate(DetalleBase): pass

class DetalleOut(DetalleBase):
    id:                int
    pedido_id:         int
    precio_compra:     float          # ← NUEVO
    subtotal:          float
    utilidad_unitaria: float          # ← NUEVO
    utilidad_subtotal: float          # ← NUEVO
    producto:          Optional[ProductoOut] = None
    model_config = {"from_attributes": True}


# ── PEDIDOS ───────────────────────────────────────────────────
class PedidoBase(BaseModel):
    cliente_id: int
    canal:      str   = "whatsapp"
    descuento:  float = 0.0

class PedidoCreate(PedidoBase): pass

class PedidoUpdate(BaseModel):
    estado:    Optional[str]   = None
    descuento: Optional[float] = None
    canal:     Optional[str]   = None

class PedidoOut(PedidoBase):
    id:             int
    estado:         str
    subtotal:       float
    total:          float
    utilidad_total: float          # ← NUEVO
    fecha_creacion: datetime
    cliente:        Optional[ClienteOut] = None
    detalles:       List[DetalleOut] = []
    model_config = {"from_attributes": True}


# ── MENSAJES ──────────────────────────────────────────────────
class MensajeBase(BaseModel):
    telefono:  Optional[str] = None
    direccion: Optional[str] = None
    contenido: str
    tipo:      str = "entrante"

class MensajeCreate(MensajeBase):
    cliente_id: Optional[int] = None

class MensajeOut(MensajeBase):
    id:         int
    cliente_id: Optional[int] = None
    leido:      bool
    fecha_creacion: datetime
    model_config = {"from_attributes": True}


# ── MOVIMIENTOS STOCK ─────────────────────────────────────────
class MovimientoBase(BaseModel):
    producto_id:     int
    tipo_movimiento: str
    cantidad:        int
    motivo:          Optional[str] = None

class MovimientoCreate(MovimientoBase): pass

class MovimientoOut(MovimientoBase):
    id:            int
    stock_antes:   int
    stock_despues: int
    fecha_creacion: datetime
    model_config = {"from_attributes": True}


# ── WEBHOOK ───────────────────────────────────────────────────
class WebhookMessage(BaseModel):
    telefono: str
    mensaje:  str
    nombre:   Optional[str] = None


# ── DASHBOARD ─────────────────────────────────────────────────
class DashboardMetrics(BaseModel):
    total_clientes:       int
    total_productos:      int
    pedidos_hoy:          int
    ventas_hoy:           float
    utilidad_hoy:         float          # ← NUEVO
    utilidad_mes:         float          # ← NUEVO
    productos_bajo_stock: int
    mensajes_no_leidos:   int
    top_productos:        list
    top_rentables:        list           # ← NUEVO
    ventas_por_dia:       list
    ventas_por_mes:       list


# ── REPORTE UTILIDAD ──────────────────────────────────────────
class ReporteUtilidadItem(BaseModel):
    pedido_id:      int
    fecha:          str
    cliente:        str
    total:          float
    utilidad_total: float
    margen:         float   # utilidad / total * 100

class ReporteUtilidad(BaseModel):
    desde:           str
    hasta:           str
    total_ventas:    float
    total_utilidad:  float
    margen_promedio: float
    pedidos:         List[ReporteUtilidadItem]
