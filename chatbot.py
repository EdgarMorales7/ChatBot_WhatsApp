import requests

ACCESS_TOKEN = "EAAK8vERGItEBPOiJ9gdZBbSHNHU89pKmOkEcPZCAOLaOLGjVcTW1h8eNMVaSVqrHvZBC5YuAtoNeSip1lgZCWofjE4Kv0oWDfNRZCsToyozCMLcONJZA7DveZAvoZAifA3RWLhz7LqrYiSnZCGK7hZCKsDSH4jxs7fHBdRij4ZCBnv6Lva3szZCk83NmCmYjXG3cWqrOtsX3KnbCCdEk30BiUjDeUZBBnz37P1sGG2tOWkDlkVG7O"
PHONE_NUMBER_ID = "670600796143745"
DESTINATARIO = "5215626885313"  # tu número de WhatsApp en formato internacional
MENSAJE = "Hola, soy un bot de prueba desde la API de Meta"

url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
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
print(r.status_code)
print(r.text)
