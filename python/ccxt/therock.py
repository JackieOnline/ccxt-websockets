# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import NotSupported


class therock (Exchange):

    def describe(self):
        return self.deep_extend(super(therock, self).describe(), {
            'id': 'therock',
            'name': 'TheRockTrading',
            'countries': ['MT'],
            'rateLimit': 1000,
            'version': 'v1',
            'has': {
                'CORS': False,
                'fetchTickers': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766869-75057fa2-5ee9-11e7-9a6f-13e641fa4707.jpg',
                'api': 'https://api.therocktrading.com',
                'www': 'https://therocktrading.com',
                'doc': [
                    'https://api.therocktrading.com/doc/v1/index.html',
                    'https://api.therocktrading.com/doc/',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'funds',
                        'funds/{id}/orderbook',
                        'funds/{id}/ticker',
                        'funds/{id}/trades',
                        'funds/tickers',
                    ],
                },
                'private': {
                    'get': [
                        'balances',
                        'balances/{id}',
                        'discounts',
                        'discounts/{id}',
                        'funds',
                        'funds/{id}',
                        'funds/{id}/trades',
                        'funds/{fund_id}/orders',
                        'funds/{fund_id}/orders/{id}',
                        'funds/{fund_id}/position_balances',
                        'funds/{fund_id}/positions',
                        'funds/{fund_id}/positions/{id}',
                        'transactions',
                        'transactions/{id}',
                        'withdraw_limits/{id}',
                        'withdraw_limits',
                    ],
                    'post': [
                        'atms/withdraw',
                        'funds/{fund_id}/orders',
                    ],
                    'delete': [
                        'funds/{fund_id}/orders/{id}',
                        'funds/{fund_id}/orders/remove_all',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.2 / 100,
                    'taker': 0.2 / 100,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0.0005,
                        'BCH': 0.0005,
                        'PPC': 0.02,
                        'ETH': 0.001,
                        'ZEC': 0.001,
                        'LTC': 0.002,
                        'EUR': 2.5,  # worst-case scenario: https://therocktrading.com/en/pages/fees
                    },
                    'deposit': {
                        'BTC': 0,
                        'BCH': 0,
                        'PPC': 0,
                        'ETH': 0,
                        'ZEC': 0,
                        'LTC': 0,
                        'EUR': 0,
                    },
                },
            },
            'wsconf': {
                'conx-tpls': {
                    'default': {
                        'type': 'pusher',
                        'baseurl': 'wss://ws-mt1.pusher.com/app/bb1fafdf79a00453b5af',
                    },
                },
                'methodmap': {
                    '_websocketTimeoutRemoveNonce': '_websocketTimeoutRemoveNonce',
                },
                'events': {
                    'ob': {
                        'conx-tpl': 'default',
                        'conx-param': {
                            'url': '{baseurl}',
                            'id': '{id}',
                        },
                    },
                },
            },
        })

    def fetch_markets(self):
        response = self.publicGetFunds()
        #
        #     {funds: [{                     id:   "BTCEUR",
        #                              description:   "Trade Bitcoin with Euro",
        #                                     type:   "currency",
        #                            base_currency:   "EUR",
        #                           trade_currency:   "BTC",
        #                                  buy_fee:    0.2,
        #                                 sell_fee:    0.2,
        #                      minimum_price_offer:    0.01,
        #                   minimum_quantity_offer:    0.0005,
        #                   base_currency_decimals:    2,
        #                  trade_currency_decimals:    4,
        #                                leverages: []                           },
        #                {                     id:   "LTCEUR",
        #                              description:   "Trade Litecoin with Euro",
        #                                     type:   "currency",
        #                            base_currency:   "EUR",
        #                           trade_currency:   "LTC",
        #                                  buy_fee:    0.2,
        #                                 sell_fee:    0.2,
        #                      minimum_price_offer:    0.01,
        #                   minimum_quantity_offer:    0.01,
        #                   base_currency_decimals:    2,
        #                  trade_currency_decimals:    2,
        #                                leverages: []                            }]}
        #
        markets = self.safe_value(response, 'funds')
        result = []
        if markets is None:
            raise ExchangeError(self.id + ' fetchMarkets got an unexpected response')
        else:
            for i in range(0, len(markets)):
                market = markets[i]
                id = self.safe_string(market, 'id')
                baseId = self.safe_string(market, 'trade_currency')
                quoteId = self.safe_string(market, 'base_currency')
                base = self.common_currency_code(baseId)
                quote = self.common_currency_code(quoteId)
                symbol = base + '/' + quote
                buy_fee = self.safe_float(market, 'buy_fee')
                sell_fee = self.safe_float(market, 'sell_fee')
                taker = max(buy_fee, sell_fee)
                taker = taker / 100
                maker = taker
                result.append({
                    'id': id,
                    'symbol': symbol,
                    'base': base,
                    'quote': quote,
                    'baseId': baseId,
                    'quoteId': quoteId,
                    'info': market,
                    'active': True,
                    'maker': maker,
                    'taker': taker,
                    'precision': {
                        'amount': self.safe_integer(market, 'trade_currency_decimals'),
                        'price': self.safe_integer(market, 'base_currency_decimals'),
                    },
                    'limits': {
                        'amount': {
                            'min': self.safe_float(market, 'minimum_quantity_offer'),
                            'max': None,
                        },
                        'price': {
                            'min': self.safe_float(market, 'minimum_price_offer'),
                            'max': None,
                        },
                        'cost': {
                            'min': None,
                            'max': None,
                        },
                    },
                })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetBalances()
        balances = response['balances']
        result = {'info': response}
        for b in range(0, len(balances)):
            balance = balances[b]
            currency = balance['currency']
            free = balance['trading_balance']
            total = balance['balance']
            used = total - free
            account = {
                'free': free,
                'used': used,
                'total': total,
            }
            result[currency] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        orderbook = self.publicGetFundsIdOrderbook(self.extend({
            'id': self.market_id(symbol),
        }, params))
        timestamp = self.parse8601(orderbook['date'])
        return self.parse_order_book(orderbook, timestamp, 'bids', 'asks', 'price', 'amount')

    def parse_ticker(self, ticker, market=None):
        timestamp = self.parse8601(ticker['date'])
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
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': self.safe_float(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': self.safe_float(ticker, 'close'),  # previous day close, if any
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume_traded'),
            'quoteVolume': self.safe_float(ticker, 'volume'),
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetFundsTickers(params)
        tickers = self.index_by(response['tickers'], 'fund_id')
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
        ticker = self.publicGetFundsIdTicker(self.extend({
            'id': market['id'],
        }, params))
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market=None):
        if not market:
            market = self.markets_by_id[trade['fund_id']]
        timestamp = self.parse8601(trade['date'])
        return {
            'info': trade,
            'id': str(trade['id']),
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': trade['side'],
            'price': trade['price'],
            'amount': trade['amount'],
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetFundsIdTrades(self.extend({
            'id': market['id'],
        }, params))
        return self.parse_trades(response['trades'], market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        if type == 'market':
            price = 0
        response = self.privatePostFundsFundIdOrders(self.extend({
            'fund_id': self.market_id(symbol),
            'side': side,
            'amount': amount,
            'price': price,
        }, params))
        return {
            'info': response,
            'id': str(response['id']),
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        return self.privateDeleteFundsFundIdOrdersId(self.extend({
            'id': id,
            'fund_id': self.market_id(symbol),
        }, params))

    def parse_order_status(self, status):
        statuses = {
            'active': 'open',
            'executed': 'closed',
            'deleted': 'canceled',
            # don't know what self status means
            # 'conditional': '?',
        }
        return self.safe_string(statuses, status, status)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = nonce + url
            headers = {
                'X-TRT-KEY': self.apiKey,
                'X-TRT-NONCE': nonce,
                'X-TRT-SIGN': self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512),
            }
            if query:
                body = self.json(query)
                headers['Content-Type'] = 'application/json'
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'errors' in response:
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response

    def _websocket_on_message(self, contextId, data):
        msg = json.loads(data)
        # console.log(data)
        self._websocket_check_sequence(contextId, msg)
        evt = self.safe_string(msg, 'event')
        if evt == 'subscription_succeeded':
            self._websocket_handle_subscription(contextId, msg)
        elif evt == 'orderbook':
            self._websocket_handle_orderbook(contextId, msg)
        elif evt == 'orderbook_diff':
            self._websocket_handle_orderbook_diff(contextId, msg)

    def _websocket_check_sequence(self, contextId, msg):
        msgData = self.safe_value(msg, 'data')
        if msgData is None:
            return
        sequeceId = self.safe_integer(msgData, 'sequence')
        if sequeceId is None:
            return
        chan = self.safe_string(msg, 'channel')
        lastSeqIdData = self._contextGet(contextId, 'sequence')
        if lastSeqIdData is None:
            lastSeqIdData = {}
        if chan in lastSeqIdData:
            lastSeqId = lastSeqIdData[chan]
            lastSeqId = self.sum(lastSeqId, 1)
            if sequeceId != lastSeqId:
                self.emit('err', 'sequence error in pusher connection ' + sequeceId + ' != ' + lastSeqId, contextId)
                return
        lastSeqIdData[chan] = sequeceId
        self._contextSet(contextId, 'sequence', lastSeqIdData)

    def _websocket_handle_orderbook(self, contextId, msg):
        chan = self.safe_string(msg, 'channel')
        symbol = self.find_symbol(chan)
        data = self.safe_value(msg, 'data')
        time = self.safe_string(data, 'time')
        timestamp = self.parse8601(time)
        ob = self.parse_order_book(data, timestamp, 'bids', 'asks', 'price', 'amount')
        symbolData = self._contextGetSymbolData(contextId, 'ob', symbol)
        symbolData['ob'] = ob
        self.emit('ob', symbol, self._cloneOrderBook(ob, symbolData['limit']))
        self._contextSetSymbolData(contextId, 'ob', symbol, symbolData)

    def _websocket_handle_orderbook_diff(self, contextId, msg):
        chan = self.safe_string(msg, 'channel')
        symbol = self.find_symbol(chan)
        symbolData = self._contextGetSymbolData(contextId, 'ob', symbol)
        if not('ob' in list(symbolData.keys())):
            # not previous snapshot -> don't process it
            return
        data = self.safe_value(msg, 'data')
        time = self.safe_string(data, 'time')
        timestamp = self.parse8601(time)
        price = self.safe_float(data, 'price')
        amount = self.safe_float(data, 'amount')
        side = self.safe_string(data, 'side')
        side = 'bids' if (side == 'bid') else 'asks'
        self.updateBidAsk([price, amount], symbolData['ob'][side], side == 'bids')
        symbolData['ob']['timestamp'] = timestamp
        symbolData['ob']['datetime'] = self.iso8601(timestamp)
        self.emit('ob', symbol, self._cloneOrderBook(symbolData['ob'], symbolData['limit']))
        self._contextSetSymbolData(contextId, 'ob', symbol, symbolData)

    def _websocket_handle_subscription(self, contextId, msg):
        chan = self.safe_string(msg, 'channel')
        event = 'ob'
        if chan == 'currency':
            event = 'trade'
        symbol = self.find_symbol(chan)
        symbolData = self._contextGetSymbolData(contextId, event, symbol)
        if 'sub-nonces' in symbolData:
            nonces = symbolData['sub-nonces']
            keys = list(nonces.keys())
            for i in range(0, len(keys)):
                nonce = keys[i]
                self._cancelTimeout(nonces[nonce])
                self.emit(nonce, True)
            symbolData['sub-nonces'] = {}
            self._contextSetSymbolData(contextId, event, symbol, symbolData)

    def _websocket_subscribe(self, contextId, event, symbol, nonce, params={}):
        if event != 'ob':
            raise NotSupported('subscribe ' + event + '(' + symbol + ') not supported for exchange ' + self.id)
        # save nonce for subscription response
        symbolData = self._contextGetSymbolData(contextId, event, symbol)
        if not('sub-nonces' in list(symbolData.keys())):
            symbolData['sub-nonces'] = {}
        symbolData['limit'] = self.safe_integer(params, 'limit', None)
        nonceStr = str(nonce)
        handle = self._setTimeout(self.timeout, self._websocketMethodMap('_websocketTimeoutRemoveNonce'), [contextId, nonceStr, event, symbol, 'sub-nonce'])
        symbolData['sub-nonces'][nonceStr] = handle
        self._contextSetSymbolData(contextId, event, symbol, symbolData)
        # remove sequenceId
        sequenceId = None
        self._contextSet(contextId, 'sequence', sequenceId)
        # send request
        id = self.market_id(symbol)
        self.websocketSendJson({
            'event': 'subscribe',
            'channel': id,
        }, contextId)

    def _websocket_unsubscribe(self, contextId, event, symbol, nonce, params={}):
        if event != 'ob':
            raise NotSupported('unsubscribe ' + event + '(' + symbol + ') not supported for exchange ' + self.id)
        id = self.market_id(symbol)
        payload = {
            'event': 'unsubscribe',
            'channel': id,
        }
        nonceStr = str(nonce)
        self.websocketSendJson(payload)
        self.emit(nonceStr, True)

    def _websocket_timeout_remove_nonce(self, contextId, timerNonce, event, symbol, key):
        symbolData = self._contextGetSymbolData(contextId, event, symbol)
        if key in symbolData:
            nonces = symbolData[key]
            if timerNonce in nonces:
                self.omit(symbolData[key], timerNonce)
                self._contextSetSymbolData(contextId, event, symbol, symbolData)

    def _get_current_websocket_orderbook(self, contextId, symbol, limit):
        data = self._contextGetSymbolData(contextId, 'ob', symbol)
        if ('ob' in list(data.keys())) and(data['ob'] is not None):
            return self._cloneOrderBook(data['ob'], limit)
        return None
