"""Dashboard, reporte de utilidad y webhook WhatsApp."""
from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Cliente, Producto, Pedido, DetallePedido, Mensaje, MovimientoStock
from app.schemas import DashboardMetrics, WebhookMessage, ReporteUtilidad, ReporteUtilidadItem

router = APIRouter(tags=["Dashboard & Webhook"])


# ── DASHBOARD ─────────────────────────────────────────────────
@router.get("/dashboard", response_model=DashboardMetrics)
def dashboard(db: Session = Depends(get_db)):
    hoy = date.today()
    mes_actual = hoy.month
    anio_actual = hoy.year

    total_clientes  = db.query(func.count(Cliente.id)).filter(Cliente.activo == True).scalar()
    total_productos = db.query(func.count(Producto.id)).filter(Producto.activo == True).scalar()

    pedidos_hoy = (
        db.query(func.count(Pedido.id))
        .filter(func.date(Pedido.fecha_creacion) == hoy)
        .scalar()
    )
    ventas_hoy = (
        db.query(func.coalesce(func.sum(Pedido.total), 0.0))
        .filter(func.date(Pedido.fecha_creacion) == hoy,
                Pedido.estado.in_(["confirmado", "entregado"]))
        .scalar()
    )

    # ── Utilidad del día ──────────────────────────────────────
    utilidad_hoy = (
        db.query(func.coalesce(func.sum(Pedido.utilidad_total), 0.0))
        .filter(func.date(Pedido.fecha_creacion) == hoy,
                Pedido.estado.in_(["confirmado", "entregado"]))
        .scalar()
    )

    # ── Utilidad del mes ──────────────────────────────────────
    utilidad_mes = (
        db.query(func.coalesce(func.sum(Pedido.utilidad_total), 0.0))
        .filter(extract("year",  Pedido.fecha_creacion) == anio_actual,
                extract("month", Pedido.fecha_creacion) == mes_actual,
                Pedido.estado.in_(["confirmado", "entregado"]))
        .scalar()
    )

    productos_bajo_stock = (
        db.query(func.count(Producto.id))
        .filter(Producto.stock <= Producto.stock_minimo, Producto.activo == True)
        .scalar()
    )
    mensajes_no_leidos = (
        db.query(func.count(Mensaje.id))
        .filter(Mensaje.leido == False, Mensaje.tipo == "entrante")
        .scalar()
    )

    # ── Top 5 productos por cantidad vendida ──────────────────
    top_raw = (
        db.query(Producto.nombre, func.sum(DetallePedido.cantidad).label("total_vendido"))
        .join(DetallePedido, Producto.id == DetallePedido.producto_id)
        .join(Pedido, DetallePedido.pedido_id == Pedido.id)
        .filter(Pedido.estado.in_(["confirmado", "entregado"]))
        .group_by(Producto.id)
        .order_by(func.sum(DetallePedido.cantidad).desc())
        .limit(6).all()
    )
    top_productos = [{"nombre": r[0], "total_vendido": r[1]} for r in top_raw]

    # ── Top 5 productos más rentables (por utilidad total) ────
    top_rent_raw = (
        db.query(
            Producto.nombre,
            func.sum(DetallePedido.utilidad_subtotal).label("utilidad_total"),
            func.sum(DetallePedido.cantidad).label("unidades"),
        )
        .join(DetallePedido, Producto.id == DetallePedido.producto_id)
        .join(Pedido, DetallePedido.pedido_id == Pedido.id)
        .filter(Pedido.estado.in_(["confirmado", "entregado"]))
        .group_by(Producto.id)
        .order_by(func.sum(DetallePedido.utilidad_subtotal).desc())
        .limit(6).all()
    )
    top_rentables = [
        {"nombre": r[0], "utilidad_total": round(float(r[1] or 0), 2), "unidades": r[2]}
        for r in top_rent_raw
    ]

    # ── Ventas por día (últimos 30) ───────────────────────────
    ventas_dia_raw = (
        db.query(func.date(Pedido.fecha_creacion).label("dia"),
                 func.sum(Pedido.total).label("total"),
                 func.sum(Pedido.utilidad_total).label("utilidad"))
        .filter(Pedido.estado.in_(["confirmado", "entregado"]))
        .group_by(func.date(Pedido.fecha_creacion))
        .order_by(func.date(Pedido.fecha_creacion).desc())
        .limit(30).all()
    )
    ventas_por_dia = [
        {"dia": str(r[0]), "total": float(r[1] or 0), "utilidad": float(r[2] or 0)}
        for r in ventas_dia_raw
    ]

    # ── Ventas por mes (últimos 12) ───────────────────────────
    ventas_mes_raw = (
        db.query(
            extract("year",  Pedido.fecha_creacion).label("anio"),
            extract("month", Pedido.fecha_creacion).label("mes"),
            func.sum(Pedido.total).label("total"),
            func.sum(Pedido.utilidad_total).label("utilidad"),
        )
        .filter(Pedido.estado.in_(["confirmado", "entregado"]))
        .group_by("anio", "mes")
        .order_by("anio", "mes")
        .limit(12).all()
    )
    ventas_por_mes = [
        {"anio": int(r[0]), "mes": int(r[1]),
         "total": float(r[2] or 0), "utilidad": float(r[3] or 0)}
        for r in ventas_mes_raw
    ]

    return DashboardMetrics(
        total_clientes=total_clientes,
        total_productos=total_productos,
        pedidos_hoy=pedidos_hoy,
        ventas_hoy=float(ventas_hoy),
        utilidad_hoy=float(utilidad_hoy),
        utilidad_mes=float(utilidad_mes),
        productos_bajo_stock=productos_bajo_stock,
        mensajes_no_leidos=mensajes_no_leidos,
        top_productos=top_productos,
        top_rentables=top_rentables,
        ventas_por_dia=ventas_por_dia,
        ventas_por_mes=ventas_por_mes,
    )


