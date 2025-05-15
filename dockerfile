FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos apache2 y mod_wsgi
RUN apt-get update && apt-get install -y apache2 apache2-dev libapache2-mod-wsgi-py3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Recoge archivos estáticos
RUN python manage.py collectstatic --noinput

# Copia el archivo de configuración de Apache (que debes crear)
COPY ./config/apache/suplemnt.conf /etc/apache2/sites-available/suplemnt.conf

# Habilita el sitio y mod_wsgi, deshabilita el default
RUN a2dissite 000-default.conf \
    && a2ensite suplemnt.conf \
    && a2enmod wsgi

# Expone el puerto 80 (HTTP estándar)
EXPOSE 80

# Ejecuta Apache en primer plano
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
