from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib
import json
import os

# Datos del correo
EMAIL_ORIGEN = os.environ.get("EMAIL_ORIGEN")
EMAIL_DESTINO = os.environ.get("EMAIL_DESTINO")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

DIAS_ANTICIPACION = 5  # Días antes del vencimiento para enviar alerta

def enviar_correo_aviso(fecha_expiracion):
    try:
        msg = EmailMessage()
        msg.set_content(f"⚠️ El token de WhatsApp expirará pronto: {fecha_expiracion}.\n\nPor favor, renueva el token manualmente.")
        msg["Subject"] = "⏳ Tu token expirará pronto"
        msg["From"] = EMAIL_ORIGEN
        msg["To"] = EMAIL_DESTINO

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ORIGEN, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("📧 Aviso enviado correctamente.")
    except Exception as e:
        print("❌ Error al enviar correo:", e)

def verificar_token():
    try:
        with open("token_info.json", "r") as f:
            data = json.load(f)
        expires_at = datetime.fromisoformat(data["expires_at"])
        ahora = datetime.utcnow()

        if expires_at - ahora <= timedelta(days=DIAS_ANTICIPACION):
            enviar_correo_aviso(expires_at)
        else:
            print("✅ El token aún es válido.")
    except Exception as e:
        print("❌ Error verificando token:", e)

# Ejecutar si se llama directamente
if __name__ == "__main__":
    verificar_token()
