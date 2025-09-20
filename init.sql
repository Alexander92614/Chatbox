-- Paso 1: Crear la secuencia para la tabla de programas
CREATE SEQUENCE IF NOT EXISTS programas_id_seq;

-- Paso 2: Crear la tabla de programas y usar la secuencia
CREATE TABLE IF NOT EXISTS "public"."programas" (
    "id" int4 NOT NULL DEFAULT nextval('programas_id_seq'::regclass),
    "nombre" varchar(255) NOT NULL,
    PRIMARY KEY ("id")
);

-- Paso 3: Crear un índice único en el nombre para evitar duplicados
CREATE UNIQUE INDEX IF NOT EXISTS programas_nombre_key ON public.programas USING btree (nombre);

-- Paso 4: Crear la tabla de usuarios
CREATE TABLE IF NOT EXISTS "public"."usuarios" (
    "id" SERIAL PRIMARY KEY,
    "nombre" VARCHAR(100) NOT NULL,
    "email" VARCHAR(100) UNIQUE NOT NULL,
    "contrasena" VARCHAR(255) NOT NULL,
    "fecha_registro" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Paso 5: Insertar los programas académicos deseados
-- Se elimina la data anterior para evitar conflictos y se inserta la lista actualizada.
TRUNCATE TABLE programas RESTART IDENTITY;
INSERT INTO programas (nombre)
VALUES
    ('Ingeniería de Sistemas'),
    ('Medicina'),
    ('Derecho'),
    ('Diseño Gráfico'),
    ('Arquitectura'),
    ('Psicología');