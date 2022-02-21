# %%
from tradeogre import TradeOgre
import time,os,random
from Settings import *
from dotenv import load_dotenv
load_dotenv()
trade_ogre = TradeOgre(key=os.environ.get('KEY'), secret=os.environ.get('SECRET'))
# %%
def IOC_BUY(ticker,quantity,price):
    res=trade_ogre.buy(ticker, quantity, price ) 
    time.sleep(0.5)
    if res['success']==True and res['uuid']!=None:
        trade_ogre.cancel(res['uuid'])

def IOC_SELL(ticker,quantity,price):
    res=trade_ogre.sell(ticker, quantity, price ) 
    time.sleep(0.5)
    if res['success']==True and res['uuid']!=None:
        trade_ogre.cancel(res['uuid'])

while True:
    # Get the current XUSD price
    USDT_BTC=float(trade_ogre.ticker('USDT-BTC')['price'])**-1
    XUSD_BTC=float(trade_ogre.ticker('BTC-XUSD')['price'])
    XUSDPRICE =XUSD_BTC/USDT_BTC
    print('xUSD price : '+ str(XUSDPRICE) +' $')
    # Get the orderbook prices
    xusd_bid=(trade_ogre.ticker('BTC-XUSD')['bid'])
    xusd_ask=(trade_ogre.ticker('BTC-XUSD')['ask'])
    btc_bid=trade_ogre.ticker('USDT-BTC')['bid']
    btc_ask=trade_ogre.ticker('USDT-BTC')['ask']
    
    if XUSDPRICE<XUSD_BUY_PRICE:
        print('Buy XUSD/USDT')
        IOC_BUY('USDT-BTC',format(QUANTITY_DOLLAR*USDT_BTC, '.10f'),btc_ask)
        IOC_BUY('BTC-XUSD',QUANTITY_DOLLAR,xusd_ask)
    elif XUSDPRICE>XUSD_SELL_PRICE:
        print('SELL XUSD/USDT')
        IOC_SELL('USDT-BTC',format(QUANTITY_DOLLAR*USDT_BTC, '.10f'),btc_bid) 
        IOC_SELL('BTC-XUSD',QUANTITY_DOLLAR,xusd_bid)

    time.sleep(5)

# %%