"""Endpoints CRUD para Productos + movimientos de stock."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Producto, MovimientoStock
from app.schemas import ProductoCreate, ProductoUpdate, ProductoOut, MovimientoCreate, MovimientoOut

router = APIRouter(prefix="/productos", tags=["Productos"])


def _enrich(p: Producto) -> dict:
    """Agrega utilidades calculadas al producto."""
    d = {c.name: getattr(p, c.name) for c in p.__table__.columns}
    d["categoria_rel"] = p.categoria_rel
    d["utilidad_minorista"] = round(p.precio_minorista - p.precio_compra, 2)
    d["utilidad_mayorista"] = round(p.precio_mayorista - p.precio_compra, 2)
    return d


@router.get("/", response_model=List[ProductoOut])
def listar_productos(
    skip: int = 0, limit: int = 100,
    activo: Optional[bool] = None,
    categoria_id: Optional[int] = None,
    nombre: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Producto)
    if activo is not None:    q = q.filter(Producto.activo == activo)
    if categoria_id:          q = q.filter(Producto.categoria_id == categoria_id)
    if nombre:                q = q.filter(Producto.nombre.ilike(f"%{nombre}%"))
    productos = q.offset(skip).limit(limit).all()
    # Enriquecer con utilidades
    results = []
    for p in productos:
        out = ProductoOut.model_validate(p)
        out.utilidad_minorista = round(p.precio_minorista - p.precio_compra, 2)
        out.utilidad_mayorista = round(p.precio_mayorista - p.precio_compra, 2)
        results.append(out)
    return results


@router.post("/", response_model=ProductoOut, status_code=201)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    if db.query(Producto).filter(Producto.codigo == producto.codigo).first():
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese código")
    db_p = Producto(**producto.model_dump())
    db.add(db_p)
    db.commit()
    db.refresh(db_p)
    out = ProductoOut.model_validate(db_p)
    out.utilidad_minorista = round(db_p.precio_minorista - db_p.precio_compra, 2)
    out.utilidad_mayorista = round(db_p.precio_mayorista - db_p.precio_compra, 2)
    return out


@router.get("/bajo-stock", response_model=List[ProductoOut])
def productos_bajo_stock(db: Session = Depends(get_db)):
    productos = db.query(Producto).filter(
        Producto.stock <= Producto.stock_minimo, Producto.activo == True
    ).all()
    results = []
    for p in productos:
        out = ProductoOut.model_validate(p)
        out.utilidad_minorista = round(p.precio_minorista - p.precio_compra, 2)
        out.utilidad_mayorista = round(p.precio_mayorista - p.precio_compra, 2)
        results.append(out)
    return results


@router.get("/{producto_id}", response_model=ProductoOut)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id == producto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    out = ProductoOut.model_validate(p)
    out.utilidad_minorista = round(p.precio_minorista - p.precio_compra, 2)
    out.utilidad_mayorista = round(p.precio_mayorista - p.precio_compra, 2)
    return out


@router.put("/{producto_id}", response_model=ProductoOut)
def actualizar_producto(producto_id: int, datos: ProductoUpdate, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id == producto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(p, campo, valor)
    db.commit()
    db.refresh(p)
    out = ProductoOut.model_validate(p)
    out.utilidad_minorista = round(p.precio_minorista - p.precio_compra, 2)
    out.utilidad_mayorista = round(p.precio_mayorista - p.precio_compra, 2)
    return out


@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id == producto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    p.activo = False
    db.commit()


# ── Movimientos de stock ──────────────────────────────────────

@router.post("/{producto_id}/movimiento", response_model=MovimientoOut, status_code=201)
def registrar_movimiento(producto_id: int, datos: MovimientoCreate, db: Session = Depends(get_db)):
    p = db.query(Producto).filter(Producto.id == producto_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    stock_antes = p.stock
    if datos.tipo_movimiento == "entrada":
        p.stock += datos.cantidad
    elif datos.tipo_movimiento in ("salida", "ajuste"):
        if p.stock < datos.cantidad:
            raise HTTPException(status_code=400, detail="Stock insuficiente")
        p.stock -= datos.cantidad
    elif datos.tipo_movimiento == "devolucion":
        p.stock += datos.cantidad
    else:
        raise HTTPException(status_code=400, detail="Tipo de movimiento inválido")
    mov = MovimientoStock(
        producto_id=producto_id, tipo_movimiento=datos.tipo_movimiento,
        cantidad=datos.cantidad, stock_antes=stock_antes,
        stock_despues=p.stock, motivo=datos.motivo,
    )
    db.add(mov)
    db.commit()
    db.refresh(mov)
    return mov


@router.get("/{producto_id}/movimientos", response_model=List[MovimientoOut])
def historial_movimientos(producto_id: int, db: Session = Depends(get_db)):
    if not db.query(Producto).filter(Producto.id == producto_id).first():
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db.query(MovimientoStock).filter(
        MovimientoStock.producto_id == producto_id
    ).order_by(MovimientoStock.fecha_creacion.desc()).all()
