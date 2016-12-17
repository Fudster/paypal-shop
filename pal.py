from paypalrestsdk  import *

configure({
  "mode": "live", # sandbox or live
  "client_id": "id",
  "client_secret": "sercet" })
  
email = "email"

def create(client_email,name,value):
    global email
    invoice = Invoice({
    'merchant_info': {
    "email": email,
    },
    "billing_info": [{
    "email": client_email
    }],
    "items": [{
    "name": name,
    "quantity": 1,
    "unit_price": {
    "currency": "USD",
    "value": value
    }
    }],
    })
    if invoice.create():
            return invoice.id
    else:
        print(invoice.error)

    invoice.send
    return invoice.id

