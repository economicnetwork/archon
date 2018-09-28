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

def send_mail_html(apikey, domain, subject, html):
    r = requests.post(
        domain,
        auth=("api", apikey),
        data={
                 "from": "ben@enet.io",
                 "to": "ben@enet.io",
                 "subject": subject,
                 "text": "",
                 "html": html
                 #"inline": images
        })
    return r