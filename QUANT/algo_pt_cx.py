#!/usr/bin/env python

from   p4defs                    import *
import p4fns
import p8fns
import sys
import math
import matplotlib.pyplot         as     plt
import dateutil.parser           as     dp
import pandas                    as     pd

mode       = 'T'
symbolX    = str(sys.argv[1])
symbolF    = str(sys.argv[2])
symbol1    = str(sys.argv[3])
symbol2    = str(sys.argv[4])
symbol0    = str(sys.argv[5])
rwindow    = int(sys.argv[6])
mwindow    = int(sys.argv[7])
deltaP     = float(sys.argv[8])
deltaN     = float(sys.argv[9])
years      = float(sys.argv[10])
dur        = int(float(sys.argv[11])*252)

ixlist     = ['NIFTY','BANKNIFTY','SP500','HDFCLIQ','EIGHTFD','FIVEFD','NIFTYIT','NIFTYPHARMA','NIFTYAUTO','NIFTYFMCG','NIFTYMETAL']
cnx500     = [row[2] for row in p4fns.read_csv(NSEEQDIR+'CNX500.csv')] 
cnx200     = [row[2] for row in p4fns.read_csv(NSEEQDIR+'CNX200.csv')] 
cnx100     = [row[2] for row in p4fns.read_csv(NSEEQDIR+'CNX100.csv')] 
cnx50      = [row[2] for row in p4fns.read_csv(NSEEQDIR+'CNX50.csv')] 
cnxlist    = cnx500
days       = int(252*years)+rwindow+mwindow-1

result     = []

# Outer Cointegration
# ============================================================================================= ##
if symbolX in cnxlist:
    datadb     = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbolX+CSV), PQS, 'SERIES', REGEQSERIES)[-days:]
    priceX     = [math.log(float(row[PQS['CLOSE']])) for row in datadb]
    vwapX      = [math.log(float(row[PQS['VWAP']])) for row in datadb]
else:
    datadb     = p4fns.read_csv(NSEIXSDBDIR+symbolX+CSV)[-days:]
    priceX     = [math.log(float(row[PXS['CLOSE']])) for row in datadb]
    vwapX      = priceX
if symbolF in cnxlist:
    datadb     = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbolF+CSV), PQS, 'SERIES', REGEQSERIES)[-days:]
    priceF     = [math.log(float(row[PQS['CLOSE']])) for row in datadb]
    vwapF      = [math.log(float(row[PQS['VWAP']])) for row in datadb]
else:
    datadb     = p4fns.read_csv(NSEIXSDBDIR+symbolF+CSV)[-days:]
    priceF     = [math.log(float(row[PXS['CLOSE']])) for row in datadb]
    vwapF      = priceF
if symbol1 in cnxlist:
    datadb     = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol1+CSV), PQS, 'SERIES', REGEQSERIES)[-days:]
    close1     = [float(row[PQS['CLOSE']]) for row in datadb]
    price1     = [math.log(float(row[PQS['CLOSE']])) for row in datadb]
    vwap1      = [math.log(float(row[PQS['VWAP']])) for row in datadb]
else:
    datadb     = p4fns.read_csv(NSEIXSDBDIR+symbol1+CSV)[-days:]
    close1     = [float(row[PXS['CLOSE']]) for row in datadb]
    price1     = [math.log(float(row[PXS['CLOSE']])) for row in datadb]
    vwap1      = price1
if symbol2 in cnxlist:
    datadb     = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol2+CSV), PQS, 'SERIES', REGEQSERIES)[-days:]
    close2     = [float(row[PQS['CLOSE']]) for row in datadb]
    price2     = [math.log(float(row[PQS['CLOSE']])) for row in datadb]
    vwap2      = [math.log(float(row[PQS['VWAP']])) for row in datadb]
else:
    datadb     = p4fns.read_csv(NSEIXSDBDIR+symbol2+CSV)[-days:]
    close2     = [float(row[PXS['CLOSE']]) for row in datadb]
    price2     = [math.log(float(row[PXS['CLOSE']])) for row in datadb]
    vwap2      = price2
dsize          = min(len(priceX), len(priceF), len(price1), len(price2))
regrP          = p4fns.rolling_regress(vwapX[-dsize:], vwapF[-dsize:], rwindow)
rlen           = len(regrP)
errorP         = [round((a/b-1)*100, 2) for a, b in zip(priceX[-rlen:], regrP[-rlen:])]
timeser        = [row[PQS['TIMESTAMP']] for row in datadb][-rlen:]
muP            = p4fns.rolling_smean(errorP, mwindow)
sgP            = p4fns.rolling_sstdd(errorP, mwindow)
mlen           = len(sgP)
errorP         = errorP[-mlen:][:dur]
timeser        = timeser[-mlen:][:dur]
tlen           = len(timeser)
muP            = muP[-mlen:][:dur]
sgP            = sgP[-mlen:][:dur]

if (symbol1==symbol2):
    errorS     = [0]*tlen
    muS        = [0]*tlen
    sgS        = [1]*tlen
else:
    regrS      = p4fns.rolling_regress(vwap1[-dsize:], vwap2[-dsize:], rwindow)
    errorS     = [round((a/b-1)*100, 2) for a, b in zip(price1[-rlen:], regrS[-rlen:])]
    muS        = p4fns.rolling_smean(errorS, mwindow)
    sgS        = p4fns.rolling_sstdd(errorS, mwindow)
    errorS     = errorS[-mlen:][:dur]
    muS        = muS[-mlen:][:dur]
    sgS        = sgS[-mlen:][:dur]
