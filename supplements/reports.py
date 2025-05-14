# importing modules
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
import os
from django.conf import settings

# initializing variables with values

def createInvoice(fileName, documentTitle, companyName, title, subTitle, user, order, order_items):
        # Crear la ruta completa para guardar el archivo
    file_path = os.path.join(settings.MEDIA_ROOT, 'invoices', fileName)
    
    # Crear el archivo PDF en la ruta especificada
    pdf = canvas.Canvas(file_path)
    text = pdf.beginText(40, 680)
    pdf.setTitle(documentTitle)

    pdf.drawCentredString(300, 770, title)

    pdf.line(30, 710, 550, 710)

    
    
    text.setFillColor(colors.black)
    text.textLine(companyName)
    pdf.line(30, 710, 550, 710)
    name = user.first_name + " " + user.last_name
    email = user.email
    phone = user.profile.phone
    address = order.address
    city = order.city
    postal_code = order.postal_code
    
    text.textLine(f"Customer: {name}")
    text.textLine(f"Email: {email}")
    text.textLine(f"Phone: {phone}")
    text.textLine(f"Address: {address}")
    text.textLine(f"City: {city}")
    text.textLine(f"Postal Code: {postal_code}")
    text.textLine(f"Order ID: {order.id}")
    text.textLine(f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    text.textLine(f"Total: ${str(order.total_cost)}")
    text.textLine("Items:")
    pdf.line(30, 710, 550, 710)
    for item in order_items:
        text.textLine(f"{item.supplement.name} - {str(item.quantity)} x ${str(item.supplement.price)} = ${str(item.price*item.quantity)}")
    text.textLine(f"Total: ${str(order.total_cost)}")
    pdf.drawText(text)
    
    pdf.save()