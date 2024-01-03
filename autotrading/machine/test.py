import configparser


cfg = configparser.ConfigParser()
cfg.read('../../conf/config.ini')

print(cfg["UPBIT"]['Access_key'])