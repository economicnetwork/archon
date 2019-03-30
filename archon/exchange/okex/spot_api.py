from .client import Client
from .consts import *


class SpotAPI(Client):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_seceret_key, passphrase, use_server_time)

    # query spot account info
    def get_account_info(self):
        return self._request_without_params(GET, SPOT_ACCOUNT_INFO)

    # query specific coin account info
    def get_coin_account_info(self, symbol):
        return self._request_without_params(GET, SPOT_COIN_ACCOUNT_INFO + str(symbol))

    # query ledger record not paging
    def get_ledger_record(self, symbol, limit=1):
        params = {}
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SPOT_LEDGER_RECORD + str(symbol) + '/ledger', params)

    # query ledger record with paging
    #def get_ledger_record_paging(self, symbol, before, after, limit):
    #    params = {'before': before, 'after': after, 'limit': limit}
    #    return self._request_with_params(GET, SPOT_LEDGER_RECORD + str(symbol) + '/ledger', params, cursor=True)

    # take order
    def take_order(self, otype, side, instrument_id, size, margin_trading=1, client_oid='', price='', funds='', ):
        params = {'type': otype, 'side': side, 'instrument_id': instrument_id, 'size': size, 'client_oid': client_oid,
                  'price': price, 'funds': funds, 'margin_trading': margin_trading}
        return self._request_with_params(POST, SPOT_ORDER, params)

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
        return self._request_with_params(POST, SPOT_ORDERS, params)

    # revoke order
    def revoke_order(self, oid, instrument_id):
        params = {'instrument_id': instrument_id}
        return self._request_with_params(POST, SPOT_REVOKE_ORDER + str(oid), params)

    # revoke orders

    # params example:
    # [
    #   {"instrument_id":"btc-usdt","order_ids":[1600593327162368,1600593327162369]},
    #   {"instrument_id":"ltc-usdt","order_ids":[243464,234465]}
    # ]
    def revoke_orders(self, params):
        return self._request_with_params(POST, SPOT_REVOKE_ORDERS, params)

    # query orders list
    #def get_orders_list(self, status, instrument_id, before, after, limit):
    #    params = {'status': status, 'instrument_id': instrument_id, 'before': before, 'after': after, 'limit': limit}
    #    return self._request_with_params(GET, SPOT_ORDERS_LIST, params, cursor=True)

    # query orders list v3
    def get_orders_list(self, status, instrument_id, froms='', to='', limit='100'):
        params = {'status': status, 'instrument_id': instrument_id, 'limit': limit}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if instrument_id:
            params['instrument_id'] = instrument_id
        return self._request_with_params(GET, SPOT_ORDERS_LIST, params, cursor=True)

    # query order info
    def get_order_info(self, order_id, instrument_id):
        params = {'instrument_id': instrument_id}
        return self._request_with_params(GET, SPOT_ORDER_INFO + str(order_id), params)

    def get_orders_pending(self, froms, to, limit, instrument_id):
        params = {}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        if instrument_id:
            params['instrument_id'] = instrument_id
        return self._request_with_params(GET, SPOT_ORDERS_PENDING, params, cursor=True)

    def get_fills(self, order_id, instrument_id, froms, to, limit):
        params = {'order_id': order_id, 'instrument_id': instrument_id}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SPOT_FILLS, params, cursor=True)

    # query spot coin info
    def get_coin_info(self):
        return self._request_without_params(GET, SPOT_COIN_INFO)

    # query depth
    def get_depth(self, instrument_id, size='', depth=''):
        params = {}
        if size:
            params['size'] = size
        if depth:
            params['depth'] = depth
        print(params)
        return self._request_with_params(GET, SPOT_DEPTH + str(instrument_id) + '/book', params)

    # query ticker info
    def get_ticker(self):
        return self._request_without_params(GET, SPOT_TICKER)

    # query specific ticker
    def get_specific_ticker(self, instrument_id):
        return self._request_without_params(GET, SPOT_SPECIFIC_TICKER + str(instrument_id) + '/ticker')

    def get_deal(self, instrument_id, froms, to, limit):
        params = {}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SPOT_DEAL + str(instrument_id) + '/trades', params)

    # query k-line info
    def get_kline(self, instrument_id, start, end, granularity):
        params = {}
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        if granularity:
            params['granularity'] = granularity
        return self._request_with_params(GET, SPOT_KLINE + str(instrument_id) + '/candles', params)




