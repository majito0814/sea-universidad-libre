"""
Módulo: pruebas/test_sistema.py
Descripción: Pruebas unitarias del SGA con pytest.

CÓMO EJECUTAR:
    pytest pruebas/ -v

COBERTURA:
    pytest pruebas/ -v --cov=modelos

Se prueban:
    ✅ Creación válida de objetos
    ✅ Validaciones (ValueError con pytest.raises)
    ✅ Cálculo de promedio
    ✅ Polimorfismo (mostrar_info diferente en cada clase)
    ✅ Herencia (Estudiante y Docente son instancias de Persona)
    ✅ Composición (calificaciones viven en matrícula)
    ✅ Agregación (GestorEstudiantes administra estudiantes)
    ✅ Asociación (Curso puede tener docente asignado)
"""

import sys
import os
import pytest

# Agrega la raíz del proyecto al path para que Python encuentre los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modelos.persona import Persona
from modelos.estudiante import Estudiante
from modelos.docente import Docente
from modelos.calificacion import Calificacion
from modelos.matricula import Matricula
from modelos.curso import Curso
from servicios.gestor_estudiantes import GestorEstudiantes
from servicios.gestor_cursos import GestorCursos


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBAS DE ESTUDIANTE
# ══════════════════════════════════════════════════════════════════════════════

def test_estudiante_creacion_valida():
    """Prueba 1: Un estudiante se crea correctamente con datos válidos."""
    est = Estudiante("EST001", "Ana Ruiz", "ana@correo.com", "ING-001", "Ing. Sistemas")
    assert est.get_nombre() == "Ana Ruiz"
    assert est.get_identificacion() == "EST001"
    assert est.get_email() == "ana@correo.com"
    assert est.get_codigo() == "ING-001"
    assert est.get_programa() == "Ing. Sistemas"
    assert est.get_promedio() == 0.0


def test_estudiante_nombre_vacio_lanza_error():
    """Prueba 2: Crear un estudiante con nombre vacío debe lanzar ValueError."""
    with pytest.raises(ValueError):
        Estudiante("EST002", "", "x@y.com", "ING-002", "Sistemas")


def test_estudiante_email_invalido_lanza_error():
    """Prueba 3: Email sin '@' debe lanzar ValueError."""
    with pytest.raises(ValueError):
        Estudiante("EST003", "Pedro", "correo-invalido", "ING-003", "Sistemas")


def test_estudiante_promedio_fuera_de_rango():
    """Prueba 4: Promedio fuera de [0.0, 5.0] debe lanzar ValueError."""
    with pytest.raises(ValueError):
        Estudiante("EST004", "Luis", "l@c.com", "ING-004", "Sistemas", promedio=6.0)


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBAS DE CALIFICACIÓN (validación crítica del enunciado)
# ══════════════════════════════════════════════════════════════════════════════

def test_calificacion_valida():
    """Prueba 5: Una calificación con nota válida se crea sin errores."""
    cal = Calificacion("Parcial 1", 4.5)
    assert cal.get_actividad() == "Parcial 1"
    assert cal.get_nota() == 4.5


def test_calificacion_nota_mayor_a_5_lanza_error():
    """Prueba 6: Nota de 6.0 debe lanzar ValueError — requerido por el enunciado."""
    with pytest.raises(ValueError):
        Calificacion("Parcial", 6.0)


def test_calificacion_nota_negativa_lanza_error():
    """Prueba 7: Nota negativa también debe lanzar ValueError."""
    with pytest.raises(ValueError):
        Calificacion("Quiz", -1.0)


def test_calificacion_actividad_vacia_lanza_error():
    """Prueba 8: Actividad vacía debe lanzar ValueError."""
    with pytest.raises(ValueError):
        Calificacion("", 3.0)


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBAS DE MATRÍCULA Y PROMEDIO
# ══════════════════════════════════════════════════════════════════════════════

def test_promedio_correcto():
    """Prueba 9: El promedio de [4.0, 5.0] debe ser 4.5 — del enunciado."""
    est = Estudiante("EST001", "Ana Ruiz", "ana@correo.com", "ING-001", "Ing. Sistemas")
    mat = Matricula(est, "IS-101")
    mat.agregar_calificacion("Parcial", 4.0)
    mat.agregar_calificacion("Final", 5.0)
    assert mat.promedio() == 4.5


def test_promedio_sin_calificaciones_es_cero():
    """Prueba 10: Sin calificaciones, el promedio debe ser 0.0."""
    est = Estudiante("EST001", "Ana Ruiz", "ana@correo.com", "ING-001", "Ing. Sistemas")
    mat = Matricula(est, "IS-101")
    assert mat.promedio() == 0.0


