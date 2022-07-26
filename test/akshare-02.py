"""
    akshare 用例
    参数优化 vs quantstats
"""
from datetime import datetime
from re import I
from turtle import position #

import backtrader as bt # 
import pandas as pd #
import akshare as ak #
import quantstats as qs #

# import matplotlib.pyplot as plt #
# plt.rcParams["font.sans-serif"] = ["SimHei"]  #中文, 雅黑 Microsoft YaHei
# plt.rcParams["axes.unicode_minus"] = False  #负数坐标轴

class MyStrategy(bt.Strategy):
    
    params = (("maperiod",20),  #ma改成20天
            ("printlog",False), )  #是否强制显示日志
   
    
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
        # today = self.datas[0].datetime.date(0)
        # self.log("Postition whit {} close/sma {:.2f}/{:.2f}".format(today.isoformat(), self.data_close[0],self.sma[0]))
        # print(self.position)
        #当前有交易指令 则返回
        if self.order:
            return 
        #是否持仓
        if not self.position: 
            if self.data_close[0] > self.sma[0]:  #收盘价上涨突破sam均线
                self.log("Buy create whit price/sma={:.2f}/{:.2f}".format(self.data_close[0],self.sma[0]), do_print=True)
                self.order = self.buy()  #全仓买入
        else:
            # self.log("Postition whit close/sma {:.2}/{:.2}".format(self.data_close[0],self.sma[0]))
            if self.data_close[0] < self.sma[0]:  #跌破sam均线
                self.log("Sell create whit price/sma={:.2f}/{:.2f}".format(self.data_close[0],self.sma[0]), do_print=True)
                self.order = self.sell()  #清仓

    def log(self, txt, dt=None, do_print=False):
        """
        日志记录， 优先判断 self.params.printlog 是否展示日志

        Args:
            txt (_type_): _description_
            dt (_type_, optional): _description_. Defaults to None.
            do_print (bool, optional): _description_. Defaults to False.
        """
        if self.params.printlog or do_print:
            dt = dt or self.datas[0].datetime.date(0)
            print("{}:  {}".format(dt.isoformat(),txt))
    #END def log 
   
    def notify_trade(self, trade):
        self.log("bar序：{}，交易通知 size:{},price:{},value:{},tradeid:{},status:{}"
              .format(len(self),trade.size,trade.price,trade.value,trade.tradeid,trade.status_names[trade.status]))
        
    def notify_order(self, order):
        do_print = True if order.status == order.Completed else False 
        
        self.log("bar序：{}，订单通知 size:{},price:{},pricelimit:{},exectype:{},tradeid:{},status:{}"
              .format(len(self),order.size,order.price,order.pricelimit,order.ExecTypes[order.exectype],order.tradeid,order.Status[order.status]),
              do_print=do_print)
       
        #Notice: 必须重置order 否则next进行不下去...
        if not order.alive():  ##order status Completed
            self.order = None
    # #END def notify_order 
    
    def stop(self):
        self.log("#STOP# MA均线 {:2d}日，期末总资金 {:.2f}".format(self.params.maperiod, self.broker.getvalue()), do_print=True)      
#END class


def main(symbol="000001", start_date:datetime=None, end_date:datetime=None, 
        start_cash=0, stake=100, commission=0.001):
    
    # 获取 前复权
    stock_qfq_df = ak.stock_zh_a_hist(symbol,
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

    cerebro = bt.Cerebro() 
    data = bt.feeds.PandasData(dataname=stock_qfq_df, fromdate=start_date, todate=end_date)  #加载数据
    cerebro.adddata(data)  #传入回测系统
    cerebro.addstrategy(MyStrategy)  #传入策略
    cerebro.broker.setcash(start_cash)  #初始资金
    cerebro.broker.setcommission(commission=commission)  #手续费
    cerebro.addsizer(bt.sizers.FixedSize, stake=stake)  #单手股数·

    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')
    backbro = cerebro.run()

    #收益
    port_value = cerebro.broker.getvalue()
    pnl = port_value - start_cash  #总收益

    print("初始资金: {}\n回测区间：{} => {}".format(
            start_cash,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"), )  
        )
    print(f"总资金: {round(port_value, 2)}")
    print(f"净收益: {round(pnl, 2)}")

    # cerebro.plot(style='candlestick')
    # use quantstats
    protfolio_stats = backbro[0].analyzers.getbyname('PyFolio')
    returns, positions, transaction, gross_lev = protfolio_stats.get_pf_items()
    returns.index = returns.index.tz_convert(None)

    import os
    download_filename = "quantstats-" + str(symbol) + ".html"
    download_filename = os.path.join(os.path.pardir, 'tmp', download_filename)
    
    qs.reports.html(returns, output=True, 
                    download_filename=download_filename, title="code:{} 中文中文 quantstats".format(symbol))    
     
    
#END def main

if __name__ == '__main__':
    symbol = "600070"  #浙江富润
    start_date = datetime(2007, 1, 4)  #开始时间
    end_date = datetime(2022, 7, 23)  #结束时间
    start_cash = 100000  #起始资金10w
    commission_fee = 0.002  #手续费0.2%
    mark_stake = 100  #大A 100股/手

    main(symbol=symbol, start_date=start_date, end_date=end_date,
         start_cash=start_cash, stake=mark_stake, commission=commission_fee)



