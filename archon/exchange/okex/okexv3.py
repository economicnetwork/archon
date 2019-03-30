import hmac
import base64
import requests
import json
import datetime

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'

base_url = 'https://www.okex.com'
    
class OKEXClient:

    def __init__(self, pw, apikey, secret):
        self.pw = pw
        self.secret = secret
        self.apikey = apikey

    def _signature(self, timestamp, method, request_path, body, secret_key):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)

    def _get_header(self, api_key, sign, timestamp, passphrase):
        header = dict()
        header[CONTENT_TYPE] = APPLICATION_JSON
        header[OK_ACCESS_KEY] = api_key
        header[OK_ACCESS_SIGN] = sign
        header[OK_ACCESS_TIMESTAMP] = str(timestamp)
        header[OK_ACCESS_PASSPHRASE] = passphrase
        return header

    def _parse_params_to_str(self, params):
        url = '?'
        for key, value in params.items():
            url = url + str(key) + '=' + str(value) + '&'

        return url[0:-1]

    def _get_timestamp(self):
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        return timestamp

    def _make_request(self, request_path):
        timestamp = self._get_timestamp()
        sign = self._signature(timestamp, 'GET', request_path, '', self.secret)
        header = self._get_header(self.apikey, sign, timestamp, self.pw)
        url = base_url + request_path
        response = requests.get(url, headers=header)
        return (response.json())

    def currency(self):
        request_path = '/api/account/v3/currencies'
        result = self._make_request(request_path)
        return result