from .client import Client
from .consts import *


class FutureAPI(Client):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_seceret_key, passphrase, use_server_time)

    # query position
    def get_position(self):
        return self._request_without_params(GET, FUTURE_POSITION)

    # query specific position
    def get_specific_position(self, instrument_id):
        return self._request_without_params(GET, FUTURE_SPECIFIC_POSITION + str(instrument_id) + '/position')

    # query accounts info
    def get_accounts(self):
        return self._request_without_params(GET, FUTURE_ACCOUNTS)

    # query coin account info
    def get_coin_account(self, symbol):
        return self._request_without_params(GET, FUTURE_COIN_ACCOUNT + str(symbol))

    # query leverage
    def get_leverage(self, symbol):
        return self._request_without_params(GET, FUTURE_GET_LEVERAGE + str(symbol) + '/leverage')

    # set leverage
    def set_leverage(self, currency, leverage, instrument_id='', direction=''):
        params = {'leverage': leverage}
        if instrument_id:
            params['instrument_id'] = instrument_id
        if direction:
            params['direction'] = direction
        return self._request_with_params(POST, FUTURE_SET_LEVERAGE + str(currency) + '/leverage', params)

    # query ledger
    def get_ledger(self, symbol):
        return self._request_without_params(GET, FUTURE_LEDGER + str(symbol) + '/ledger')

    # delete position
    # def revoke_position(self, position_data):
    #     params = {'position_data': position_data}
    #     return self._request_with_params(DELETE, FUTURE_DELETE_POSITION, params)
    def revoke_position(self, position_data):
        params = {'position_data': position_data}
        return self._request_with_params(POST, FUTURE_DELETE_POSITION, params)

    # take order
    def take_order(self, client_oid, instrument_id, otype, price, size, match_price, leverage):
        # params = {'instrument_id': instrument_id, 'otype': otype, 'price': price, 'order': order_Qty, 'match_price': match_price, 'client_id': client_id}
        params = {'client_oid': client_oid, 'instrument_id': instrument_id, 'type': otype, 'price': price, 'size': size, 'match_price':match_price, 'leverage': leverage}
        return self._request_with_params(POST, FUTURE_ORDER, params)

    #take orders
    def take_orders(self, instrument_id, orders_data, leverage):
        params = {'instrument_id': instrument_id, 'orders_data': orders_data, 'leverage': leverage}
        return self._request_with_params(POST, FUTURE_ORDERS, params)

    # revoke order
    def revoke_order(self, instrument_id, order_id):
        return self._request_without_params(POST, FUTURE_REVOKE_ORDER + str(instrument_id) + '/' + str(order_id))

    # revoke orders

    def revoke_orders(self, instrument_id, order_ids):
        params = {'order_ids': order_ids}
        return self._request_with_params(POST, FUTURE_REVOKE_ORDERS+str(instrument_id), params)

    # query order list
    #def get_order_list(self, status, before, after, limit, instrument_id=''):
    #   params = {'status': status, 'before': before, 'after': after, 'limit': limit, 'instrument_id': instrument_id}
    #    return self._request_with_params(GET, FUTURE_ORDERS_LIST, params)

    # query order list
    def get_order_list(self, status, froms, to, limit, instrument_id=''):
        params = {'status': status, 'instrument_id': instrument_id}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, FUTURE_ORDERS_LIST+'/'+str(instrument_id), params)

    # query order info
    def get_order_info(self, order_id, instrument_id):
        return self._request_without_params(GET, FUTURE_ORDER_INFO + str(instrument_id) + '/' + str(order_id))

    # query fills
    def get_fills(self, order_id, instrument_id, froms, to, limit):
        params = {'order_id': order_id, 'instrument_id': instrument_id}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, FUTURE_FILLS, params)

    # get products info
    def get_products(self):
        return self._request_without_params(GET, FUTURE_PRODUCTS_INFO)

    # get depth
    def get_depth(self, instrument_id, size):
        params = {'size': size}
        return self._request_with_params(GET, FUTURE_DEPTH + str(instrument_id) + '/book', params)

    # get ticker
    def get_ticker(self):
        return self._request_without_params(GET, FUTURE_TICKER)

    # get specific ticker
    def get_specific_ticker(self, instrument_id):
        return self._request_without_params(GET, FUTURE_SPECIFIC_TICKER + str(instrument_id) + '/ticker')

    # query trades
    #def get_trades(self, instrument_id, before, after, limit):
    #    params = {'before': before, 'after': after, 'limit': limit}
    #    return self._request_with_params(GET, FUTURE_TRADES + str(instrument_id) + '/trades', params, cursor=True)

    # query trades v3
    def get_trades(self, instrument_id, froms=0, to=0, limit=0):
        params = {'instrument_id': instrument_id}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, FUTURE_TRADES + str(instrument_id) + '/trades', params, cursor=True)

    # query k-line
    def get_kline(self, instrument_id, granularity, start='', end=''):
        params = {'granularity': granularity, 'start': start, 'end': end}
        return self._request_with_params(GET, FUTURE_KLINE + str(instrument_id) + '/candles', params)

    # query index
    def get_index(self, instrument_id):
        return self._request_without_params(GET, FUTURE_INDEX + str(instrument_id) + '/index')

    # query rate
    def get_rate(self):
        return self._request_without_params(GET, FUTURE_RATE)

    # query estimate price
    def get_estimated_price(self, instrument_id):
        return self._request_without_params(GET, FUTURE_ESTIMAT_PRICE + str(instrument_id) + '/estimated_price')

    # query the total platform of the platform
    def get_holds(self, instrument_id):
        return self._request_without_params(GET, FUTURE_HOLDS + str(instrument_id) + '/open_interest')

    # query limit price
    def get_limit(self, instrument_id):
        return self._request_without_params(GET, FUTURE_LIMIT + str(instrument_id) + '/price_limit')

    # query limit price
    def get_liquidation(self, instrument_id, status=0, froms = 0, to = 0, limit = 0):
        params = {'instrument_id': instrument_id, 'status': status}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_without_params(GET, FUTURE_LIQUIDATION + str(instrument_id) + '/liquidation')

    # query holds amount
    def get_holds_amount(self, instrument_id):
        return self._request_without_params(GET, HOLD_AMOUNT+ str(instrument_id) + '/holds')

    # query mark price
    def get_mark_price(self, instrument_id):
        return self._request_without_params(GET, FUTURE_MARK +str(instrument_id) + '/mark_price')
