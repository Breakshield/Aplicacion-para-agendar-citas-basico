import sqlite3
import hashlib

DB = "citas.db"

def conectar():
    return sqlite3.connect(DB)

def crear_tablas():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        fecha TEXT,
        hora TEXT,
        medico TEXT
    )
    """)

    conn.commit()
    conn.close()

    crear_admin()

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def crear_admin():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE usuario='admin'")
    if not c.fetchone():
        c.execute(
            "INSERT INTO usuarios VALUES (NULL, ?, ?)",
            ("admin", hash_pass("admin123"))
        )
    conn.commit()
    conn.close()

def validar_login(usuario, password):
    conn = conectar()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND password=?",
        (usuario, hash_pass(password))
    )
    ok = c.fetchone() is not None
    conn.close()
    return ok

def agregar_cita(nombre, fecha, hora, medico):
    conn = conectar()
    c = conn.cursor()

    
    c.execute("""
        SELECT * FROM citas
        WHERE fecha=? AND hora=? AND medico=?
    """, (fecha, hora, medico))

    if c.fetchone():
        conn.close()
        return False, "Ese médico ya tiene una cita en ese horario"

  
    c.execute(
        "INSERT INTO citas VALUES (NULL, ?, ?, ?, ?)",
        (nombre, fecha, hora, medico)
    )
    conn.commit()
    conn.close()
    return True, "Cita agendada correctamente"


def obtener_citas():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM citas")
    datos = c.fetchall()
    conn.close()
    return datos

def eliminar_cita(id_cita):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM citas WHERE id = ?", (id_cita,))
    conn.commit()
    conn.close()

def buscar_citas_por_nombre(nombre):
    conn = conectar()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM citas WHERE nombre LIKE ?",
        (f"%{nombre}%",)
    )
    datos = c.fetchall()
    conn.close()
    return datos

def registrar_usuario(usuario, password):
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO usuarios VALUES (NULL, ?, ?)",
            (usuario, hash_pass(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def editar_cita(id_cita, nombre, fecha, hora, medico):
    conn = conectar()
    c = conn.cursor()


    c.execute("""
        SELECT * FROM citas
        WHERE fecha=? AND hora=? AND medico=? AND id!=?
    """, (fecha, hora, medico, id_cita))

    if c.fetchone():
        conn.close()
        return False, "Ese horario ya está ocupado"

    c.execute("""
        UPDATE citas
        SET nombre=?, fecha=?, hora=?, medico=?
        WHERE id=?
    """, (nombre, fecha, hora, medico, id_cita))

    conn.commit()
    conn.close()
    return True, "Cita actualizada"
