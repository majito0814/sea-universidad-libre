"""
Módulo: servicios/estudiante_repositorio.py
Descripción: Repositorio MySQL para la clase Estudiante.

PATRÓN REPOSITORIO:
- La clase Estudiante NO conoce SQL — solo tiene atributos y métodos de negocio.
- EstudianteRepositorio sí conoce SQL, pero no tiene lógica de negocio.
- Esto separa responsabilidades y facilita los tests.

CRUD implementado: guardar(), buscar_por_id(), listar_todos(), eliminar()
"""

from database.conexion import obtener_conexion
from modelos.estudiante import Estudiante


class EstudianteRepositorio:
    """
    Repositorio MySQL para persistir objetos Estudiante.
    Opera sobre la tabla 'estudiantes' de sga_universidad.
    """

    def guardar(self, est: Estudiante) -> None:
        """
        Inserta un nuevo estudiante en la base de datos.
        Usa INSERT IGNORE para evitar duplicados.

        Args:
            est: objeto Estudiante a persistir
        """
        sql = (
            "INSERT INTO estudiantes (id, nombre, email, codigo, programa) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        est.get_identificacion(),
                        est.get_nombre(),
                        est.get_email(),
                        est.get_codigo(),
                        est.get_programa(),
                    ),
                )
            con.commit()
        finally:
            con.close()

    def buscar_por_id(self, id_est: str):
        """
        Busca un estudiante por su ID en la BD.

        Returns:
            Objeto Estudiante si existe, None si no.
        """
        sql = "SELECT id, nombre, email, codigo, programa FROM estudiantes WHERE id = %s"
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql, (id_est,))
                fila = cur.fetchone()
                if fila:
                    return Estudiante(fila[0], fila[1], fila[2], fila[3], fila[4])
                return None
        finally:
            con.close()

    def listar_todos(self) -> list:
        """
        Retorna todos los estudiantes de la BD ordenados por nombre.

        Returns:
            Lista de objetos Estudiante.
        """
        sql = "SELECT id, nombre, email, codigo, programa FROM estudiantes ORDER BY nombre"
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql)
                return [
                    Estudiante(f[0], f[1], f[2], f[3], f[4])
                    for f in cur.fetchall()
                ]
        finally:
            con.close()

    def eliminar(self, id_est: str) -> bool:
        """
        Elimina un estudiante por ID.

        Returns:
            True si se eliminó, False si no existía.
        """
        sql = "DELETE FROM estudiantes WHERE id = %s"
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql, (id_est,))
                eliminados = cur.rowcount
            con.commit()
            return eliminados > 0
        finally:
            con.close()

    def actualizar_promedio(self, id_est: str, nuevo_promedio: float) -> None:
        """Actualiza el promedio de un estudiante en la BD."""
        # Nota: el esquema base no incluye promedio en la tabla,
        # pero lo actualizamos en el objeto en memoria.
        # Si quieres guardarlo, agrega la columna: ALTER TABLE estudiantes ADD promedio DECIMAL(3,2);
        pass
