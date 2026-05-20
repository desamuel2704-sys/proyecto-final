"""
=============================================================
  PROYECTO FINAL - INTELIGENCIA DE NEGOCIOS 5925 | 2026-1
  Backend: Generador de Base de Datos para Power BI
  Modelo: Ventas Retail Colombia
=============================================================
Ejecutar:  python backend.py
Genera:    proyecto.db  (SQLite, listo para importar en Power BI)
=============================================================
"""

import sqlite3
import random
import os
from datetime import date, timedelta

# ── Configuración ──────────────────────────────────────────
DB_PATH = "proyecto.db"
SEED    = 42
random.seed(SEED)

# ── Datos maestros ─────────────────────────────────────────
CATEGORIAS = [
    (1, "Electrónica",      "Dispositivos y accesorios tecnológicos"),
    (2, "Ropa y Calzado",   "Moda para hombre, mujer y niños"),
    (3, "Hogar y Muebles",  "Decoración y mobiliario"),
    (4, "Alimentos",        "Productos de consumo masivo"),
    (5, "Deportes",         "Artículos deportivos y fitness"),
]

PRODUCTOS = [
    # (id, nombre, categoria_id, precio_costo, precio_venta)
    (1,  "Smartphone básico",      1, 350_000,  699_000),
    (2,  "Audífonos Bluetooth",    1,  45_000,  120_000),
    (3,  "Cargador USB-C 65W",     1,  18_000,   55_000),
    (4,  "Tablet 10 pulgadas",     1, 480_000,  950_000),
    (5,  "Camiseta deportiva",     2,  15_000,   45_000),
    (6,  "Jean clásico",           2,  35_000,   95_000),
    (7,  "Tenis running",          2,  70_000,  180_000),
    (8,  "Chaqueta impermeable",   2,  85_000,  220_000),
    (9,  "Silla ergonómica",       3, 180_000,  420_000),
    (10, "Lámpara LED escritorio", 3,  22_000,   68_000),
    (11, "Estante modular",        3,  95_000,  230_000),
    (12, "Arroz 5kg",              4,   9_500,   18_000),
    (13, "Aceite de cocina 3L",    4,  12_000,   22_500),
    (14, "Café molido 500g",       4,  14_000,   28_000),
    (15, "Bicicleta estática",     5, 320_000,  750_000),
    (16, "Mancuernas 10kg par",    5,  45_000,  110_000),
    (17, "Colchoneta yoga",        5,  12_000,   35_000),
    (18, "Termo deportivo 1L",     5,   8_000,   28_000),
]

TIENDAS = [
    (1, "Bogotá Centro",     "Bogotá",       "Cundinamarca"),
    (2, "Bogotá Salitre",    "Bogotá",       "Cundinamarca"),
    (3, "Medellín El Poblado","Medellín",    "Antioquia"),
    (4, "Medellín Centro",   "Medellín",     "Antioquia"),
    (5, "Cali Norte",        "Cali",         "Valle del Cauca"),
    (6, "Barranquilla",      "Barranquilla", "Atlántico"),
    (7, "Bucaramanga",       "Bucaramanga",  "Santander"),
]

VENDEDORES = [
    (1, "Ana García",       "Bogotá"),
    (2, "Carlos López",     "Bogotá"),
    (3, "María Martínez",   "Medellín"),
    (4, "Juan Rodríguez",   "Medellín"),
    (5, "Luisa Vargas",     "Cali"),
    (6, "Pedro Jiménez",    "Barranquilla"),
    (7, "Diana Torres",     "Bucaramanga"),
    (8, "Andrés Morales",   "Bogotá"),
]

CANALES = ["Tienda física", "E-commerce", "Mayorista", "Teléfono"]


# ── Helpers ────────────────────────────────────────────────
def fecha_aleatoria(inicio: date, fin: date) -> date:
    delta = (fin - inicio).days
    return inicio + timedelta(days=random.randint(0, delta))


