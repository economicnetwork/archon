""" mailgun """
import requests

def send_simple_message(apikey, domain, subject, text):
    print ("send message")
    r = requests.post(
        domain,
        auth=("api", apikey),
        data={"from": "ben@enet.io",
              "to": "ben@enet.io",
              "subject": subject,
              "text": text})
    print (r.text)

