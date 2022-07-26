"""
    akshare 用例
"""
from datetime import datetime #

import backtrader as bt # 
import matplotlib.pyplot as plt #
import akshare as ak #
import pandas as pd #

plt.rcParams["font.sans-serif"] = ["SimHei"]  #中文, 雅黑 Microsoft YaHei
plt.rcParams["axes.unicode_minus"] = False  #负数坐标轴


start_date = datetime(2000, 1, 1)  #开始时间
end_date = datetime(2022, 7, 23)  #结束时间
start_cash = 1000000


# 获取 平安银行 前复权
stock_qfq_df = ak.stock_zh_a_hist(symbol="000001", 
                                period='daily',
                                start_date=start_date.strftime("%Y%m%d"),
                                end_date=end_date.strftime("%Y%m%d"),
                                adjust="qfq"
                                ).iloc[:,:6]  #切割前6列数据
stock_qfq_df.columns = [
    'date',
    'open',
    'close',
    'high',
    'low',
    'volume',
]
# backtrader要求使用date作为日期索引
stock_qfq_df.index = pd.to_datetime(stock_qfq_df['date'])

class MyStrategy(bt.Strategy):
    
    params = (("maperiod",20),)  #ma改成20天
    
    def __init__(self):
        
        self.data_close = self.datas[0].close  #指定价格序列

        #初始化交易 买卖价和手续费
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        
        #添加移动均线指标      
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )
        
    def next(self):
        """
        sam策略
        """
        #当前有交易指令 则返回
        if self.order:
            return 
        #是否持仓
        if not self.position: 
            if self.data_close[0] > self.sma[0]:  #收盘价上涨突破sam均线
                self.order = self.buy(size=100)  #全仓买入
        else:
            if self.data_close[0] < self.sma[0]:  #跌破sam均线
                self.order = self.sell(size=100)  #清仓
#END class

cerebro = bt.Cerebro() 
data = bt.feeds.PandasData(dataname=stock_qfq_df, fromdate=start_date, todate=end_date)  #加载数据
cerebro.adddata(data)  #传入回测系统
cerebro.addstrategy(MyStrategy)  #传入策略
cerebro.broker.setcash(start_cash)  #初始资金100w
cerebro.broker.setcommission(commission=0.002)  #手续费0.2%
cerebro.run()

port_value = cerebro.broker.getvalue()
pnl = port_value - start_cash  #总收益


print("初始资金: {}\n回测区间：{} => {}".format(
        start_cash,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"), )  
      )
print(f"总资金: {round(port_value, 2)}")
print(f"净收益: {round(pnl, 2)}")



cerebro.plot(style='candlestick')


