import configparser
import hashlib
from urllib.parse import urlencode

import autotrading.machine.base_machine as base_machine
import requests
import pprint
import uuid
import jwt


class UpbitMachine(base_machine.Machine):
    BASE_URL = "https://api.upbit.com/v1"
    TRADE_CURRENCY = ["BTC", "KRW"]
    ACCESS_KEY = None
    SECRET_KEY = None

    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read('/Users/ijeong-u/PycharmProjects/CoinBot/conf/config.ini')
        self.ACCESS_KEY = cfg['UPBIT']['Access_key']
        self.SECRET_KEY = cfg['UPBIT']['Secret_key']

    def __get_jwt_header(self, query=None):
        """
        :param query: request parameter in dictionary.
        :return: dictionary of jwt.
        """
        payload = {
            "access_key": self.ACCESS_KEY,
            "nonce": str(uuid.uuid4())
        }

        if query is not None:
            m = hashlib.sha512()
            m.update(urlencode(query, doseq=True).replace("%5B%5D=", "[]=").encode())
            query_hash = m.hexdigest()
            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = "SHA512"

        jwt_token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")  # PyJWT >= 2.0
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorization_token}
        return headers

    def get_filled_orders(self, market=None, uuids=None):
        """
        체결된 주문들 정보 리턴하는 메서드
        :param market: market ID str.
        :param uuids: list of order uuids.
        :return:
        """

        url = self.BASE_URL + "/orders"

        param = {'states[]': ['done', 'cancel']}
        if market is not None:
            param['market'] = market
        if uuids is not None:
            param['uuids[]'] = uuids

        response = requests.get(url, params=param, headers=self.__get_jwt_header(param))
        # pprint.pprint(response.json())
        return response.json()

    def get_unfilled_orders(self, market=None, uuids=None):
        """
        미체결된 주문들 정보 리턴하는 메서드
        :return:
        """
        url = self.BASE_URL + "/orders"

        param = {'states[]': ['wait', 'watch']}
        if market is not None:
            param['market'] = market
        if uuids is not None:
            param['uuids[]'] = uuids

        response = requests.get(url, params=param, headers=self.__get_jwt_header(param))
        # pprint.pprint(response.json())

        return response.json()

    def get_ticker(self, currency_type):
        """

        :param currency_type:
        :return:
        """
        url = self.BASE_URL + '/trades/ticks?market={}'.format(currency_type)

        # GET 요청 보내기
        response = requests.get(url)
        r_json = response.json()

        # 응답 받은 데이터 확인
        pprint.pprint(r_json)

        return r_json

    def get_wallet_status(self):
        """

        :returns: json dictionary of wallet status.
        """
        url = self.BASE_URL + '/accounts'

        # GET 요청
        response = requests.get(url, headers=self.__get_jwt_header(None))

        # 응답 받은 데이터 확인
        pprint.pprint(response.json())

        # 리턴
        return response.json()

    def get_coin_addresses(self):
        """

        :return: json dictionary of coin addresses

        """
        url = self.BASE_URL + '/deposits/coin_addresses'

        response = requests.get(url, headers=self.__get_jwt_header())

    def get_token(self):
        """
        :return: access token. if None, return None.
        """
        if self.ACCESS_KEY is not None:
            return self.ACCESS_KEY
        else:
            return None

    def set_token(self):
        """
        null function.
        :return: nothing
        """
        pass

    def get_upbit_api_key(self):
        """

        :return: every access tokens of the account and their expiry/expiration date.
        """
        url = self.BASE_URL + '/api_keys'

        headers = self.__get_jwt_header()
        resp = requests.get(url, headers=headers)
        pprint.pprint(resp.json())
        return resp.json()

    def get_username(self):

        pass

    def buy_order(self):
        pass

    def sell_order(self):
        pass

    def cancel_order(self):
        pass

    def get_my_order_status(self):
        pass

    def get_chance_of(self, market):
        """

        :param market: KRW-BTC etc.
        :return: json dictionary of the chance of market.
        """
        url = self.BASE_URL + '/orders/chance'
        param = {'market': market}
        headers = self.__get_jwt_header(query=param)
        resp = requests.get(url, headers=headers, params=param)
        # pprint.pprint(resp.json())
        return resp.json()
