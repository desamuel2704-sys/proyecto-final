# 📊 Proyecto Final — Inteligencia de Negocios 5925 · 2026-1
## Dashboard Power BI · Ventas Retail Colombia

![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-F2C811?logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![DAX](https://img.shields.io/badge/DAX-Avanzado-0078D4?logo=microsoftazure&logoColor=white)

---

## 🎯 Descripción del Proyecto

Aplicación de conceptos de **Inteligencia de Negocios, DAX y diseño visual** sobre un modelo de Ventas Retail Colombia con datos 2024-2026.  
El proyecto evalúa: Modelo Estrella, Tabla Calendario, medidas DAX avanzadas (CALCULATE, SAMEPERIODLASTYEAR, RANKX, TOPN), diseño UI/UX de dashboards y control de versiones.

---

## 📁 Estructura del Repositorio

```
proyecto-bi-5925/
│
├── backend.py                   # Genera la base de datos SQLite
├── proyecto.db                  # Base de datos (generada por backend.py)
│
├── medidas_DAX.dax              # Todas las medidas DAX documentadas
│
├── preguntas_respuestas_BI.docx # Página de Preguntas y Respuestas (entregable)
│
├── [nombre_grupo].pbix          # Archivo Power BI (subir aquí)
│
└── README.md                    # Este archivo
```

---

## 🚀 Cómo Ejecutar el Backend

### Requisitos
- Python 3.10 o superior
- No requiere librerías externas (solo `sqlite3`, `random`, `os` — todo incluido en Python)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/proyecto-bi-5925.git
cd proyecto-bi-5925

# 2. Generar la base de datos
python backend.py

# Salida esperada:
# ✅  BASE DE DATOS GENERADA: proyecto.db
# ================================================
#   dim_categoria               5 filas
#   dim_producto               18 filas
#   dim_tienda                  7 filas
#   dim_vendedor                8 filas
#   dim_fecha               1.096 filas
#   fact_ventas             3.000 filas
# ================================================
```

---

## 🔌 Importar en Power BI Desktop

1. Abrir **Power BI Desktop**
2. **Obtener datos** → Buscar "SQLite" → Seleccionar `proyecto.db`
3. Marcar **todas las tablas** → Cargar
4. En la vista **Modelo**, conectar las claves foráneas:
   - `fact_ventas[fecha]` → `dim_fecha[fecha]`
   - `fact_ventas[producto_id]` → `dim_producto[producto_id]`
   - `fact_ventas[tienda_id]` → `dim_tienda[tienda_id]`
   - `fact_ventas[vendedor_id]` → `dim_vendedor[vendedor_id]`
   - `dim_producto[categoria_id]` → `dim_categoria[categoria_id]`
5. Seleccionar `dim_fecha` → **Marcar como tabla de fechas** → Columna de fecha: `fecha`
6. Crear una tabla vacía llamada `_Medidas` y copiar las medidas del archivo `medidas_DAX.dax`

---

## 📐 Modelo Estrella

```
                    dim_categoria
                         │
                         │ categoria_id
                         │
dim_tienda ──── fact_ventas ──── dim_producto
  tienda_id │       │       │ producto_id
            │  fecha│       │
            │       │       │
       dim_fecha  dim_vendedor
                  vendedor_id
```

| Tabla          | Tipo      | Filas  | Descripción                               |
|----------------|-----------|--------|-------------------------------------------|
| `fact_ventas`  | Hechos    | 3 000  | Transacciones con cantidad, precio, desc. |
| `dim_fecha`    | Dim. Tiempo | 1 096 | Calendario 2024-2026, marcada oficial    |
| `dim_producto` | Dimensión | 18     | Precio costo + venta para margen          |
| `dim_categoria`| Dimensión | 5      | Jerarquía Categoría → Producto            |
| `dim_tienda`   | Dimensión | 7      | 5 ciudades colombianas                    |
| `dim_vendedor` | Dimensión | 8      | Vendedores con ciudad base                |

---

## 📏 Medidas DAX Implementadas

Todas las medidas están documentadas en `medidas_DAX.dax`. Resumen:

| # | Medida | Función DAX Clave |
|---|--------|-------------------|
| 1 | Ingresos Totales | `SUMX` |
| 2 | Costo Total | `SUMX` + `RELATED` |
| 3 | Utilidad Bruta | Resta de medidas |
| 4 | Margen Bruto % | `DIVIDE` |
| 5 | Ingresos Año Anterior | `CALCULATE` + `SAMEPERIODLASTYEAR` |
| 6 | Variación YoY % | `DIVIDE` + medidas |
| 7 | Ingresos YTD | `CALCULATE` + `DATESYTD` |
| 8 | Ingresos QTD / MTD | `DATESQTD` / `DATESMTD` |
| 9 | Promedio Móvil 3M | `DATESINPERIOD` |
| 10 | Rank Producto | `RANKX` + `ALL` |
| 11 | % Participación | `DIVIDE` + `CALCULATE` + `ALL` |
| 12 | Cumplimiento Meta % | `DIVIDE` (meta = año ant. × 1.10) |

---

## 🎨 Principios de Diseño UI/UX Aplicados

- **Regla de los 5 segundos**: KPIs críticos visibles al primer vistazo (tarjetas en la parte superior).
- **Paleta estratégica**: Azul corporativo + semáforo verde/rojo para variaciones.
- **Etiquetas descriptivas**: Títulos de visual en formato "Métrica · Dimensión · Período".
- **Limpieza visual**: Sin bordes de gráficos, sin decimales en valores > 1 M, sin leyendas redundantes.
- **Segmentadores sincronizados**: Año, Categoría, Ciudad aplican globalmente a todas las páginas.

---

## ❓ Preguntas y Respuestas de Negocio

Ver el documento **`preguntas_respuestas_BI.docx`** para las 7 preguntas clave con:
- Respuesta directa con valores del dataset
- Gráfica específica que la soporta
- Filtros necesarios para llegar a la conclusión

---

## 👥 Equipo

| Nombre | GitHub | Ciudad |
|--------|--------|--------|
| Samuel Lozano | [@TU_USUARIO](https://github.com/TU_USUARIO) | Bogotá |
| [Compañero 2] | [@usuario2](https://github.com/usuario2) | — |
| [Compañero 3] | [@usuario3](https://github.com/usuario3) | — |

> ⚠️ **Recordatorio:** Cada integrante debe alojar el proyecto en su **propio repositorio personal público** y enviar su link individual.

---

## 📝 Notas de Entrega

- La calificación se basa **exclusivamente** en la calidad del archivo `.pbix`.
- Este repositorio debe contener: `backend.py`, `proyecto.db`, `.pbix` y `preguntas_respuestas_BI.docx`.
- Penalización de **10 puntos** por enviar el link del repositorio de un compañero.

---

*"Una visualización no es un conjunto de gráficos bonitos; es la respuesta exacta a un problema de negocio."*
