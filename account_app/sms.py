
import http.client
import json


def verification(phone_number, code):
    conn = http.client.HTTPSConnection("api2.ippanel.com")
    payload = json.dumps({
        "code": "ijhyfyi1irepd33",
        "sender": "3000505",
        "recipient": phone_number,
        "variable": {
            "code": code
        }
    })
    headers = {
        'apikey': 'eADy5YxBCSbnOI58usFDNpD5qzsnT3NAGH4RcuJXJIk=',
        'Content-Type': 'application/json',
        'Cookie': 'TS0177e476=0150a3e24e04874134dfd1bd5c65872f68c46a920efd859609d593ca9d48072507268ec821466d8aa3136e08191fcd1c9bfcc5abdd'
    }
    conn.request("POST", "/api/v1/sms/pattern/normal/send", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def SendSMS(phone_number, total_price):
    conn = http.client.HTTPSConnection("api2.ippanel.com")
    payload = json.dumps({
        "code": "ijhyfyi1irepd33",
        "sender": "3000505",
        "recipient": phone_number,
        "variable": {
            "total_price": total_price,
            "user_phone": phone_number
        }
    })
    headers = {
        'apikey': 'eADy5YxBCSbnOI58usFDNpD5qzsnT3NAGH4RcuJXJIk=',
        'Content-Type': 'application/json',
        'Cookie': 'TS0177e476=0150a3e24e04874134dfd1bd5c65872f68c46a920efd859609d593ca9d48072507268ec821466d8aa3136e08191fcd1c9bfcc5abdd'
    }
    conn.request("POST", "/api/v1/sms/pattern/normal/send", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))