import requests
import base64
from datetime import datetime
from django.conf import settings

def lipa_na_mpesa_stk(phone, amount):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY

    password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()

    access_token = get_mpesa_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {"Authorization": f"Bearer {access_token}"}

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "TrendScript Purchase",
        "TransactionDesc": "Digital Product Purchase",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def get_mpesa_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(consumer_key, consumer_secret))

    return response.json().get("access_token")
