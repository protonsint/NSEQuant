## ############################################################################################# ##
## Sub Routines
## ############################################################################################# ##
from   p4defs            import *
import p4fns
from   scipy             import stats
import matplotlib.pyplot       as     plt

## ********************************************************************************************* ##
## Statistics
## ********************************************************************************************* ##

## Find regression expected value of a list
## =========================================== ##
def regress(data, indep):
    slope, intercept, rvalue, pvalue, stderr  = stats.linregress(indep, data)
    predict        = indep[-1]*slope + intercept
    return predict

## Find rolling regression expected value of a list
## ================================================ ##
def rolling_regress(data, indep, window):
    rpred          = []
    for i in range(0, len(data)-window+1):
        rpred.append(regress(data[i:i+window], indep[i:i+window])) 
    return rpred    

## Find correlation between two lists
## =========================================== ##
def corr(data1, data2):
    corrcoeff      = round(stats.pearsonr(data1,data2)[0]*100,2)
    return corrcoeff

## Find regression r-value 
## =========================================== ##
def rvalue(data, indep):
    slope, intercept, rvalue, pvalue, stderr  = stats.linregress(indep, data)
    return rvalue*100

## Find mean rvalue between two lists with given window and intervals
## ========================================================================== ##
def mean_rvalue(data1, data2, window, interval):
    samples        = p4fns.sample(range(0,len(data1)), interval) 
    rlist          = []
    for i in samples:
        if (i>=window):
            rlist.append(rvalue(data1[i-window:i+1],data2[i-window:i+1]))
    mean_r         = round(p4fns.smean(rlist), 2)
    return mean_r

## ********************************************************************************************* ##
## Plots
## ********************************************************************************************* ##
def plot3axis(df, axis1, axis2, axis3, axis4):
    fig, ax        = plt.subplots(figsize=(15,7))
    ax2, ax3       = ax.twinx(), ax.twinx()
    rspine         = ax3.spines['right']
    rspine.set_position(('axes', 1.15))
    ax3.set_frame_on(True)
    ax3.patch.set_visible(False)
    ax2.set_yscale('log')
    fig.subplots_adjust(right=0.75)
    df[axis1].plot(ax=ax, style='b-', linewidth=2, figsize=(15,7))
    df[axis2].plot(ax=ax, style='y-', linewidth=2)
    df[axis3].plot(ax=ax2, style='g-', secondary_y=True, linewidth=2)
    df[axis4].plot(ax=ax3, style='r-', linewidth=2)
    plt.show()
    
def plot2axis(df, second):
    df.plot(figsize=(15,7),linewidth=2, secondary_y=second, grid=True)
    plt.show()

def plot1axis(df):
    df.plot(figsize=(15,7),linewidth=2, grid=True)
    plt.show()

## ********************************************************************************************* ##
## Plots
## ********************************************************************************************* ##
def listpr(datadf):
    for row in datadf:
        print (row)
## ********************************************************************************************* ##
## Portfolio and Ledger
## ********************************************************************************************* ##
def genledger(timestamp, cash):
    header         = LEDGERCOL
    opencash       = [timestamp,'CASH','CASH','XX','XX','XX',cash,cash]
    ledgerdf       = [header, opencash]
    return ledgerdf

def appendledger(ledgerin, timestamp, symbol, instrument, optiontyp, expirydt,\
                 strikepr, volume, price):
    ledgerdf       = ledgerin
    turnover       = round(volume * price, 2)
    ledgerdf.append([timestamp, symbol, instrument, optiontyp, expirydt, strikepr, volume, turnover])
    ledgerdf.append([timestamp, 'CASH', 'CASH', 'XX', 'XX', 'XX', -turnover, -turnover])
    return ledgerdf

def updateledger(ledgerin, timestamp, operator):
    ledgerdf       = ledgerin
    ledger         = p4fns.filterdf(ledgerin[1:], PLS, 'INSTRUMENT', ['OPTIDX','OPTSTK','FUTIVX','FUTSTK','FUTIDX'])
    ledger         = p4fns.filterts(ledger, PLS, 'EXPIRY_DT', timestamp, operator)
    appenddf       = []
    for row in ledger:
        instrument = row[PLS['INSTRUMENT']]
        symbol     = row[PLS['SYMBOL']]
        optiontyp  = row[PLS['OPTION_TYP']]
        expirydt   = row[PLS['EXPIRY_DT']]
        strikepr   = row[PLS['STRIKE_PR']]
        idf        = p4fns.filterdf(ledger, PLS, 'INSTRUMENT', [instrument])
        idf        = p4fns.filterdf(idf, PLS, 'SYMBOL', [symbol])
        idf        = p4fns.filterdf(idf, PLS, 'OPTION_TYP', [optiontyp])
        idf        = p4fns.filterdf(idf, PLS, 'EXPIRY_DT', [expirydt])
        idf        = p4fns.filterdf(idf, PLS, 'STRIKE_PR', [strikepr])
        cumvol     = 0
        for irow in idf:
            cumvol = cumvol + irow[PLS['VOLUME']]
        adf        = p4fns.filterdf(appenddf, PLS, 'INSTRUMENT', [instrument])
        adf        = p4fns.filterdf(adf, PLS, 'SYMBOL', [symbol])
        adf        = p4fns.filterdf(adf, PLS, 'OPTION_TYP', [optiontyp])
        adf        = p4fns.filterdf(adf, PLS, 'EXPIRY_DT', [expirydt])
        adf        = p4fns.filterdf(adf, PLS, 'STRIKE_PR', [strikepr])
        appvol     = 0
        for prow in adf:
            appvol     = appvol + prow[PLS['VOLUME']]
        if (appvol+cumvol != 0):
            expvalue   = float(p4fns.findvalue(expirydt, instrument, symbol, optiontyp, expirydt, strikepr, 'CLOSE'))
            appenddf   = appendledger(appenddf, expirydt, symbol, instrument, optiontyp, expirydt,\
                          strikepr, (-appvol-cumvol), expvalue)
    ledgerdf       = ledgerdf+appenddf 
    return ledgerdf

