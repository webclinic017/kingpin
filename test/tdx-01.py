"""
    测试通达信数据
"""
from mootdx.quotes import Quotes

client = Quotes.factory(market='std',multithread=True, heartbeat=True)

bars = client.bars(symbol='600036', frequency=9, offset=10)

print(bars)

