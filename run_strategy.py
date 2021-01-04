import os, sys, argparse, datetime
import pandas as pd
import backtrader as bt
from backtrader import Cerebro
from strategies.GoldenCross import GoldenCross
from strategies.BuyHold import BuyHold
from strategies.strategy import TestStrategy
from strategies.rsimean import RSIMean
from strategies.bbands import BBands
from strategies.stoploss import ManualStopOrStopTrail

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # prices = pd.read_csv('data/spy_2000-2020.csv', index_col='Date', parse_dates=True)

    # initialize the Cerebro engine
    cerebro = Cerebro()
    START_VALUE = 1000
    cerebro.broker.setcash(START_VALUE)

    # add OHLC data feed
    # feed = bt.feeds.PandasData(dataname=prices)
    feed = bt.feeds.YahooFinanceData(
        dataname='ADBE',
        # Do not pass values before this date
        fromdate=datetime.datetime(2020, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2020, 12, 31),
        reverse=False)

    cerebro.adddata(feed)

    strategies = {
        "golden_cross": GoldenCross,
        "buy_hold": BuyHold,
        "strategy": TestStrategy,
        "rsi_mean": RSIMean,
        "bbands": BBands,
        "stop_loss": ManualStopOrStopTrail
    }

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("strategy", help="Which strategy to run", type=str)
    args = parser.parse_args()

    if not args.strategy in strategies:
        print("Invalid strategy, must select one of {}".format(strategies.keys()))
        sys.exit()

    cerebro.addstrategy(strategy=strategies[args.strategy])

    # Add a FixedSize sizer according to the stake


    cerebro.broker.setcommission(commission=0.000)  # 0.5% of the operation value
    cerebro.addsizer(bt.sizers.AllInSizer)

    cerebro.run()

    # cerebro.strategy.set_sma(opt_slow, opt_fast)

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('Final Cash Value: %.2f' % cerebro.broker.get_cash())
    roi = (cerebro.broker.get_value() / START_VALUE) - 1.0
    print('ROI:        {:.2f}%'.format(100.0 * roi))

    cerebro.plot()
