# BodegaOS

Sistema de gestión para bodegas con venta por **WhatsApp y chatbot**. Controla clientes, productos, pedidos y stock en tiempo real. 100% open source, sin costo alguno.

---

## ✨ Funcionalidades

- 👥 **Clientes** — CRUD, identificación automática por teléfono/correo
- 📦 **Productos** — CRUD, categorías, precios minorista/mayorista, control de stock
- 🛒 **Pedidos** — Creación, gestión de items, confirmación con descuento automático de stock
- 📊 **Dashboard** — Métricas en tiempo real: ventas, pedidos, bajo stock, top productos
- 💬 **Chat** — Bandeja de mensajes por cliente, visualización de conversaciones
- 🤖 **Chatbot WhatsApp** — Webhook simulado con respuestas automáticas inteligentes
- 📈 **Trazabilidad** — Historial completo de movimientos de stock

---

## 🛠 Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11 + FastAPI |
| ORM | SQLAlchemy 2.x |
| Base de datos | SQLite |
| Validación | Pydantic v2 |
| Servidor | Uvicorn |
| Frontend | HTML + CSS + JS (sin frameworks) |

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/bodegaos.git
cd bodegaos
```

### 2. Configurar el backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
```

### 3. Iniciar el servidor
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor arranca en `http://127.0.0.1:8000` y crea la base de datos automáticamente con datos de prueba.

### 4. Abrir el frontend

Abre `frontend/index.html` en tu navegador, o sirve la carpeta con cualquier servidor estático:

```bash
# Opción rápida con Python
cd frontend
python -m http.server 5500
# Luego ir a http://localhost:5500
```

---

## 📁 Estructura del proyecto

```
bodegaos/
├── backend/
│   ├── app/
│   │   ├── main.py           # Punto de entrada FastAPI
│   │   ├── database.py       # Conexión SQLite
│   │   ├── config/           # Settings (pydantic-settings)
│   │   ├── models/           # Modelos SQLAlchemy
│   │   ├── schemas/          # Schemas Pydantic v2
│   │   ├── routes/           # Endpoints REST
│   │   │   ├── clientes.py
│   │   │   ├── productos.py
│   │   │   ├── pedidos.py
│   │   │   ├── mensajes.py
│   │   │   └── dashboard.py  # + webhook WhatsApp
│   │   └── utils/
│   │       └── seed.py       # Datos de prueba
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html            # Landing
│   ├── dashboard.html        # Métricas
│   ├── productos.html        # Gestión de productos
│   ├── clientes.html         # Gestión de clientes
│   ├── pedidos.html          # Gestión de pedidos
│   ├── chat.html             # Chat + simulador WhatsApp
│   ├── css/style.css         # Estilos globales
│   └── js/
│       ├── utils.js          # API fetch, toast, formatters
│       └── sidebar.js        # Sidebar compartido
└── docs/
    ├── arquitectura.md
    ├── endpoints.md
    └── diagrama_bd.md
```

---

## 🤖 Chatbot WhatsApp

Simula mensajes enviando POST a `/api/webhook/whatsapp`:

```bash
curl -X POST http://localhost:8000/api/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -d '{"telefono": "51999123456", "mensaje": "hola", "nombre": "Pedro"}'
```

Palabras clave soportadas:
- `hola` / `buenas` → Bienvenida
- `catálogo` / `productos` → Lista de productos
- `pedido` → Instrucciones para pedir
- `estado` / `mi orden` → Estado de pedidos
- `[nombre de producto]` → Búsqueda automática

---

## 📡 API Docs

Con el servidor corriendo:
- **Swagger UI**: http://127.0.0.1:8000/api/docs
- **ReDoc**: http://127.0.0.1:8000/api/redoc

---

## 🗺 Roadmap

- [ ] Integración real con WhatsApp Business API (Meta)
- [ ] Autenticación JWT
- [ ] Roles y permisos (admin / vendedor)
- [ ] Exportar reportes a Excel/PDF
- [ ] Notificaciones de bajo stock por WhatsApp
- [ ] App móvil (PWA)

---

## 📄 Licencia

MIT — libre para uso personal y comercial.
