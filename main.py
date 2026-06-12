"""
Módulo: main.py
Descripción: Punto de entrada del Sistema de Gestión Académica (SGA).
             Menú principal con 5 módulos: Estudiantes, Cursos,
             Matrículas, Reportes y Salir.

CÓMO EJECUTAR:
    python main.py

NOTA SOBRE MySQL:
    El sistema intenta conectarse a MySQL. Si no está disponible,
    los datos se manejan en memoria (sin persistencia).
"""

from servicios.gestor_estudiantes import GestorEstudiantes
from servicios.gestor_cursos import GestorCursos
from modelos.estudiante import Estudiante
from modelos.docente import Docente
from modelos.curso import Curso

# ── Instancias globales de los gestores ────────────────────────────────────
gestor_est = GestorEstudiantes()
gestor_cur = GestorCursos()
docentes = []  # lista en memoria para docentes

# ── Intentar conectar con MySQL (opcional, no falla si no está disponible) ── 
try:
    from database.conexion import probar_conexion
    from servicios.estudiante_repositorio import EstudianteRepositorio
    from servicios.curso_repositorio import CursoRepositorio
    from servicios.matricula_repositorio import MatriculaRepositorio

    MYSQL_DISPONIBLE = probar_conexion()
    if MYSQL_DISPONIBLE:
        repo_est = EstudianteRepositorio()
        repo_cur = CursoRepositorio()
        repo_mat = MatriculaRepositorio()
except Exception:
    MYSQL_DISPONIBLE = False


# ══════════════════════════════════════════════════════════════════════════════
# UTILIDADES
# ══════════════════════════════════════════════════════════════════════════════

def limpiar_pantalla():
    """Imprime líneas en blanco para simular limpiar la pantalla."""
    print("\n" * 2)


def pedir_texto(mensaje: str) -> str:
    """Pide un texto y valida que no esté vacío."""
    while True:
        valor = input(f"  {mensaje}: ").strip()
        if valor:
            return valor
        print("  ⚠ No puede estar vacío. Intenta de nuevo.")


def pedir_numero(mensaje: str, minimo: float, maximo: float) -> float:
    """Pide un número en un rango y valida la entrada."""
    while True:
        try:
            valor = float(input(f"  {mensaje} [{minimo}-{maximo}]: "))
            if minimo <= valor <= maximo:
                return valor
            print(f"  ⚠ Debe estar entre {minimo} y {maximo}.")
        except ValueError:
            print("  ⚠ Ingresa un número válido.")


def encabezado(titulo: str) -> None:
    """Imprime un encabezado visual."""
    largo = 50
    print("\n" + "═" * largo)
    print(f"  {titulo.upper()}")
    print("═" * largo)


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1: ESTUDIANTES
# ══════════════════════════════════════════════════════════════════════════════

def menu_estudiantes():
    """Submenú de gestión de estudiantes."""
    while True:
        encabezado("Módulo Estudiantes")
        print("  1. Registrar nuevo estudiante")
        print("  2. Listar todos los estudiantes")
        print("  3. Buscar estudiante por ID")
        print("  4. Eliminar estudiante")
        print("  0. Volver al menú principal")

        opcion = input("\n  Elige una opción: ").strip()

        if opcion == "1":
            registrar_estudiante()
        elif opcion == "2":
            listar_estudiantes()
        elif opcion == "3":
            buscar_estudiante()
        elif opcion == "4":
            eliminar_estudiante()
        elif opcion == "0":
            break
        else:
            print("  ⚠ Opción no válida.")


def registrar_estudiante():
    """Registra un nuevo estudiante en el sistema."""
    encabezado("Registrar Estudiante")
    try:
        id_est = pedir_texto("Identificación (ej: 1234567890)")
        nombre = pedir_texto("Nombre completo")
        email = pedir_texto("Email")
        codigo = pedir_texto("Código de estudiante (ej: ING-2024-01)")
        programa = pedir_texto("Programa académico (ej: Ingeniería de Sistemas)")

        est = Estudiante(id_est, nombre, email, codigo, programa)
        gestor_est.registrar(est)

        # Persistir en MySQL si está disponible
        if MYSQL_DISPONIBLE:
            repo_est.guardar(est)
            print("\n  ✅ Estudiante registrado en memoria y en MySQL.")
        else:
            print("\n  ✅ Estudiante registrado en memoria (MySQL no disponible).")

    except ValueError as error:
        print(f"\n  ❌ Error de validación: {error}")
    except Exception as error:
        print(f"\n  ❌ Error inesperado: {error}")

    input("\n  Presiona ENTER para continuar...")


