CREATE DATABASE gestion_espacios;
USE gestion_espacios;
CREATE TABLE Usuarios (
	id_usuario INT NOT NULL AUTO_INCREMENT,
    codigo VARCHAR(8) NOT NULL,
    dni VARCHAR(8) NOT NULL,
	nombre VARCHAR(50) NOT NULL,
	apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
	contra VARCHAR(255) NOT NULL,
	rol ENUM('Estudiante', 'Profesor', 'Administrador') NOT NULL,
	PRIMARY KEY (id_usuario),
    UNIQUE INDEX codigo_UNIQUE (codigo ASC),
    UNIQUE INDEX dni_UNIQUE (dni ASC),
	UNIQUE INDEX correo_UNIQUE (correo ASC))
ENGINE = InnoDB;
CREATE TABLE Espacios(
   id_espacio INT NOT NULL AUTO_INCREMENT,
   nombre VARCHAR(45) NOT NULL,
   tipo ENUM('salon', 'laboratorio', 'otro') NOT NULL,
   ubicacion VARCHAR(100),
   capacidad INT,
   disponibilidad ENUM('Si','No') NOT NULL DEFAULT 'Si',
  PRIMARY KEY (id_espacio))
ENGINE = InnoDB;
CREATE TABLE Cursos(
   id_curso VARCHAR(10) NOT NULL,
   nombre VARCHAR(100) NOT NULL,
   ciclo INT NOT NULL,
   creditos INT NOT NULL,
   PRIMARY KEY (id_curso))
ENGINE = InnoDB;
CREATE TABLE Horario(
   id_horario INT NOT NULL auto_increment,
   dia ENUM('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado','Domingo') NOT NULL,
   hora_inicio TIME NOT NULL,
   hora_fin TIME NOT NULL,
  PRIMARY KEY (id_horario))
ENGINE = InnoDB;
CREATE TABLE Programacion_cursos (
	id_progrmacion_curso INT NOT NULL auto_increment,
    seccion INT NOT NULL,
	profesor VARCHAR(100) NULL,
	cantidad_matriculados INT NOT NULL DEFAULT 0,
	id_curso VARCHAR(10) NOT NULL,
	id_horario INT NOT NULL,
	PRIMARY KEY (id_progrmacion_curso),
    FOREIGN KEY (id_curso) REFERENCES Cursos(id_curso),
    FOREIGN KEY (id_horario) REFERENCES Horario(id_horario)
)
ENGINE = InnoDB;


-- SHOW CREATE TABLE nombre_tabla;
-- DROP TABLE nombre_tabla;
