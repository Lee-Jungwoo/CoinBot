import pyupbit
import pprint
import requests

f = open("UpbitKey.txt")
lines = f.readlines()
f.close()

access_key = lines[0].split()[0]
secret_key = lines[1].split()[0]


upbit = pyupbit.Upbit(access_key, secret_key)

# import autotrading.machine.upbit_machine as m
#
# m.UpbitMachine().get_ticker()





response = upbit.buy_limit_order("KRW-BTC", 5000, 1)

# upbit.cancel_order('d6dfb56c-7af5-4f9a-b612-cb9824e3dc53')
# # pprint.pprint(upbit.get_balances())
# pprint.pprint(upbit.get_order("KRW-BTC"))


#
# # anotherResp = upbit.sell_limit_order("KRW-BTC",5000,1)


