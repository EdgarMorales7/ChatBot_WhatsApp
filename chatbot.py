from flask import Flask, request
import os
import requests

app = Flask(__name__)  # <== ¡Esto es lo que gunicorn está buscando!

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

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
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "messaging_product": "whatsapp",
        "to": destinatario,
        "type": "text",
        "text": {"body": texto}
    }
    r = requests.post(url, headers=headers, json=body)
    print("📤 Código de respuesta:", r.status_code)
    print("📝 Respuesta:", r.text)
