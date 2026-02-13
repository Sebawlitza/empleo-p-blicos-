import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ------------------------------
# CONFIGURACIÓN
# ------------------------------
URL = "https://www.empleospublicos.cl"
PALABRA_CLAVE = "Diseñador"

# Correo de notificación
REMITENTE = "sebastian.bawlitza@gmail.com"
PASSWORD = "ydnlakekkjileobz"  # tu contraseña de aplicación
DESTINATARIO = "tu_correo@gmail.com"

# Empleos ya vistos
empleos_vistos = set()

# ------------------------------
# FUNCIONES
# ------------------------------

def enviar_correo(asunto, mensaje):
    msg = MIMEMultipart()
    msg['From'] = REMITENTE
    msg['To'] = DESTINATARIO
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(REMITENTE, PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[{datetime.now()}] Correo enviado correctamente")
    except Exception as e:
        print(f"[{datetime.now()}] Error al enviar correo:", e)


def revisar_empleos():
    print(f"[{datetime.now()}] Revisando empleos...")
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except Exception as e:
        print(f"[{datetime.now()}] Error al cargar la página:", e)
        return

    soup = BeautifulSoup(response.text, "html.parser")
    ofertas = []

    # Reemplaza este selector por el correcto según la página
    for elemento in soup.find_all("a"):
        texto = elemento.get_text()
        if PALABRA_CLAVE.lower() in texto.lower() and texto not in empleos_vistos:
            ofertas.append(texto)
            empleos_vistos.add(texto)

    if of

