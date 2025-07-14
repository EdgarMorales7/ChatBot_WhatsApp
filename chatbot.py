from flask import Flask, request
from email.message import EmailMessage
import os
import requests
import smtplib
import json

app = Flask(__name__)  # Necesario para gunicorn

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

EMAIL_ORIGEN = os.environ.get("EMAIL_ORIGEN")
EMAIL_DESTINO = os.environ.get("EMAIL_DESTINO")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

def obtener_access_token():
    try:
        with open("token_info.json", "r") as f:
            data = json.load(f)
        return data["access_token"]
    except Exception as e:
        print("❌ No se pudo leer el token:", e)
        return None

@app.route("/webhook", methods=["GET"])
def verificar():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Token inválido", 403

@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    data = request.get_json()
    print("📥 Mensaje recibido:\n", data)

    try:
        mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        numero = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
        enviar_mensaje(numero, f"Eco: {mensaje}")
    except Exception as e:
        print("❌ Error procesando mensaje:", e)

    return "ok", 200

def enviar_mensaje(destinatario, texto):
    access_token = obtener_access_token()
    if not access_token:
        return

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "messaging_product": "whatsapp",
        "to": destinatario,
        "type": "text",
        "text": {"body": texto}
    }

    r = requests.post(url, headers=headers, json=body)

    if r.status_code == 401:
        mensaje_error = r.json()["error"]["message"]
        print("❗ Token inválido o expirado:", mensaje_error)
        enviar_alerta_correo(mensaje_error)

    elif r.status_code != 200:
        print("⚠️ Otro error:", r.status_code, r.text)
    else:
        print("✅ Mensaje enviado correctamente")

def enviar_alerta_correo(mensaje_error):
    try:
        msg = EmailMessage()
        msg.set_content(f"⚠️ Error en tu bot de WhatsApp:\n\n{mensaje_error}")
        msg["Subject"] = "🚨 Token de WhatsApp expirado o inválido"
        msg["From"] = EMAIL_ORIGEN
        msg["To"] = EMAIL_DESTINO

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ORIGEN, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("📧 Correo de alerta enviado correctamente.")
    except Exception as e:
        print("❌ Error al enviar correo:", e)

if __name__ == "__main__":
    app.run(debug=True)