def listar_estudiantes():
    """Muestra todos los estudiantes registrados."""
    encabezado("Lista de Estudiantes")
    estudiantes = gestor_est.listar_todos()
    if not estudiantes:
        print("  (No hay estudiantes registrados)")
    else:
        print(f"  Total: {len(estudiantes)} estudiante(s)\n")
        for est in estudiantes:
            print(est.mostrar_info())
            print("  " + "-" * 40)
    input("\n  Presiona ENTER para continuar...")


def buscar_estudiante():
    """Busca y muestra un estudiante por ID."""
    encabezado("Buscar Estudiante")
    id_est = pedir_texto("Identificación del estudiante")
    est = gestor_est.buscar_por_id(id_est)
    if est:
        print(f"\n{est.mostrar_info()}")
    else:
        print(f"\n  ❌ No se encontró estudiante con ID '{id_est}'.")
    input("\n  Presiona ENTER para continuar...")


def eliminar_estudiante():
    """Elimina un estudiante del sistema."""
    encabezado("Eliminar Estudiante")
    id_est = pedir_texto("Identificación del estudiante a eliminar")
    eliminado = gestor_est.eliminar(id_est)
    if eliminado:
        print(f"\n  ✅ Estudiante '{id_est}' eliminado correctamente.")
    else:
        print(f"\n  ❌ No se encontró estudiante con ID '{id_est}'.")
    input("\n  Presiona ENTER para continuar...")


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2: CURSOS Y DOCENTES
# ══════════════════════════════════════════════════════════════════════════════

def menu_cursos():
    """Submenú de gestión de cursos."""
    while True:
        encabezado("Módulo Cursos")
        print("  1. Registrar nuevo docente")
        print("  2. Crear nuevo curso")
        print("  3. Asignar docente a curso")
        print("  4. Listar todos los cursos")
        print("  0. Volver al menú principal")

        opcion = input("\n  Elige una opción: ").strip()

        if opcion == "1":
            registrar_docente()
        elif opcion == "2":
            crear_curso()
        elif opcion == "3":
            asignar_docente_a_curso()
        elif opcion == "4":
            listar_cursos()
        elif opcion == "0":
            break
        else:
            print("  ⚠ Opción no válida.")


def registrar_docente():
    """Registra un nuevo docente."""
    encabezado("Registrar Docente")
    try:
        id_doc = pedir_texto("Identificación")
        nombre = pedir_texto("Nombre completo")
        email = pedir_texto("Email")
        especialidad = pedir_texto("Especialidad")
        titulo = pedir_texto("Título académico (ej: Magíster, PhD)")

        doc = Docente(id_doc, nombre, email, especialidad, titulo)
        docentes.append(doc)
        print(f"\n  ✅ Docente '{nombre}' registrado correctamente.")
    except ValueError as error:
        print(f"\n  ❌ Error: {error}")
    input("\n  Presiona ENTER para continuar...")


def crear_curso():
    """Crea un nuevo curso académico."""
    encabezado("Crear Curso")
    try:
        codigo = pedir_texto("Código del curso (ej: IS-101)")
        nombre = pedir_texto("Nombre del curso")
        creditos = int(pedir_numero("Créditos", 1, 10))
        cupo = int(pedir_numero("Cupo máximo", 1, 200))

        curso = Curso(codigo, nombre, creditos, cupo)
        gestor_cur.agregar_curso(curso)

        if MYSQL_DISPONIBLE:
            repo_cur.guardar(curso)
        print(f"\n  ✅ Curso '{nombre}' creado correctamente.")
    except ValueError as error:
        print(f"\n  ❌ Error: {error}")
    input("\n  Presiona ENTER para continuar...")


