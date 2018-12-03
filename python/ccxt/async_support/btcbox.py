# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import InvalidNonce


class btcbox (Exchange):

    def describe(self):
        return self.deep_extend(super(btcbox, self).describe(), {
            'id': 'btcbox',
            'name': 'BtcBox',
            'countries': ['JP'],
            'rateLimit': 1000,
            'version': 'v1',
            'has': {
                'CORS': False,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchTickers': False,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/31275803-4df755a8-aaa1-11e7-9abb-11ec2fad9f2d.jpg',
                'api': 'https://www.btcbox.co.jp/api',
                'www': 'https://www.btcbox.co.jp/',
                'doc': 'https://www.btcbox.co.jp/help/asm',
            },
            'api': {
                'public': {
                    'get': [
                        'depth',
                        'orders',
                        'ticker',
                    ],
                },
                'private': {
                    'post': [
                        'balance',
                        'trade_add',
                        'trade_cancel',
                        'trade_list',
                        'trade_view',
                        'wallet',
                    ],
                },
            },
            'markets': {
                'BTC/JPY': {'id': 'BTC/JPY', 'symbol': 'BTC/JPY', 'base': 'BTC', 'quote': 'JPY', 'baseId': 'btc', 'quoteId': 'jpy'},
                'ETH/JPY': {'id': 'ETH/JPY', 'symbol': 'ETH/JPY', 'base': 'ETH', 'quote': 'JPY', 'baseId': 'eth', 'quoteId': 'jpy'},
                'LTC/JPY': {'id': 'LTC/JPY', 'symbol': 'LTC/JPY', 'base': 'LTC', 'quote': 'JPY', 'baseId': 'ltc', 'quoteId': 'jpy'},
                'BCH/JPY': {'id': 'BCH/JPY', 'symbol': 'BCH/JPY', 'base': 'BCH', 'quote': 'JPY', 'baseId': 'bch', 'quoteId': 'jpy'},
            },
            'exceptions': {
                '104': AuthenticationError,
                '105': PermissionDenied,
                '106': InvalidNonce,
                '107': InvalidOrder,  # price should be an integer
                '200': InsufficientFunds,
                '201': InvalidOrder,  # amount too small
                '202': InvalidOrder,  # price should be [0 : 1000000]
                '203': OrderNotFound,
                '401': OrderNotFound,  # cancel canceled, closed or non-existent order
                '402': DDoSProtection,
            },
        })

    async def fetch_balance(self, params={}):
        await self.load_markets()
        balances = await self.privatePostBalance()
        result = {'info': balances}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            currency = currencies[i]
            lowercase = currency.lower()
            if lowercase == 'dash':
                lowercase = 'drk'
            account = self.account()
            free = lowercase + '_balance'
            used = lowercase + '_lock'
            if free in balances:
                account['free'] = float(balances[free])
            if used in balances:
                account['used'] = float(balances[used])
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {}
        numSymbols = len(self.symbols)
        if numSymbols > 1:
            request['coin'] = market['baseId']
        orderbook = await self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(orderbook)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': self.safe_float(ticker, 'volume'),
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {}
        numSymbols = len(self.symbols)
        if numSymbols > 1:
            request['coin'] = market['baseId']
        ticker = await self.publicGetTicker(self.extend(request, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        timestamp = int(trade['date']) * 1000  # GMT time
        return {
            'info': trade,
            'id': trade['tid'],
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': trade['type'],
            'price': trade['price'],
            'amount': trade['amount'],
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {}
        numSymbols = len(self.symbols)
        if numSymbols > 1:
            request['coin'] = market['baseId']
        response = await self.publicGetOrders(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'amount': amount,
            'price': price,
            'type': side,
        }
        numSymbols = len(self.symbols)
        if numSymbols > 1:
            request['coin'] = market['baseId']
        response = await self.privatePostTradeAdd(self.extend(request, params))
        return {
            'info': response,
            'id': response['id'],
        }

    async def cancel_order(self, id, symbol=None, params={}):
        await self.load_markets()
        return await self.privatePostTradeCancel(self.extend({
            'id': id,
        }, params))

    def parse_order(self, order):
        # {"id":11,"datetime":"2014-10-21 10:47:20","type":"sell","price":42000,"amount_original":1.2,"amount_outstanding":1.2,"status":"closed","trades":[]}
        id = self.safe_string(order, 'id')
        timestamp = self.parse8601(order['datetime'] + '+09:00')  # Tokyo time
        amount = self.safe_float(order, 'amount_original')
        remaining = self.safe_float(order, 'amount_outstanding')
        filled = None
        if amount is not None:
            if remaining is not None:
                filled = amount - remaining
        price = self.safe_float(order, 'price')
        cost = None
        if price is not None:
            if filled is not None:
                cost = filled * price
        # status is set by fetchOrder method only
        statuses = {
            # TODO: complete list
            'part': 'open',  # partially or not at all executed
            'all': 'closed',  # fully executed
            'cancelled': 'canceled',
            'closed': 'closed',  # never encountered, seems to be bug in the doc
        }
        status = None
        if order['status'] in statuses:
            status = statuses[order['status']]
        # fetchOrders do not return status, use heuristic
        if status is None:
            if remaining is not None and remaining == 0:
                status = 'closed'
        trades = None  # todo: self.parse_trades(order['trades'])
        return {
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'amount': amount,
            'remaining': remaining,
            'filled': filled,
            'side': order['type'],
            'type': None,
            'status': status,
            'symbol': 'BTC/JPY',
            'price': price,
            'cost': cost,
            'trades': trades,
            'fee': None,
            'info': order,
        }

    async def fetch_order(self, id, symbol=None, params={}):
        await self.load_markets()
        response = await self.privatePostTradeView(self.extend({
            'id': id,
        }, params))
        return self.parse_order(response)

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        response = await self.privatePostTradeList(self.extend({
            'type': 'all',  # 'open' or 'all'
        }, params))
        # status(open/closed/canceled) is None
        return self.parse_orders(response)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        response = await self.privatePostTradeList(self.extend({
            'type': 'open',  # 'open' or 'all'
        }, params))
        orders = self.parse_orders(response)
        # btcbox does not return status, but we know it's 'open' as we queried for open orders
        for i in range(0, len(orders)):
            order = orders[i]
            order['status'] = 'open'
        return orders

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            query = self.extend({
                'key': self.apiKey,
                'nonce': nonce,
            }, params)
            request = self.urlencode(query)
            secret = self.hash(self.encode(self.secret))
            query['signature'] = self.hmac(self.encode(request), self.encode(secret))
            body = self.urlencode(query)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body):
        # typical error response: {"result":false,"code":"401"}
        if httpCode >= 400:
            return  # resort to defaultErrorHandler
        if body[0] != '{':
            return  # not json, resort to defaultErrorHandler
        response = json.loads(body)
        result = self.safe_value(response, 'result')
        if result is None or result is True:
            return  # either public API(no error codes expected) or success
        errorCode = self.safe_value(response, 'code')
        feedback = self.id + ' ' + self.json(response)
        exceptions = self.exceptions
        if errorCode in exceptions:
            raise exceptions[errorCode](feedback)
        raise ExchangeError(feedback)  # unknown message
