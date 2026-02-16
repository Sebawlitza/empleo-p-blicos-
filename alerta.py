import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Credenciales ===
TELEGRAM_TOKEN = "8123123059:AAHm4RP6lM7tzOMYG0IRj3vw6aknTjiN9J4"
TELEGRAM_CHAT_ID = "5367397088"
GMAIL_USER = "sebastian.bawlitza@gmail.com"
GMAIL_PASSWORD = "ydnlakekkjileobz"
GMAIL_TO = "sebastian.bawlitza@gmail.com"

URL = "https://www.empleospublicos.cl"
PALABRAS_CLAVE = ["Diseñador", "Diseño Gráfico"]

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
        response = requests.get(URL, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        empleos = soup.find_all("a")
        nuevos_empleos = []

        for e in empleos:
            texto = e.get_text().strip()
            if any(palabra.lower() in texto.lower() for palabra in PALABRAS_CLAVE):
                nuevos_empleos.append(texto)

        if nuevos_empleos:
            # Eliminamos duplicados visuales
            nuevos_empleos = list(set(nuevos_empleos))
            mensaje = "Nuevas ofertas encontradas:\n" + "\n".join(nuevos_empleos)
            print(mensaje)
            enviar_telegram(mensaje)
            enviar_gmail("Alerta de empleos", mensaje)
        else:
            print("No hay nuevas ofertas.")
    except Exception as e:
        print(f"Error al revisar empleos: {e}")

# EJECUCIÓN ÚNICA (GitHub Actions se encargará de repetirlo)
if __name__ == "__main__":
    revisar_empleos()

