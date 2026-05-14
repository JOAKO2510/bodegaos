"""Datos de prueba para desarrollo — ejecutar una vez."""
from sqlalchemy.orm import Session
from app.models import Cliente, Producto


def seed_data(db: Session):
    """Inserta datos de muestra si la base está vacía."""
    if db.query(Cliente).count() > 0:
        return  # Ya hay datos

    # Clientes
    clientes = [
        Cliente(nombre="María García", telefono="51987654321", correo="maria@ejemplo.com",
                direccion="Av. Lima 123", tipo_cliente="minorista"),
        Cliente(nombre="Distribuidora López", telefono="51912345678", correo="lopez@dist.com",
                direccion="Jr. Comercio 456", tipo_cliente="mayorista"),
        Cliente(nombre="Juan Pérez", telefono="51999111222", correo="juan@mail.com",
                direccion="Calle Real 789", tipo_cliente="minorista"),
    ]
    db.add_all(clientes)

    # Productos
    productos = [
        Producto(codigo="ACE001", nombre="Aceite Vegetal 1L", categoria="Abarrotes",
                 precio_minorista=5.50, precio_mayorista=4.80, stock=120, stock_minimo=20),
        Producto(codigo="ARR001", nombre="Arroz Extra 5kg", categoria="Granos",
                 precio_minorista=14.90, precio_mayorista=13.00, stock=80, stock_minimo=15),
        Producto(codigo="AZU001", nombre="Azúcar Rubia 1kg", categoria="Abarrotes",
                 precio_minorista=3.20, precio_mayorista=2.80, stock=200, stock_minimo=30),
        Producto(codigo="SAL001", nombre="Sal de Mesa 1kg", categoria="Abarrotes",
                 precio_minorista=1.50, precio_mayorista=1.20, stock=8, stock_minimo=10),
        Producto(codigo="FID001", nombre="Fideos Spaghetti 500g", categoria="Pastas",
                 precio_minorista=2.80, precio_mayorista=2.30, stock=3, stock_minimo=20),
        Producto(codigo="ATU001", nombre="Atún en Conserva 170g", categoria="Conservas",
                 precio_minorista=4.50, precio_mayorista=3.90, stock=60, stock_minimo=10),
        Producto(codigo="JAB001", nombre="Jabón de Lavar 250g", categoria="Limpieza",
                 precio_minorista=1.80, precio_mayorista=1.40, stock=45, stock_minimo=10),
        Producto(codigo="DET001", nombre="Detergente 500g", categoria="Limpieza",
                 precio_minorista=6.90, precio_mayorista=6.00, stock=35, stock_minimo=8),
    ]
    db.add_all(productos)
    db.commit()
    print("✅ Datos de prueba insertados correctamente")
