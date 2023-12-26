import pyupbit
import requests

f = open("key.txt")
lines = f.readlines()

access_key = lines[0].split()[0]
secret_key = lines[1].split()[0]

upbit = pyupbit.Upbit(access_key, secret_key)
balances = upbit.get_balances()
print(balances)

