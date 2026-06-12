"""
Módulo: calificacion.py
Descripción: Representa una calificación dentro de una matrícula.

RELACIÓN POO: COMPOSICIÓN (parte de Matricula)
- Una Calificacion nace DENTRO de una Matricula y muere con ella.
- Si la matrícula se elimina, las calificaciones también desaparecen.

ENCAPSULAMIENTO:
- La nota es privada y validada estrictamente entre 0.0 y 5.0.
"""


class Calificacion:
    """
    Calificación individual de una actividad académica.
    Siempre vive dentro de una Matricula (composición fuerte).
    """

    NOTA_MINIMA = 0.0
    NOTA_MAXIMA = 5.0

    def __init__(self, actividad: str, nota: float):
        self.set_actividad(actividad)
        self.set_nota(nota)

    # ── SETTERS con validación ──────────────────────────────────────────────

    def set_actividad(self, actividad: str) -> None:
        """Valida que el nombre de la actividad no esté vacío."""
        if not actividad or not actividad.strip():
            raise ValueError("El nombre de la actividad no puede estar vacío.")
        self.__actividad = actividad.strip()

    def set_nota(self, nota: float) -> None:
        """
        Valida que la nota esté entre 0.0 y 5.0.
        Lanza ValueError si está fuera del rango — pytest.raises lo verifica.
        """
        try:
            nota = float(nota)
        except (TypeError, ValueError) as error:
            raise ValueError("La nota debe ser un número decimal.") from error

        if not self.NOTA_MINIMA <= nota <= self.NOTA_MAXIMA:
            raise ValueError(
                f"La nota debe estar entre {self.NOTA_MINIMA} y {self.NOTA_MAXIMA}. "
                f"Recibido: {nota}"
            )
        self.__nota = nota

    # ── GETTERS ────────────────────────────────────────────────────────────

    def get_actividad(self) -> str:
        """Retorna el nombre de la actividad evaluada."""
        return self.__actividad

    def get_nota(self) -> float:
        """Retorna la nota obtenida."""
        return self.__nota

    # ── REPRESENTACIÓN ─────────────────────────────────────────────────────

    def __str__(self) -> str:
        return f"{self.__actividad}: {self.__nota:.1f}"

    def __repr__(self) -> str:
        return f"Calificacion(actividad='{self.__actividad}', nota={self.__nota})"
