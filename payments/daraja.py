import requests
import base64
from datetime import datetime
from requests.auth import HTTPBasicAuth

CONSUMER_KEY = "tWUnxd5X8pAujLAG4jVJZwnxQECsMSNBt64aHJLaQqGZaOyG"
CONSUMER_SECRET = "vYlMGAs1tALWeUhv2yFTbsfW9ucrpDq1xJhYubJitVb324MnmreeCSqqOIfcBmcj"

BASE_URL = "https://sandbox.safaricom.co.ke"

SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

CALLBACK_URL = "https://b8e7-196-207-146-193.ngrok-free.app/api/payments/callback"


def get_access_token():

    url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET)
    )

    return response.json()["access_token"]


def stk_push(phone_number, amount, account_reference):

    access_token = get_access_token()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password = base64.b64encode(
        (SHORTCODE + PASSKEY + timestamp).encode()
    ).decode("utf-8")

    url = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": "Ticket Payment"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()