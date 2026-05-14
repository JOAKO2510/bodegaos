"""Modelos SQLAlchemy — tablas de BodegaOS."""
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"
    id             = Column(Integer, primary_key=True, index=True)
    nombre         = Column(String(100), unique=True, nullable=False, index=True)
    emoji          = Column(String(10), nullable=True, default="📦")
    activo         = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    productos      = relationship("Producto", back_populates="categoria_rel")


class Cliente(Base):
    __tablename__ = "clientes"
    id             = Column(Integer, primary_key=True, index=True)
    nombre         = Column(String(150), nullable=False)
    telefono       = Column(String(20), unique=True, index=True, nullable=True)
    correo         = Column(String(150), unique=True, index=True, nullable=True)
    direccion      = Column(String(250), nullable=True)
    tipo_cliente   = Column(String(20), default="minorista")
    activo         = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    pedidos        = relationship("Pedido", back_populates="cliente")
    mensajes       = relationship("Mensaje", back_populates="cliente")


class Producto(Base):
    __tablename__ = "productos"
    id               = Column(Integer, primary_key=True, index=True)
    codigo           = Column(String(50), unique=True, index=True, nullable=False)
    nombre           = Column(String(200), nullable=False, index=True)
    descripcion      = Column(Text, nullable=True)
    categoria_id     = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    precio_compra    = Column(Float, nullable=False, default=0.0)   # ← NUEVO
    precio_minorista = Column(Float, nullable=False, default=0.0)
    precio_mayorista = Column(Float, nullable=False, default=0.0)
    stock            = Column(Integer, nullable=False, default=0)
    stock_minimo     = Column(Integer, nullable=False, default=5)
    activo           = Column(Boolean, default=True)
    fecha_creacion   = Column(DateTime, default=datetime.utcnow)
    categoria_rel    = relationship("Categoria", back_populates="productos")
    detalles         = relationship("DetallePedido", back_populates="producto")
    movimientos      = relationship("MovimientoStock", back_populates="producto")


class Pedido(Base):
    __tablename__ = "pedidos"
    id              = Column(Integer, primary_key=True, index=True)
    cliente_id      = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    estado          = Column(String(30), default="pendiente")
    canal           = Column(String(30), default="whatsapp")
    subtotal        = Column(Float, default=0.0)
    descuento       = Column(Float, default=0.0)
    total           = Column(Float, default=0.0)
    utilidad_total  = Column(Float, default=0.0)   # ← NUEVO
    fecha_creacion  = Column(DateTime, default=datetime.utcnow)
    cliente         = relationship("Cliente", back_populates="pedidos")
    detalles        = relationship("DetallePedido", back_populates="pedido")


class DetallePedido(Base):
    __tablename__ = "detalle_pedido"
    id                 = Column(Integer, primary_key=True, index=True)
    pedido_id          = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    producto_id        = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad           = Column(Integer, nullable=False, default=1)
    precio_unitario    = Column(Float, nullable=False, default=0.0)
    precio_compra      = Column(Float, nullable=False, default=0.0)   # ← NUEVO (snapshot)
    subtotal           = Column(Float, nullable=False, default=0.0)
    utilidad_unitaria  = Column(Float, nullable=False, default=0.0)   # ← NUEVO
    utilidad_subtotal  = Column(Float, nullable=False, default=0.0)   # ← NUEVO
    pedido             = relationship("Pedido", back_populates="detalles")
    producto           = relationship("Producto", back_populates="detalles")


class Mensaje(Base):
    __tablename__ = "mensajes"
    id             = Column(Integer, primary_key=True, index=True)
    cliente_id     = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    telefono       = Column(String(20), nullable=True)
    direccion      = Column(String(250), nullable=True)
    contenido      = Column(Text, nullable=False)
    tipo           = Column(String(10), default="entrante")
    leido          = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    cliente        = relationship("Cliente", back_populates="mensajes")


class MovimientoStock(Base):
    __tablename__ = "movimientos_stock"
    id              = Column(Integer, primary_key=True, index=True)
    producto_id     = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo_movimiento = Column(String(20), nullable=False)
    cantidad        = Column(Integer, nullable=False)
    stock_antes     = Column(Integer, nullable=False)
    stock_despues   = Column(Integer, nullable=False)
    motivo          = Column(String(250), nullable=True)
    fecha_creacion  = Column(DateTime, default=datetime.utcnow)
    producto        = relationship("Producto", back_populates="movimientos")