def asignar_docente_a_curso():
    """Asigna un docente existente a un curso — ASOCIACIÓN."""
    encabezado("Asignar Docente a Curso")
    if not docentes:
        print("  ⚠ No hay docentes registrados aún.")
        input("\n  Presiona ENTER para continuar...")
        return

    codigo_curso = pedir_texto("Código del curso")
    curso = gestor_cur.buscar_curso(codigo_curso)
    if not curso:
        print(f"  ❌ No existe el curso '{codigo_curso}'.")
        input("\n  Presiona ENTER para continuar...")
        return

    print("\n  Docentes disponibles:")
    for doc in docentes:
        print(f"    [{doc.get_identificacion()}] {doc.get_nombre()}")

    id_doc = pedir_texto("ID del docente a asignar")
    docente_encontrado = next(
        (d for d in docentes if d.get_identificacion() == id_doc), None
    )
    if docente_encontrado:
        curso.asignar_docente(docente_encontrado)
        docente_encontrado.agregar_curso(curso)
        print(f"\n  ✅ Docente '{docente_encontrado.get_nombre()}' asignado a '{codigo_curso}'.")
    else:
        print(f"  ❌ No se encontró docente con ID '{id_doc}'.")

    input("\n  Presiona ENTER para continuar...")


def listar_cursos():
    """Lista todos los cursos disponibles."""
    encabezado("Lista de Cursos")
    cursos = gestor_cur.listar_cursos()
    if not cursos:
        print("  (No hay cursos registrados)")
    else:
        for curso in cursos:
            print(str(curso))
            print("  " + "-" * 40)
    input("\n  Presiona ENTER para continuar...")


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3: MATRÍCULAS Y CALIFICACIONES
# ══════════════════════════════════════════════════════════════════════════════

def menu_matriculas():
    """Submenú de matrículas y calificaciones."""
    while True:
        encabezado("Módulo Matrículas")
        print("  1. Matricular estudiante en curso")
        print("  2. Agregar calificación a matrícula")
        print("  3. Ver matrículas de un estudiante")
        print("  0. Volver al menú principal")

        opcion = input("\n  Elige una opción: ").strip()

        if opcion == "1":
            matricular_estudiante()
        elif opcion == "2":
            agregar_calificacion()
        elif opcion == "3":
            ver_matriculas_estudiante()
        elif opcion == "0":
            break
        else:
            print("  ⚠ Opción no válida.")


def matricular_estudiante():
    """Matricula un estudiante en un curso."""
    encabezado("Matricular Estudiante")
    try:
        id_est = pedir_texto("ID del estudiante")
        est = gestor_est.buscar_por_id(id_est)
        if not est:
            print(f"  ❌ No existe estudiante con ID '{id_est}'.")
            input("\n  Presiona ENTER para continuar...")
            return

        codigo_curso = pedir_texto("Código del curso")
        matricula = gestor_cur.matricular(est, codigo_curso)
        print(f"\n  ✅ '{est.get_nombre()}' matriculado en '{codigo_curso}'.")

        if MYSQL_DISPONIBLE:
            repo_mat.guardar(matricula)

    except ValueError as error:
        print(f"\n  ❌ Error: {error}")
    input("\n  Presiona ENTER para continuar...")


def agregar_calificacion():
    """Agrega una calificación a una matrícula existente — COMPOSICIÓN."""
    encabezado("Agregar Calificación")
    try:
        id_est = pedir_texto("ID del estudiante")
        est = gestor_est.buscar_por_id(id_est)
        if not est:
            print(f"  ❌ No existe estudiante '{id_est}'.")
            input("\n  Presiona ENTER para continuar...")
            return

        codigo_curso = pedir_texto("Código del curso")
        mat = gestor_cur.buscar_matricula(id_est, codigo_curso)
        if not mat:
            print(f"  ❌ El estudiante no está matriculado en '{codigo_curso}'.")
            input("\n  Presiona ENTER para continuar...")
            return

        actividad = pedir_texto("Nombre de la actividad (ej: Parcial 1, Final)")
        nota = pedir_numero("Nota", 0.0, 5.0)

        mat.agregar_calificacion(actividad, nota)
        print(f"\n  ✅ Calificación agregada. Promedio actual: {mat.promedio():.2f}")

    except ValueError as error:
        print(f"\n  ❌ Error: {error}")
    input("\n  Presiona ENTER para continuar...")


