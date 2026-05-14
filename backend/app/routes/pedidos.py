"""Endpoints para Pedidos — incluye cálculo de utilidad al confirmar."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pedido, DetallePedido, Producto, MovimientoStock
from app.schemas import PedidoCreate, PedidoUpdate, PedidoOut, DetalleCreate, DetalleOut

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def _recalcular_totales(pedido: Pedido, db: Session):
    subtotal = sum(d.subtotal for d in pedido.detalles)
    pedido.subtotal = subtotal
    pedido.total    = max(0.0, subtotal - pedido.descuento)
    db.commit()


@router.get("/", response_model=List[PedidoOut])
def listar_pedidos(
    skip: int = 0, limit: int = 100,
    estado: Optional[str] = None,
    cliente_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Pedido)
    if estado:     q = q.filter(Pedido.estado == estado)
    if cliente_id: q = q.filter(Pedido.cliente_id == cliente_id)
    return q.order_by(Pedido.fecha_creacion.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=PedidoOut, status_code=201)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    db_pedido = Pedido(**pedido.model_dump())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


@router.get("/{pedido_id}", response_model=PedidoOut)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.put("/{pedido_id}", response_model=PedidoOut)
def actualizar_pedido(pedido_id: int, datos: PedidoUpdate, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(pedido, campo, valor)
    db.commit()
    db.refresh(pedido)
    return pedido


@router.post("/{pedido_id}/items", response_model=DetalleOut, status_code=201)
def agregar_item(pedido_id: int, detalle: DetalleCreate, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if pedido.estado not in ("pendiente", "en_proceso"):
        raise HTTPException(status_code=400, detail=f"No se puede modificar un pedido en estado: {pedido.estado}")
    producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto.stock < detalle.cantidad:
        raise HTTPException(status_code=400, detail=f"Stock insuficiente. Disponible: {producto.stock}")

    subtotal          = detalle.cantidad * detalle.precio_unitario
    utilidad_unitaria = round(detalle.precio_unitario - producto.precio_compra, 2)
    utilidad_subtotal = round(utilidad_unitaria * detalle.cantidad, 2)

    db_detalle = DetallePedido(
        pedido_id=pedido_id,
        producto_id=detalle.producto_id,
        cantidad=detalle.cantidad,
        precio_unitario=detalle.precio_unitario,
        precio_compra=producto.precio_compra,       # snapshot del precio de compra actual
        subtotal=subtotal,
        utilidad_unitaria=utilidad_unitaria,
        utilidad_subtotal=utilidad_subtotal,
    )
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)
    pedido.estado = "en_proceso"
    _recalcular_totales(pedido, db)
    db.refresh(db_detalle)
    return db_detalle


@router.post("/{pedido_id}/confirmar", response_model=PedidoOut)
def confirmar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if pedido.estado == "confirmado":
        raise HTTPException(status_code=400, detail="El pedido ya está confirmado")
    if pedido.estado in ("entregado", "cancelado"):
        raise HTTPException(status_code=400, detail=f"No se puede confirmar un pedido {pedido.estado}")
    if not pedido.detalles:
        raise HTTPException(status_code=400, detail="El pedido no tiene productos")

    utilidad_acumulada = 0.0

    for detalle in pedido.detalles:
        producto = detalle.producto
        if producto.stock < detalle.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}",
            )
        # Descontar stock
        stock_antes    = producto.stock
        producto.stock -= detalle.cantidad

        # Registrar movimiento
        db.add(MovimientoStock(
            producto_id=producto.id,
            tipo_movimiento="salida",
            cantidad=detalle.cantidad,
            stock_antes=stock_antes,
            stock_despues=producto.stock,
            motivo=f"Pedido #{pedido.id} confirmado",
        ))

        # Acumular utilidad del pedido
        utilidad_acumulada += detalle.utilidad_subtotal

    # Descontar descuento de la utilidad también
    pedido.utilidad_total = round(max(0.0, utilidad_acumulada - pedido.descuento), 2)
    pedido.estado = "confirmado"
    db.commit()
    db.refresh(pedido)
    return pedido


@router.delete("/{pedido_id}/items/{detalle_id}", status_code=204)
def eliminar_item(pedido_id: int, detalle_id: int, db: Session = Depends(get_db)):
    detalle = db.query(DetallePedido).filter(
        DetallePedido.id == detalle_id, DetallePedido.pedido_id == pedido_id
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    pedido = detalle.pedido
    db.delete(detalle)
    db.commit()
    _recalcular_totales(pedido, db)
