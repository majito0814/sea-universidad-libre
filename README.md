# 🎓 SGA — Sistema de Gestión Académica

**Universidad Libre | Ingeniería de Sistemas | Programación I — 2026**

Proyecto final integrador que implementa un Sistema de Gestión Académica
usando Programación Orientada a Objetos en Python, con persistencia en MySQL.

---

## 👥 Integrantes del Grupo

Nombre: Maria Jose Agudelo
Materia: Programación Orientada a Objetos
Universidad: Universidad Libre

---

## 📋 Descripción del Proyecto

El SGA es un sistema de consola que permite gestionar:

- **Estudiantes** — registro, búsqueda, eliminación
- **Docentes** — registro y asignación a cursos
- **Cursos** — creación y administración
- **Matrículas** — vinculación estudiante-curso con calificaciones
- **Reportes** — estadísticas del sistema

---

## 🏗️ Arquitectura del Proyecto

```
sga-universidad-libre/
├── modelos/               ← Clases de dominio (POO)
│   ├── persona.py         ← Clase abstracta base (Abstracción)
│   ├── estudiante.py      ← Hereda de Persona (Herencia)
│   ├── docente.py         ← Hereda de Persona (Herencia)
│   ├── curso.py           ← Tiene Docente (Asociación)
│   ├── matricula.py       ← Contiene Calificacion (Composición)
│   └── calificacion.py    ← Parte de Matricula (Composición)
├── servicios/             ← Lógica de negocio y acceso a datos
│   ├── gestor_estudiantes.py     ← Agrega Estudiantes (Agregación)
│   ├── gestor_cursos.py          ← Gestiona cursos y matrículas
│   ├── estudiante_repositorio.py ← CRUD MySQL para Estudiante
│   ├── curso_repositorio.py      ← CRUD MySQL para Curso
│   └── matricula_repositorio.py  ← CRUD MySQL para Matricula
├── database/
│   ├── conexion.py        ← Configuración central de MySQL
│   └── sga_universidad.sql← Script para crear las tablas
├── pruebas/
│   └── test_sistema.py    ← 20 pruebas unitarias con pytest
├── diagramas/
│   └── diagrama_clases.png← UML del sistema
├── main.py                ← Punto de entrada — menú principal
└── README.md
```

---

## 🔑 Pilares POO Implementados

| Pilar | Dónde | Cómo |
|-------|-------|------|
| **Abstracción** | `Persona` | Clase base abstracta con `ABC` — no se instancia directamente |
| **Encapsulamiento** | Todas las clases | Atributos `self.__x` con getters/setters validados |
| **Herencia** | `Estudiante`, `Docente` | `class Estudiante(Persona)` con `super().__init__()` |
| **Polimorfismo** | `mostrar_info()` | Cada clase imprime información distinta al mismo método |

## 🔗 Relaciones Implementadas

| Tipo | Clases | Descripción |
|------|--------|-------------|
| **Asociación** | `Curso` → `Docente` | El curso 'usa' al docente; ambos existen de forma independiente |
| **Agregación** | `GestorEstudiantes` ◇ `Estudiante` | El gestor agrupa estudiantes que existen sin él |
| **Composición** | `Matricula` ◆ `Calificacion` | Las calificaciones nacen y mueren con la matrícula |

---

## ⚙️ Requisitos e Instalación

### 1. Python 3.10+
```bash
python --version   # debe mostrar 3.10 o superior
```

### 2. Dependencias Python
```bash
pip install pytest pylint black mysql-connector-python
```

### 3. MySQL (obligatorio para persistencia)
- Descargar MySQL Community Server: https://dev.mysql.com/downloads/mysql/
- Descargar MySQL Workbench: https://dev.mysql.com/downloads/workbench/

### 4. Crear la base de datos
```sql
-- Abrir MySQL Workbench y ejecutar:
-- database/sga_universidad.sql
```

### 5. Configurar la contraseña de MySQL
En `database/conexion.py`, cambia:
```python
"password": "root",   # ← pon aquí tu contraseña real de MySQL
```

---

## 🚀 Cómo Ejecutar

```bash
# Ejecutar el sistema completo
python main.py

# Ejecutar las pruebas
pytest pruebas/ -v

# Analizar calidad de código
pylint modelos/ servicios/

# Formatear el código
black modelos/ servicios/
```

---

## 🧪 Pruebas (pytest)

El archivo `pruebas/test_sistema.py` contiene **20 pruebas** que verifican:

- ✅ Creación válida de objetos
- ✅ Validaciones con `ValueError` (notas inválidas, campos vacíos)
- ✅ Cálculo de promedio
- ✅ Polimorfismo (`mostrar_info()` diferente por clase)
- ✅ Herencia (`isinstance` con `Persona`)
- ✅ Abstracción (`Persona` no se puede instanciar)
- ✅ Composición (calificaciones en matrícula)
- ✅ Agregación (gestor de estudiantes)
- ✅ Asociación (docente en curso)
- ✅ Reglas de negocio (no duplicados, doble matrícula)

```
pytest pruebas/ -v
========================= 20 passed in 0.XX s =========================
```

---

## 🗃️ Base de Datos MySQL

Tablas creadas por `sga_universidad.sql`:

| Tabla | Descripción |
|-------|-------------|
| `estudiantes` | Datos personales y académicos del estudiante |
| `docentes` | Datos del docente y su especialidad |
| `cursos` | Cursos con referencia al docente (FK) |
| `matriculas` | Relación estudiante-curso (muchos a muchos) |
| `calificaciones` | Notas ligadas a una matrícula (ON DELETE CASCADE) |

---

## 🛠️ Comandos Git del equipo

```bash
git pull origin main
git add .
git commit -m "Descripción clara del cambio realizado"
git push origin main
git log --oneline --graph
```

---

## 📚 Bibliografía

- Python Software Foundation. (2026). *Python Documentation — Classes*. https://docs.python.org/3/tutorial/classes.html
- Object Management Group. (2017). *UML Specification v2.5.1*. https://www.omg.org/spec/UML/
- pytest. (2026). *pytest Documentation*. https://docs.pytest.org/en/stable/
- Martin, R. C. (2009). *Clean Code*. Prentice Hall.
