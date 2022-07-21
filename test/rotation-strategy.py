'''
股债ETF轮动
    一共三个 ETF轮动 510050.XSHG 159915.XSHE 511010.XSHG
    涉及ETF：上证50ETF(SH:510050)、创业板(SZ:159915)、国债ETF(SH:511010)
			上证50代表国家队，创业板代表散户，国债赌经济下行
		历史净值查看 天天基金：http://fundf10.eastmoney.com/jjjz_510050.html
			择时
			每天开盘前，从3个ETF中选出过去一个月涨幅最高的，和持仓的ETF比较，如果不一致，就调仓到涨幅高的。
				如果缩短周期，比如看过去1周，那么对趋势和震荡更敏感。
				如果拉长周期，比如看过去半年，那么对趋势和震荡更迟钝。
			理想的情况是对趋势敏感，对震荡迟钝，但不能两得，所以折衷一下，看1个月的。
			
			仓位控制
			如果过去一个月，3个ETF都是下跌的，就空仓，否则永远满仓。
举个例子，当前满仓创业板ETF，过去一个月涨幅最多的是50ETF，就在开盘时无脑卖创业板买50。

'''

# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    # 在context中保存全局变量
    context.stocks = ['510050.XSHG', '159915.XSHE', '511010.XSHG']
    context.dstock = None #默认当天持仓 开盘前更改
    context.DAY_COUNT = 20 #默认20个交易日 大概一个月自然日

    # 实时打印日志
    #logger.info("RunInfo: {}".format(context.run_info))

# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    '''
        每天开盘前 选择最近1一个月的收盘价, 默认20个交易日
        TODO 当前持仓增长与计算etf一样 则不更改合约
    '''

    context.dstock = None #默认当天持仓 开盘前更改
    s1tmp = 0
    for hbar in context.stocks:
        hdata = history_bars(hbar, context.DAY_COUNT, '1d', 'close' )
        htmp = 100* (hdata[-1] - hdata[0]) / hdata[0]
        logger.info("bid[" + str(hbar) +  "]: " + str(htmp) )

        if htmp > s1tmp:
            s1tmp = htmp
            context.dstock = hbar

    #2 打印今天策略
    posts = context.portfolio.positions
    logger.info("Today Buy["+ str(context.dstock)+"](" + str(s1tmp) + ") Sell["+ str(posts.keys())  +"]")
    #print( s1tmp, context.dstock )
#END def before


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合信息

    # 使用order_shares(id_or_ins, amount)方法进行落单


    #TEST
    #order_shares(context.stocks[2], 1000)
    #context.dstock = context.stocks[0]
    #print(context.portfolio)

    #1 判断现有持仓
    posts = context.portfolio.positions
    poslen =len(posts)
     
    if poslen > 1:
        logger.error("Error positions: " + format(context.portfolio)   )
        #raise TypeError("Error positions")


    #3 判断是否 需要 清空其他仓位 
    for bid,bar in posts.items():
        if bid != context.dstock:
            #抛掉
            order_shares(bar.order_book_id, -bar.sellable)
            logger.info("[Sell] bid:" + str(bar.order_book_id) +  " amount:" + str(bar.sellable) )

    #4 买入s1
    if context.dstock is  None:
        logger.info("[None] bid")
    else:
        batp = order_target_percent(context.dstock, 1)
        logger.info("[Buy] bid:" + str(context.dstock) + " Order: {}" . format(batp) )


'''
    if context.dstock is None:
       
    #3 交换股
    elseif context.dstock not in context.portfolio.positions:
        for bid,bar in context.portfolio.positions.items():
            #空仓 抛掉所有
            order_shares(bar.order_book_id, -bar.sellable)
            logger.info("[NSell] bar:" + str(bar.order_book_id) +  " amount:" + str(bar.sellable) )
    


    #END if

'''   
    
    
    

# after_trading函数会在每天交易结束后被调用，当天只会被调用一次
def after_trading(context):
    pass
