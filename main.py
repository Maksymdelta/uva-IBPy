# Declare the components with respective parameters

# Import stuff here later

#from data import DataHandler #actually a subclass of DataHandler
import os
os.chdir("/home/taylor/backtester/")

import Queue
import time

from data import HistoricCSVDataHandler
from strategy import BuyAndHoldStrategy
from portfolio import NaivePortfolio 
from execution import SimulatedExecutionHandler

start_date = '2015-03-13' #figure out better solution for this
events = Queue.Queue(maxsize=100)
bars = HistoricCSVDataHandler(events, "/home/taylor/backtester/csv/", ['yhoo'])
strategy = BuyAndHoldStrategy(bars, events)
port = NaivePortfolio(bars, events, start_date, initial_capital=100000.)
broker = SimulatedExecutionHandler(events)

while True:
    # Update the bars (specific backtest code, as opposed to live trading)
    if bars.continue_backtest == True:
        bars.update_bars()
    else:
        break
    
    # Handle the events
    while True:
        try:
            event = events.get(False)
        except Queue.Empty:
            break
        else:
            if event is not None:
                if event.type == 'MARKET':
                    print 'MARKET!'
                    strategy.calculate_signals(event)
                    port.update_timeindex(event)

                elif event.type == 'SIGNAL':
                    print 'SIGNAL!'
                    port.update_signal(event)

                elif event.type == 'ORDER':
                    print 'ORDER!'
                    broker.execute_order(event) #problem

                elif event.type == 'FILL':
                    print 'FILL!'
                    port.update_fill(event)

    #time.sleep(.1)
