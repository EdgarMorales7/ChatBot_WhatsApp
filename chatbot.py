import requests

ACCESS_TOKEN = "EAAK8vERGItEBPL9yzbLRZCTelRZAEXnb1u9INFL2Gs8f7OUWN6OQ0JybBLz8VcZBRr60ELj3be8nevl3abNJQSNWjqZAp0ZBYUQIZBmHoRbm6kqDZBZAiLJY3UWwd94rwphvDglYZA1bcD1eFlQw01hmgBJNO6wZCjAih8kukZAaaBELBbimQdo3mNZB6LPNlxPZAe76VG9hY4f0cODFhZC1NTbYTWPN0Gt4S4vDpCN9ql5sKZATwZDZD"
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
