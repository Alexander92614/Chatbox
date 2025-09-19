# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los requerimientos e instalarlos
COPY requerimientos.txt .
RUN pip install --no-cache-dir -r requerimientos.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto en el que corre la app
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
