import requests
import json
import itertools  
import datetime
import time

class Bolsa:
    def __init__(self, name, compra, venda):
        self.name = name
        self.venda = venda 
        self.compra = compra
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



current_ = 0
current_json = 0

while True:
    blinktrade_request = requests.get('https://api.blinktrade.com/api/v1/BRL/orderbook')
    mrcBTC_request = requests.get('https://www.mercadobitcoin.net/api/BTC/orderbook/')

    info = json.dumps(blinktrade_request.json())
    foxbit_dict = json.loads(info)
    FOXBIT = Bolsa("FOXBIT",foxbit_dict["asks"][0][0],foxbit_dict["bids"][0][0])
    FOXBIT_json = ["FOXBIT",foxbit_dict["asks"][0][0],foxbit_dict["bids"][0][0]]

    info = json.dumps(mrcBTC_request.json())
    mrcBTC_dict = json.loads(info)
    MRCBTC = Bolsa("MRCBTC",mrcBTC_dict["asks"][0][0],mrcBTC_dict["bids"][0][0])
    MRCBTC_json = ["MRCBTC",mrcBTC_dict["asks"][0][0],mrcBTC_dict["bids"][0][0]]

    listData_json = [FOXBIT_json,MRCBTC_json]
    listData = [FOXBIT,MRCBTC]
    output_json = json.dumps(listData_json)

    if current_json != output_json:
        current_ = listData
        current_json = output_json
        datafile = open('BrasilExchanges.csv', 'a')
        for a, b in itertools.permutations(current_, 2):
            if a.compra < b.venda:
                datafile.write("%s;%s;%s;%s;%s;%s\n" %(datetime.datetime.now() ,a.name,a.compra,b.name,b.venda,(b.venda/a.compra)-1))
                print ("%s // %s // Compra: %s // %s //Venda: %s // Spread %s\n" %(datetime.datetime.now() ,a.name,a.compra,b.name,b.venda,(b.venda/a.compra)-1))  
        datafile.close()
        print("Alive")
