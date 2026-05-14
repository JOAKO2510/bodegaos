# BodegaOS — Arquitectura del Sistema

## Visión General

BodegaOS es un sistema de gestión para bodegas que operan principalmente por WhatsApp y chatbot. Permite identificar clientes, gestionar productos, procesar pedidos y controlar el stock en tiempo real.

---

## Stack Tecnológico

| Capa        | Tecnología              |
|-------------|-------------------------|
| Backend     | Python 3.11 + FastAPI   |
| ORM         | SQLAlchemy 2.x          |
| Base de datos | SQLite                |
| Validación  | Pydantic v2             |
| Servidor    | Uvicorn                 |
| Frontend    | HTML + CSS + JS puro    |
| Estilos     | Bootstrap 5             |

---

## Flujo Principal

```
Cliente WhatsApp
      │
      ▼
POST /webhook/whatsapp
      │
      ├── ¿Cliente existe? ──No──► Crear cliente automáticamente
      │          │
      │         Sí
      │          │
      ▼          ▼
  Guardar mensaje entrante
      │
      ▼
  Procesar intención
  ├── Saludo → Bienvenida
  ├── Catálogo → Listar productos activos
  ├── Buscar producto → Filtro por nombre
  ├── Pedido → Crear/consultar pedido
  └── Estado → Consultar estado de pedido
      │
      ▼
  Guardar mensaje saliente
      │
      ▼
  Retornar respuesta al cliente
```

---

## Estructura de Carpetas

```
bodegaos/
├── backend/
│   ├── app/
│   │   ├── main.py           # Punto de entrada FastAPI
│   │   ├── database.py       # Conexión SQLite + SessionLocal
│   │   ├── config/           # Configuración y variables de entorno
│   │   ├── models/           # Modelos SQLAlchemy (tablas)
│   │   ├── schemas/          # Schemas Pydantic (validación)
│   │   ├── routes/           # Endpoints FastAPI
│   │   ├── services/         # Lógica de negocio
│   │   └── utils/            # Helpers y utilidades
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html            # Login / landing
│   ├── dashboard.html        # Métricas principales
│   ├── productos.html        # CRUD productos
│   ├── clientes.html         # CRUD clientes
│   ├── pedidos.html          # Gestión pedidos
│   ├── chat.html             # Bandeja de mensajes / chatbot
│   ├── css/                  # Estilos propios
│   ├── js/                   # Lógica frontend por módulo
│   └── assets/               # Imágenes / íconos
└── docs/
    ├── arquitectura.md
    ├── endpoints.md
    └── diagrama_bd.md
```

---

## Principios de Diseño

1. **Simple primero**: SQLite sin necesidad de servidor externo.
2. **Sin dependencias de pago**: 100% open source.
3. **API REST clara**: Todos los endpoints siguen convenciones REST.
4. **Trazabilidad**: Cada movimiento de stock queda registrado.
5. **Extensible**: Fácil de conectar con WhatsApp Business API real.
