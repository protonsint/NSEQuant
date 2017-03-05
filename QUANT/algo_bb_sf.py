#!/usr/bin/env python

from   p4defs                    import *
import p4fns
import p8fns
import sys
import math
import dateutil.parser           as     dp
import pandas                    as     pd

mode           = 'T'
symbol1        = str(sys.argv[1])
symbol2        = str(sys.argv[2])
mwindow        = int(sys.argv[3])
deltaP         = float(sys.argv[4])
deltaN         = float(sys.argv[5])
years          = int(sys.argv[6])
dur            = int(sys.argv[7])*252

ixlist         = ['NIFTY','BANKNIFTY']
cnx500         = [row[2] for row in p4fns.read_csv(NSEEQDIR+'CNX500.csv')] 
cnx100         = [row[2] for row in p4fns.read_csv(NSEEQDIR+'CNX100.csv')] 
cnx50          = [row[2] for row in p4fns.read_csv(NSEEQDIR+'CNX50.csv')] 
cnxlist        = cnx500
days           = 252*years+mwindow

result     = []
# ============================================================================================= ##
# Bollinger Band
# ============================================================================================= ##
if symbol1 in cnxlist:
    datadb     = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol1+CSV), PQS, 'SERIES', REGEQSERIES)[-days:]
    price1     = [math.log(float(row[PQS['CLOSE']])) for row in datadb]
    vwap1      = [math.log(float(row[PQS['VWAP']])) for row in datadb]
    instrm1    = 'EQ'
else:
    datadb     = p4fns.read_csv(NSEIXSDBDIR+symbol1+CSV)[-days:]
    price1     = [math.log(float(row[PXS['CLOSE']])) for row in datadb]
    vwap1      = price1
    instrm1    = 'IX'
if symbol2 in cnxlist:
    datadb     = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol2+CSV), PQS, 'SERIES', REGEQSERIES)[-days:]
    price2     = [math.log(float(row[PQS['CLOSE']])) for row in datadb]
    instrm2    = 'EQ'
else:
    datadb     = p4fns.read_csv(NSEIXSDBDIR+symbol2+CSV)[-days:]
    price2     = [math.log(float(row[PXS['CLOSE']])) for row in datadb]
    instrm2    = 'IX'
dsize          = min(len(price1), len(price2))
mu             = p4fns.rolling_smean(vwap1[-dsize:], mwindow)
sg             = p4fns.rolling_sstdd(vwap1[-dsize:], mwindow)
mlen           = len(sg)
timeser        = [row[PQS['TIMESTAMP']] for row in datadb][-mlen:][:dur]
price1         = price1[-mlen:][:dur]
price2         = price2[-mlen:][:dur]
mu             = mu[-mlen:][:dur]
sg             = sg[-mlen:][:dur]
tlen           = len(timeser)

startdate      = timeser[0]
enddate        = timeser[-1]
capital        = 1000000
#startprice1    = float(p4fns.findvalue(startdate, instrm1, symbol1, 'XX', 'XX', 'XX', 'CLOSE'))
#startprice2    = float(p4fns.findvalue(startdate, instrm2, symbol2, 'XX', 'XX', 'XX', 'CLOSE'))
startprice1    = price1[0]
startprice2    = price1[0]

if (mode=='T') or (mode=='C') or (mode=='D'):
    print startdate
    print enddate

# Trading strategy
# ==============================================================
state          = 'PA'
own1           = False
own2           = False
own            = [0]*tlen
ledgerdf       = p8fns.genledger(startdate, capital)

