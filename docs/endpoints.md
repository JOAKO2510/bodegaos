# Documentación de Endpoints — BodegaOS

Base URL: `http://127.0.0.1:8000/api`

---

## Clientes

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET    | `/clientes/` | Listar clientes (parámetros: `skip`, `limit`, `activo`) |
| POST   | `/clientes/` | Crear cliente |
| GET    | `/clientes/buscar?telefono=X` | Buscar por teléfono o correo |
| GET    | `/clientes/{id}` | Obtener cliente por ID |
| PUT    | `/clientes/{id}` | Actualizar cliente |
| DELETE | `/clientes/{id}` | Desactivar cliente |

### Body: Crear/Actualizar cliente
```json
{
  "nombre": "María García",
  "telefono": "51987654321",
  "correo": "maria@ejemplo.com",
  "direccion": "Av. Lima 123",
  "tipo_cliente": "minorista"
}
```

---

## Productos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET    | `/productos/` | Listar (parámetros: `activo`, `categoria`, `nombre`) |
| POST   | `/productos/` | Crear producto |
| GET    | `/productos/bajo-stock` | Productos con stock ≤ stock_mínimo |
| GET    | `/productos/{id}` | Obtener por ID |
| PUT    | `/productos/{id}` | Actualizar |
| DELETE | `/productos/{id}` | Desactivar |
| POST   | `/productos/{id}/movimiento` | Registrar movimiento de stock |
| GET    | `/productos/{id}/movimientos` | Historial de movimientos |

### Body: Movimiento de stock
```json
{
  "producto_id": 1,
  "tipo_movimiento": "entrada",
  "cantidad": 50,
  "motivo": "Reposición mensual"
}
```
Tipos: `entrada` | `salida` | `ajuste` | `devolucion`

---

## Pedidos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET    | `/pedidos/` | Listar (parámetros: `estado`, `cliente_id`) |
| POST   | `/pedidos/` | Crear pedido |
| GET    | `/pedidos/{id}` | Obtener pedido con detalles |
| PUT    | `/pedidos/{id}` | Actualizar estado/descuento |
| POST   | `/pedidos/{id}/items` | Agregar producto al pedido |
| DELETE | `/pedidos/{id}/items/{detalle_id}` | Eliminar item del pedido |
| POST   | `/pedidos/{id}/confirmar` | **Confirmar pedido y descontar stock** |

### Body: Crear pedido
```json
{
  "cliente_id": 1,
  "canal": "whatsapp",
  "descuento": 0
}
```

### Body: Agregar item
```json
{
  "producto_id": 3,
  "cantidad": 2,
  "precio_unitario": 5.50
}
```

### Flujo de estados
```
pendiente → en_proceso → confirmado → entregado
                              └── cancelado
```

---

## Mensajes

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET    | `/mensajes/` | Listar mensajes |
| POST   | `/mensajes/` | Crear mensaje |
| GET    | `/mensajes/cliente/{id}` | Chat de un cliente |
| PUT    | `/mensajes/{id}/leer` | Marcar mensaje como leído |
| PUT    | `/mensajes/cliente/{id}/leer-todos` | Marcar todos como leídos |

---

## Dashboard

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET    | `/dashboard` | Todas las métricas del dashboard |

### Respuesta
```json
{
  "total_clientes": 45,
  "total_productos": 120,
  "pedidos_hoy": 8,
  "ventas_hoy": 350.50,
  "productos_bajo_stock": 3,
  "mensajes_no_leidos": 12,
  "top_productos": [{"nombre": "Aceite Vegetal 1L", "total_vendido": 48}],
  "ventas_por_dia": [{"dia": "2025-01-15", "total": 180.00}],
  "ventas_por_mes": [{"anio": 2025, "mes": 1, "total": 4500.00}]
}
```

---

## Webhook WhatsApp (simulado)

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST   | `/webhook/whatsapp` | Simular mensaje entrante de WhatsApp |

### Body
```json
{
  "telefono": "51987654321",
  "mensaje": "hola",
  "nombre": "Juan Pérez"
}
```

### Respuesta
```json
{
  "cliente_id": 1,
  "cliente_nombre": "Juan Pérez",
  "mensaje_recibido": "hola",
  "respuesta": "¡Hola Juan Pérez! 👋 Bienvenido a nuestra bodega..."
}
```

### Palabras clave del chatbot
| Entrada | Respuesta |
|---------|-----------|
| `hola`, `buenas` | Mensaje de bienvenida |
| `catálogo`, `productos` | Lista de productos disponibles |
| `pedido` | Instrucciones para pedir |
| `estado`, `mi orden` | Lista de pedidos del cliente |
| `[nombre de producto]` | Búsqueda de producto |

---

## Documentación interactiva

- Swagger UI: `http://127.0.0.1:8000/api/docs`
- ReDoc: `http://127.0.0.1:8000/api/redoc`
