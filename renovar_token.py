import requests
import json
from datetime import datetime, timedelta

# === DATOS DE TU APP DE META ===
CLIENT_ID = "770466738741969"
CLIENT_SECRET = "8fbe0cbdb1db670472ce21d96bc99e21"

# 🔁 Sustituye este token por el que generes manualmente desde Meta (dura 1 hora)
TOKEN_CORTO = "PEGAR_AQUI_TU_TOKEN_TEMPORAL"

# === URL para convertir a token de 60 días ===
url = "https://graph.facebook.com/v18.0/oauth/access_token"

params = {
    "grant_type": "fb_exchange_token",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "fb_exchange_token": TOKEN_CORTO
}

response = requests.get(url, params=params)
data = response.json()

if "access_token" in data:
    nuevo_token = data["access_token"]
    expires_in = data.get("expires_in", 60 * 60 * 24 * 60)  # 60 días por defecto
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

    # Guardar el nuevo token en token_info.json
    with open("token_info.json", "w") as f:
        json.dump({
            "access_token": nuevo_token,
            "expires_at": expires_at.isoformat()
        }, f, indent=4)

    print("✅ Token renovado correctamente.")
    print(f"📅 Expira el: {expires_at}")
    print("📁 Guardado en token_info.json")

else:
    print("❌ Error al renovar token:")
    print(json.dumps(data, indent=4))
