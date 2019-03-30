from .client import Client
from .consts import *


class SwapAPI(Client):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_seceret_key, passphrase, use_server_time)

    def get_position(self):
        return self._request_without_params(GET, SWAP_POSITIONS)

    def get_specific_position(self, instrument_id):
        return self._request_without_params(GET, SWAP_POSITION+str(instrument_id) + '/position')

    def get_accounts(self):
        return self._request_without_params(GET, SWAP_ACCOUNTS)

    def get_coin_account(self, instrument_id):
        return self._request_without_params(GET, SWAP_ACCOUNT+str(instrument_id)+'/accounts')

    def get_settings(self, instrument_id):
        return self._request_without_params(GET, SWAP_ACCOUNTS+'/'+str(instrument_id)+'/settings')

    def set_leverage(self, instrument_id, leverate, side):
        params = {}
        params['leverage'] = leverate
        params['side'] = side
        return self._request_with_params(POST, SWAP_ACCOUNTS+'/'+str(instrument_id)+'/leverage', params)

    def get_ledger(self, instrument_id, froms='', to='', limit=''):
        params = {}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_ACCOUNTS+'/'+str(instrument_id)+'/ledger', params)

    def take_order(self, instrument_id, size, otype, price, client_oid, match_price):
        params = {'instrument_id': instrument_id, 'size': size, 'type': otype, 'price': price}
        if client_oid:
            params['client_oid'] = client_oid
        if match_price:
            params['match_price'] = match_price
        return self._request_with_params(POST, SWAP_ORDER, params)

    def take_orders(self, order_data, instrument_id):
        params = {'instrument_id': instrument_id, 'order_data': order_data}
        return self._request_with_params(POST, SWAP_ORDERS, params)

    def revoke_order(self, order_id, instrument_id):
        return self._request_without_params(POST, SWAP_CANCEL_ORDER+str(instrument_id)+'/'+str(order_id))

    def revoke_orders(self, ids, instrument_id):
        params = {'ids': ids}
        return self._request_with_params(POST, SWAP_CANCEL_ORDERS+str(instrument_id), params)

    def get_order_list(self, status, instrument_id, froms='', to='', limit=''):
        params = {'status': status}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_ORDERS+'/'+str(instrument_id), params)

    def get_order_info(self, instrument_id, order_id):
        return self._request_without_params(GET, SWAP_ORDERS+'/'+str(instrument_id)+'/'+str(order_id))

    def get_fills(self, order_id, instrument_id, froms='', to='', limit=''):
        params = {'order_id': order_id, 'instrument_id': instrument_id}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_FILLS, params)

    def get_instruments(self):
        return self._request_without_params(GET, SWAP_INSTRUMENTS)

    def get_depth(self, instrument_id, size):
        if size:
            params={'size': size}
            return self._request_with_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/depth', params)
        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/depth')

    def get_ticker(self):
        return self._request_without_params(GET, SWAP_TICKETS)

    def get_specific_ticker(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/ticker')

    def get_trades(self, instrument_id, froms='', to='', limit=''):
        params = {}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/trades', params)

    def get_kline(self, instrument_id, granularity, start, end):
        params = {}
        if granularity:
            params['granularity'] = granularity
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        return self._request_with_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/candles', params)

    def get_index(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/index')

    def get_rate(self):
        return self._request_without_params(GET, SWAP_RATE)

    def get_holds(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/open_interest')

    def get_limit(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/price_limit')

    def get_liquidation(self, instrument_id, status, froms='', to='', limit=''):
        params = {'status': status}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/liquidation', params)

    def get_holds_amount(self, instrument_id):
        return self._request_without_params(GET, SWAP_ACCOUNTS + '/' + str(instrument_id) + '/holds')

    def get_funding_time(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/funding_time')

    def get_mark_price(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/mark_price')

    def get_historical_funding_rate(self, instrument_id, froms='', to='', limit=''):
        params = {}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/historical_funding_rate', params)
