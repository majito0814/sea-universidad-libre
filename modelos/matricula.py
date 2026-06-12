"""
Módulo: matricula.py
Descripción: Vincula a un Estudiante con un Curso y contiene sus calificaciones.

RELACIÓN POO:
- COMPOSICIÓN con Calificacion: las calificaciones nacen y mueren con la matrícula.
  Si la matrícula se elimina, las calificaciones desaparecen también.
- Conecta Estudiante ↔ Curso (relación muchos a muchos resuelta con esta clase).

ENCAPSULAMIENTO: atributos privados con acceso controlado.
"""

from modelos.calificacion import Calificacion


class Matricula:
    """
    Matrícula académica: vincula un Estudiante con un Curso.
    Contiene las calificaciones del estudiante en ese curso específico.

    COMPOSICIÓN: las Calificaciones son parte de la Matricula y
    no tienen sentido fuera de ella.
    """

    def __init__(self, estudiante, curso_codigo: str):
        """
        Args:
            estudiante: objeto Estudiante (puede ser objeto real o ID)
            curso_codigo: código del curso en el que se matricula
        """
        if estudiante is None:
            raise ValueError("El estudiante no puede ser None.")
        if not curso_codigo or not str(curso_codigo).strip():
            raise ValueError("El código del curso no puede estar vacío.")

        self.__estudiante = estudiante
        self.__curso_codigo = str(curso_codigo).strip().upper()
        # COMPOSICIÓN: las calificaciones viven dentro de la matrícula
        self.__calificaciones = []

    # ── GETTERS ────────────────────────────────────────────────────────────

    def get_estudiante(self):
        """Retorna el objeto Estudiante."""
        return self.__estudiante

    def get_curso_codigo(self) -> str:
        """Retorna el código del curso."""
        return self.__curso_codigo

    def get_calificaciones(self) -> list:
        """Retorna una copia de la lista de calificaciones."""
        return list(self.__calificaciones)

    # ── MÉTODOS DE NEGOCIO ─────────────────────────────────────────────────

    def agregar_calificacion(self, actividad: str, nota: float) -> None:
        """
        COMPOSICIÓN en acción: crea una Calificacion dentro de esta matrícula.
        La Calificacion no existe de forma independiente.

        Args:
            actividad: nombre de la actividad (ej: 'Parcial 1', 'Final')
            nota: valor entre 0.0 y 5.0 (Calificacion valida esto)
        """
        nueva = Calificacion(actividad, nota)  # composición: nace aquí
        self.__calificaciones.append(nueva)

    def promedio(self) -> float:
        """
        Calcula el promedio de todas las calificaciones.
        Retorna 0.0 si no hay calificaciones aún.
        """
        if not self.__calificaciones:
            return 0.0
        total = sum(cal.get_nota() for cal in self.__calificaciones)
        return round(total / len(self.__calificaciones), 2)

    def cantidad_calificaciones(self) -> int:
        """Retorna cuántas calificaciones tiene la matrícula."""
        return len(self.__calificaciones)

    # ── REPRESENTACIÓN ─────────────────────────────────────────────────────

    def __str__(self) -> str:
        nombre_est = self.__estudiante.get_nombre()
        lineas = [
            f"[MATRÍCULA]",
            f"  Estudiante : {nombre_est}",
            f"  Curso      : {self.__curso_codigo}",
            f"  Promedio   : {self.promedio():.2f}",
            f"  Notas      :",
        ]
        if self.__calificaciones:
            for cal in self.__calificaciones:
                lineas.append(f"    - {cal}")
        else:
            lineas.append("    (Sin calificaciones aún)")
        return "\n".join(lineas)
