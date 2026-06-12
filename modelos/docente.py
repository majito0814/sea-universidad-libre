"""
Módulo: docente.py
Descripción: Representa a un docente universitario.

PILAR POO aplicado: HERENCIA + POLIMORFISMO + ENCAPSULAMIENTO
- Herencia: Docente extiende Persona con super().__init__()
- Polimorfismo: mostrar_info() imprime datos propios del docente,
  distinto a lo que hace Estudiante.mostrar_info()
"""

from modelos.persona import Persona


class Docente(Persona):
    """
    Docente universitario. Hereda de Persona y agrega:
    - especialidad
    - título académico
    - lista de cursos que dicta (ASOCIACIÓN con Curso)
    """

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        email: str,
        especialidad: str,
        titulo: str,
    ):
        # Herencia correcta: reutilizamos la lógica de Persona
        super().__init__(identificacion, nombre, email)

        self.set_especialidad(especialidad)
        self.set_titulo(titulo)
        # Un docente puede dictar varios cursos — ASOCIACIÓN 1→*
        self.__cursos_dictados = []

    # ── SETTERS con validación ──────────────────────────────────────────────

    def set_especialidad(self, especialidad: str) -> None:
        """Valida que la especialidad no esté vacía."""
        if not especialidad or not especialidad.strip():
            raise ValueError("La especialidad no puede estar vacía.")
        self.__especialidad = especialidad.strip()

    def set_titulo(self, titulo: str) -> None:
        """Valida que el título no esté vacío."""
        if not titulo or not titulo.strip():
            raise ValueError("El título académico no puede estar vacío.")
        self.__titulo = titulo.strip()

    # ── GETTERS ────────────────────────────────────────────────────────────

    def get_especialidad(self) -> str:
        """Retorna la especialidad del docente."""
        return self.__especialidad

    def get_titulo(self) -> str:
        """Retorna el título académico."""
        return self.__titulo

    def get_cursos_dictados(self) -> list:
        """Retorna la lista de cursos que dicta este docente."""
        return list(self.__cursos_dictados)

    # ── MÉTODOS DE NEGOCIO ─────────────────────────────────────────────────

    def agregar_curso(self, curso) -> None:
        """
        ASOCIACIÓN: el docente 'conoce' sus cursos.
        Si el docente desaparece, los cursos pueden seguir existiendo.
        """
        self.__cursos_dictados.append(curso)

    # ── POLIMORFISMO ────────────────────────────────────────────────────────

    def mostrar_info(self) -> str:
        """
        Muestra información específica del docente.
        Diferente a Estudiante.mostrar_info() — eso es POLIMORFISMO.
        """
        cursos = len(self.__cursos_dictados)
        return (
            f"[DOCENTE]\n"
            f"  ID           : {self.get_identificacion()}\n"
            f"  Nombre       : {self.get_nombre()}\n"
            f"  Email        : {self.get_email()}\n"
            f"  Especialidad : {self.__especialidad}\n"
            f"  Título       : {self.__titulo}\n"
            f"  Cursos       : {cursos} curso(s) asignado(s)"
        )
