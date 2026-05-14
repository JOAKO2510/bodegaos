"""Endpoints CRUD para Categorías."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Categoria
from app.schemas import CategoriaCreate, CategoriaUpdate, CategoriaOut

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("/", response_model=List[CategoriaOut])
def listar_categorias(activo: bool = None, db: Session = Depends(get_db)):
    """Lista todas las categorías."""
    q = db.query(Categoria)
    if activo is not None:
        q = q.filter(Categoria.activo == activo)
    return q.order_by(Categoria.nombre).all()


@router.post("/", response_model=CategoriaOut, status_code=201)
def crear_categoria(cat: CategoriaCreate, db: Session = Depends(get_db)):
    """Crea una nueva categoría."""
    existe = db.query(Categoria).filter(Categoria.nombre == cat.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")
    db_cat = Categoria(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.get("/{cat_id}", response_model=CategoriaOut)
def obtener_categoria(cat_id: int, db: Session = Depends(get_db)):
    """Obtiene una categoría por ID."""
    cat = db.query(Categoria).filter(Categoria.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return cat


@router.put("/{cat_id}", response_model=CategoriaOut)
def actualizar_categoria(cat_id: int, datos: CategoriaUpdate, db: Session = Depends(get_db)):
    """Actualiza una categoría."""
    cat = db.query(Categoria).filter(Categoria.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(cat, campo, valor)
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{cat_id}", status_code=204)
def eliminar_categoria(cat_id: int, db: Session = Depends(get_db)):
    """Desactiva una categoría."""
    cat = db.query(Categoria).filter(Categoria.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    cat.activo = False
    db.commit()
