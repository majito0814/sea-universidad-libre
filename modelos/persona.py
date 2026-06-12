"""
Módulo: persona.py
Descripción: Clase base abstracta que representa a cualquier miembro
             de la universidad (estudiante o docente).

PILAR POO aplicado: ABSTRACCIÓN + ENCAPSULAMIENTO
- Abstracción: Persona no se instancia directamente, representa la idea
  general de "miembro universitario" sin ser específica.
- Encapsulamiento: todos los atributos son privados (self.__x)
  y se accede/modifica solo a través de getters y setters validados.
"""

from abc import ABC, abstractmethod


class Persona(ABC):
    """
    Clase abstracta base para todo miembro de la universidad.
    No se puede instanciar directamente — solo Estudiante y Docente
    heredan de esta clase.
    """

    def __init__(self, identificacion: str, nombre: str, email: str):
        # Usamos los setters para que las validaciones se ejecuten
        # desde el primer momento, incluso al construir el objeto.
        self.set_identificacion(identificacion)
        self.set_nombre(nombre)
        self.set_email(email)

    # ── SETTERS con validación ──────────────────────────────────────────────

    def set_identificacion(self, identificacion: str) -> None:
        """Valida que la identificación no esté vacía."""
        if not identificacion or not identificacion.strip():
            raise ValueError("La identificación no puede estar vacía.")
        self.__identificacion = identificacion.strip()

    def set_nombre(self, nombre: str) -> None:
        """Valida que el nombre tenga al menos 2 caracteres."""
        if not nombre or len(nombre.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        self.__nombre = nombre.strip()

    def set_email(self, email: str) -> None:
        """Valida que el email contenga '@'."""
        if not email or "@" not in email:
            raise ValueError("El email debe contener '@'.")
        self.__email = email.strip()

    # ── GETTERS ────────────────────────────────────────────────────────────

    def get_identificacion(self) -> str:
        """Retorna la identificación de la persona."""
        return self.__identificacion

    def get_nombre(self) -> str:
        """Retorna el nombre completo."""
        return self.__nombre

    def get_email(self) -> str:
        """Retorna el email."""
        return self.__email

    # ── MÉTODO ABSTRACTO ───────────────────────────────────────────────────

    @abstractmethod
    def mostrar_info(self) -> str:
        """
        POLIMORFISMO: cada subclase implementa su propia versión.
        Retorna un string con la información del miembro.
        """

    # ── REPRESENTACIÓN ─────────────────────────────────────────────────────

    def __str__(self) -> str:
        return self.mostrar_info()
