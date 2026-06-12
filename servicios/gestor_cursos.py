"""
Módulo: gestor_cursos.py
Descripción: Servicio que administra cursos y matrículas del SGA.

RELACIÓN POO: ASOCIACIÓN con Curso y Matricula
- GestorCursos conoce los cursos y las matrículas pero no los posee en sentido fuerte.
- Responsabilidad única: administrar la lógica de cursos y matriculaciones.
"""

from modelos.curso import Curso
from modelos.matricula import Matricula


class GestorCursos:
    """
    Servicio de gestión de cursos y matrículas.
    Conecta estudiantes con cursos mediante objetos Matricula.
    """

    def __init__(self):
        self.__cursos = []
        self.__matriculas = []

    # ── GESTIÓN DE CURSOS ──────────────────────────────────────────────────

    def agregar_curso(self, curso: Curso) -> None:
        """Agrega un curso al sistema. Valida que el código sea único."""
        if not isinstance(curso, Curso):
            raise TypeError("Solo se pueden agregar objetos de tipo Curso.")
        if self.buscar_curso(curso.get_codigo()):
            raise ValueError(f"Ya existe el curso con código '{curso.get_codigo()}'.")
        self.__cursos.append(curso)

    def buscar_curso(self, codigo: str):
        """Busca un curso por código. Retorna None si no existe."""
        for curso in self.__cursos:
            if curso.get_codigo() == codigo.upper():
                return curso
        return None

    def listar_cursos(self) -> list:
        """Retorna la lista de todos los cursos."""
        return list(self.__cursos)

    def eliminar_curso(self, codigo: str) -> bool:
        """Elimina un curso por código. Retorna True si lo eliminó."""
        for i, curso in enumerate(self.__cursos):
            if curso.get_codigo() == codigo.upper():
                self.__cursos.pop(i)
                return True
        return False

    # ── GESTIÓN DE MATRÍCULAS ──────────────────────────────────────────────

    def matricular(self, estudiante, curso_codigo: str) -> Matricula:
        """
        Matricula a un estudiante en un curso.
        Valida que el curso exista y que no esté ya matriculado.

        Args:
            estudiante: objeto Estudiante
            curso_codigo: código del curso

        Returns:
            Matricula creada
        """
        curso = self.buscar_curso(curso_codigo)
        if not curso:
            raise ValueError(f"No existe el curso '{curso_codigo}'.")

        # Verificar si ya está matriculado
        if self.buscar_matricula(estudiante.get_identificacion(), curso_codigo):
            raise ValueError(
                f"El estudiante '{estudiante.get_nombre()}' "
                f"ya está matriculado en '{curso_codigo}'."
            )

        matricula = Matricula(estudiante, curso_codigo)
        self.__matriculas.append(matricula)
        return matricula

    def buscar_matricula(self, id_estudiante: str, curso_codigo: str):
        """Busca una matrícula por estudiante y curso. Retorna None si no existe."""
        for mat in self.__matriculas:
            misma_id = mat.get_estudiante().get_identificacion() == id_estudiante
            mismo_curso = mat.get_curso_codigo() == curso_codigo.upper()
            if misma_id and mismo_curso:
                return mat
        return None

    def listar_matriculas_estudiante(self, id_estudiante: str) -> list:
        """Retorna todas las matrículas de un estudiante."""
        return [
            mat for mat in self.__matriculas
            if mat.get_estudiante().get_identificacion() == id_estudiante
        ]

    def listar_matriculas_curso(self, curso_codigo: str) -> list:
        """Retorna todas las matrículas de un curso."""
        return [
            mat for mat in self.__matriculas
            if mat.get_curso_codigo() == curso_codigo.upper()
        ]

    def total_matriculas(self) -> int:
        """Retorna el número total de matrículas en el sistema."""
        return len(self.__matriculas)
