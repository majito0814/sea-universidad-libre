"""
Módulo: gestor_estudiantes.py
Descripción: Servicio que administra el registro de estudiantes en memoria
             y se conecta con el repositorio MySQL para persistencia.

RELACIÓN POO: AGREGACIÓN con Estudiante
- GestorEstudiantes 'contiene' estudiantes, pero los estudiantes
  pueden existir sin el gestor.
- El gestor no crea ni destruye estudiantes; solo los agrupa y administra.
"""

from modelos.estudiante import Estudiante


class GestorEstudiantes:
    """
    Servicio central de gestión de estudiantes.

    AGREGACIÓN: agrupa objetos Estudiante que existen de forma independiente.
    Responsabilidad única: administrar la colección de estudiantes.
    """

    def __init__(self):
        # AGREGACIÓN: lista de objetos Estudiante ya existentes
        self.__estudiantes = []

    # ── OPERACIONES CRUD en memoria ─────────────────────────────────────────

    def registrar(self, estudiante: Estudiante) -> None:
        """
        Agrega un estudiante al sistema.
        Valida que no exista ya un estudiante con el mismo ID.
        """
        if not isinstance(estudiante, Estudiante):
            raise TypeError("Solo se pueden registrar objetos de tipo Estudiante.")
        if self.buscar_por_id(estudiante.get_identificacion()):
            raise ValueError(
                f"Ya existe un estudiante con ID '{estudiante.get_identificacion()}'."
            )
        self.__estudiantes.append(estudiante)

    def buscar_por_id(self, identificacion: str):
        """
        Busca y retorna un estudiante por su identificación.
        Retorna None si no lo encuentra.
        """
        for est in self.__estudiantes:
            if est.get_identificacion() == identificacion:
                return est
        return None

    def listar_todos(self) -> list:
        """Retorna una copia de la lista completa de estudiantes."""
        return list(self.__estudiantes)

    def eliminar(self, identificacion: str) -> bool:
        """
        Elimina un estudiante por su ID.
        Retorna True si se eliminó, False si no se encontró.
        """
        for i, est in enumerate(self.__estudiantes):
            if est.get_identificacion() == identificacion:
                self.__estudiantes.pop(i)
                return True
        return False

    def total_estudiantes(self) -> int:
        """Retorna cuántos estudiantes están registrados."""
        return len(self.__estudiantes)

    # ── REPORTES ────────────────────────────────────────────────────────────

    def listar_con_promedio_mayor(self, minimo: float) -> list:
        """Retorna estudiantes cuyo promedio es mayor o igual al mínimo dado."""
        return [
            est for est in self.__estudiantes
            if est.get_promedio() >= minimo
        ]
