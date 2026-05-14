"""Endpoints CRUD para Clientes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session


from app.database import get_db
from app.models import Cliente
from app.schemas import ClienteCreate, ClienteUpdate, ClienteOut

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=List[ClienteOut])
def listar_clientes(
    skip: int = 0,
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """Lista todos los clientes con filtro opcional por estado activo."""
    q = db.query(Cliente)
    if activo is not None:
        q = q.filter(Cliente.activo == activo)
    return q.offset(skip).limit(limit).all()


@router.post("/", response_model=ClienteOut, status_code=201)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Crea un nuevo cliente."""
    db_cliente = Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@router.get("/buscar", response_model=Optional[ClienteOut])
def buscar_cliente(
    telefono: Optional[str] = Query(None),
    correo: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Busca cliente por teléfono o correo."""
    if telefono:
        cliente = db.query(Cliente).filter(Cliente.telefono == telefono).first()
        if cliente:
            return cliente
    if correo:
        cliente = db.query(Cliente).filter(Cliente.correo == correo).first()
        if cliente:
            return cliente
    return None


@router.get("/{cliente_id}", response_model=ClienteOut)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtiene un cliente por ID."""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.put("/{cliente_id}", response_model=ClienteOut)
def actualizar_cliente(
    cliente_id: int, datos: ClienteUpdate, db: Session = Depends(get_db)
):
    """Actualiza los datos de un cliente."""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{cliente_id}", status_code=204)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Elimina (desactiva) un cliente."""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente.activo = False
    db.commit()
