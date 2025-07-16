from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib
import json
import os

# Configuración del correo
EMAIL_ORIGEN = os.environ.get("EMAIL_ORIGEN")
EMAIL_DESTINO = os.environ.get("EMAIL_DESTINO")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

DIAS_ANTICIPACION = 5  # Días antes del vencimiento para enviar alerta

def enviar_correo_aviso(fecha_expiracion):
    try:
        msg = EmailMessage()
        msg.set_content(
            f"⚠️ El token de WhatsApp expirará pronto: {fecha_expiracion}.\n\n"
            "Por favor, renueva el token manualmente en la herramienta de Meta y actualízalo en Render."
        )
        msg["Subject"] = "⏳ Tu token de WhatsApp expirará pronto"
        msg["From"] = EMAIL_ORIGEN
        msg["To"] = EMAIL_DESTINO

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ORIGEN, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("📧 Correo de aviso enviado.")
    except Exception as e:
        print("❌ Error al enviar correo:", e)

def verificar_token():
    try:
        with open("token_info.json", "r") as f:
            data = json.load(f)
        fecha_expiracion = datetime.fromisoformat(data["expires_at"])
        hoy = datetime.utcnow()

        dias_restantes = (fecha_expiracion - hoy).days

        if dias_restantes <= DIAS_ANTICIPACION:
            print(f"⏰ El token expira en {dias_restantes} días.")
            enviar_correo_aviso(fecha_expiracion)
        else:
            print(f"✅ Token válido. Expira en {dias_restantes} días.")
    except Exception as e:
        print("❌ Error al verificar token:", e)

if __name__ == "__main__":
    verificar_token()
