CREATE TABLE ASISTENCIA(
        id INT IDENTITY(1,1) PRIMARY KEY,
	nombre_asig VARCHAR(100) NOT NULL,
	hora_clase_semanal INT NOT NULL,
);


CREATE TABLE ASISTENCIA(
	id INT IDENTITY(1,1) PRIMARY KEY,
	cedula_id INT NOT NULL FOREIGN KEY REFERENCES USUARIOS(cedula_id),
	tipo_trabajador INT NOT NULL,
	dia VARCHAR(10) NOT NULL,
	fecha DATE NOT NULL,
	hora_entrada TIME NOT NULL,
	hora_slida TIME NULL,
	observaciones VARCHAR(250) NULL,
);

CREATE TABLE BITACORA (
       id INT IDENTITY(1,1) PRIMARY KEY,
       fecha DATETIME2 NOT NULL DEFAULT GETDATE(),
       usuario_id INT NOT NULL,
       accion VARCHAR(300) NOT NULL,
       FOREIGN KEY (usuario_id) REFERENCES USUARIOS(id)
);

CREATE TABLE CURSOS_ASIGNADOS (
	id INT IDENTITY(1,1) PRIMARY KEY,
	grado_ano VARCHAR (10) NOT NULL,
	seccion VARCHAR(10) NOT NULL,
	salon_id FOREIGN KEY
);

CREATE TABLE HORARIO_DE_TRABAJO (
	id INT IDENTITY(1,1) PRIMARY KEY,
	dia VARCHAR(10) NOT NULL,
	hora_inicio TIME (7) NOT NULL,
	hora_fin TIME (7) NOT NULL,
	usuario_id FOREIGN KEY 
);

CREATE TABLE PERIODO_ACADEMICO (
	id INT IDENTITY(1,1) PRIMARY KEY,
	label VARCHAR(50) NOT NULL,
	fecha_inicio DATE NOT NULL,
	fecha_fin DATE NOT NULL,
);

CREATE TABLE SALON_DE_CLASE (
	id INT IDENTITY(1,1) PRIMARY KEY,
	numero_aula VARCHAR(10) NOT NULL,
	piso INT NOT NULL,
);

CREATE TABLE TIPO_DE_PERSONAL (
	id INT IDENTITY(1,1) PRIMARY KEY,
	descripcion VARCHAR(50) NOT NULL,

);

CREATE TABLE USUARIOS (
    id INT IDENTITY(1,1) PRIMARY KEY,
    cedula_id INT NOT NULL UNIQUE,
    nacionalidad CHAR(1) NOT NULL,
    primer_apellido VARCHAR(20) NOT NULL,
    segundo_apellido VARCHAR(20),
    primer_nombre VARCHAR(20) NOT NULL,
    segundo_nombre VARCHAR(20),
    fecha_nac DATE NOT NULL,
    domicilio VARCHAR(50) NOT NULL,
    nro_telf VARCHAR(15) NOT NULL,
    e_mail VARCHAR(70) NOT NULL,
    tipo_trabajador INT NOT NULL,
    contrasena VARCHAR(10) NOT NULL,
    FOREIGN KEY (tipo_trabajador) REFERENCES TIPO_DE_PERSONAL(id)
);

