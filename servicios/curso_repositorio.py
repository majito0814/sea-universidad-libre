"""
Módulo: servicios/curso_repositorio.py
Descripción: Repositorio MySQL para la clase Curso.

PATRÓN REPOSITORIO: Curso no conoce SQL; este repositorio sí.
"""

from database.conexion import obtener_conexion
from modelos.curso import Curso


class CursoRepositorio:
    """
    Repositorio MySQL para persistir objetos Curso.
    Opera sobre la tabla 'cursos' de sga_universidad.
    """

    def guardar(self, curso: Curso) -> None:
        """Inserta un nuevo curso en la base de datos."""
        sql = (
            "INSERT INTO cursos (codigo, nombre, creditos, cupo_maximo, docente_id) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        docente_id = None
        if curso.tiene_docente():
            docente_id = curso.get_docente().get_identificacion()

        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        curso.get_codigo(),
                        curso.get_nombre(),
                        curso.get_creditos(),
                        curso.get_cupo_maximo(),
                        docente_id,
                    ),
                )
            con.commit()
        finally:
            con.close()

    def buscar_por_codigo(self, codigo: str):
        """
        Busca un curso por su código.

        Returns:
            Objeto Curso si existe, None si no.
        """
        sql = (
            "SELECT codigo, nombre, creditos, cupo_maximo "
            "FROM cursos WHERE codigo = %s"
        )
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql, (codigo.upper(),))
                fila = cur.fetchone()
                if fila:
                    return Curso(fila[0], fila[1], fila[2], fila[3])
                return None
        finally:
            con.close()

    def listar_todos(self) -> list:
        """Retorna todos los cursos ordenados por nombre."""
        sql = (
            "SELECT codigo, nombre, creditos, cupo_maximo "
            "FROM cursos ORDER BY nombre"
        )
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql)
                return [
                    Curso(f[0], f[1], f[2], f[3])
                    for f in cur.fetchall()
                ]
        finally:
            con.close()

    def eliminar(self, codigo: str) -> bool:
        """Elimina un curso por código. Retorna True si lo eliminó."""
        sql = "DELETE FROM cursos WHERE codigo = %s"
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql, (codigo.upper(),))
                eliminados = cur.rowcount
            con.commit()
            return eliminados > 0
        finally:
            con.close()
