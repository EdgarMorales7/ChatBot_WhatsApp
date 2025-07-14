import requests
import os

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
DESTINATARIO = "5215626885313"  # Tu número de WhatsApp
MENSAJE = "Hola, soy un bot de prueba desde la API de Meta"

url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
body = {
    "messaging_product": "whatsapp",
    "to": DESTINATARIO,
    "type": "text",
    "text": {
        "body": MENSAJE
    }
}

r = requests.post(url, headers=headers, json=body)
print("📤 Código de respuesta:", r.status_code)
print("📝 Respuesta:", r.text)
