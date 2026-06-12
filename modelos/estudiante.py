"""
Módulo: estudiante.py
Descripción: Representa a un estudiante universitario.

PILAR POO aplicado: HERENCIA + POLIMORFISMO + ENCAPSULAMIENTO
- Herencia: Estudiante extiende Persona usando super().__init__()
  para reutilizar nombre, identificación y email sin repetir código.
- Polimorfismo: mostrar_info() se implementa de forma diferente
  a la de Docente, aunque comparten la misma firma del método.
- Encapsulamiento: atributos propios también son privados.
"""

from modelos.persona import Persona


class Estudiante(Persona):
    """
    Estudiante universitario. Hereda de Persona y agrega:
    - código de estudiante
    - programa académico
    - promedio acumulado
    """

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        email: str,
        codigo: str,
        programa: str,
        promedio: float = 0.0,
    ):
        # Llamamos al constructor del padre para reutilizar su lógica.
        # Esto es HERENCIA correcta con super().__init__()
        super().__init__(identificacion, nombre, email)

        # Atributos propios del estudiante (encapsulados)
        self.set_codigo(codigo)
        self.set_programa(programa)
        self.set_promedio(promedio)

    # ── SETTERS con validación ──────────────────────────────────────────────

    def set_codigo(self, codigo: str) -> None:
        """Valida que el código no esté vacío."""
        if not codigo or not codigo.strip():
            raise ValueError("El código del estudiante no puede estar vacío.")
        self.__codigo = codigo.strip()

    def set_programa(self, programa: str) -> None:
        """Valida que el programa tenga al menos 3 caracteres."""
        if not programa or len(programa.strip()) < 3:
            raise ValueError("El programa académico debe tener al menos 3 caracteres.")
        self.__programa = programa.strip()

    def set_promedio(self, promedio: float) -> None:
        """Valida que el promedio esté entre 0.0 y 5.0."""
        try:
            promedio = float(promedio)
        except (TypeError, ValueError) as error:
            raise ValueError("El promedio debe ser un número.") from error
        if not 0.0 <= promedio <= 5.0:
            raise ValueError("El promedio debe estar entre 0.0 y 5.0.")
        self.__promedio = promedio

    # ── GETTERS ────────────────────────────────────────────────────────────

    def get_codigo(self) -> str:
        """Retorna el código del estudiante."""
        return self.__codigo

    def get_programa(self) -> str:
        """Retorna el programa académico."""
        return self.__programa

    def get_promedio(self) -> float:
        """Retorna el promedio acumulado."""
        return self.__promedio

    # ── POLIMORFISMO: implementación propia de mostrar_info() ──────────────

    def mostrar_info(self) -> str:
        """
        Muestra información específica del estudiante.
        Es diferente a la de Docente — eso es POLIMORFISMO.
        """
        return (
            f"[ESTUDIANTE]\n"
            f"  ID        : {self.get_identificacion()}\n"
            f"  Nombre    : {self.get_nombre()}\n"
            f"  Email     : {self.get_email()}\n"
            f"  Código    : {self.__codigo}\n"
            f"  Programa  : {self.__programa}\n"
            f"  Promedio  : {self.__promedio:.2f}"
        )
