"""seed_productos.py — Productos reales de bodega peruana con categorías propias."""
from sqlalchemy.orm import Session
from app.models import Categoria, Producto, Cliente


CATEGORIAS = [
    ("Aceites",           "🛢"),
    ("Granos",            "🌾"),
    ("Abarrotes",         "🛒"),
    ("Pastas",            "🍝"),
    ("Conservas",         "🥫"),
    ("Lácteos",           "🥛"),
    ("Galletas",          "🍪"),
    ("Bebidas",           "🥤"),
    ("Bebidas calientes", "☕"),
    ("Limpieza",          "🧴"),
    ("Higiene",           "🪥"),
    ("Condimentos",       "🧂"),
    ("Snacks",            "🍿"),
]


def seed_data(db: Session):
    if db.query(Producto).count() > 0:
        return

    # ── 1. Crear categorías ──────────────────────────────
    cat_map = {}  # nombre -> id
    for nombre, emoji in CATEGORIAS:
        cat = db.query(Categoria).filter(Categoria.nombre == nombre).first()
        if not cat:
            cat = Categoria(nombre=nombre, emoji=emoji)
            db.add(cat)
            db.flush()
        cat_map[nombre] = cat.id

    # ── 2. Crear clientes de ejemplo ─────────────────────
    clientes = [
        Cliente(nombre="María Quispe",          telefono="51987001001",
                correo="maria@ejemplo.com",     direccion="Av. Tupac Amaru 234", tipo_cliente="minorista"),
        Cliente(nombre="Distribuidora El Mercado", telefono="51912002002",
                correo="dist.mercado@gmail.com",direccion="Jr. Comercio 890",   tipo_cliente="mayorista"),
        Cliente(nombre="Juan Carlos Ramos",     telefono="51999003003",
                correo="jcramos@mail.com",      direccion="Calle Los Laureles 12", tipo_cliente="minorista"),
    ]
    db.add_all(clientes)

    # ── 3. Crear productos ───────────────────────────────
    # (codigo, nombre, descripcion, categoria, p_min, p_may, stock, s_min)
    raw = [
        ("ACE-PRI-VEG-1L",  "Aceite Primor Vegetal 1L",           "Aceite vegetal Primor botella 1L",           "Aceites",           6.50, 5.80, 120, 20),
        ("ACE-PRI-VEG-5L",  "Aceite Primor Vegetal 5L",           "Aceite vegetal Primor bidón 5L",             "Aceites",          29.90,27.00,  40,  8),
        ("ACE-COC-BAL-1L",  "Aceite Cocinero Balanceado 1L",      "Aceite Cocinero balanceado botella 1L",      "Aceites",           6.20, 5.50, 100, 20),
        ("ACE-COC-BAL-5L",  "Aceite Cocinero Balanceado 5L",      "Aceite Cocinero balanceado bidón 5L",        "Aceites",          28.50,25.80,  35,  8),
        ("ACE-CAP-VEG-1L",  "Aceite Capri Vegetal 1L",            "Aceite vegetal Capri botella 1L",            "Aceites",           6.00, 5.30,  80, 15),
        ("ACE-SAO-VEG-1L",  "Aceite Sao Vegetal 1L",              "Aceite vegetal Sao botella 1L",              "Aceites",           5.80, 5.10,  60, 12),
        ("ARR-COS-EXT-1KG", "Arroz Costeño Extra 1kg",            "Arroz extra Costeño bolsa 1kg",              "Granos",            3.50, 3.10, 200, 40),
        ("ARR-COS-EXT-5KG", "Arroz Costeño Extra 5kg",            "Arroz extra Costeño bolsa 5kg",              "Granos",           15.90,14.50,  80, 15),
        ("ARR-NIL-EXT-1KG", "Arroz Nil Extra 1kg",                "Arroz extra Nil bolsa 1kg",                  "Granos",            3.30, 2.90, 150, 30),
        ("ARR-PLE-EXT-1KG", "Arroz El Plebeyo Extra 1kg",         "Arroz extra El Plebeyo bolsa 1kg",           "Granos",            3.20, 2.80, 120, 25),
        ("ARR-COS-INT-1KG", "Arroz Costeño Integral 1kg",         "Arroz integral Costeño bolsa 1kg",           "Granos",            4.20, 3.70,  50, 10),
        ("AZU-COS-RUB-1KG", "Azúcar Costeño Rubia 1kg",           "Azúcar rubia Costeño bolsa 1kg",             "Abarrotes",         3.20, 2.80, 200, 40),
        ("AZU-COS-BLA-1KG", "Azúcar Costeño Blanca 1kg",          "Azúcar blanca refinada Costeño bolsa 1kg",   "Abarrotes",         3.50, 3.10, 150, 30),
        ("AZU-COS-RUB-5KG", "Azúcar Costeño Rubia 5kg",           "Azúcar rubia Costeño bolsa 5kg",             "Abarrotes",        15.00,13.50,  60, 12),
        ("SAL-SAL-MES-1KG", "Sal Salinas de Mesa 1kg",            "Sal de mesa yodada bolsa 1kg",               "Abarrotes",         1.20, 0.95, 300, 50),
        ("SAL-SAL-MES-2KG", "Sal Salinas de Mesa 2kg",            "Sal de mesa yodada bolsa 2kg",               "Abarrotes",         2.20, 1.80, 150, 30),
        ("FID-DVT-SPA-500", "Fideos Don Vittorio Spaghetti 500g", "Fideos spaghetti Don Vittorio bolsa 500g",   "Pastas",            2.80, 2.40, 150, 30),
        ("FID-DVT-COD-500", "Fideos Don Vittorio Codo 500g",      "Fideos codo Don Vittorio bolsa 500g",        "Pastas",            2.80, 2.40, 120, 25),
        ("FID-SIB-SPA-500", "Fideos Sibarita Spaghetti 500g",     "Fideos spaghetti Sibarita bolsa 500g",       "Pastas",            2.60, 2.20, 100, 20),
        ("FID-SJO-SPA-500", "Fideos San Jorge Spaghetti 500g",    "Fideos spaghetti San Jorge bolsa 500g",      "Pastas",            2.70, 2.30, 100, 20),
        ("FID-MOL-SPA-500", "Fideos Molitalia Spaghetti 500g",    "Fideos spaghetti Molitalia bolsa 500g",      "Pastas",            2.90, 2.50,  80, 15),
        ("ATU-PRI-ACE-170", "Atún Primor en Aceite 170g",         "Atún en aceite vegetal Primor lata 170g",    "Conservas",         4.80, 4.20, 120, 24),
        ("ATU-PRI-AGU-170", "Atún Primor al Agua 170g",           "Atún al agua Primor lata 170g",              "Conservas",         4.50, 3.90, 100, 20),
        ("ATU-AYD-ACE-170", "Atún Ayudín en Aceite 170g",         "Atún en aceite Ayudín lata 170g",            "Conservas",         4.20, 3.60,  80, 15),
        ("ATU-SJO-ACE-170", "Atún San Jorge en Aceite 170g",      "Atún en aceite San Jorge lata 170g",         "Conservas",         4.30, 3.70,  80, 15),
        ("ATU-HAY-ACE-170", "Atún Hayduk en Aceite 170g",         "Atún en aceite Hayduk lata 170g",            "Conservas",         4.00, 3.40,  60, 12),
        ("LEC-GLO-EVA-400", "Leche Gloria Evaporada 400g",        "Leche evaporada entera Gloria tarro 400g",   "Lácteos",           3.80, 3.30, 200, 40),
        ("LEC-GLO-EVA-170", "Leche Gloria Evaporada 170g",        "Leche evaporada entera Gloria tarro 170g",   "Lácteos",           1.80, 1.50, 250, 50),
        ("LEC-PVI-EVA-400", "Leche Pura Vida Evaporada 400g",     "Leche evaporada Pura Vida tarro 400g",       "Lácteos",           3.50, 3.00, 150, 30),
        ("LEC-GLO-CHO-400", "Leche Gloria Chocolatada 400g",      "Leche chocolatada Gloria tarro 400g",        "Lácteos",           3.90, 3.40, 120, 24),
        ("GAL-SJO-SOD-210", "Galleta San Jorge Soda 210g",        "Galletas de soda San Jorge paquete 210g",    "Galletas",          2.50, 2.10, 100, 20),
        ("GAL-SJO-INT-210", "Galleta San Jorge Integral 210g",    "Galletas integrales San Jorge paquete 210g", "Galletas",          2.80, 2.40,  80, 15),
        ("GAL-CAS-CHO-170", "Galleta Casino Chocolate 170g",      "Galletas Casino rellenas chocolate 170g",    "Galletas",          2.20, 1.85, 120, 25),
        ("GAL-CAS-VAI-170", "Galleta Casino Vainilla 170g",       "Galletas Casino rellenas vainilla 170g",     "Galletas",          2.20, 1.85, 100, 20),
        ("BEB-INK-KOL-500", "Inca Kola 500ml",                    "Gaseosa Inca Kola botella 500ml",            "Bebidas",           2.00, 1.65, 200, 40),
        ("BEB-INK-KOL-1L5", "Inca Kola 1.5L",                    "Gaseosa Inca Kola botella 1.5L",             "Bebidas",           4.50, 3.90,  80, 15),
        ("BEB-COC-COL-500", "Coca-Cola 500ml",                    "Gaseosa Coca-Cola botella 500ml",            "Bebidas",           2.00, 1.65, 180, 36),
        ("BEB-PEP-PEP-500", "Pepsi 500ml",                        "Gaseosa Pepsi botella 500ml",                "Bebidas",           1.80, 1.45, 120, 24),
        ("BEB-AJE-KOL-500", "Kola Real 500ml",                    "Gaseosa Kola Real botella 500ml",            "Bebidas",           1.20, 0.95, 150, 30),
        ("BEB-SAN-AGU-500", "Agua San Luis 500ml",                "Agua mineral San Luis sin gas 500ml",        "Bebidas",           1.20, 0.95, 200, 40),
        ("BEB-SAN-AGU-1L5", "Agua San Luis 1.5L",                 "Agua mineral San Luis sin gas 1.5L",         "Bebidas",           2.50, 2.10, 120, 24),
        ("CAF-NES-CLA-6G",  "Nescafé Clásico Sobre 6g",           "Café soluble Nescafé clásico sobre 6g",      "Bebidas calientes", 0.80, 0.60, 200, 40),
        ("CAF-NES-CLA-50G", "Nescafé Clásico Frasco 50g",         "Café soluble Nescafé clásico frasco 50g",    "Bebidas calientes", 9.90, 8.60,  40,  8),
        ("CAF-ALT-MOL-500", "Café Altomayo Molido 500g",          "Café molido Altomayo bolsa 500g",            "Bebidas calientes",14.50,12.80,  30,  6),
        ("LIM-SAP-LEJ-1L",  "Lejía Sapolio 1L",                   "Lejía blanqueadora Sapolio botella 1L",      "Limpieza",          3.50, 2.90,  80, 16),
        ("LIM-SAP-DET-360", "Detergente Sapolio 360g",            "Detergente Sapolio bolsa 360g",              "Limpieza",          4.20, 3.60,  60, 12),
        ("LIM-BOL-DET-360", "Detergente Bolívar 360g",            "Detergente Bolívar bolsa 360g",              "Limpieza",          4.00, 3.40,  70, 14),
        ("LIM-BOL-DET-1KG", "Detergente Bolívar 1kg",             "Detergente Bolívar bolsa 1kg",               "Limpieza",          9.50, 8.20,  40,  8),
        ("LIM-AYU-JAB-150", "Jabón Ayudín Limón 150g",            "Jabón de lavar Ayudín limón barra 150g",     "Limpieza",          1.50, 1.20, 100, 20),
        ("HIG-SUB-SHA-400", "Shampoo Suave 400ml",                "Shampoo Suave clásico botella 400ml",        "Higiene",           8.50, 7.40,  40,  8),
        ("HIG-COL-CRE-100", "Pasta Dental Colgate 100ml",         "Crema dental Colgate triple acción 100ml",   "Higiene",           5.50, 4.80,  60, 12),
        ("HIG-SOF-PAP-4R",  "Papel Higiénico Suave 4 rollos",     "Papel higiénico Suave doble hoja 4 rollos",  "Higiene",           5.90, 5.10,  50, 10),
        ("CON-SIB-AJI-78",  "Sazonador Sibarita Ají Panca 78g",   "Sazonador Sibarita ají panca sobre 78g",     "Condimentos",       2.50, 2.10,  80, 16),
        ("CON-SIB-COM-78",  "Sazonador Sibarita Comino 78g",      "Sazonador Sibarita comino sobre 78g",        "Condimentos",       2.50, 2.10,  80, 16),
        ("CON-AJI-AJI-7G",  "Ajinomoto 7g",                       "Glutamato monosódico Ajinomoto sobre 7g",    "Condimentos",       0.50, 0.35, 300, 60),
        ("CON-ALC-MAY-100", "Mayonesa Alacena 100g",              "Mayonesa Alacena sachet 100g",               "Condimentos",       1.80, 1.45, 150, 30),
        ("CON-ALC-AJI-85",  "Crema Ají Amarillo Alacena 85g",     "Crema de ají amarillo Alacena sachet 85g",   "Condimentos",       2.00, 1.65, 100, 20),
        ("MEN-COS-FRE-500", "Frijol Canario Costeño 500g",        "Frijol canario Costeño bolsa 500g",          "Granos",            4.50, 3.90,  80, 16),
        ("MEN-COS-LEN-500", "Lenteja Costeño 500g",               "Lenteja verde Costeño bolsa 500g",           "Granos",            4.20, 3.60,  70, 14),
        ("MEN-COS-ARV-500", "Arveja Costeño 500g",                "Arveja partida Costeño bolsa 500g",          "Granos",            3.80, 3.20,  60, 12),
        ("SNK-LAY-CLA-42",  "Papas Lay's Clásicas 42g",           "Papas fritas Lay's clásicas bolsa 42g",      "Snacks",            2.50, 2.10, 100, 20),
        ("SNK-LAY-LIM-42",  "Papas Lay's Limón 42g",              "Papas fritas Lay's limón bolsa 42g",         "Snacks",            2.50, 2.10,  80, 16),
        ("SNK-INK-CHI-50",  "Chifles Inka Chips 50g",             "Chifles de plátano Inka Chips bolsa 50g",    "Snacks",            2.00, 1.65,  80, 16),
    ]

    productos = [
        Producto(
            codigo=cod, nombre=nom, descripcion=desc,
            categoria_id=cat_map.get(cat),
            precio_minorista=p_min, precio_mayorista=p_may,
            stock=stock, stock_minimo=s_min, activo=True,
        )
        for cod, nom, desc, cat, p_min, p_may, stock, s_min in raw
    ]
    db.add_all(productos)
    db.commit()
    print(f"✅ {len(CATEGORIAS)} categorías, {len(productos)} productos y {len(clientes)} clientes insertados")