# ── REPORTE DE UTILIDAD ───────────────────────────────────────
@router.get("/reporte/utilidad", response_model=ReporteUtilidad)
def reporte_utilidad(
    desde: str = Query(default=None, description="Fecha inicio YYYY-MM-DD"),
    hasta: str = Query(default=None, description="Fecha fin YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Reporte detallado de utilidad por rango de fechas."""
    hoy = date.today()
    d_desde = date.fromisoformat(desde) if desde else date(hoy.year, hoy.month, 1)
    d_hasta = date.fromisoformat(hasta) if hasta else hoy

    pedidos = (
        db.query(Pedido)
        .filter(
            func.date(Pedido.fecha_creacion) >= d_desde,
            func.date(Pedido.fecha_creacion) <= d_hasta,
            Pedido.estado.in_(["confirmado", "entregado"]),
        )
        .order_by(Pedido.fecha_creacion.desc())
        .all()
    )

    items = []
    total_ventas   = 0.0
    total_utilidad = 0.0

    for p in pedidos:
        margen = round((p.utilidad_total / p.total * 100) if p.total > 0 else 0, 1)
        items.append(ReporteUtilidadItem(
            pedido_id=p.id,
            fecha=str(p.fecha_creacion.date()),
            cliente=p.cliente.nombre if p.cliente else "—",
            total=p.total,
            utilidad_total=p.utilidad_total,
            margen=margen,
        ))
        total_ventas   += p.total
        total_utilidad += p.utilidad_total

    margen_promedio = round((total_utilidad / total_ventas * 100) if total_ventas > 0 else 0, 1)

    return ReporteUtilidad(
        desde=str(d_desde),
        hasta=str(d_hasta),
        total_ventas=round(total_ventas, 2),
        total_utilidad=round(total_utilidad, 2),
        margen_promedio=margen_promedio,
        pedidos=items,
    )


# ── WEBHOOK WHATSAPP ──────────────────────────────────────────
SALUDOS  = ["hola","buenos días","buenas tardes","buenas noches","hey","hi","ola","buenas"]
CATALOGOS= ["catálogo","catalogo","productos","lista","que tienen","qué tienen","ver productos"]
PEDIDO_KW= ["pedido","quiero pedir","hacer pedido","mi pedido"]
ESTADO_KW= ["estado","mi orden","cómo va","como va"]

def _respuesta_automatica(mensaje: str, cliente, db: Session) -> str:
    texto = mensaje.lower().strip()
    if any(s in texto for s in SALUDOS):
        return (f"¡Hola {cliente.nombre}! 👋 Bienvenido a nuestra bodega.\n\n"
                "¿En qué te puedo ayudar?\n"
                "• Escribe *catálogo* para ver productos\n"
                "• Escribe el nombre de un producto para buscarlo\n"
                "• Escribe *pedido* para crear un pedido\n"
                "• Escribe *estado* para ver tus pedidos")
    if any(c in texto for c in CATALOGOS):
        productos = db.query(Producto).filter(Producto.activo==True, Producto.stock>0).limit(10).all()
        if not productos:
            return "Lo siento, no hay productos disponibles en este momento. 😕"
        lineas = ["📦 *Nuestro Catálogo:*\n"]
        for p in productos:
            lineas.append(f"• {p.nombre} — S/ {p.precio_minorista:.2f} (stock: {p.stock})")
        lineas.append("\nEscribe el nombre del producto que deseas para más info.")
        return "\n".join(lineas)
    if any(e in texto for e in ESTADO_KW):
        pedidos = db.query(Pedido).filter(Pedido.cliente_id==cliente.id).order_by(Pedido.fecha_creacion.desc()).limit(3).all()
        if not pedidos:
            return "No tienes pedidos registrados aún. Escribe *catálogo* para ver nuestros productos. 🛒"
        lineas = ["📋 *Tus últimos pedidos:*\n"]
        for p in pedidos:
            lineas.append(f"• Pedido #{p.id} — Estado: {p.estado} — Total: S/ {p.total:.2f}")
        return "\n".join(lineas)
    if any(k in texto for k in PEDIDO_KW):
        return ("¡Perfecto! Para crear tu pedido, por favor dime:\n\n"
                "1️⃣ El nombre del producto\n2️⃣ La cantidad\n\n"
                "Ejemplo: *2 Aceite Vegetal*\n\n"
                "También puedes visitar nuestra web para gestionar tu pedido. 🛒")
    productos = db.query(Producto).filter(Producto.nombre.ilike(f"%{texto}%"), Producto.activo==True).limit(5).all()
    if productos:
        lineas = [f"🔍 Encontré estos productos para *{texto}*:\n"]
        for p in productos:
            lineas.append(f"• {p.nombre}\n  Precio: S/ {p.precio_minorista:.2f} | Stock: {p.stock} unidades\n")
        return "\n".join(lineas)
    return ("No entendí tu mensaje 😅 Puedes escribir:\n"
            "• *catálogo* — ver productos\n• *pedido* — hacer un pedido\n"
            "• *estado* — ver tus pedidos\n• El nombre de un producto para buscarlo")


@router.post("/webhook/whatsapp")
def webhook_whatsapp(datos: WebhookMessage, db: Session = Depends(get_db)):
    from app.models import Cliente as ClienteModel, Mensaje as MensajeModel
    cliente = db.query(ClienteModel).filter(ClienteModel.telefono == datos.telefono).first()
    if not cliente:
        cliente = ClienteModel(nombre=datos.nombre or f"Cliente {datos.telefono}", telefono=datos.telefono)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
    db.add(MensajeModel(cliente_id=cliente.id, telefono=datos.telefono, contenido=datos.mensaje, tipo="entrante", leido=False))
    db.commit()
    respuesta = _respuesta_automatica(datos.mensaje, cliente, db)
    db.add(MensajeModel(cliente_id=cliente.id, telefono=datos.telefono, contenido=respuesta, tipo="saliente", leido=True))
    db.commit()
    return {"cliente_id": cliente.id, "cliente_nombre": cliente.nombre, "mensaje_recibido": datos.mensaje, "respuesta": respuesta}
