"""
Módulo: servicios/matricula_repositorio.py
Descripción: Repositorio MySQL para persistir Matriculas y Calificaciones.

PATRÓN REPOSITORIO: separa la lógica SQL de las clases de dominio.
COMPOSICIÓN reflejada en SQL: calificaciones tienen ON DELETE CASCADE
en su llave foránea hacia matriculas.
"""

from database.conexion import obtener_conexion


class MatriculaRepositorio:
    """
    Repositorio MySQL para Matricula y sus Calificaciones.
    Opera sobre las tablas 'matriculas' y 'calificaciones'.
    """

    def guardar(self, matricula) -> int:
        """
        Guarda una matrícula en la BD y retorna su ID generado.

        Args:
            matricula: objeto Matricula

        Returns:
            ID entero de la matrícula insertada
        """
        sql = (
            "INSERT INTO matriculas (estudiante_id, curso_codigo) "
            "VALUES (%s, %s)"
        )
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        matricula.get_estudiante().get_identificacion(),
                        matricula.get_curso_codigo(),
                    ),
                )
                matricula_id = cur.lastrowid
            con.commit()
            return matricula_id
        finally:
            con.close()

    def guardar_calificacion(
        self, matricula_id: int, actividad: str, nota: float
    ) -> None:
        """
        Inserta una calificación en la BD ligada a una matrícula.

        Args:
            matricula_id: ID de la matrícula en la BD
            actividad: nombre de la actividad
            nota: valor entre 0.0 y 5.0
        """
        sql = (
            "INSERT INTO calificaciones (matricula_id, actividad, nota) "
            "VALUES (%s, %s, %s)"
        )
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql, (matricula_id, actividad, nota))
            con.commit()
        finally:
            con.close()

    def buscar_matricula_id(self, id_estudiante: str, curso_codigo: str):
        """
        Busca el ID numérico de una matrícula en la BD.

        Returns:
            ID entero si existe, None si no.
        """
        sql = (
            "SELECT id FROM matriculas "
            "WHERE estudiante_id = %s AND curso_codigo = %s"
        )
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql, (id_estudiante, curso_codigo.upper()))
                fila = cur.fetchone()
                return fila[0] if fila else None
        finally:
            con.close()

    def listar_por_estudiante(self, id_estudiante: str) -> list:
        """Retorna los códigos de cursos en los que está matriculado el estudiante."""
        sql = (
            "SELECT curso_codigo FROM matriculas "
            "WHERE estudiante_id = %s"
        )
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql, (id_estudiante,))
                return [fila[0] for fila in cur.fetchall()]
        finally:
            con.close()

    def eliminar(self, id_matricula: int) -> bool:
        """
        Elimina una matrícula por ID.
        MySQL elimina en cascada las calificaciones asociadas (ON DELETE CASCADE).
        """
        sql = "DELETE FROM matriculas WHERE id = %s"
        con = obtener_conexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql, (id_matricula,))
                eliminados = cur.rowcount
            con.commit()
            return eliminados > 0
        finally:
            con.close()
