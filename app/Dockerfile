# Usa una imagen oficial de Python como base
FROM public.ecr.aws/docker/library/python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias e instálalas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación al contenedor
COPY . .

# Expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
