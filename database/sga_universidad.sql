-- ============================================================
-- ARCHIVO: database/sga_universidad.sql
-- DESCRIPCIÓN: Script para crear la base de datos del SGA
--              en MySQL. Ejecutar en MySQL Workbench.
-- ============================================================

-- 1. Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS sga_universidad
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE sga_universidad;

-- 2. Tabla de docentes (va antes de cursos por la llave foránea)
CREATE TABLE IF NOT EXISTS docentes (
    id           VARCHAR(20)  PRIMARY KEY,
    nombre       VARCHAR(120) NOT NULL,
    email        VARCHAR(120) NOT NULL,
    especialidad VARCHAR(120),
    titulo       VARCHAR(80)
);

-- 3. Tabla de estudiantes
CREATE TABLE IF NOT EXISTS estudiantes (
    id       VARCHAR(20)  PRIMARY KEY,
    nombre   VARCHAR(120) NOT NULL,
    email    VARCHAR(120) NOT NULL,
    codigo   VARCHAR(30)  NOT NULL,
    programa VARCHAR(120)
);

-- 4. Tabla de cursos (referencia a docentes)
CREATE TABLE IF NOT EXISTS cursos (
    codigo      VARCHAR(20)  PRIMARY KEY,
    nombre      VARCHAR(120) NOT NULL,
    creditos    INT          DEFAULT 3,
    cupo_maximo INT          DEFAULT 30,
    docente_id  VARCHAR(20),
    FOREIGN KEY (docente_id) REFERENCES docentes(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- 5. Tabla de matrículas (estudiante ↔ curso, muchos a muchos)
CREATE TABLE IF NOT EXISTS matriculas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id   VARCHAR(20) NOT NULL,
    curso_codigo    VARCHAR(20) NOT NULL,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id)
        ON DELETE CASCADE,
    FOREIGN KEY (curso_codigo)  REFERENCES cursos(codigo)
        ON DELETE CASCADE,
    UNIQUE KEY uq_matricula (estudiante_id, curso_codigo)
);

-- 6. Tabla de calificaciones (parte de matrícula — composición)
CREATE TABLE IF NOT EXISTS calificaciones (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    matricula_id INT          NOT NULL,
    actividad   VARCHAR(80)  NOT NULL,
    nota        DECIMAL(3,1) NOT NULL,
    CONSTRAINT chk_nota CHECK (nota >= 0.0 AND nota <= 5.0),
    FOREIGN KEY (matricula_id) REFERENCES matriculas(id)
        ON DELETE CASCADE   -- si borra matrícula, borra calificaciones
);

-- ============================================================
-- Datos de prueba iniciales (opcionales)
-- Descomenta estas líneas si quieres datos de ejemplo al inicio
-- ============================================================

-- INSERT INTO docentes VALUES ('DOC001','Diana Romero','diana@unilibre.edu.co','Programación','Magíster');
-- INSERT INTO estudiantes VALUES ('EST001','Ana Ruiz','ana@correo.com','ING-001','Ingeniería de Sistemas',0.0);
-- INSERT INTO cursos VALUES ('IS-101','Programación I',3,30,'DOC001');