close1         = close1[-mlen:][:dur]
close2         = close2[-mlen:][:dur]

if symbol1 in cnxlist:
    instrm1    = 'EQ'
else:
    instrm1    = 'IX'
if symbol2 in cnxlist:
    instrm2    = 'EQ'
else:
    instrm2    = 'IX'
if symbol0 in cnxlist:
    instrm0    = 'EQ'
else:
    instrm0    = 'IX'
startdate      = timeser[0]
enddate        = timeser[-1]
capital        = 1000000
startprice1    = float(p4fns.findvalue(startdate, instrm1, symbol1, 'XX', 'XX', 'XX', 'CLOSE'))
startprice2    = float(p4fns.findvalue(startdate, instrm2, symbol2, 'XX', 'XX', 'XX', 'CLOSE'))
startprice0    = float(p4fns.findvalue(startdate, instrm0, symbol0, 'XX', 'XX', 'XX', 'CLOSE'))

if (mode=='T') or (mode=='C') or (mode=='D'):
    print startdate
    print enddate

# Pair trading strategy
# ==============================================================
state          = 'PA_SA'
own1           = False
own2           = False
own0           = False
own            = [0]*tlen
ledgerdf       = p8fns.genledger(startdate, capital)

for i in range(0, tlen):
    PUpper             = True if (errorP[i] > (muP[i]+deltaP*sgP[i])) else False
    PLower             = True if (errorP[i] < (muP[i]-deltaN*sgP[i])) else False
    SUpper             = True if (errorS[i] > (muS[i]+deltaP*sgS[i])) else False
    SLower             = True if (errorS[i] < (muS[i]-deltaN*sgS[i])) else False
    if (state == 'PA_SA'):
        if PUpper:
             state     = 'PB'
        elif SUpper:
             state     = 'PA_SB'
    elif (state == 'PA_SB'):
        if PUpper:
             state     = 'PB'
        elif SLower:
             state     = 'PA_SA'
    elif (state == 'PB'):
        if PLower:
            if (errorS[i] < muS[i]):
                 state = 'PA_SA'
            else:
                 state = 'PA_SB'
            
    if (state != 'PB'):
        if (own0 == True):
            holding    = p8fns.getlgvolume(ledgerdf,symbol0,instrm0,'XX','XX','XX')
            ledgerdf   = p8fns.tradebyvol(ledgerdf, timeser[i], instrm0, symbol0, 'XX', 'XX', 'XX', -holding)
            own0       = False
    if (state != 'PA_SA'):
        if (own1 == True):
            holding    = p8fns.getlgvolume(ledgerdf,symbol1,instrm1,'XX','XX','XX')
            ledgerdf   = p8fns.tradebyvol(ledgerdf, timeser[i], instrm1, symbol1, 'XX', 'XX', 'XX', -holding)
            own1       = False
    if (state != 'PA_SB'):
        if (own2 == True):
            holding    = p8fns.getlgvolume(ledgerdf,symbol2,instrm2,'XX','XX','XX')
            ledgerdf   = p8fns.tradebyvol(ledgerdf, timeser[i], instrm2, symbol2, 'XX', 'XX', 'XX', -holding)
            own2       = False

    cashbal            = p8fns.getlgvolume(ledgerdf,'CASH','CASH','XX','XX','XX')
    if (state == 'PB'):
        if (own0 == False):
            ledgerdf   = p8fns.tradebyval(ledgerdf, timeser[i], instrm0, symbol0, 'XX', 'XX', 'XX', cashbal)
            own0       = True
    if (state == 'PA_SA'):
        if (own1 == False):
            ledgerdf   = p8fns.tradebyval(ledgerdf, timeser[i], instrm1, symbol1, 'XX', 'XX', 'XX', cashbal)
            own1       = True
    if (state == 'PA_SB'):
        if (own2 == False):
            ledgerdf   = p8fns.tradebyval(ledgerdf, timeser[i], instrm2, symbol2, 'XX', 'XX', 'XX', cashbal)
            own2       = True

    if (own1 == True):
        own[i]         = 1
        if (own2 == True) or (own0 == True):
            print "More than one Trade"
            exit()
    elif (own2 == True):
        own[i]         = -1 
        if (own1 == True) or (own0 == True):
            print "More than one Trade"
            exit()
    elif (own0 == True):
        own[i]         = 0 
        if (own1 == True) or (own2 == True):
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

# Buy and hold symbol0
# ==============================================================
ledgerdf           = p8fns.genledger(startdate, capital)
ledgerdf           = p8fns.tradebyval(ledgerdf, startdate, instrm0, symbol0, 'XX', 'XX', 'XX', capital)
portfoliodf        = p8fns.getportfolio(ledgerdf, enddate)
profit0            = round((p8fns.getpfvalue(portfoliodf,'TOTAL','XX','XX','XX','XX')-capital)/capital*100,1)
if (mode=='T') or (mode=='C') or (mode=='D'):
    print profit0

# Ownership statistics
# ==============================================================
if (mode=='T') or (mode=='C') or (mode=='D'):
    print 'Hold0 '+str(round(float(own.count(0))/len(own)*100))
    print 'Hold1 '+str(round(float(own.count(1))/len(own)*100))
    print 'Hold2 '+str(round(float(own.count(-1))/len(own)*100))

result.append([symbolX,symbolF,symbol1,symbol2,symbol0,startdate,enddate,dur,rwindow,mwindow,trades,profit,profit1,profit2,profit0])

if (mode=='W'):
    p4fns.write_csv('temp.csv', result, 'a')
elif (mode=='C') or (mode=='D'):
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

