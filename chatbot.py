import requests

ACCESS_TOKEN = "EAAK8vERGItEBPKR3qgXsMuSgpghzcmIZC3UZByfNGyTesZAknVw66UyZAZAH6Lu2y3zLviZAiAUlssntmpvRGWgDbpLbclhTAaYi5VDWJDnisW537oQTLQJgXQZByGfr4cCZBZBnOUb3B8ZCL6cSaUD0ISnlfexM4KpRQvjNiYrW1jcaTXWuZCFZAzRMOcS7AL4PRsZBYfD6hKLELb0cvQimZC0if7M48ZAuMJhVxRx8ysnSIvuXe0ZD"
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
