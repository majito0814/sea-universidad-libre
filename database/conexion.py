"""
Módulo: database/conexion.py
Descripción: Centraliza la configuración y conexión a MySQL.

BUENA PRÁCTICA: un solo lugar para la conexión.
Si cambia el host o la contraseña, solo se modifica aquí.

INSTALACIÓN del conector:
    pip install mysql-connector-python

IMPORTANTE: cambia 'password' por tu contraseña real de MySQL.
"""

import mysql.connector
from mysql.connector import Error

# ── Configuración de conexión ──────────────────────────────────────────────
# ⚠ NO subas credenciales reales a GitHub.
# En producción usa variables de entorno: os.environ.get('DB_PASSWORD')
CONFIG_BD = {
    "host": "localhost",
    "user": "root",
    "password": "root",          # ← Cambia esto por tu contraseña MySQL
    "database": "sga_universidad",
    "charset": "utf8mb4",
    "autocommit": False,
}


def obtener_conexion():
    """
    Crea y retorna una conexión activa a MySQL.

    Returns:
        mysql.connector.connection: conexión lista para usar

    Raises:
        ConnectionError: si no puede conectarse a la base de datos
    """
    try:
        conexion = mysql.connector.connect(**CONFIG_BD)
        return conexion
    except Error as error:
        raise ConnectionError(
            f"No se pudo conectar a MySQL.\n"
            f"Verifica que MySQL Server esté corriendo y las credenciales.\n"
            f"Error original: {error}"
        ) from error


def probar_conexion() -> bool:
    """
    Prueba rápida para verificar que la conexión funciona.
    Útil para diagnosticar problemas al inicio del programa.

    Returns:
        True si la conexión es exitosa, False si falla.
    """
    try:
        con = obtener_conexion()
        con.close()
        return True
    except ConnectionError:
        return False
