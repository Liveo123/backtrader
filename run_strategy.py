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
from strategies.emacrossover import EMACrossOver

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # prices = pd.read_csv('data/spy_2000-2020.csv', index_col='Date', parse_dates=True)
    final_year_roi = 0
    final_6month_roi = 0
    stock_count = 0
    stock_count = 0

    yearly = 55
    six_month = 20 #9
    sel_stocks = (("DECK", yearly, six_month),
                  ("TTSH", yearly, six_month),
                  ("TSLA", yearly, six_month),
                  ("MYRG",yearly, six_month),
                  ("FTNT",yearly, six_month),
                  ("GRMN", yearly, six_month),
                  ("ACLS", yearly, six_month),
                  ("ADBE",yearly, six_month),
                  ("HLNE", yearly, six_month),
                  ("MSFT",yearly, six_month),
                  ("HZO", yearly, six_month), # BBS*
                  ("SAM",yearly, six_month),# BB*
                  ("SNBR", yearly, six_month), # BBB
                  ("NSIT", yearly, six_month), # BSB*
                  ("BMI", yearly, six_month), # BBB*
                  ("ALGN", yearly, six_month), # BBB**
                  ("TPX",yearly, six_month), # BSB
                  ("SITE",yearly, six_month), # BBB
                  ("AAPL", yearly, six_month), # BBB
                  ("CCS",yearly, six_month), # BSB
                  ("GNRC",yearly, six_month), # BBB*
                  ("V", yearly, six_month),
                  ("VIPS", yearly, six_month), # BBB*
                  ("ENVA", yearly, six_month), # BBB*
                  )

    # sel_stocks = (("DECK")) # ("TTSH"), ("TSLA"))
    for sel_stock in sel_stocks:
        avg_roi = 0
        buy_or_sell = ""
        for strat in ['bbands1']:
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
                "sma_cross": SmaCross,
                "emacrossover": EMACrossOver
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
                cerebro.addstrategy(strategy=strategies[args.strategy])
                # cerebro.addstrategy(strategy=GoldenCross)


            # Add a FixedSize sizer according to the stake

            cerebro.broker.setcommission(commission=0.000)  # 0.5% of the operation value
            cerebro.addsizer(bt.sizers.AllInSizer)

            ## Set up for looping through the stocks

            # Loop through selected stocks
            # Download the relevant feed
            if strat == 'bbands2':
                start_date = datetime.datetime(2020, 7, 1)
            else:
                start_date = datetime.datetime(2020, 1, 12)

            feed = bt.feeds.YahooFinanceData(
                dataname=sel_stock[0],
                # Do not pass values before this date
                fromdate=start_date,
                # Do not pass values after this date
                todate=datetime.datetime(2021, 1, 12),
                reverse=False)

            cerebro.adddata(feed)

            print(f'Stock = {sel_stock[0]}, strategy = {strat}, start={start_date}')
            results = cerebro.run()
            if strat in ['bbands1', 'bbands2']:
                for i, strat_result in enumerate(results):
                    if strat_result.params.BuyLast:
                        buy_or_sell += "BUY "
                    else:
                        buy_or_sell += "SELL "

                print(buy_or_sell)

                #     print(strat_result.params.LastTransaction)
                # print("strat_parameters - {}: {}".format(i, strat_result.params))
        # cerebro.strategy.set_sma(opt_slow, opt_fast)

            # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
            # print('Final Cash Value: %.2f' % cerebro.broker.get_cash())
            roi = (cerebro.broker.get_value() / START_VALUE) - 1.0
            print('ROI:        {:.2f}%'.format(100.0 * roi))
            avg_roi += roi
            # if strat == 'bbands1':
            final_year_roi += roi
            # elif strat == 'bban?ds2':
            #     final_6month_roi += roi
            stock_count += 1

            if strat == 'golden_cross':
                print(f"######### AVG = {round((avg_roi/3), 2)}%")
            # cerebro.plot()

    print(f'Final year ROI mean  = {final_year_roi/stock_count}')
    # print(f'Final 6 month ROI mean = {final_6month_roi/stock_count}')
