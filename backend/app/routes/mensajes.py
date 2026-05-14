"""Endpoints para Mensajes y chat por cliente."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Mensaje, Cliente
from app.schemas import MensajeCreate, MensajeOut

router = APIRouter(prefix="/mensajes", tags=["Mensajes"])


@router.get("/", response_model=List[MensajeOut])
def listar_mensajes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos los mensajes."""
    return (
        db.query(Mensaje)
        .order_by(Mensaje.fecha_creacion.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("/", response_model=MensajeOut, status_code=201)
def crear_mensaje(mensaje: MensajeCreate, db: Session = Depends(get_db)):
    """Registra un nuevo mensaje."""
    db_mensaje = Mensaje(**mensaje.model_dump())
    db.add(db_mensaje)
    db.commit()
    db.refresh(db_mensaje)
    return db_mensaje


@router.get("/cliente/{cliente_id}", response_model=List[MensajeOut])
def chat_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtiene el historial de chat de un cliente."""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return (
        db.query(Mensaje)
        .filter(Mensaje.cliente_id == cliente_id)
        .order_by(Mensaje.fecha_creacion.asc())
        .all()
    )


@router.put("/{mensaje_id}/leer", response_model=MensajeOut)
def marcar_leido(mensaje_id: int, db: Session = Depends(get_db)):
    """Marca un mensaje como leído."""
    mensaje = db.query(Mensaje).filter(Mensaje.id == mensaje_id).first()
    if not mensaje:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    mensaje.leido = True
    db.commit()
    db.refresh(mensaje)
    return mensaje


@router.put("/cliente/{cliente_id}/leer-todos")
def marcar_todos_leidos(cliente_id: int, db: Session = Depends(get_db)):
    """Marca todos los mensajes de un cliente como leídos."""
    db.query(Mensaje).filter(
        Mensaje.cliente_id == cliente_id, Mensaje.leido == False
    ).update({"leido": True})
    db.commit()
    return {"detail": "Mensajes marcados como leídos"}
