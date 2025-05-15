# Usa una imagen oficial de Python
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Permitir pasar secrets como argumentos desde GitHub Actions
ARG API_KEY
ENV API_KEY=${API_KEY}

# Establece el directorio de trabajo
WORKDIR /

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Recoge archivos estáticos (si usas archivos con {% static %} en templates)
RUN python manage.py collectstatic --noinput

# Expone el puerto que usará Gunicorn (no el de desarrollo)
EXPOSE 8000

# Ejecuta la app (usa Gunicorn, no python run.py)
CMD ["gunicorn", "suplemnt.wsgi:application", "--bind", "0.0.0.0:8000"]
