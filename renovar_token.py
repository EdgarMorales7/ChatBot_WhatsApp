import requests
import json
from datetime import datetime, timedelta

# Coloca aquí tus datos de la App de Meta
CLIENT_ID = "770466738741969"
CLIENT_SECRET = "8fbe0cbdb1db670472ce21d96bc99e21"
TOKEN_CORTO = "EAAK8vERGItEBPCKr2XJnEE8IvU7WNII1cxsFZBcfeZAKi2YPEB1V7HAsEFQE4ZAPy3NMloAKAC1wbSd4i30gxoZAjZAZCW3ElYPJk9el7iHSqQkHVpkvevdMSJ4ncIKylan5lT3jQbFDEBAccyeSFBJpwNTRfVD2RvPpsrhGHUkrOYi1lTICDijZCvI2U8xtWhz4U0NEPhSBHugpqRg93H0PEJ1DPEFX8lXnl4ZD"  # El token corto que copias del dashboard

# URL para convertir a token de largo plazo
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
    expires_in = data.get("expires_in", 60 * 60 * 24 * 60)  # por defecto 60 días
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

    # Guardar en token_info.json
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
