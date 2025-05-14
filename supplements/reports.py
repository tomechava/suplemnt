# importing modules
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

# initializing variables with values

def createInvoice(fileName, documentTitle, companyName, title, subTitle, user, order, order_items):
    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)

    pdf.drawCentredString(300, 770, title)

    pdf.line(30, 710, 550, 710)

    text = pdf.beginText(40, 680)
    text.setFont("Courier", 18)
    text.setFillColor(colors.red)
    name = user.first_name + " " + user.last_name
    email = user.email
    phone = user.profile.phone
    address = order.address
    city = order.city
    postal_code = order.postal_code
    
    text.textLine(f"Customer: {name}    Email: {email}   Phone: {phone}")
    text.textLine(f"Address: {address}   City: {city}   Postal Code: {postal_code}")
    text.textLine(f"Order ID: {order.id}   Date: {order.created_at}")
    text.textLine(f"Total: {str(order.total_cost)}")
    text.textLine("Items:")
    text.setFont("Courier", 12)
    for item in order_items:
        text.textLine(f"{item.supplement.name} - {str(item.quantity)} x {str(item.supplement.price)} = {str(item.price*item.quantity)}")
    text.textLine(f"Total: {str(order.total_cost)}")
    pdf.drawText(text)

    pdf.save()