# ── Construcción de la DB ──────────────────────────────────
def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"  ↳ BD anterior eliminada: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # ── Dimensión: Categorías ──
    cur.execute("""
        CREATE TABLE dim_categoria (
            categoria_id   INTEGER PRIMARY KEY,
            nombre         TEXT NOT NULL,
            descripcion    TEXT
        )
    """)
    cur.executemany(
        "INSERT INTO dim_categoria VALUES (?,?,?)", CATEGORIAS
    )

    # ── Dimensión: Productos ──
    cur.execute("""
        CREATE TABLE dim_producto (
            producto_id    INTEGER PRIMARY KEY,
            nombre         TEXT NOT NULL,
            categoria_id   INTEGER NOT NULL,
            precio_costo   REAL NOT NULL,
            precio_venta   REAL NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES dim_categoria(categoria_id)
        )
    """)
    cur.executemany(
        "INSERT INTO dim_producto VALUES (?,?,?,?,?)", PRODUCTOS
    )

    # ── Dimensión: Tiendas ──
    cur.execute("""
        CREATE TABLE dim_tienda (
            tienda_id      INTEGER PRIMARY KEY,
            nombre_tienda  TEXT NOT NULL,
            ciudad         TEXT NOT NULL,
            departamento   TEXT NOT NULL
        )
    """)
    cur.executemany(
        "INSERT INTO dim_tienda VALUES (?,?,?,?)", TIENDAS
    )

    # ── Dimensión: Vendedores ──
    cur.execute("""
        CREATE TABLE dim_vendedor (
            vendedor_id    INTEGER PRIMARY KEY,
            nombre         TEXT NOT NULL,
            ciudad_base    TEXT NOT NULL
        )
    """)
    cur.executemany(
        "INSERT INTO dim_vendedor VALUES (?,?,?)", VENDEDORES
    )

    # ── Dimensión: Tiempo (Tabla Calendario) ──
    # Power BI la usará como tabla de fechas oficial
    cur.execute("""
        CREATE TABLE dim_fecha (
            fecha          TEXT PRIMARY KEY,
            anio           INTEGER,
            trimestre      INTEGER,
            mes            INTEGER,
            nombre_mes     TEXT,
            semana_anio    INTEGER,
            dia            INTEGER,
            nombre_dia     TEXT,
            es_fin_semana  INTEGER
        )
    """)

    MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
             "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    DIAS  = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

    inicio_cal = date(2024, 1, 1)
    fin_cal    = date(2026, 12, 31)
    d = inicio_cal
    filas_cal = []
    while d <= fin_cal:
        filas_cal.append((
            str(d),
            d.year,
            (d.month - 1) // 3 + 1,
            d.month,
            MESES[d.month - 1],
            d.isocalendar()[1],
            d.day,
            DIAS[d.weekday()],
            1 if d.weekday() >= 5 else 0,
        ))
        d += timedelta(days=1)
    cur.executemany("INSERT INTO dim_fecha VALUES (?,?,?,?,?,?,?,?,?)", filas_cal)

    # ── Tabla de Hechos: Ventas ──
    cur.execute("""
        CREATE TABLE fact_ventas (
            venta_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha          TEXT NOT NULL,
            tienda_id      INTEGER NOT NULL,
            producto_id    INTEGER NOT NULL,
            vendedor_id    INTEGER NOT NULL,
            canal          TEXT NOT NULL,
            cantidad       INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            descuento_pct  REAL NOT NULL DEFAULT 0,
            FOREIGN KEY (fecha)       REFERENCES dim_fecha(fecha),
            FOREIGN KEY (tienda_id)   REFERENCES dim_tienda(tienda_id),
            FOREIGN KEY (producto_id) REFERENCES dim_producto(producto_id),
            FOREIGN KEY (vendedor_id) REFERENCES dim_vendedor(vendedor_id)
        )
    """)

    # Generar 3 000 registros de ventas (2024-01-01 → 2026-05-19)
    inicio_v = date(2024, 1, 1)
    fin_v    = date(2026, 5, 19)
    ventas = []
    for _ in range(3_000):
        prod = random.choice(PRODUCTOS)          # (id, nombre, cat, costo, pvp)
        tienda_id   = random.randint(1, len(TIENDAS))
        vendedor_id = random.randint(1, len(VENDEDORES))
        canal       = random.choice(CANALES)
        cantidad    = random.randint(1, 15)
        descuento   = random.choice([0, 0, 0, 5, 10, 15, 20])  # mayoría sin descuento
        ventas.append((
            str(fecha_aleatoria(inicio_v, fin_v)),
            tienda_id,
            prod[0],
            vendedor_id,
            canal,
            cantidad,
            prod[4],   # precio_venta
            descuento,
        ))

    cur.executemany(
        "INSERT INTO fact_ventas "
        "(fecha, tienda_id, producto_id, vendedor_id, canal, cantidad, precio_unitario, descuento_pct) "
        "VALUES (?,?,?,?,?,?,?,?)",
        ventas,
    )

    con.commit()

    # ── Resumen ──
    print("\n✅  BASE DE DATOS GENERADA: proyecto.db")
    print("=" * 48)
    for tabla in ["dim_categoria","dim_producto","dim_tienda",
                  "dim_vendedor","dim_fecha","fact_ventas"]:
        n = cur.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
        print(f"  {tabla:<22}  {n:>6,} filas")
    print("=" * 48)
    con.close()


if __name__ == "__main__":
    print("🚀  Generando base de datos...")
    build_database()
    print("\n➡️  Importa 'proyecto.db' en Power BI Desktop:")
    print("    Obtener datos → Base de datos SQLite → proyecto.db")