def ver_matriculas_estudiante():
    """Muestra todas las matrículas y notas de un estudiante."""
    encabezado("Matrículas del Estudiante")
    id_est = pedir_texto("ID del estudiante")
    matriculas = gestor_cur.listar_matriculas_estudiante(id_est)
    if not matriculas:
        print(f"  (Sin matrículas para ID '{id_est}')")
    else:
        for mat in matriculas:
            print(str(mat))
            print("  " + "-" * 40)
    input("\n  Presiona ENTER para continuar...")


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 4: REPORTES
# ══════════════════════════════════════════════════════════════════════════════

def menu_reportes():
    """Submenú de reportes del sistema."""
    while True:
        encabezado("Módulo Reportes")
        print("  1. Total de estudiantes y cursos")
        print("  2. Estudiantes con promedio >= X")
        print("  3. Cursos con docente asignado")
        print("  0. Volver al menú principal")

        opcion = input("\n  Elige una opción: ").strip()

        if opcion == "1":
            reporte_totales()
        elif opcion == "2":
            reporte_promedio()
        elif opcion == "3":
            reporte_cursos_docente()
        elif opcion == "0":
            break
        else:
            print("  ⚠ Opción no válida.")


def reporte_totales():
    """Muestra estadísticas generales del sistema."""
    encabezado("Reporte General")
    print(f"  📚 Estudiantes registrados : {gestor_est.total_estudiantes()}")
    print(f"  📖 Cursos disponibles      : {len(gestor_cur.listar_cursos())}")
    print(f"  📝 Matrículas activas      : {gestor_cur.total_matriculas()}")
    print(f"  👩‍🏫 Docentes registrados    : {len(docentes)}")
    print(f"  🗄️  MySQL disponible        : {'Sí ✅' if MYSQL_DISPONIBLE else 'No ❌'}")
    input("\n  Presiona ENTER para continuar...")


def reporte_promedio():
    """Lista estudiantes con promedio mayor a un mínimo."""
    encabezado("Estudiantes por Promedio")
    minimo = pedir_numero("Promedio mínimo", 0.0, 5.0)
    lista = gestor_est.listar_con_promedio_mayor(minimo)
    if lista:
        for est in lista:
            print(f"  • {est.get_nombre()} — {est.get_promedio():.2f}")
    else:
        print(f"  (Ningún estudiante tiene promedio >= {minimo})")
    input("\n  Presiona ENTER para continuar...")


def reporte_cursos_docente():
    """Lista los cursos que tienen docente asignado."""
    encabezado("Cursos con Docente Asignado")
    cursos = gestor_cur.listar_cursos()
    con_docente = [c for c in cursos if c.tiene_docente()]
    if con_docente:
        for c in con_docente:
            print(f"  • [{c.get_codigo()}] {c.get_nombre()} → {c.get_docente().get_nombre()}")
    else:
        print("  (Ningún curso tiene docente asignado aún)")
    input("\n  Presiona ENTER para continuar...")


# ══════════════════════════════════════════════════════════════════════════════
# MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def menu_principal():
    """Menú principal del SGA. Bucle while True — no falla con entradas inválidas."""
    print("\n" + "█" * 50)
    print("  SISTEMA DE GESTIÓN ACADÉMICA — SGA")
    print("  Universidad Libre | Ingeniería de Sistemas")
    print("█" * 50)

    estado_mysql = "✅ Conectado" if MYSQL_DISPONIBLE else "❌ No disponible (modo memoria)"
    print(f"\n  MySQL: {estado_mysql}\n")

    while True:
        print("\n" + "═" * 50)
        print("  MENÚ PRINCIPAL")
        print("═" * 50)
        print("  1. 👨‍🎓 Estudiantes")
        print("  2. 📚 Cursos y Docentes")
        print("  3. 📝 Matrículas y Calificaciones")
        print("  4. 📊 Reportes")
        print("  0. 🚪 Salir")
        print("═" * 50)

        try:
            opcion = input("\n  Elige una opción: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  👋 Hasta luego.")
            break

        if opcion == "1":
            menu_estudiantes()
        elif opcion == "2":
            menu_cursos()
        elif opcion == "3":
            menu_matriculas()
        elif opcion == "4":
            menu_reportes()
        elif opcion == "0":
            print("\n  👋 Gracias por usar el SGA. ¡Hasta pronto!")
            break
        else:
            print("  ⚠ Opción no válida. Elige entre 0 y 4.")


# ── PUNTO DE ENTRADA ───────────────────────────────────────────────────────
if __name__ == "__main__":
    menu_principal()
