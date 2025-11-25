# IMAGEN BASE Python 11 (usamos Python 3.11)
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios (app.py y requirements.txt)
# Asegúrate de tener app.py y requirements.txt en el mismo directorio donde construyes la imagen
COPY . .

# Instalar dependencias
# --no-cache-dir para no guardar caché pip en la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto (la app escucha en el puerto 80)
EXPOSE 5050

# Ejecutar la aplicación 
CMD ["python","app.py"]