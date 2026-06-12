"""
Módulo: curso.py
Descripción: Representa un curso académico en el SGA.

RELACIÓN POO: ASOCIACIÓN con Docente
- Un Curso 'usa a' un Docente, pero si el docente no existe,
  el curso puede seguir existiendo (docente = None).
- Cardinalidad: 1 docente → muchos cursos.

ENCAPSULAMIENTO: todos los atributos son privados con getters/setters.
"""


class Curso:
    """
    Curso académico ofrecido en la universidad.
    Se asocia (débilmente) a un Docente que lo dicta.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        creditos: int = 3,
        cupo_maximo: int = 30,
    ):
        self.set_codigo(codigo)
        self.set_nombre(nombre)
        self.set_creditos(creditos)
        self.set_cupo_maximo(cupo_maximo)
        # ASOCIACIÓN: el curso puede tener o no un docente asignado
        self.__docente = None

    # ── SETTERS con validación ──────────────────────────────────────────────

    def set_codigo(self, codigo: str) -> None:
        """Valida que el código no esté vacío."""
        if not codigo or not codigo.strip():
            raise ValueError("El código del curso no puede estar vacío.")
        self.__codigo = codigo.strip().upper()

    def set_nombre(self, nombre: str) -> None:
        """Valida que el nombre tenga al menos 3 caracteres."""
        if not nombre or len(nombre.strip()) < 3:
            raise ValueError("El nombre del curso debe tener al menos 3 caracteres.")
        self.__nombre = nombre.strip()

    def set_creditos(self, creditos: int) -> None:
        """Valida que los créditos sean entre 1 y 10."""
        try:
            creditos = int(creditos)
        except (TypeError, ValueError) as error:
            raise ValueError("Los créditos deben ser un número entero.") from error
        if not 1 <= creditos <= 10:
            raise ValueError("Los créditos deben estar entre 1 y 10.")
        self.__creditos = creditos

    def set_cupo_maximo(self, cupo_maximo: int) -> None:
        """Valida que el cupo sea al menos 1."""
        try:
            cupo_maximo = int(cupo_maximo)
        except (TypeError, ValueError) as error:
            raise ValueError("El cupo máximo debe ser un número entero.") from error
        if cupo_maximo < 1:
            raise ValueError("El cupo máximo debe ser al menos 1.")
        self.__cupo_maximo = cupo_maximo

    # ── GETTERS ────────────────────────────────────────────────────────────

    def get_codigo(self) -> str:
        """Retorna el código único del curso."""
        return self.__codigo

    def get_nombre(self) -> str:
        """Retorna el nombre del curso."""
        return self.__nombre

    def get_creditos(self) -> int:
        """Retorna la cantidad de créditos académicos."""
        return self.__creditos

    def get_cupo_maximo(self) -> int:
        """Retorna el cupo máximo de estudiantes."""
        return self.__cupo_maximo

    def get_docente(self):
        """Retorna el docente asignado (puede ser None)."""
        return self.__docente

    # ── MÉTODOS DE NEGOCIO ─────────────────────────────────────────────────

    def asignar_docente(self, docente) -> None:
        """
        ASOCIACIÓN: el curso 'conoce' a su docente.
        El docente puede existir aunque el curso desaparezca.
        """
        self.__docente = docente

    def tiene_docente(self) -> bool:
        """Informa si el curso tiene docente asignado."""
        return self.__docente is not None

    # ── REPRESENTACIÓN ─────────────────────────────────────────────────────

    def __str__(self) -> str:
        docente_nombre = (
            self.__docente.get_nombre() if self.tiene_docente() else "Sin asignar"
        )
        return (
            f"[CURSO]\n"
            f"  Código    : {self.__codigo}\n"
            f"  Nombre    : {self.__nombre}\n"
            f"  Créditos  : {self.__creditos}\n"
            f"  Cupo      : {self.__cupo_maximo}\n"
            f"  Docente   : {docente_nombre}"
        )
