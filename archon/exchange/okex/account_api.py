from .client import Client
from .consts import *
from .exceptions import OkexParamsException


class AccountAPI(Client):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_seceret_key, passphrase, use_server_time)

    # get all currencies list
    def get_currencies(self):
        return self._request_without_params(GET, CURRENCIES_INFO)

    # get wallet info
    def get_wallet(self):
        return self._request_without_params(GET, WALLET_INFO)

    # get specific currency info
    def get_currency(self, symbol):
        return self._request_without_params(GET, CURRENCY_INFO + str(symbol))

    # coin withdraw
    def coin_withdraw(self, currency, amount, destination, to_address, trade_pwd, fee):
        params = {'currency': currency, 'amount': amount, 'destination': destination, 'to_address': to_address, 'trade_pwd': trade_pwd, 'fee': fee}
        return self._request_with_params(POST, COIN_WITHDRAW, params)

    # query the fee of coin withdraw
    def get_coin_fee(self, symbol=''):
        params = {}
        if symbol:
            params['currency'] = symbol
        return self._request_with_params(GET, COIN_FEE, params)

    # query all recently coin withdraw record
    def get_coins_withdraw_record(self):
        return self._request_without_params(GET, COINS_WITHDRAW_RECORD)

    # query specific coin withdraw record
    def get_coin_withdraw_record(self, symbol):
        return self._request_without_params(GET, COIN_WITHDRAW_RECORD + str(symbol))

    # query ledger record
    # def get_ledger_record(self, before, after, limit, currency='', ctype=''):
    #    params = {'before': before, 'after': after, 'limit': limit, 'currency': currency, 'type': ctype}
    #    return self._request_with_params(GET, LEDGER_RECORD, params, cursor=True)

    # query ledger record v3
    def get_ledger_record(self, froms=0, to=1, limit=100, currency='', ctype=''):
        params = {}
        if currency:
            params['currency'] = currency
        if ctype:
            params['type'] = ctype
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, LEDGER_RECORD, params, cursor=True)

    # query top up address
    def get_top_up_address(self, symbol):
        params = {'currency': symbol}
        return self._request_with_params(GET, TOP_UP_ADDRESS, params)

    # query top up records
    def get_top_up_records(self):
        return self._request_without_params(GET, COIN_TOP_UP_RECORDS)

    # query top up record
    def get_top_up_record(self, symbol):
        return self._request_without_params(GET, COIN_TOP_UP_RECORD + str(symbol))

    # coin transfer
    def coin_transfer(self, currency, amount, account_from, account_to, sub_account='', instrument_id=''):
        params = {'currency': currency, 'amount': amount, 'from': account_from, 'to': account_to}
        if sub_account:
            params['sub_account'] = sub_account
        if instrument_id:
            params['instrument_id'] = instrument_id
        return self._request_with_params('POST', COIN_TRANSFER, params)

