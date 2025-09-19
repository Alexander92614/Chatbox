-- Crear la tabla para los programas académicos
CREATE TABLE programas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL
);

-- Crear una tabla de ejemplo para usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insertar los programas iniciales desde el archivo programas.txt
INSERT INTO programas (nombre) VALUES
('Ingeniería de Sistemas'),
('Derecho'),
('Contaduría Pública'),
('Administración de Empresas'),
('Psicología');
