import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Credenciales ya configuradas ===
# Telegram
TELEGRAM_TOKEN = "8123123059:AAHm4RP6lM7tzOMYG0IRj3vw6aknTjiN9J4"
TELEGRAM_CHAT_ID = "5367397088"  # reemplaza con tu chat ID real

# Gmail
GMAIL_USER = "sebastian.bawlitza@gmail.com"
GMAIL_PASSWORD = "ydnlakekkjileobz"  # contraseña de aplicación
GMAIL_TO = "sebastian.bawlitza@gmail.com"

# === Configuración de búsqueda ===
URL = "https://www.empleospublicos.cl"
PALABRAS_CLAVE = ["Diseñador", "Diseño Gráfico"]

# Para no repetir notificaciones de empleos ya vistos
empleos_vistos = set()

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error enviando Telegram: {e}")

def enviar_gmail(asunto, mensaje):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = GMAIL_TO
        msg['Subject'] = asunto
        msg.attach(MIMEText(mensaje, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, GMAIL_TO, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Error enviando Gmail: {e}")

def revisar_empleos():
    print(f"[{datetime.now()}] Revisando empleos...")
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar todos los empleos (ajustar selector según la página)
        empleos = soup.find_all("a")  # Aquí puedes poner un selector más específico
        nuevos_empleos = []

        for e in empleos:
            texto = e.get_text()
            if any(palabra.lower() in texto.lower() for palabra in PALABRAS_CLAVE):
                if texto not in empleos_vistos:
                    empleos_vistos.add(texto)
                    nuevos_empleos.append(texto)

        if nuevos_empleos:
            mensaje = "Nuevas ofertas encontradas:\n" + "\n".join(nuevos_empleos)
            print(mensaje)
            enviar_telegram(mensaje)
            enviar_gmail("Alerta de empleos", mensaje)
        else:
            print("No hay nuevas ofertas.")

    except Exception as e:
        print(f"Error al revisar empleos: {e}")

# === Programar ejecución cada 3 horas ===
schedule.every(3).hours.do(revisar_empleos)

# Ejecutar inmediatamente la primera vez
revisar_empleos()

# Mantener el script corriendo
while True:
    schedule.run_pending()
    time.sleep(60)

