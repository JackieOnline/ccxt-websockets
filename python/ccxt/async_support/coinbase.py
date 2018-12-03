# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import DDoSProtection


class coinbase (Exchange):

    def describe(self):
        return self.deep_extend(super(coinbase, self).describe(), {
            'id': 'coinbase',
            'name': 'Coinbase',
            'countries': ['US'],
            'rateLimit': 400,  # 10k calls per hour
            'version': 'v2',
            'userAgent': self.userAgents['chrome'],
            'headers': {
                'CB-VERSION': '2018-05-30',
            },
            'has': {
                'CORS': True,
                'cancelOrder': False,
                'createDepositAddress': False,
                'createOrder': False,
                'deposit': False,
                'fetchBalance': True,
                'fetchClosedOrders': False,
                'fetchCurrencies': True,
                'fetchDepositAddress': False,
                'fetchMarkets': False,
                'fetchMyTrades': False,
                'fetchOHLCV': False,
                'fetchOpenOrders': False,
                'fetchOrder': False,
                'fetchOrderBook': False,
                'fetchOrders': False,
                'fetchTicker': True,
                'fetchTickers': False,
                'fetchBidsAsks': False,
                'fetchTrades': False,
                'withdraw': False,
                'fetchTransactions': False,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'fetchMySells': True,
                'fetchMyBuys': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/40811661-b6eceae2-653a-11e8-829e-10bfadb078cf.jpg',
                'api': 'https://api.coinbase.com',
                'www': 'https://www.coinbase.com',
                'doc': 'https://developers.coinbase.com/api/v2',
                'fees': 'https://support.coinbase.com/customer/portal/articles/2109597-buy-sell-bank-transfer-fees',
                'referral': 'https://www.coinbase.com/join/58cbe25a355148797479dbd2',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
            },
            'api': {
                'public': {
                    'get': [
                        'currencies',
                        'time',
                        'exchange-rates',
                        'users/{user_id}',
                        'prices/{symbol}/buy',
                        'prices/{symbol}/sell',
                        'prices/{symbol}/spot',
                    ],
                },
                'private': {
                    'get': [
                        'accounts',
                        'accounts/{account_id}',
                        'accounts/{account_id}/addresses',
                        'accounts/{account_id}/addresses/{address_id}',
                        'accounts/{account_id}/addresses/{address_id}/transactions',
                        'accounts/{account_id}/transactions',
                        'accounts/{account_id}/transactions/{transaction_id}',
                        'accounts/{account_id}/buys',
                        'accounts/{account_id}/buys/{buy_id}',
                        'accounts/{account_id}/sells',
                        'accounts/{account_id}/sells/{sell_id}',
                        'accounts/{account_id}/deposits',
                        'accounts/{account_id}/deposits/{deposit_id}',
                        'accounts/{account_id}/withdrawals',
                        'accounts/{account_id}/withdrawals/{withdrawal_id}',
                        'payment-methods',
                        'payment-methods/{payment_method_id}',
                        'user',
                        'user/auth',
                    ],
                    'post': [
                        'accounts',
                        'accounts/{account_id}/primary',
                        'accounts/{account_id}/addresses',
                        'accounts/{account_id}/transactions',
                        'accounts/{account_id}/transactions/{transaction_id}/complete',
                        'accounts/{account_id}/transactions/{transaction_id}/resend',
                        'accounts/{account_id}/buys',
                        'accounts/{account_id}/buys/{buy_id}/commit',
                        'accounts/{account_id}/sells',
                        'accounts/{account_id}/sells/{sell_id}/commit',
                        'accounts/{account_id}/deposists',
                        'accounts/{account_id}/deposists/{deposit_id}/commit',
                        'accounts/{account_id}/withdrawals',
                        'accounts/{account_id}/withdrawals/{withdrawal_id}/commit',
                    ],
                    'put': [
                        'accounts/{account_id}',
                        'user',
                    ],
                    'delete': [
                        'accounts/{id}',
                        'accounts/{account_id}/transactions/{transaction_id}',
                    ],
                },
            },
            'exceptions': {
                'two_factor_required': AuthenticationError,  # 402 When sending money over 2fa limit
                'param_required': ExchangeError,  # 400 Missing parameter
                'validation_error': ExchangeError,  # 400 Unable to validate POST/PUT
                'invalid_request': ExchangeError,  # 400 Invalid request
                'personal_details_required': AuthenticationError,  # 400 User’s personal detail required to complete self request
                'identity_verification_required': AuthenticationError,  # 400 Identity verification is required to complete self request
                'jumio_verification_required': AuthenticationError,  # 400 Document verification is required to complete self request
                'jumio_face_match_verification_required': AuthenticationError,  # 400 Document verification including face match is required to complete self request
                'unverified_email': AuthenticationError,  # 400 User has not verified their email
                'authentication_error': AuthenticationError,  # 401 Invalid auth(generic)
                'invalid_token': AuthenticationError,  # 401 Invalid Oauth token
                'revoked_token': AuthenticationError,  # 401 Revoked Oauth token
                'expired_token': AuthenticationError,  # 401 Expired Oauth token
                'invalid_scope': AuthenticationError,  # 403 User hasn’t authenticated necessary scope
                'not_found': ExchangeError,  # 404 Resource not found
                'rate_limit_exceeded': DDoSProtection,  # 429 Rate limit exceeded
                'internal_server_error': ExchangeError,  # 500 Internal server error
            },
            'markets': {
                'BTC/USD': {'id': 'btc-usd', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD'},
                'LTC/USD': {'id': 'ltc-usd', 'symbol': 'LTC/USD', 'base': 'LTC', 'quote': 'USD'},
                'ETH/USD': {'id': 'eth-usd', 'symbol': 'ETH/USD', 'base': 'ETH', 'quote': 'USD'},
                'BCH/USD': {'id': 'bch-usd', 'symbol': 'BCH/USD', 'base': 'BCH', 'quote': 'USD'},
            },
            'options': {
                'accounts': [
                    'wallet',
                    'fiat',
                    # 'vault',
                ],
            },
        })

    async def fetch_time(self):
        response = await self.publicGetTime()
        data = response['data']
        return self.parse8601(data['iso'])

    async def load_accounts(self, reload=False):
        if reload:
            self.accounts = await self.fetch_accounts()
        else:
            if self.accounts:
                return self.accounts
            else:
                self.accounts = await self.fetch_accounts()
                self.accountsById = self.index_by(self.accounts, 'id')
        return self.accounts

    async def fetch_accounts(self):
        await self.load_markets()
        response = await self.privateGetAccounts()
        return response['data']

    async def fetch_my_sells(self, symbol=None, since=None, limit=None, params={}):
        # they don't have an endpoint for all historical trades
        accountId = self.safe_string_2(params, 'account_id', 'accountId')
        if accountId is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires an account_id or accountId extra parameter, use fetchAccounts or loadAccounts to get ids of all your accounts.')
        await self.load_markets()
        query = self.omit(params, ['account_id', 'accountId'])
        sells = await self.privateGetAccountsAccountIdSells(self.extend({
            'account_id': accountId,
        }, query))
        return self.parse_trades(sells['data'], None, since, limit)

    async def fetch_my_buys(self, symbol=None, since=None, limit=None, params={}):
        # they don't have an endpoint for all historical trades
        accountId = self.safe_string_2(params, 'account_id', 'accountId')
        if accountId is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires an account_id or accountId extra parameter, use fetchAccounts or loadAccounts to get ids of all your accounts.')
        await self.load_markets()
        query = self.omit(params, ['account_id', 'accountId'])
        buys = await self.privateGetAccountsAccountIdBuys(self.extend({
            'account_id': accountId,
        }, query))
        return self.parse_trades(buys['data'], None, since, limit)

    async def fetch_transactions_with_method(self, method, code=None, since=None, limit=None, params={}):
        accountId = self.safe_string_2(params, 'account_id', 'accountId')
        if accountId is None:
            raise ArgumentsRequired(self.id + ' fetchTransactionsWithMethod requires an account_id or accountId extra parameter, use fetchAccounts or loadAccounts to get ids of all your accounts.')
        await self.load_markets()
        query = self.omit(params, ['account_id', 'accountId'])
        response = await getattr(self, method)(self.extend({
            'account_id': accountId,
        }, query))
        return self.parseTransactions(response['data'], None, since, limit)

    async def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        return await self.fetch_transactions_with_method('privateGetAccountsAccountIdWithdrawals', code, since, limit, params)

    async def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        return await self.fetch_transactions_with_method('privateGetAccountsAccountIdDeposits', code, since, limit, params)

    def parse_transaction_status(self, status):
        statuses = {
            'created': 'pending',
            'completed': 'ok',
            'canceled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, market=None):
        #
        #    DEPOSIT
        #        id: '406176b1-92cf-598f-ab6e-7d87e4a6cac1',
        #        status: 'completed',
        #        payment_method: [Object],
        #        transaction: [Object],
        #        user_reference: 'JQKBN85B',
        #        created_at: '2018-10-01T14:58:21Z',
        #        updated_at: '2018-10-01T17:57:27Z',
        #        resource: 'deposit',
        #        resource_path: '/v2/accounts/7702be4f-de96-5f08-b13b-32377c449ecf/deposits/406176b1-92cf-598f-ab6e-7d87e4a6cac1',
        #        committed: True,
        #        payout_at: '2018-10-01T14:58:34Z',
        #        instant: True,
        #        fee: [Object],
        #        amount: [Object],
        #        subtotal: [Object],
        #        hold_until: '2018-10-04T07:00:00Z',
        #        hold_days: 3
        #
        #    WITHDRAWAL
        #       {
        #           "id": "67e0eaec-07d7-54c4-a72c-2e92826897df",
        #           "status": "completed",
        #           "payment_method": {
        #             "id": "83562370-3e5c-51db-87da-752af5ab9559",
        #             "resource": "payment_method",
        #             "resource_path": "/v2/payment-methods/83562370-3e5c-51db-87da-752af5ab9559"
        #           },
        #           "transaction": {
        #             "id": "441b9494-b3f0-5b98-b9b0-4d82c21c252a",
        #             "resource": "transaction",
        #             "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/transactions/441b9494-b3f0-5b98-b9b0-4d82c21c252a"
        #           },
        #           "amount": {
        #             "amount": "10.00",
        #             "currency": "USD"
        #           },
        #           "subtotal": {
        #             "amount": "10.00",
        #             "currency": "USD"
        #           },
        #           "created_at": "2015-01-31T20:49:02Z",
        #           "updated_at": "2015-02-11T16:54:02-08:00",
        #           "resource": "withdrawal",
        #           "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/withdrawals/67e0eaec-07d7-54c4-a72c-2e92826897df",
        #           "committed": True,
        #           "fee": {
        #             "amount": "0.00",
        #             "currency": "USD"
        #           },
        #           "payout_at": "2015-02-18T16:54:00-08:00"
        #         }
        amountObject = self.safe_value(transaction, 'amount', {})
        feeObject = self.safe_value(transaction, 'fee', {})
        id = self.safe_string(transaction, 'id')
        timestamp = self.parse8601(self.safe_value(transaction, 'created_at'))
        updated = self.parse8601(self.safe_value(transaction, 'updated_at'))
        orderId = None
        type = self.safe_string(transaction, 'resource')
        amount = self.safe_float(amountObject, 'amount')
        currencyId = self.safe_string(amountObject, 'currency')
        currency = self.common_currency_code(currencyId)
        feeCost = self.safe_float(feeObject, 'amount')
        feeCurrencyId = self.safe_string(feeObject, 'currency')
        feeCurrency = self.common_currency_code(feeCurrencyId)
        fee = {
            'cost': feeCost,
            'currency': feeCurrency,
        }
        status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        if status is None:
            committed = self.safe_value(transaction, 'committed')
            status = 'ok' if committed else 'pending'
        return {
            'info': transaction,
            'id': id,
            'txid': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': None,
            'tag': None,
            'type': type,
            'amount': amount,
            'currency': currency,
            'status': status,
            'updated': updated,
            'fee': fee,
        }

    def parse_trade(self, trade, market=None):
        #
        #     {
        #       "id": "67e0eaec-07d7-54c4-a72c-2e92826897df",
        #       "status": "completed",
        #       "payment_method": {
        #         "id": "83562370-3e5c-51db-87da-752af5ab9559",
        #         "resource": "payment_method",
        #         "resource_path": "/v2/payment-methods/83562370-3e5c-51db-87da-752af5ab9559"
        #       },
        #       "transaction": {
        #         "id": "441b9494-b3f0-5b98-b9b0-4d82c21c252a",
        #         "resource": "transaction",
        #         "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/transactions/441b9494-b3f0-5b98-b9b0-4d82c21c252a"
        #       },
        #       "amount": {
        #         "amount": "1.00000000",
        #         "currency": "BTC"
        #       },
        #       "total": {
        #         "amount": "10.25",
        #         "currency": "USD"
        #       },
        #       "subtotal": {
        #         "amount": "10.10",
        #         "currency": "USD"
        #       },
        #       "created_at": "2015-01-31T20:49:02Z",
        #       "updated_at": "2015-02-11T16:54:02-08:00",
        #       "resource": "buy",
        #       "resource_path": "/v2/accounts/2bbf394c-193b-5b2a-9155-3b4732659ede/buys/67e0eaec-07d7-54c4-a72c-2e92826897df",
        #       "committed": True,
        #       "instant": False,
        #       "fee": {
        #         "amount": "0.15",
        #         "currency": "USD"
        #       },
        #       "payout_at": "2015-02-18T16:54:00-08:00"
        #     }
        #
        symbol = None
        totalObject = self.safe_value(trade, 'total', {})
        amountObject = self.safe_value(trade, 'amount', {})
        subtotalObject = self.safe_value(trade, 'subtotal', {})
        feeObject = self.safe_value(trade, 'fee', {})
        id = self.safe_string(trade, 'id')
        timestamp = self.parse8601(self.safe_value(trade, 'created_at'))
        if market is None:
            baseId = self.safe_string(totalObject, 'currency')
            quoteId = self.safe_string(amountObject, 'currency')
            if (baseId is not None) and(quoteId is not None):
                base = self.common_currency_code(baseId)
                quote = self.common_currency_code(quoteId)
                symbol = base + '/' + quote
        orderId = None
        side = self.safe_string(trade, 'resource')
        type = None
        cost = self.safe_float(subtotalObject, 'amount')
        amount = self.safe_float(amountObject, 'amount')
        price = None
        if cost is not None:
            if amount is not None:
                price = cost / amount
        feeCost = self.safe_float(feeObject, 'amount')
        feeCurrencyId = self.safe_string(feeObject, 'currency')
        feeCurrency = self.common_currency_code(feeCurrencyId)
        fee = {
            'cost': feeCost,
            'currency': feeCurrency,
        }
        return {
            'info': trade,
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    async def fetch_currencies(self, params={}):
        response = await self.publicGetCurrencies(params)
        currencies = response['data']
        result = {}
        for c in range(0, len(currencies)):
            currency = currencies[c]
            id = currency['id']
            name = currency['name']
            code = self.common_currency_code(id)
            minimum = self.safe_float(currency, 'min_size')
            result[code] = {
                'id': id,
                'code': code,
                'info': currency,  # the original payload
                'name': name,
                'active': True,
                'fee': None,
                'precision': None,
                'limits': {
                    'amount': {
                        'min': minimum,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': None,
                        'max': None,
                    },
                },
            }
        return result

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        timestamp = self.seconds()
        market = self.market(symbol)
        request = self.extend({
            'symbol': market['id'],
        }, params)
        buy = await self.publicGetPricesSymbolBuy(request)
        sell = await self.publicGetPricesSymbolSell(request)
        spot = await self.publicGetPricesSymbolSpot(request)
        ask = self.safe_float(buy['data'], 'amount')
        bid = self.safe_float(sell['data'], 'amount')
        last = self.safe_float(spot['data'], 'amount')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'bid': bid,
            'ask': ask,
            'last': last,
            'high': None,
            'low': None,
            'bidVolume': None,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': None,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': None,
            'info': {
                'buy': buy,
                'sell': sell,
                'spot': spot,
            },
        }

    async def fetch_balance(self, params={}):
        response = await self.privateGetAccounts()
        balances = response['data']
        accounts = self.safe_value(params, 'type', self.options['accounts'])
        result = {'info': response}
        for b in range(0, len(balances)):
            balance = balances[b]
            if self.in_array(balance['type'], accounts):
                currencyId = balance['balance']['currency']
                code = currencyId
                if currencyId in self.currencies_by_id:
                    code = self.currencies_by_id[currencyId]['code']
                total = self.safe_float(balance['balance'], 'amount')
                free = total
                used = None
                if code in result:
                    result[code]['free'] += total
                    result[code]['total'] += total
                else:
                    account = {
                        'free': free,
                        'used': used,
                        'total': total,
                    }
                    result[code] = account
        return self.parse_balance(result)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        request = '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if method == 'GET':
            if query:
                request += '?' + self.urlencode(query)
        url = self.urls['api'] + '/' + self.version + request
        if api == 'private':
            self.check_required_credentials()
            nonce = str(self.nonce())
            payload = ''
            if method != 'GET':
                if query:
                    body = self.json(query)
                    payload = body
            what = nonce + method + '/' + self.version + request + payload
            signature = self.hmac(self.encode(what), self.encode(self.secret))
            headers = {
                'CB-ACCESS-KEY': self.apiKey,
                'CB-ACCESS-SIGN': signature,
                'CB-ACCESS-TIMESTAMP': nonce,
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body):
        if not isinstance(body, basestring):
            return  # fallback to default error handler
        if len(body) < 2:
            return  # fallback to default error handler
        if (body[0] == '{') or (body[0] == '['):
            response = json.loads(body)
            feedback = self.id + ' ' + body
            #
            #    {"error": "invalid_request", "error_description": "The request is missing a required parameter, includes an unsupported parameter value, or is otherwise malformed."}
            #
            # or
            #
            #    {
            #      "errors": [
            #        {
            #          "id": "not_found",
            #          "message": "Not found"
            #        }
            #      ]
            #    }
            #
            exceptions = self.exceptions
            errorCode = self.safe_string(response, 'error')
            if errorCode is not None:
                if errorCode in exceptions:
                    raise exceptions[errorCode](feedback)
                else:
                    raise ExchangeError(feedback)
            errors = self.safe_value(response, 'errors')
            if errors is not None:
                if isinstance(errors, list):
                    numErrors = len(errors)
                    if numErrors > 0:
                        errorCode = self.safe_string(errors[0], 'id')
                        if errorCode is not None:
                            if errorCode in exceptions:
                                raise exceptions[errorCode](feedback)
                            else:
                                raise ExchangeError(feedback)
            data = self.safe_value(response, 'data')
            if data is None:
                raise ExchangeError(self.id + ' failed due to a malformed response ' + self.json(response))