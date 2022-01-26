BEGIN;
CREATE TABLE ttr_app_plantel (
    id integer NOT NULL PRIMARY KEY,
    nombre varchar(60),
    url_logo varchar(65535),
    mision varchar(65535),
    vision varchar(65535),
    nivel integer NOT NULL
)
;
CREATE TABLE ttr_app_myuser (
    user_ptr_id integer NOT NULL PRIMARY KEY REFERENCES auth_user (id),
    full_name varchar(60),
    rol integer NOT NULL,
    plantel_id integer NOT NULL REFERENCES ttr_app_plantel (id)
)
;
CREATE TABLE ttr_app_departamento (
    id integer NOT NULL PRIMARY KEY,
    nombre varchar(60),
    plantel_id integer NOT NULL REFERENCES ttr_app_plantel (id)
)
;
CREATE TABLE ttr_app_academia (
    id integer NOT NULL PRIMARY KEY,
    nombre varchar(60),
    depto_id integer NOT NULL REFERENCES ttr_app_departamento (id)
)
;
CREATE TABLE ttr_app_asignatura (
    id integer NOT NULL PRIMARY KEY,
    nombre varchar(60),
    fecha_creacion datetime NOT NULL,
    autor_id integer NOT NULL REFERENCES ttr_app_myuser (user_ptr_id),
    academia_id integer NOT NULL REFERENCES ttr_app_academia (id),
    presidente_id integer REFERENCES ttr_app_myuser (user_ptr_id)
)
;
CREATE TABLE ttr_app_clases_asignaturas (
    id integer NOT NULL PRIMARY KEY,
    clases_id integer NOT NULL,
    asignatura_id integer NOT NULL REFERENCES ttr_app_asignatura (id),
    UNIQUE (clases_id, asignatura_id)
)
;
CREATE TABLE ttr_app_clases (
    user_id integer NOT NULL PRIMARY KEY REFERENCES ttr_app_myuser (user_ptr_id)
)
;
CREATE TABLE ttr_app_instrumentoevaluacion (
    id integer NOT NULL PRIMARY KEY,
    level_show integer NOT NULL,
    titulo varchar(60),
    descripcion varchar(65535),
    fecha_creacion datetime NOT NULL,
    autor_id integer NOT NULL REFERENCES ttr_app_myuser (user_ptr_id),
    asignatura_id integer REFERENCES ttr_app_asignatura (id),
    oficial TINYINT(1) NOT NULL,
    fecha_modif datetime NOT NULL
)
;
CREATE TABLE ttr_app_rubrica (
    instrumentoevaluacion_ptr_id integer NOT NULL PRIMARY KEY REFERENCES ttr_app_instrumentoevaluacion (id)
)
;
CREATE TABLE ttr_app_categoriarubrica (
    id integer NOT NULL PRIMARY KEY,
    texto varchar(65535),
    rubrica_id integer NOT NULL REFERENCES ttr_app_rubrica (instrumentoevaluacion_ptr_id)
)
;
CREATE TABLE ttr_app_ponderacionrubrica (
    id integer NOT NULL PRIMARY KEY,
    valor varchar(65535),
    rubrica_id integer NOT NULL REFERENCES ttr_app_rubrica (instrumentoevaluacion_ptr_id)
)
;
CREATE TABLE ttr_app_criteriorubrica (
    id integer NOT NULL PRIMARY KEY,
    rubrica_id integer NOT NULL REFERENCES ttr_app_rubrica (instrumentoevaluacion_ptr_id),
    ponderacion_id integer NOT NULL REFERENCES ttr_app_ponderacionrubrica (id),
    categoria_id integer NOT NULL REFERENCES ttr_app_categoriarubrica (id),
    descripcion varchar(60)
)
;
CREATE TABLE ttr_app_listacotejo (
    instrumentoevaluacion_ptr_id integer NOT NULL PRIMARY KEY REFERENCES ttr_app_instrumentoevaluacion (id)
)
;
CREATE TABLE ttr_app_indicadorcotejo (
    id integer NOT NULL PRIMARY KEY,
    listacotejo_id integer NOT NULL REFERENCES ttr_app_listacotejo (instrumentoevaluacion_ptr_id),
    texto varchar(60),
    check_field TINYINT(1) NOT NULL,
    observaciones varchar(65535)
)
;
CREATE TABLE ttr_app_listaobservacion (
    instrumentoevaluacion_ptr_id integer NOT NULL PRIMARY KEY REFERENCES ttr_app_instrumentoevaluacion (id)
)
;
CREATE TABLE ttr_app_indicadorlistaobs (
    id integer NOT NULL PRIMARY KEY,
    listaobs_id integer NOT NULL REFERENCES ttr_app_listaobservacion (instrumentoevaluacion_ptr_id),
    texto varchar(60),
    valor integer NOT NULL
)
;
CREATE TABLE ttr_app_evaluacioninstrumento (
    id integer NOT NULL PRIMARY KEY,
    user_id integer NOT NULL REFERENCES ttr_app_myuser (user_ptr_id),
    instrumento_id integer NOT NULL REFERENCES ttr_app_instrumentoevaluacion (id),
    valor integer NOT NULL,
    fecha_creacion datetime NOT NULL,
    fecha_modif datetime NOT NULL
)
;
CREATE TABLE ttr_app_comentarioinstrumento (
    id integer NOT NULL PRIMARY KEY,
    user_id integer NOT NULL REFERENCES ttr_app_myuser (user_ptr_id),
    instrumento_id integer NOT NULL REFERENCES ttr_app_instrumentoevaluacion (id),
    texto varchar(65535),
    fecha_creacion datetime NOT NULL,
    fecha_modif datetime NOT NULL
)
;
CREATE INDEX ttr_app_myuser_5795a7f1 ON ttr_app_myuser (plantel_id);
CREATE INDEX ttr_app_departamento_5795a7f1 ON ttr_app_departamento (plantel_id);
CREATE INDEX ttr_app_academia_0190c970 ON ttr_app_academia (depto_id);
CREATE INDEX ttr_app_asignatura_40e8bcf3 ON ttr_app_asignatura (autor_id);
CREATE INDEX ttr_app_asignatura_530809dc ON ttr_app_asignatura (academia_id);
CREATE INDEX ttr_app_asignatura_6c340e16 ON ttr_app_asignatura (presidente_id);
CREATE INDEX ttr_app_clases_asignaturas_4f1bcf64 ON ttr_app_clases_asignaturas (clases_id);
CREATE INDEX ttr_app_clases_asignaturas_40ada371 ON ttr_app_clases_asignaturas (asignatura_id);
CREATE INDEX ttr_app_instrumentoevaluacion_40e8bcf3 ON ttr_app_instrumentoevaluacion (autor_id);
CREATE INDEX ttr_app_instrumentoevaluacion_40ada371 ON ttr_app_instrumentoevaluacion (asignatura_id);
CREATE INDEX ttr_app_categoriarubrica_b2cedf11 ON ttr_app_categoriarubrica (rubrica_id);
CREATE INDEX ttr_app_ponderacionrubrica_b2cedf11 ON ttr_app_ponderacionrubrica (rubrica_id);
CREATE INDEX ttr_app_criteriorubrica_b2cedf11 ON ttr_app_criteriorubrica (rubrica_id);
CREATE INDEX ttr_app_criteriorubrica_9af82b6d ON ttr_app_criteriorubrica (ponderacion_id);
CREATE INDEX ttr_app_criteriorubrica_5f2644f7 ON ttr_app_criteriorubrica (categoria_id);
CREATE INDEX ttr_app_indicadorcotejo_9eeae0a3 ON ttr_app_indicadorcotejo (listacotejo_id);
CREATE INDEX ttr_app_indicadorlistaobs_a1ae714f ON ttr_app_indicadorlistaobs (listaobs_id);
CREATE INDEX ttr_app_evaluacioninstrumento_6340c63c ON ttr_app_evaluacioninstrumento (user_id);
CREATE INDEX ttr_app_evaluacioninstrumento_82cf80c8 ON ttr_app_evaluacioninstrumento (instrumento_id);
CREATE INDEX ttr_app_comentarioinstrumento_6340c63c ON ttr_app_comentarioinstrumento (user_id);
CREATE INDEX ttr_app_comentarioinstrumento_82cf80c8 ON ttr_app_comentarioinstrumento (instrumento_id);
CREATE TABLE auth_permission (
    id integer NOT NULL PRIMARY KEY,
    name varchar(50) NOT NULL,
    content_type_id integer NOT NULL REFERENCES django_content_type (id),
    codename varchar(100) NOT NULL,
    UNIQUE (content_type_id, codename)
)
;
CREATE TABLE auth_group_permissions (
    id integer NOT NULL PRIMARY KEY,
    group_id integer NOT NULL,
    permission_id integer NOT NULL REFERENCES auth_permission (id),
    UNIQUE (group_id, permission_id)
)
;
CREATE TABLE auth_group (
    id integer NOT NULL PRIMARY KEY,
    name varchar(80) NOT NULL UNIQUE
)
;
CREATE TABLE auth_user_groups (
    id integer NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    group_id integer NOT NULL REFERENCES auth_group (id),
    UNIQUE (user_id, group_id)
)
;
CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    permission_id integer NOT NULL REFERENCES auth_permission (id),
    UNIQUE (user_id, permission_id)
)
;
CREATE TABLE auth_user (
    id integer NOT NULL PRIMARY KEY,
    password varchar(128) NOT NULL,
    last_login datetime NOT NULL,
    is_superuser TINYINT(1) NOT NULL,
    username varchar(30) NOT NULL UNIQUE,
    first_name varchar(30) NOT NULL,
    last_name varchar(30) NOT NULL,
    email varchar(75) NOT NULL,
    is_staff TINYINT(1) NOT NULL,
    is_active TINYINT(1) NOT NULL,
    date_joined datetime NOT NULL
)
;
CREATE INDEX auth_permission_37ef4eb4 ON auth_permission (content_type_id);
CREATE INDEX auth_group_permissions_5f412f9a ON auth_group_permissions (group_id);
CREATE INDEX auth_group_permissions_83d7f98b ON auth_group_permissions (permission_id);
CREATE INDEX auth_user_groups_6340c63c ON auth_user_groups (user_id);
CREATE INDEX auth_user_groups_5f412f9a ON auth_user_groups (group_id);
CREATE INDEX auth_user_user_permissions_6340c63c ON auth_user_user_permissions (user_id);
CREATE INDEX auth_user_user_permissions_83d7f98b ON auth_user_user_permissions (permission_id);

COMMIT;
