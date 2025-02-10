CREATE TABLE USUARIOS (
id INT IDENTITY(1,1) PRIMARY KEY,
    cedula_id INT NOT NULL UNIQUE,
    nacionalidad CHAR(1),
    primer_apellido VARCHAR(100) NOT NULL,
    segundo_apellido VARCHAR(100),
    primer_nombre VARCHAR(100) NOT NULL,
    segundo_nombre VARCHAR(100),
    fecha_nac DATE NOT NULL,
    domicilio VARCHAR(100) NOT NULL,
    nro_telf VARCHAR(15) NOT NULL,
    e_mail VARCHAR(100) NOT NULL,
    tipo_trabajador VARCHAR(15) NOT NULL,
    contrasena VARCHAR(255) NOT NULL
)
;
CREATE TABLE ASIGNATURA (
	id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_asig VARCHAR(100) NOT NULL,
    horas_clase_semanal INT NOT NULL
)
;
CREATE TABLE SALON_DE_CLASE (
	id INT IDENTITY(1,1) PRIMARY KEY,
    numero_aula VARCHAR(10) NOT NULL,
    piso INT NOT NULL
)
;
CREATE TABLE CURSOS_ASIGNADOS (
	id INT IDENTITY(1,1) PRIMARY KEY,
    grado_ano VARCHAR(10) NOT NULL,
    seccion VARCHAR(10) NOT NULL
)
;
CREATE TABLE TIPO_DE_PERSONAL (
	id INT IDENTITY(1,1) PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
)
;
CREATE TABLE PERIODO_ACADEMICO (
	id INT IDENTITY(1,1) PRIMARY KEY,		
    label VARCHAR(50) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
)
;
CREATE TABLE ASISTENCIA (
	id INT IDENTITY(1,1) PRIMARY KEY,
    dia VARCHAR(10) NOT NULL,
    fecha DATE NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_salida TIME NOT NULL,
    tipo_usuario VARCHAR(15),
    observaciones TEXT,
    FOREIGN KEY (usuario) REFERENCES USUARIOS(id)
)
;
CREATE TABLE HORARIO_DE_TRABAJO (
	id INT IDENTITY (1,1) PRIMARY KEY NOT NULL,
	dia VARCHAR(7) NOT NULL,
	fecha DATE NOT NULL,
	hora_inicio TIME NOT NULL,
	hora_fin TIME NOT NULL
)
;
CREATE TABLE BITACORA (
    id INT IDENTITY(1,1) PRIMARY KEY,
    usuario_id INT NOT NULL,
    accion VARCHAR(255) NOT NULL,
    detalles TEXT,
    fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (usuario_id) REFERENCES USUARIOS(id)
)
;