def test_matricula_composicion_calificaciones():
    """Prueba 11: Las calificaciones se crean dentro de la matrícula (composición)."""
    est = Estudiante("EST001", "Ana Ruiz", "ana@correo.com", "ING-001", "Ing. Sistemas")
    mat = Matricula(est, "IS-101")
    mat.agregar_calificacion("Quiz 1", 3.5)
    mat.agregar_calificacion("Quiz 2", 4.0)
    assert mat.cantidad_calificaciones() == 2


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBAS DE POLIMORFISMO Y HERENCIA
# ══════════════════════════════════════════════════════════════════════════════

def test_polimorfismo_mostrar_info_diferente():
    """
    Prueba 12: mostrar_info() de Estudiante ≠ mostrar_info() de Docente.
    Esto verifica el POLIMORFISMO — del enunciado.
    """
    est = Estudiante("EST001", "Ana Ruiz", "ana@correo.com", "ING-001", "Ing. Sistemas")
    doc = Docente("DOC001", "Dr. Lopez", "lopez@correo.com", "POO", "Magíster")
    assert est.mostrar_info() != doc.mostrar_info()


def test_herencia_estudiante_es_persona():
    """
    Prueba 13: Estudiante es instancia de Persona (herencia correcta).
    Persona es abstracta — no se puede instanciar directamente.
    """
    est = Estudiante("EST001", "Ana Ruiz", "ana@correo.com", "ING-001", "Ing. Sistemas")
    assert isinstance(est, Persona)


def test_herencia_docente_es_persona():
    """Prueba 14: Docente también es instancia de Persona."""
    doc = Docente("DOC001", "Dr. Lopez", "lopez@correo.com", "POO", "Magíster")
    assert isinstance(doc, Persona)


def test_persona_no_se_puede_instanciar_directamente():
    """
    Prueba 15: Persona es abstracta — no puede instanciarse.
    ABSTRACCIÓN en acción.
    """
    with pytest.raises(TypeError):
        Persona("X001", "Juan", "juan@x.com")  # TypeError por clase abstracta


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBAS DE RELACIONES (Asociación, Agregación)
# ══════════════════════════════════════════════════════════════════════════════

def test_asociacion_curso_docente():
    """Prueba 16: Un Curso puede tener un Docente asignado (asociación)."""
    doc = Docente("DOC001", "Dr. Lopez", "lopez@correo.com", "POO", "Magíster")
    curso = Curso("IS-101", "Programación I", 3, 30)
    assert not curso.tiene_docente()
    curso.asignar_docente(doc)
    assert curso.tiene_docente()
    assert curso.get_docente().get_nombre() == "Dr. Lopez"


def test_agregacion_gestor_estudiantes():
    """
    Prueba 17: GestorEstudiantes agrega estudiantes (agregación).
    Los estudiantes existen independientemente del gestor.
    """
    gestor = GestorEstudiantes()
    est = Estudiante("EST001", "Ana Ruiz", "ana@correo.com", "ING-001", "Ing. Sistemas")
    gestor.registrar(est)
    assert gestor.total_estudiantes() == 1
    encontrado = gestor.buscar_por_id("EST001")
    assert encontrado is not None
    assert encontrado.get_nombre() == "Ana Ruiz"


def test_gestor_no_permite_duplicados():
    """Prueba 18: Registrar dos estudiantes con el mismo ID lanza ValueError."""
    gestor = GestorEstudiantes()
    est1 = Estudiante("EST001", "Ana Ruiz", "ana@correo.com", "ING-001", "Ing. Sistemas")
    est2 = Estudiante("EST001", "Otro Nombre", "otro@correo.com", "ING-002", "Sistemas")
    gestor.registrar(est1)
    with pytest.raises(ValueError):
        gestor.registrar(est2)


def test_gestor_cursos_matricular():
    """Prueba 19: El GestorCursos matricula correctamente a un estudiante en un curso."""
    gestor_c = GestorCursos()
    est = Estudiante("EST001", "Ana Ruiz", "ana@correo.com", "ING-001", "Ing. Sistemas")
    curso = Curso("IS-101", "Programación I", 3, 30)
    gestor_c.agregar_curso(curso)
    mat = gestor_c.matricular(est, "IS-101")
    assert mat is not None
    assert mat.get_curso_codigo() == "IS-101"


def test_gestor_cursos_no_doble_matricula():
    """Prueba 20: Matricular al mismo estudiante dos veces en el mismo curso lanza ValueError."""
    gestor_c = GestorCursos()
    est = Estudiante("EST001", "Ana Ruiz", "ana@correo.com", "ING-001", "Ing. Sistemas")
    curso = Curso("IS-101", "Programación I", 3, 30)
    gestor_c.agregar_curso(curso)
    gestor_c.matricular(est, "IS-101")
    with pytest.raises(ValueError):
        gestor_c.matricular(est, "IS-101")
