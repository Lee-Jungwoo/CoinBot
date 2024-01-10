import upbit_machine
import pprint

m = upbit_machine.UpbitMachine()
m.buy_limit_order("BTC-KRW", 1, 5000)
