# Diagrama de Base de Datos — BodegaOS

## Diagrama Entidad-Relación (Mermaid)

```mermaid
erDiagram
    CLIENTES {
        int id PK
        string nombre
        string telefono
        string correo
        string direccion
        string tipo_cliente
        bool activo
        datetime fecha_creacion
    }

    PRODUCTOS {
        int id PK
        string codigo
        string nombre
        string descripcion
        string categoria
        float precio_minorista
        float precio_mayorista
        int stock
        int stock_minimo
        bool activo
        datetime fecha_creacion
    }

    PEDIDOS {
        int id PK
        int cliente_id FK
        string estado
        string canal
        float subtotal
        float descuento
        float total
        datetime fecha_creacion
    }

    DETALLE_PEDIDO {
        int id PK
        int pedido_id FK
        int producto_id FK
        int cantidad
        float precio_unitario
        float subtotal
    }

    MENSAJES {
        int id PK
        int cliente_id FK
        string telefono
        string direccion
        string contenido
        string tipo
        bool leido
        datetime fecha_creacion
    }

    MOVIMIENTOS_STOCK {
        int id PK
        int producto_id FK
        string tipo_movimiento
        int cantidad
        int stock_antes
        int stock_despues
        string motivo
        datetime fecha_creacion
    }

    CLIENTES ||--o{ PEDIDOS : "realiza"
    CLIENTES ||--o{ MENSAJES : "envía"
    PEDIDOS ||--|{ DETALLE_PEDIDO : "contiene"
    PRODUCTOS ||--o{ DETALLE_PEDIDO : "incluido en"
    PRODUCTOS ||--o{ MOVIMIENTOS_STOCK : "registra"
```

## Descripción de Relaciones

| Relación | Tipo | Descripción |
|----------|------|-------------|
| CLIENTES → PEDIDOS | 1:N | Un cliente puede tener muchos pedidos |
| CLIENTES → MENSAJES | 1:N | Un cliente puede tener muchos mensajes |
| PEDIDOS → DETALLE_PEDIDO | 1:N | Un pedido contiene uno o más productos |
| PRODUCTOS → DETALLE_PEDIDO | 1:N | Un producto puede estar en muchos pedidos |
| PRODUCTOS → MOVIMIENTOS_STOCK | 1:N | Cada producto registra todos sus movimientos |

## Estados de Pedido

```
pendiente → en_proceso → confirmado → entregado
                              │
                              └── cancelado
```

## Tipos de Movimiento de Stock

| Tipo | Descripción |
|------|-------------|
| `entrada` | Reposición de inventario |
| `salida` | Descuento por pedido confirmado |
| `ajuste` | Corrección manual de stock |
| `devolucion` | Retorno de mercadería |
