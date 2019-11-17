from .client import Client
from .consts import *

#params = {'before': before, 'after': after, 'limit': limit, 'recordType': recordType}

class LeverAPI(Client):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_seceret_key, passphrase, use_server_time)

    # query lever account info
    def get_account_info(self):
        return self._request_without_params(GET, LEVER_ACCOUNT)

    # query specific account info
    def get_specific_account(self, instrument_id):
        return self._request_without_params(GET, LEVER_COIN_ACCOUNT + str(instrument_id))

    # query ledger record
    def get_ledger_record(self, instrument_id, froms, to, type, limit):
        params = {}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if type:
            params['type'] = type
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, LEVER_LEDGER_RECORD + str(instrument_id) + '/ledger', params, cursor=True)

    # query lever config info
    def get_config_info(self):
        return self._request_without_params(GET, LEVER_CONFIG)

    # query specific config info
    def get_specific_config_info(self, instrument_id):
        return self._request_without_params(GET, LEVER_SPECIFIC_CONFIG + str(instrument_id) + '/availability')

    # query borrow coin info
    #def get_borrow_coin(self, status, before, after, limit):
    #    params = {'before': before, 'after': after, 'limit': limit, 'status': status}
    #    return self._request_with_params(GET, LEVER_BORROW_RECORD, params, cursor=True)

    def get_borrow_coin(self, status, froms, to, limit):
        params = {'from': froms, 'to': to, 'limit': limit, 'status': status}
        return self._request_with_params(GET, LEVER_BORROW_RECORD, params, cursor=True)

    # query specific borrow coin info
    #def get_specific_borrow_coin(self, instrument_id, status, before, after, limit):
    #    params = {'before': before, 'after': after, 'limit': limit, 'status': status}
    #    return self._request_with_params(GET, LEVER_BORROW_RECORD + str(instrument_id) + '/borrowed', params, cursor=True)

    def get_specific_borrow_coin(self, instrument_id, status, froms, to, limit):
        params = {'from': froms, 'to': to, 'limit': limit, 'status': status}
        return self._request_with_params(GET, LEVER_BORROW_RECORD + str(instrument_id) + '/borrowed', params, cursor=True)

    # borrow coin
    def borrow_coin(self, instrument_id, currency, amount):
        params = {'instrument_id': instrument_id, 'currency': currency, 'amount': amount}
        return self._request_with_params(POST, LEVER_BORROW_COIN, params)

    # repayment coin
    def repayment_coin(self, borrow_id, instrument_id, currency, amount):
        params = {'instrument_id': instrument_id, 'currency': currency, 'amount': amount, 'borrow_id': borrow_id}
        return self._request_with_params(POST, LEVER_REPAYMENT_COIN, params)

    # take order
    def take_order(self, instrument_id, otype, side, size='', client_oid='', price='', margin_trading='', notional=''):
        params = {'instrument_id': instrument_id, 'type': otype, 'side': side,
                  'client_oid': client_oid}
        if otype == 'limit':
            params['price'] = price
            params['size'] = size
        elif otype == 'market':
            if size:
                params['size'] = size
            if notional:
                params['notional'] = notional

        if margin_trading:
            params['margin_trading'] = margin_trading

        return self._request_with_params(POST, LEVER_ORDER, params)

    # take orders
    # 市价单
    # params = [
    #   {"client_oid":"20180728","instrument_id":"btc-usdt","side":"sell","type":"market"," size ":"0.001"," notional ":"10001","margin_trading ":"1"},
    #   {"client_oid":"20180728","instrument_id":"btc-usdt","side":"sell","type":"limit"," size ":"0.001","notional":"10002","margin_trading ":"1"}
    # ]
    # 限价单
    # params = [
    #   {"client_oid":"20180728","instrument_id":"btc-usdt","side":"sell","type":"limit","size":"0.001","price":"10001","margin_trading ":"1"},
    #   {"client_oid":"20180728","instrument_id":"btc-usdt","side":"sell","type":"limit","size":"0.001","price":"10002","margin_trading ":"1"}
    # ]
    def take_orders(self, params):
        return self._request_with_params(POST, LEVER_ORDERS, params)

    # revoke order
    def revoke_order(self, oid, instrument_id, client_oid):
        params = {'instrument_id': instrument_id}
        if client_oid:
            params['client_oid'] = client_oid
        return self._request_with_params(POST, LEVER_REVOKE_ORDER + str(oid), params)

    # revoke orders
    #
    # params = [
    #   {"instrument_id":"btc-usdt","order_ids":[23464,23465]},
    #   {"instrument_id":"ltc-usdt","order_ids":[243464,234465]}
    # ]
    def revoke_orders(self, params):
        return self._request_with_params(POST, LEVER_REVOKE_ORDERS, params)

    # query order list
    #def get_order_list_paging(self, status, before, after, limit, instrument_id):
    #    params = {'status': status, 'before': before, 'after': after, 'limit': limit, 'instrument_id': instrument_id}
    #    return self._request_with_params(GET, LEVER_ORDER_LIST, params, cursor=True)

    # query order list
    def get_order_list(self, status, froms, to, limit, instrument_id):
        params = {'status': status, 'from': froms, 'to': to, 'limit': limit, 'instrument_id': instrument_id}
        return self._request_with_params(GET, LEVER_ORDER_LIST, params, cursor=True)

    def get_order_pending(self, instrument_id, froms, to, limit):
        params = {}
        if instrument_id:
            params['instrument_id'] = instrument_id
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, LEVEL_ORDERS_PENDING, params, cursor=True)

    # query order info
    def get_order_info(self, oid, instrument_id):
        params = {'instrument_id': instrument_id}
        return self._request_with_params(GET, LEVER_ORDER_INFO + str(oid), params)

    # query fills
    # def get_fills_v3(self, order_id, instrument_id, before, after, limit):
    #     params = {'before': before, 'after': after, 'limit': limit, 'order_id': order_id, 'instrument_id': instrument_id}
    #     return self._request_with_params(GET, LEVER_FILLS, params, cursor=True)

    def get_fills(self, order_id, instrument_id, froms, to, limit):
        params = {'from': froms, 'to': to, 'limit': limit, 'order_id': order_id, 'instrument_id': instrument_id}
        return self._request_with_params(GET, LEVER_FILLS, params, cursor=True)
