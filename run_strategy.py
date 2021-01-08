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
from strategies.sma_cross import SmaCross

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # prices = pd.read_csv('data/spy_2000-2020.csv', index_col='Date', parse_dates=True)

    sel_stocks = (("DECK", 12, 20),
                  ("TTSH", 19, 19),
                  ("TSLA", 10, 11),
                  ("MYRG", 8, 15),
                  ("FTNT", 22, 8),
                  ("GRMN", 39, 37),
                  ("ACLS", 50, 40),
                  ("ADBE", 8, 15),
                  ("HLNE", 17, 17),
                  ("MSFT", 12, 8),
                  ("HZO", 22, 20),
                  ("SAM", 9, 25),
                  ("SNBR", 24, 20),
                  ("NSIT", 19, 20),
                  ("BMI", 10, 12),
                  ("ALGN", 45, 20),
                  ("TPX", 44, 20),
                  ("SITE", 8, 15),
                  ("AAPL", 15, 20),
                  ("CCS", 31, 20),
                  ("GNRC", 30, 20),
                  ("VIPS", 10, 20),
                  )

    # sel_stocks = (("DECK")) # ("TTSH"), ("TSLA"))
    for sel_stock in sel_stocks:
        avg_roi = 0
        for strat in ['bbands1', 'bbands2', 'golden_cross']:
            # initialize the Cerebro engine
            cerebro = Cerebro()
            START_VALUE = 1000
            cerebro.broker.setcash(START_VALUE)

            # add OHLC data feed
            # feed = bt.feeds.PandasData(dataname=prices)


            strategies = {
                "golden_cross": GoldenCross,
                "buy_hold": BuyHold,
                "strategy": TestStrategy,
                "rsi_mean": RSIMean,
                "bbands": BBands,
                "stop_loss": ManualStopOrStopTrail,
                "sma_cross": SmaCross
            }

            # parse command line arguments
            parser = argparse.ArgumentParser()
            parser.add_argument("strategy", help="Which strategy to run", type=str)
            args = parser.parse_args()

            if not args.strategy in strategies:
                print("Invalid strategy, must select one of {}".format(strategies.keys()))
                sys.exit()

            # if args.strategy == 'bbands':
            if strat == 'bbands1':
                # cerebro.addstrategy(strategy=strategies[args.strategy],
                cerebro.addstrategy(strategy=BBands,
                                    BBandsperiod=sel_stock[1])
            elif strat=='bbands2':
                cerebro.addstrategy(strategy=BBands,
                                    BBandsperiod=sel_stock[2])
            else:
                # cerebro.addstrategy(strategy=strategies[args.strategy])
                cerebro.addstrategy(strategy=GoldenCross)


            # Add a FixedSize sizer according to the stake

            cerebro.broker.setcommission(commission=0.000)  # 0.5% of the operation value
            cerebro.addsizer(bt.sizers.AllInSizer)

            ## Set up for looping through the stocks

            # Loop through selected stocks
            # Download the relevant feed
            if strat == 'bbands2':
                start_date = datetime.datetime(2020, 7, 1)
            else:
                start_date = datetime.datetime(2020, 1, 1)

            feed = bt.feeds.YahooFinanceData(
                dataname=sel_stock[0],
                # Do not pass values before this date
                fromdate=start_date,
                # Do not pass values after this date
                todate=datetime.datetime(2020, 12, 31),
                reverse=False)

            cerebro.adddata(feed)

            print(f'Stock = {sel_stock[0]}, strategy = {strat}, start={start_date}')
            results = cerebro.run()
            if strat not in ['golden_cross']:
                for i, strat_result in enumerate(results):
                    print(strat_result.params.LastTransaction)
                # print("strat_parameters - {}: {}".format(i, strat_result.params))
        # cerebro.strategy.set_sma(opt_slow, opt_fast)

            # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
            # print('Final Cash Value: %.2f' % cerebro.broker.get_cash())
            roi = (cerebro.broker.get_value() / START_VALUE) - 1.0
            print('ROI:        {:.2f}%'.format(100.0 * roi))
            avg_roi += roi
            if strat == 'golden_cross':
                print(f"######### AVG = {round((avg_roi/3), 2)}%")
            # cerebro.plot()
