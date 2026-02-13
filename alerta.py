import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# === CONFIGURACIÓN ===

URL = "https://www.empleospublicos.cl"

# Palabras clave que quieres buscar
PALABRAS_CLAVE = ["Diseñador", "Diseño Gráfico"]

# Telegram
TELEGRAM_TOKEN = "8123123059:AAHm4RP6lM7tzOMYG0IRj3vw6aknTjiN9J4"
TELEGRAM_CHAT_ID = "5367397088"  # reemplaza con tu chat ID real

# Gmail (opcional)
GMAIL_USER = "sebastian.bawlitza@gmail.com"
GMAIL_PASSWORD = "<ydnlakekkjileobz>"  # tu contraseña de aplicación
GMAIL_TO = "sebastian.bawlitza@gmail.com"

# Historial de empleos ya vistos
empleos_vistos = set()

# === FUNCIONES ===

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error enviando Telegram: {e}")

def enviar_gmail(asunto, mensaje):
    try:
        msg = MIMEText(mensaje)
        msg["Subject"] = asunto
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_TO

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
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

        textos = [t.get_text(strip=True) for t in soup.find_all(text=True)
                  if any(p.lower() in t.lower() for p in PALABRAS_CLAVE)]

        nuevos = [t for t in textos if t not in empleos_vistos]

        if nuevos:
            mensaje = "¡Nuevas ofertas de empleo encontradas!\n\n" + "\n\n".join(nuevos)
            enviar_telegram(mensaje)
            enviar_gmail("Nuevas ofertas de empleo", mensaje)
            for t in nuevos:
                empleos_vistos.add(t)
        else:
            print("No hay nuevas ofertas.")
    except Exception as e:
        print(f"[Error al revisar la página]: {e}")

# === PROGRAMACIÓN AUTOMÁTICA ===
schedule.every(3).hours.do(revisar_empleos)

if __name__ == "__main__":
    revisar_empleos()  # Primera revisión inmediata
    while True:
        schedule.run_pending()
        time.sleep(60)