def getportfolio(ledgerdf, timestamp):
    ledgerdf       = [row[:PLS['TURNOVER']]+row[PLS['TURNOVER']+1:] for row in ledgerdf[1:]]
    portfoliodf    = [PORTFCOL]
    for row in ledgerdf:
        sectype   = [row[PLS['SYMBOL']], row[PLS['INSTRUMENT']], row[PLS['OPTION_TYP']], row[PLS['EXPIRY_DT']], row[PLS['STRIKE_PR']]]
        updated    = False
        for prow in portfoliodf:
            secptype       = [prow[PPS['SYMBOL']], prow[PPS['INSTRUMENT']], prow[PPS['OPTION_TYP']], prow[PPS['EXPIRY_DT']], prow[PPS['STRIKE_PR']]]
            if (secptype == sectype):
                updated    = True
        if (updated == False):
            cum_vol        = 0
            for lrow in ledgerdf:
                secltype   = [lrow[PLS['SYMBOL']], lrow[PLS['INSTRUMENT']], lrow[PLS['OPTION_TYP']], lrow[PLS['EXPIRY_DT']], lrow[PLS['STRIKE_PR']]]
                if (secltype == sectype):
                     cum_vol   = cum_vol + lrow[PLS['VOLUME']]
            if (cum_vol != 0):
                if (row[PLS['SYMBOL']] == 'CASH'):
                    price      = 1
                else:
                    price      = float(p4fns.findvalue(timestamp, row[PLS['INSTRUMENT']], row[PLS['SYMBOL']], row[PLS['OPTION_TYP']], row[PLS['EXPIRY_DT']], row[PLS['STRIKE_PR']], 'CLOSE'))
                value          = round(price*cum_vol, 2)
                cum_vol        = round(cum_vol, 2)
                prow   = [row[PLS['SYMBOL']], row[PLS['INSTRUMENT']], row[PLS['OPTION_TYP']], row[PLS['EXPIRY_DT']], row[PLS['STRIKE_PR']], cum_vol, value]
                portfoliodf.append(prow)
    return portfoliodf

def getpfvalue(portfoliodf, symbol, instrument, option_typ, expiry_dt, strike_pr):
    value          = 0
    if (symbol=='TOTAL'):
       for prow in portfoliodf[1:]:
           value   = value + prow[PPS['VALUE']]
    else:
       for prow in portfoliodf[1:]:
           if (prow[PPS['SYMBOL']]==symbol) and (prow[PPS['INSTRUMENT']]==instrument) and (prow[PPS['OPTION_TYP']]==option_typ) and\
              (prow[PPS['EXPIRY_DT']]==expiry_dt) and (prow[PPS['STRIKE_PR']]==strike_pr):
               value   = value + prow[PPS['VALUE']]
    return value

def getpfvolume(portfoliodf, symbol, instrument, option_typ, expiry_dt, strike_pr):
    volume         = 0
    for prow in portfoliodf[1:]:
        if (prow[PPS['SYMBOL']]==symbol) and (prow[PPS['INSTRUMENT']]==instrument) and (prow[PPS['OPTION_TYP']]==option_typ) and\
           (prow[PPS['EXPIRY_DT']]==expiry_dt) and (prow[PPS['STRIKE_PR']]==strike_pr):
            volume  = volume + prow[PPS['VOLUME']]
    return volume

def getlgvolume(ledgerdf, symbol, instrument, option_typ, expiry_dt, strike_pr):
    volume         = 0
    for lrow in ledgerdf[1:]:
        if (lrow[PLS['SYMBOL']]==symbol) and (lrow[PLS['INSTRUMENT']]==instrument) and (lrow[PLS['OPTION_TYP']]==option_typ) and\
           (lrow[PLS['EXPIRY_DT']]==expiry_dt) and (lrow[PLS['STRIKE_PR']]==strike_pr):
            volume  = volume + lrow[PLS['VOLUME']]
    return volume

## ********************************************************************************************* ##
## Trade (Buy and Sell securities)
## ********************************************************************************************* ##
def tradebyval(ledgerin, timestamp, instrument, symbol, optiontyp, expirydt, strikepr, turnover):
    price          = float(p4fns.findvalue(timestamp, instrument, symbol, optiontyp, expirydt, strikepr, 'CLOSE'))
    volume         = int(turnover/price)
    price          = round(price, 2)
    ledgerdf       = appendledger(ledgerin, timestamp, symbol, instrument, optiontyp, expirydt, strikepr, volume, price)
    return ledgerdf

def tradebyvol(ledgerin, timestamp, instrument, symbol, optiontyp, expirydt, strikepr, volume):
    price          = float(p4fns.findvalue(timestamp, instrument, symbol, optiontyp, expirydt, strikepr, 'CLOSE'))
    price          = round(price, 2)
    ledgerdf       = appendledger(ledgerin, timestamp, symbol, instrument, optiontyp, expirydt, strikepr, volume, price)
    return ledgerdf
