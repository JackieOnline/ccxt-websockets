# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.decimal_to_precision import TRUNCATE
from ccxt.base.decimal_to_precision import DECIMAL_PLACES


class livecoin (Exchange):

    def describe(self):
        return self.deep_extend(super(livecoin, self).describe(), {
            'id': 'livecoin',
            'name': 'LiveCoin',
            'countries': ['US', 'UK', 'RU'],
            'rateLimit': 1000,
            'userAgent': self.userAgents['chrome'],
            'has': {
                'fetchDepositAddress': True,
                'CORS': False,
                'fetchTickers': True,
                'fetchCurrencies': True,
                'fetchTradingFees': True,
                'fetchOrders': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'withdraw': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27980768-f22fc424-638a-11e7-89c9-6010a54ff9be.jpg',
                'api': 'https://api.livecoin.net',
                'www': 'https://www.livecoin.net',
                'doc': 'https://www.livecoin.net/api?lang=en',
            },
            'api': {
                'public': {
                    'get': [
                        'exchange/all/order_book',
                        'exchange/last_trades',
                        'exchange/maxbid_minask',
                        'exchange/order_book',
                        'exchange/restrictions',
                        'exchange/ticker',  # omit params to get all tickers at once
                        'info/coinInfo',
                    ],
                },
                'private': {
                    'get': [
                        'exchange/client_orders',
                        'exchange/order',
                        'exchange/trades',
                        'exchange/commission',
                        'exchange/commissionCommonInfo',
                        'payment/balances',
                        'payment/balance',
                        'payment/get/address',
                        'payment/history/size',
                        'payment/history/transactions',
                    ],
                    'post': [
                        'exchange/buylimit',
                        'exchange/buymarket',
                        'exchange/cancellimit',
                        'exchange/selllimit',
                        'exchange/sellmarket',
                        'payment/out/capitalist',
                        'payment/out/card',
                        'payment/out/coin',
                        'payment/out/okpay',
                        'payment/out/payeer',
                        'payment/out/perfectmoney',
                        'payment/voucher/amount',
                        'payment/voucher/make',
                        'payment/voucher/redeem',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0.18 / 100,
                    'taker': 0.18 / 100,
                },
            },
            'commonCurrencies': {
                'BTCH': 'Bithash',
                'CPC': 'CapriCoin',
                'EDR': 'E-Dinar Coin',  # conflicts with EDR for Endor Protocol and EDRCoin
                'eETT': 'EETT',
                'FirstBlood': '1ST',
                'FORTYTWO': '42',
                'ORE': 'Orectic',
                'RUR': 'RUB',
                'SCT': 'SpaceCoin',
                'TPI': 'ThaneCoin',
                'wETT': 'WETT',
                'XBT': 'Bricktox',
            },
            'exceptions': {
                '1': ExchangeError,
                '10': AuthenticationError,
                '100': ExchangeError,  # invalid parameters
                '101': AuthenticationError,
                '102': AuthenticationError,
                '103': InvalidOrder,  # invalid currency
                '104': InvalidOrder,  # invalid amount
                '105': InvalidOrder,  # unable to block funds
                '11': AuthenticationError,
                '12': AuthenticationError,
                '2': AuthenticationError,  # "User not found"
                '20': AuthenticationError,
                '30': AuthenticationError,
                '31': NotSupported,
                '32': ExchangeError,
                '429': DDoSProtection,
                '503': ExchangeNotAvailable,
            },
        })

    def fetch_markets(self):
        markets = self.publicGetExchangeTicker()
        restrictions = self.publicGetExchangeRestrictions()
        restrictionsById = self.index_by(restrictions['restrictions'], 'currencyPair')
        result = []
        for p in range(0, len(markets)):
            market = markets[p]
            id = market['symbol']
            baseId, quoteId = id.split('/')
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            coinRestrictions = self.safe_value(restrictionsById, symbol)
            precision = {
                'price': 5,
                'amount': 8,
                'cost': 8,
            }
            limits = {
                'amount': {
                    'min': math.pow(10, -precision['amount']),
                    'max': math.pow(10, precision['amount']),
                },
            }
            if coinRestrictions:
                precision['price'] = self.safe_integer(coinRestrictions, 'priceScale', 5)
                limits['amount']['min'] = self.safe_float(coinRestrictions, 'minLimitQuantity', limits['amount']['min'])
            limits['price'] = {
                'min': math.pow(10, -precision['price']),
                'max': math.pow(10, precision['price']),
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def fetch_currencies(self, params={}):
        response = self.publicGetInfoCoinInfo(params)
        currencies = response['info']
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = currency['symbol']
            # todo: will need to rethink the fees
            # to add support for multiple withdrawal/deposit methods and
            # differentiated fees for each particular method
            code = self.common_currency_code(id)
            precision = 8  # default precision, todo: fix "magic constants"
            active = (currency['walletStatus'] == 'normal')
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,
                'name': currency['name'],
                'active': active,
                'fee': currency['withdrawFee'],  # todo: redesign
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': currency['minOrderAmount'],
                        'max': math.pow(10, precision),
                    },
                    'price': {
                        'min': math.pow(10, -precision),
                        'max': math.pow(10, precision),
                    },
                    'cost': {
                        'min': currency['minOrderAmount'],
                        'max': None,
                    },
                    'withdraw': {
                        'min': currency['minWithdrawAmount'],
                        'max': math.pow(10, precision),
                    },
                    'deposit': {
                        'min': currency['minDepositAmount'],
                        'max': None,
                    },
                },
            }
        result = self.append_fiat_currencies(result)
        return result

    def append_fiat_currencies(self, result):
        precision = 8
        defaults = {
            'info': None,
            'active': True,
            'fee': None,
            'precision': precision,
            'limits': {
                'withdraw': {'min': None, 'max': None},
                'deposit': {'min': None, 'max': None},
                'amount': {'min': None, 'max': None},
                'cost': {'min': None, 'max': None},
                'price': {
                    'min': math.pow(10, -precision),
                    'max': math.pow(10, precision),
                },
            },
        }
        currencies = [
            {'id': 'USD', 'code': 'USD', 'name': 'US Dollar'},
            {'id': 'EUR', 'code': 'EUR', 'name': 'Euro'},
            # {'id': 'RUR', 'code': 'RUB', 'name': 'Russian ruble'},
        ]
        currencies.append({
            'id': 'RUR',
            'code': self.common_currency_code('RUR'),
            'name': 'Russian ruble',
        })
        for i in range(0, len(currencies)):
            currency = currencies[i]
            code = currency['code']
            result[code] = self.extend(defaults, currency)
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        balances = self.privateGetPaymentBalances()
        result = {'info': balances}
        for b in range(0, len(balances)):
            balance = balances[b]
            currency = balance['currency']
            account = None
            if currency in result:
                account = result[currency]
            else:
                account = self.account()
            if balance['type'] == 'total':
                account['total'] = float(balance['value'])
            if balance['type'] == 'available':
                account['free'] = float(balance['value'])
            if balance['type'] == 'trade':
                account['used'] = float(balance['value'])
            result[currency] = account
        return self.parse_balance(result)

    def fetch_trading_fees(self, params={}):
        self.load_markets()
        response = self.privateGetExchangeCommissionCommonInfo(params)
        commission = self.safe_float(response, 'commission')
        return {
            'info': response,
            'maker': commission,
            'taker': commission,
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'currencyPair': self.market_id(symbol),
            'groupByPrice': 'false',
        }
        if limit is not None:
            request['depth'] = limit  # 100
        orderbook = self.publicGetExchangeOrderBook(self.extend(request, params))
        timestamp = orderbook['timestamp']
        return self.parse_order_book(orderbook, timestamp)

    def parse_ticker(self, ticker, market=None):
        timestamp = self.milliseconds()
        symbol = None
        if market:
            symbol = market['symbol']
        vwap = self.safe_float(ticker, 'vwap')
        baseVolume = self.safe_float(ticker, 'volume')
        quoteVolume = None
        if baseVolume is not None and vwap is not None:
            quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'best_bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'best_ask'),
            'askVolume': None,
            'vwap': self.safe_float(ticker, 'vwap'),
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetExchangeTicker(params)
        tickers = self.index_by(response, 'symbol')
        ids = list(tickers.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            market = self.markets_by_id[id]
            symbol = market['symbol']
            ticker = tickers[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        ticker = self.publicGetExchangeTicker(self.extend({
            'currencyPair': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        timestamp = trade['time'] * 1000
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'id': str(trade['id']),
            'order': None,
            'type': None,
            'side': trade['type'].lower(),
            'price': trade['price'],
            'amount': trade['quantity'],
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetExchangeLastTrades(self.extend({
            'currencyPair': market['id'],
        }, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'orderId': id,
        }
        response = self.privateGetExchangeOrder(self.extend(request, params))
        return self.parse_order(response)

    def parse_order_status(self, status):
        statuses = {
            'OPEN': 'open',
            'PARTIALLY_FILLED': 'open',
            'EXECUTED': 'closed',
            'CANCELLED': 'canceled',
            'PARTIALLY_FILLED_AND_CANCELLED': 'canceled',
        }
        if status in statuses:
            return statuses[status]
        return status

    def parse_order(self, order, market=None):
        timestamp = None
        if 'lastModificationTime' in order:
            timestamp = self.safe_string(order, 'lastModificationTime')
            if timestamp is not None:
                if timestamp.find('T') >= 0:
                    timestamp = self.parse8601(timestamp)
                else:
                    timestamp = self.safe_integer(order, 'lastModificationTime')
        # TODO currently not supported by livecoin
        # trades = self.parse_trades(order['trades'], market, since, limit)
        trades = None
        status = self.parse_order_status(self.safe_string_2(order, 'status', 'orderStatus'))
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'currencyPair')
            marketId = self.safe_string(order, 'symbol', marketId)
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
        type = None
        side = None
        if 'type' in order:
            lowercaseType = order['type'].lower()
            orderType = lowercaseType.split('_')
            type = orderType[0]
            side = orderType[1]
        price = self.safe_float(order, 'price')
        # of the next two lines the latter overrides the former, if present in the order structure
        remaining = self.safe_float(order, 'remainingQuantity')
        remaining = self.safe_float(order, 'remaining_quantity', remaining)
        amount = self.safe_float(order, 'quantity', remaining)
        filled = None
        if remaining is not None:
            filled = amount - remaining
        cost = None
        if filled is not None and price is not None:
            cost = filled * price
        feeRate = self.safe_float(order, 'commission_rate')
        feeCost = None
        if cost is not None and feeRate is not None:
            feeCost = cost * feeRate
        feeCurrency = None
        if market is not None:
            symbol = market['symbol']
            feeCurrency = market['quote']
        return {
            'info': order,
            'id': order['id'],
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'filled': filled,
            'remaining': remaining,
            'trades': trades,
            'fee': {
                'cost': feeCost,
                'currency': feeCurrency,
                'rate': feeRate,
            },
        }

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['currencyPair'] = market['id']
        if since is not None:
            request['issuedFrom'] = int(since)
        if limit is not None:
            request['endRow'] = limit - 1
        response = self.privateGetExchangeClientOrders(self.extend(request, params))
        result = []
        rawOrders = []
        if response['data']:
            rawOrders = response['data']
        for i in range(0, len(rawOrders)):
            order = rawOrders[i]
            result.append(self.parse_order(order, market))
        return result

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        result = self.fetch_orders(symbol, since, limit, self.extend({
            'openClosed': 'OPEN',
        }, params))
        return result

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        result = self.fetch_orders(symbol, since, limit, self.extend({
            'openClosed': 'CLOSED',
        }, params))
        return result

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        method = 'privatePostExchange' + self.capitalize(side) + type
        market = self.market(symbol)
        order = {
            'quantity': self.amount_to_precision(symbol, amount),
            'currencyPair': market['id'],
        }
        if type == 'limit':
            order['price'] = self.price_to_precision(symbol, price)
        response = getattr(self, method)(self.extend(order, params))
        result = {
            'info': response,
            'id': str(response['orderId']),
        }
        success = self.safe_value(response, 'success')
        if success:
            result['status'] = 'open'
        return result

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        currencyPair = market['id']
        response = self.privatePostExchangeCancellimit(self.extend({
            'orderId': id,
            'currencyPair': currencyPair,
        }, params))
        message = self.safe_string(response, 'message', self.json(response))
        if 'success' in response:
            if not response['success']:
                raise InvalidOrder(message)
            elif 'cancelled' in response:
                if response['cancelled']:
                    return {
                        'status': 'canceled',
                        'info': response,
                    }
                else:
                    raise OrderNotFound(message)
        raise ExchangeError(self.id + ' cancelOrder() failed: ' + self.json(response))

    def withdraw(self, code, amount, address, tag=None, params={}):
        # Sometimes the response with be {key: null} for all keys.
        # An example is if you attempt to withdraw more than is allowed when withdrawal fees are considered.
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        wallet = address
        if tag is not None:
            wallet += '::' + tag
        request = {
            'amount': self.decimal_to_precision(amount, TRUNCATE, currency['precision'], DECIMAL_PLACES),
            'currency': currency['id'],
            'wallet': wallet,
        }
        response = self.privatePostPaymentOutCoin(self.extend(request, params))
        id = self.safe_integer(response, 'id')
        if id is None:
            raise InsufficientFunds(self.id + ' insufficient funds to cover requested withdrawal amount post fees ' + self.json(response))
        return {
            'info': response,
            'id': id,
        }

    def fetch_deposit_address(self, currency, params={}):
        request = {
            'currency': currency,
        }
        response = self.privateGetPaymentGetAddress(self.extend(request, params))
        address = self.safe_string(response, 'wallet')
        tag = None
        if address.find(':') >= 0:
            parts = address.split(':')
            address = parts[0]
            tag = parts[2]
        self.check_address(address)
        return {
            'currency': currency,
            'address': address,
            'tag': tag,
            'info': response,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + path
        query = self.urlencode(self.keysort(params))
        if method == 'GET':
            if params:
                url += '?' + query
        if api == 'private':
            self.check_required_credentials()
            if method == 'POST':
                body = query
            signature = self.hmac(self.encode(query), self.encode(self.secret), hashlib.sha256)
            headers = {
                'Api-Key': self.apiKey,
                'Sign': signature.upper(),
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return
        if body[0] == '{':
            response = json.loads(body)
            if code >= 300:
                errorCode = self.safe_string(response, 'errorCode')
                if errorCode in self.exceptions:
                    ExceptionClass = self.exceptions[errorCode]
                    raise ExceptionClass(self.id + ' ' + body)
                else:
                    raise ExchangeError(self.id + ' ' + body)
            # returns status code 200 even if success == False
            success = self.safe_value(response, 'success', True)
            if not success:
                message = self.safe_string(response, 'message')
                if message is not None:
                    if message.find('Cannot find order') >= 0:
                        raise OrderNotFound(self.id + ' ' + body)
                exception = self.safe_string(response, 'exception')
                if exception is not None:
                    if exception.find('Minimal amount is') >= 0:
                        raise InvalidOrder(self.id + ' ' + body)
                raise ExchangeError(self.id + ' ' + body)