#!/usr/bin/env python
from   p4defs             import *
import m4fns
import p4fns

cnx500         = p4fns.read_csv(NSEEQDIR+'CNX500.csv') 
cnxlist        = [row[PXL['SYMBOL']] for row in cnx500]

## ============================================================================================= ##
## Daily Candlestick and Volume chart
## ============================================================================================= ##
#donelist           = [row[0] for row in p4fns.read_csv(IMGDLYLOG)]
#todolist           = [sym for sym in cnxlist if sym not in donelist]
#periods            = {'3M':63,'6M':126,'1Y':252,'2Y':504,'4Y':1008}
#for symbol in todolist:
#    m4fns.pltcandle(symbol, periods)
#    p4fns.write_csv(IMGDLYLOG, [[symbol]], 'a')
#
## ============================================================================================= ##
## Volume and Volatility Bar
## ============================================================================================= ##
#donelist           = [row[0] for row in p4fns.read_csv(IMGVOLLOG)]
#todolist           = [sym for sym in cnxlist if sym not in donelist]
#for symbol in todolist:
#    m4fns.pltvol(symbol)
#    p4fns.write_csv(IMGVOLLOG, [[symbol]], 'a')
#
### ============================================================================================= ##
## Bollinger Bands
## ============================================================================================= ##
#donelist           = [row[0] for row in p4fns.read_csv(IMGBOBLOG)]
#todolist           = [sym for sym in cnxlist if sym not in donelist]
#deltaP             = 1.5
#deltaN             = 1.5
#periods            = {'1Y':252}
#mawin              = 63
#for symbol in todolist:
#    m4fns.pltbollinger(symbol, periods, deltaP, deltaN, mawin)
#    p4fns.write_csv(IMGBOBLOG, [[symbol]], 'a')

## ============================================================================================= ##
## Auto Regression
## ============================================================================================= ##
#donelist           = [row[0] for row in p4fns.read_csv(IMGAURLOG)]
#todolist           = [sym for sym in cnxlist if sym not in donelist]
#deltaP             = 1.5
#deltaN             = 1.5
#period             = 252
#rwindow            = 252
#mwindow            = 94
#for symbol in todolist:
#    m4fns.pltautoregres(symbol, period, deltaP, deltaN, rwindow, mwindow)
#    p4fns.write_csv(IMGAURLOG, [[symbol]], 'a')
#
## ============================================================================================= ##
## Cross Regression
## ============================================================================================= ##
#donelist           = [row[0] for row in p4fns.read_csv(IMGCRRLOG)]
#todolist           = [sym for sym in cnxlist if sym not in donelist]
todolist           = ['HDFCBANK']
deltaP             = 1.5
deltaN             = 1.5
period             = 252
rwindow            = 252
mwindow            = 94
for symbol in todolist:
    m4fns.pltcrosregres(symbol, period, deltaP, deltaN, rwindow, mwindow)
#    p4fns.write_csv(IMGCRRLOG, [[symbol]], 'a')
