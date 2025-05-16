# 🧪 SUPLEMNT — Plataforma de E-commerce de Suplementos

**suplemnt** es una plataforma de comercio electrónico desarrollada con **Django** para la venta de suplementos nutricionales. Este proyecto incluye funcionalidades completas para gestión de productos, autenticación de usuarios, carrito de compras, procesamiento de órdenes, generación de facturas y un asistente conversacional potenciado con Gemini API.

---

## 🚀 Deployment con Docker + Apache + GitHub Actions

### 🧱 Infraestructura

Este proyecto está configurado para desplegarse en un contenedor Docker usando **Apache2 como servidor web** y **mod_wsgi** para servir la aplicación Django. Utiliza también **GitHub Actions** para construir y publicar automáticamente la imagen Docker a Docker Hub al hacer push a la rama `main`.

### 📦 Imagen Docker

El contenedor incluye:
- Python 3.11
- Apache2 + mod_wsgi
- Django 5+
- Todas las dependencias listadas en `requirements.txt`
- Soporte para archivos estáticos y ejecución mediante Gunicorn (o mod_wsgi si prefieres)

### 🧪 ¿Cómo ejecutar en tu máquina local?

1. **Clona el repositorio**

```bash
git clone https://github.com/tu_usuario/suplemnt.git
cd suplemnt
```

2. **Crea un entorno virtual y activa**
```bash
python -m venv env
source env/bin/activate
```

3. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

4. **(Opcional) Configura variables de entorno**
Si usas funcionalidades como Gemini API, asegúrate de definir:
```bash
export API_KEY=tu_clave_api_de_gemini
```

5. **Corre el servidor de desarrollo**
```bash
python manage.py runserver
```

## Diagrama de Clases

![2f11038b-9205-46d6-93aa-6b07911cb512](https://github.com/user-attachments/assets/c55dc1bb-38fe-48e9-bdd7-4ad860891233)


## Diagrama de Arquitectura

![9cc26fcf-95f4-4ca3-b9e4-ba001bf6d395](https://github.com/user-attachments/assets/56e5193a-e669-4629-b0c0-cfd4e2ddf823)

# 📦 Dependencias Clave del Proyecto `suplemnt`

El proyecto `suplemnt` hace uso de las siguientes bibliotecas externas destacadas:

## 🤖 Gemini API (`google-generativeai`)
Utilizada para integrar un chatbot inteligente en la plataforma. Permite responder preguntas de los usuarios, asistir durante el proceso de compra y enriquecer la experiencia en tiempo real. La API key se gestiona mediante variables de entorno para mantener la seguridad.

## 🧾 ReportLab (`reportlab`)
Usada para generar facturas en formato PDF cuando se completa una orden. Permite crear documentos personalizados con encabezados, detalles de productos y totales, listos para descargar o enviar al cliente.

Estas dependencias están declaradas en el archivo `requirements.txt` del proyecto y se instalan automáticamente como parte del flujo de despliegue en Docker.


