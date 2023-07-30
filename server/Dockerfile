# Utiliza una imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio /app/
COPY requirements.txt /app/

# Instala las dependencias definidas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación al directorio /app/
COPY . /app/

# Expone el puerto 8000, que es el puerto por defecto utilizado por Django
EXPOSE 8000

# Comando por defecto para ejecutar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