for i in range(0, tlen):
    PUpper             = True if (price1[i] > (mu[i]+deltaP*sg[i])) else False
    PLower             = True if (price1[i] < (mu[i]-deltaN*sg[i])) else False
    if (state == 'PA'):
        if PUpper:
            state      = 'PB'
    elif (state == 'PB'):
        if PLower:
            state      = 'PA'
            
    if (state != 'PA'):
        if (own1 == True):
            holding    = p8fns.getlgvolume(ledgerdf,symbol1,instrm1,'XX','XX','XX')
            ledgerdf   = p8fns.tradebyvol(ledgerdf, timeser[i], instrm1, symbol1, 'XX', 'XX', 'XX', -holding)
            own1       = False
    if (state != 'PB'):
        if (own2 == True):
            holding    = p8fns.getlgvolume(ledgerdf,symbol2,instrm2,'XX','XX','XX')
            ledgerdf   = p8fns.tradebyvol(ledgerdf, timeser[i], instrm2, symbol2, 'XX', 'XX', 'XX', -holding)
            own2       = False

    cashbal            = p8fns.getlgvolume(ledgerdf,'CASH','CASH','XX','XX','XX')
    if (state == 'PA'):
        if (own1 == False):
            ledgerdf   = p8fns.tradebyval(ledgerdf, timeser[i], instrm1, symbol1, 'XX', 'XX', 'XX', cashbal)
            own1       = True
    if (state == 'PB'):
        if (own2 == False):
            ledgerdf   = p8fns.tradebyval(ledgerdf, timeser[i], instrm2, symbol2, 'XX', 'XX', 'XX', cashbal)
            own2       = True

    if (own1 == True):
        own[i]         = 1
        if (own2 == True):
            print "More than one Trade"
            exit()
    elif (own2 == True):
        own[i]         = -1 
        if (own1 == True):
            print "More than one Trade"
            exit()

portfoliodf        = p8fns.getportfolio(ledgerdf, enddate)
trades             = (len(ledgerdf)-4)/4
profit             = round((p8fns.getpfvalue(portfoliodf,'TOTAL','XX','XX','XX','XX')-capital)/capital*100,1)
if (mode=='D'):
    p8fns.listpr(ledgerdf)
    p8fns.listpr(portfoliodf)
if (mode=='T') or (mode=='C') or (mode=='D'):
    print str(tlen/252)+' years, '+str(tlen%252)+' days'
    print 'No of trades: '+str(trades)
    print profit

# Buy and hold symbol1
# ==============================================================
ledgerdf           = p8fns.genledger(startdate, capital)
ledgerdf           = p8fns.tradebyval(ledgerdf, startdate, instrm1, symbol1, 'XX', 'XX', 'XX', capital)
portfoliodf        = p8fns.getportfolio(ledgerdf, enddate)
profit1            = round((p8fns.getpfvalue(portfoliodf,'TOTAL','XX','XX','XX','XX')-capital)/capital*100,1)
if (mode=='T') or (mode=='C') or (mode=='D'):
    print profit1

# Buy and hold symbol2
# ==============================================================
ledgerdf           = p8fns.genledger(startdate, capital)
ledgerdf           = p8fns.tradebyval(ledgerdf, startdate, instrm2, symbol2, 'XX', 'XX', 'XX', capital)
portfoliodf        = p8fns.getportfolio(ledgerdf, enddate)
profit2            = round((p8fns.getpfvalue(portfoliodf,'TOTAL','XX','XX','XX','XX')-capital)/capital*100,1)
if (mode=='T') or (mode=='C') or (mode=='D'):
    print profit2

# Ownership statistics
# ==============================================================
if (mode=='T') or (mode=='C') or (mode=='D'):
    print 'Hold1 '+str(round(float(own.count(1))/len(own)*100))
    print 'Hold2 '+str(round(float(own.count(-1))/len(own)*100))

result.append([symbol1,symbol2,startdate,enddate,dur,mwindow,trades,profit,profit1,profit2])

if (mode=='W'):
    p4fns.write_csv('RESULTS/temp.csv', result, 'a')
elif (mode=='C'):
# Plot
# ==============================================================
    df             = pd.DataFrame()
    df['TIME']     = [dp.parse(row) for row in timeser]
    df['ERR']      = errorP
    df['OWN']      = own
    df[symbol1]    = close1
    df[symbol2]    = close2
    df['MU']       = muP
    df['PL']       = [muP[i] + deltaP*sgP[i] for i in range(0,tlen)]
    df['NL']       = [muP[i] - deltaN*sgP[i] for i in range(0,tlen)]
    df             = df.set_index(['TIME'])
    p8fns.plot3axis(df, ['ERR','MU','PL','NL'],'OWN',symbol1,symbol2)

