import sqlite3

# Base de datos SQLite
DB_FILE = "tareas.db"


def conectar_db():
    # Crea y devuelve la conexión
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Crea la tabla si no existe
    with conectar_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contrasena TEXT NOT NULL
            )
        """)
        conn.commit()


def usuario_existe(usuario):
    # Verifica si el usuario ya está registrado
    with conectar_db() as conn:
        cursor = conn.execute(
            "SELECT id FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        return cursor.fetchone() is not None


def crear_usuario(usuario, hash_contrasena):
    # Guarda un nuevo usuario con contraseña hasheada
    with conectar_db() as conn:
        conn.execute(
            "INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
            (usuario, hash_contrasena)
        )
        conn.commit()


def obtener_usuario(usuario):
    # Busca un usuario por nombre
    with conectar_db() as conn:
        cursor = conn.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        return cursor.fetchone()