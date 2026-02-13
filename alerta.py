import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime

URL = "https://www.empleospublicos.cl"
PALABRA_CLAVE = "Diseñador"

empleos_vistos = set()

def revisar_empleos():
    print(f"\n[{datetime.now()}] Revisando empleos...")
    
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    textos = soup.get_text().split("\n")
    
    nuevos = []
    
    for linea in textos:
        if PALABRA_CLAVE.lower() in linea.lower():
            if linea not in empleos_vistos:
                empleos_vistos.add(linea)
                nuevos.append(linea.strip())
    
    if nuevos:
        print("🚨 Nuevas ofertas encontradas:")
        for n in nuevos:
            print("-", n)
    else:
        print("No hay nuevas ofertas.")

revisar_empleos()

schedule.every(3).hours.do(revisar_empleos)

while True:
    schedule.run_pending()
    time.sleep(60)


