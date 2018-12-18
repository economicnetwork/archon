""" mailgun """
import requests

def send_simple_message(afacade, subject, text):
    apikey = afacade.mail_api_key
    domain = afacade.mail_domain
    email_from = afacade.email_from
    email_to = afacade.email_to
    print ("send message")
    r = requests.post(
        domain,
        auth=("api", apikey),
        data={"from": email_from,
              "to": email_to,
              "subject": subject,
              "text": text})
    print (r.text)

def send_mail_html(afacade, subject, html):
    apikey = afacade.mail_api_key
    domain = afacade.mail_domain
    email_from = afacade.email_from
    email_to = afacade.email_to
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