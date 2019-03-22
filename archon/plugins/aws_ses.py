import boto3
from botocore.exceptions import ClientError

class AwsSes:

    def __init__(self, sender):
        """ key management through .aws working dir credentials """
        AWS_REGION = "us-east-1"
        self.ses_client = boto3.client('ses',region_name=AWS_REGION)
        self.SENDER = sender

    def html_body(self):
        body = "mymessage"
        BODY_HTML = """<html><head></head><body><h1>Email</h1><p>%s</p></body></html>"""%(body)
        return BODY_HTML

    def send_mail(self, recipient, body, subject):
        CHARSET = "UTF-8"        

        try:
            response = self.ses_client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': body,
                        }
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': subject,
                    },
                },
                Source=self.SENDER,
            )

        except ClientError as e:
            print (e)
            print(e.response['Error']['Message'])
        else:
            print("Email sent Message ID:"),
            print(response['MessageId'])

