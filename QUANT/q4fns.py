#!/usr/bin/env python
from   p4defs            import *
import p4fns
import dateutil.parser   as     dp
import math
import os.path as path

TECHCOLTYP         = {'SYMBOL':'S','PRICE':'F','GAIN':'F','MKT_CAP':'I','MC_PERCENT':'I'}
today              = p4fns.read_csv(NSEIXSDBDIR+'NIFTY'+CSV)[-1][PXS['TIMESTAMP']]

## ********************************************************************************************* ##
## Daily Closing Data
## ********************************************************************************************* ##
def qntdaily(symbol):
    eqsdbdf        = p4fns.readhdr_csv(NSEEQSDBDIR+symbol+CSV) 
    eqsdb          = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)[-252:]
    eqsdbdf        = eqsdbdf+eqsdb
    inputdf        = p4fns.rearrange(eqsdbdf, PQS, JSONCOL)
    p4fns.write_json(JSONDLYDIR+symbol+JSON, inputdf, EQCOLTYP)

## ********************************************************************************************* ##
## General Information
## ********************************************************************************************* ##
def qntgenl(symbol, name, sector, industry, mktcap, mcpercent):
    techtitle      = ['SYMBOL','PRICE','GAIN','NAME','SECTOR','INDUSTRY','MKT_CAP','MC_PERCENT',\
                      'VOLATILITY','MAX_VTY','MIN_VTY','VOLUME','MAX_VOL','MIN_VOL']
    techtable      = []
    srow           = []
    srow.append(symbol)
    eqsdb          = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)

    ## Current Values
    ## ============================================== ##
    curprice       = eqsdb[-1][PQS['CLOSE']]
    srow.append(curprice)
    change         = round(float(eqsdb[-1][PQS['GAIN']]), 2)
    srow.append(change)
    srow.append(name)
    srow.append(sector)
    srow.append(industry)
    srow.append(mktcap)
    srow.append(mcpercent)

    ## Volatility
    ## ============================================== ##
    if path.isfile(NSEDVSDBDIR+symbol+CSV):
        dvsdb      = p4fns.filterdf(p4fns.filterdf(p4fns.filterdf(p4fns.read_csv(NSEDVSDBDIR+symbol+CSV),\
                                                   PDS, 'INSTRUMENT', ['OPTSTK']),\
                                                   PDS, 'TIMESTAMP', [today]),\
                                                   PDS, 'T2E', [str(x) for x in range(1,50)])
        ivlist     = [float(row[PDS['IV']]) for row in dvsdb]
        wtlist     = [float(row[PDS['VAL_INLAKH']]) for row in dvsdb]
        if sum(wtlist) >= 100:
            avgiv  = round(p4fns.wmean(ivlist, wtlist), 2)
        else:
            avgiv  = 0
    else:
        avgiv      = 0
    eqdata         = eqsdb[-756:]
    gain           = [float(row[PQS['GAIN']]) for row in eqdata]
    cum_gain       = p4fns.rolling_sum(gain, 21)
    rol_stdd       = p4fns.rolling_sstdd(cum_gain, 21)
    if (avgiv==0):
        stdd1m     = round(p4fns.sstdd(cum_gain)*math.sqrt(12), 2)
        volatility = stdd1m
    else:
        volatility = avgiv
    max_stdd       = max([volatility, round(max(rol_stdd)*math.sqrt(12), 2)])
    min_stdd       = min([volatility, round(min(rol_stdd)*math.sqrt(12), 2)])
    srow.append(volatility)
    srow.append(max_stdd)
    srow.append(min_stdd)

    ## Volume
    ## ============================================== ##
    eqdata         = eqsdb[-252:]
    turnover       = [round(float(row[PQS['TURNOVER']])/10000000, 2) for row in eqdata]
    volume         = p4fns.rolling_emean(turnover, 3)
    max_vol        = max(volume)
    min_vol        = min(volume)
    srow.append(turnover[-1])
    srow.append(max_vol)
    srow.append(min_vol)

    ## Create JSON File
    ## ============================================== ##
    techtable.append(srow)
    p4fns.write_csv(NSEGENLDIR+symbol+CSV, [techtitle]+techtable, 'w')
    p4fns.write_json(JSONGENLDIR+symbol+JSON, [techtitle]+techtable, TECHCOLTYP)
    genltable      = []
    grow           = []
    grow.append(symbol)
    grow.append(name)
    grow.append(sector)
    grow.append(industry)
    grow.append(curprice)
    grow.append(change)
    grow.append(mktcap)
    grow.append(turnover[-1])
    grow.append(volatility)
    genltable.append(grow)
    p4fns.write_csv(NSETECHDIR+'NSEGenl'+CSV, genltable, 'a')

## ********************************************************************************************* ##
## Performance Information
## ********************************************************************************************* ##
def qntperf(symbol, name):
    perftable      = []
    eqsdb          = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)

    ## Price Values
    ## ============================================== ##
    price          = [float(row[PQS['CLOSE']]) for row in eqsdb]
    perf1w         = round(math.log(price[-1]/price[-5])*100, 2) if len(price)>5 else '-'
    perf1m         = round(math.log(price[-1]/price[-21])*100, 2) if len(price)>21 else '-'
    perf3m         = round(math.log(price[-1]/price[-63])*100, 2) if len(price)>63 else '-'
    perf6m         = round(math.log(price[-1]/price[-126])*100, 2) if len(price)>126 else '-'
    perf1y         = round(math.log(price[-1]/price[-252])*100, 2) if len(price)>252 else '-'
    perf2y         = round(math.log(price[-1]/price[-504])*100, 2) if len(price)>504 else '-'
    perf4y         = round(math.log(price[-1]/price[-1008])*100, 2) if len(price)>1008 else '-'

    ## Volatility Values
    ## ============================================== ##
    gain           = [float(row[PQS['GAIN']]) for row in eqsdb]
    stdd1w         = round(p4fns.sstdd(gain[-5:])*math.sqrt(252), 2) if len(price)>5 else '-'
    stdd1m         = round(p4fns.sstdd(gain[-21:])*math.sqrt(252), 2) if len(price)>21 else '-'
    stdd3m         = round(p4fns.sstdd(gain[-63:])*math.sqrt(252), 2) if len(price)>63 else '-'
    stdd6m         = round(p4fns.sstdd(gain[-126:])*math.sqrt(252), 2) if len(price)>126 else '-'
    stdd1y         = round(p4fns.sstdd(gain[-252:])*math.sqrt(252), 2) if len(price)>252 else '-'
    stdd2y         = round(p4fns.sstdd(gain[-504:])*math.sqrt(252), 2) if len(price)>504 else '-'
    stdd4y         = round(p4fns.sstdd(gain[-1008:])*math.sqrt(252), 2) if len(price)>1008 else '-'
    perftable.append([symbol,name,perf1w,perf1m,perf3m,perf6m,perf1y,perf2y,perf4y,\
                      stdd1w,stdd1m,stdd3m,stdd6m,stdd1y,stdd2y,stdd4y])
    p4fns.write_csv(NSETECHDIR+'NSEPerf'+CSV, perftable, 'a')

## ********************************************************************************************* ##
## Technical Information (Channel)
## ********************************************************************************************* ##
def qnttech(symbol, name):
    techtable      = []
    eqsdb          = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)

    ## Price Bands
    ## ============================================== ##
    price          = [float(row[PQS['CLOSE']]) for row in eqsdb]
    vwap           = [float(row[PQS['VWAP']]) for row in eqsdb]
    pb1m           = int((price[-1]-min(price[-21:]))/(max(price[-21:])-min(price[-21:]))*100) if len(price)>21 else '-'
    pb3m           = int((price[-1]-min(price[-63:]))/(max(price[-63:])-min(price[-63:]))*100) if len(price)>63 else '-'
    pb6m           = int((price[-1]-min(price[-126:]))/(max(price[-126:])-min(price[-126:]))*100) if len(price)>126 else '-'
    pb1y           = int((price[-1]-min(price[-252:]))/(max(price[-252:])-min(price[-252:]))*100) if len(price)>252 else '-'

    ## Bollinger Bands
    ## ============================================== ##
    dsize          = len(price)
    period         = [21, 63, 126, 252]
    bb             = ['-']*4
    for i in range(0,4):
        if (dsize > period[i]+1):
           mu      = p4fns.rolling_emean(vwap[-(period[i]+1):], period[i])[-1]
           sg      = p4fns.rolling_sstdd(vwap[-(period[i]+1):], period[i])[-1]
           bb[i]   = int(p4fns.cumnormdist((price[-1]-mu)/sg)*100)

    techtable.append([symbol,name,pb1m,pb3m,pb6m,pb1y,bb[0],bb[1],bb[2],bb[3]])
    p4fns.write_csv(NSETECHDIR+'NSETech'+CSV, techtable, 'a')

### ============================================================================================= ##
### Best Candidates for Statistical Arbitrage for each (Sector, Industry)
### ============================================================================================= ##
def qntpair(symbol, period, deltaP, deltaN, rwindow, mwindow, pairlist):
    title      = ['PAIR','NORM','DWSTAT']
    maxper     = period+rwindow+mwindow-1
    table      = []

    datadb         = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)[-maxper:]
    pclose         = [math.log(float(row[PQS['CLOSE']])) for row in datadb]
    pvwap          = [math.log(float(row[PQS['VWAP']])) for row in datadb]
    dsize          = len(pclose)
    if (dsize>=rwindow+mwindow+40):
        for pair in pairlist:
            reffdb         = p4fns.read_csv(NSEEQSDBDIR+pair+CSV)[-maxper:]
            pvwapR         = [math.log(float(row[PQS['VWAP']])) for row in reffdb]
            
            regr           = p4fns.rolling_regress(pvwap[-dsize:], pvwapR[-dsize:], rwindow)
            rlen           = len(regr)
            error          = [round((a/b-1)*100, 2) for a, b in zip(pclose[-rlen:], regr[-rlen:])]
            mu             = p4fns.rolling_smean(error, mwindow)
            sg             = p4fns.rolling_sstdd(error, mwindow)
            mlen           = len(sg)
            error          = error[-mlen:]
            normdist       = int(p4fns.cumnormdist((error[-1]-mu[-1])/sg[-1])*100)
            et_t1          = sum([math.pow((error[i]-error[i-1]), 2) for i in range(1, mlen)])
            et_sq          = sum([math.pow(error[i],2) for i in range(0, mlen)])
            dwstat         = round(et_t1/et_sq, 2)
            table.append([pair, normdist, dwstat])
        
        p4fns.write_csv(NSEPAIRDIR+symbol+CSV, [title]+table, 'w')
        p4fns.write_json(JSONPAIRDIR+symbol+JSON, [title]+table, [])

## ============================================================================================= ##
## Result effect
## ============================================================================================= ##
def qntresult(symbol, resdf):
    techtitle      = ['SYMBOL']
    techtable      = []
    result         = [dp.parse(row[PRES['TIMESTAMP']]).strftime('%Y-%m-%d') for row in resdf if row[PRES['SYMBOL']]==symbol][-8:]
    srow           = []
    srow.append(symbol)
    eqsdb          = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)
    for res in result:
        backmean   = p4fns.smean([float(row[PQS['CLOSE']]) for row in p4fns.blockdf(eqsdb, PQS, res, 21, 'be')])
        fronmean   = p4fns.smean([float(row[PQS['CLOSE']]) for row in p4fns.blockdf(eqsdb, PQS, res, 21, 'fe')])
        effect     = round(math.log(fronmean/backmean)*100, 2)
        srow.append(effect)
        techtitle.append(res)
    techtable.append(srow)
    techtable      = [techtitle]+techtable
    p4fns.write_json(JSONRESDIR+symbol+JSON, techtable, TECHCOLTYP)

## ============================================================================================= ##
## Events Catalog
## ============================================================================================= ##
def qntevent(symbol, bonuspst, bonusfut, splitpst, splitfut, rightpst, rightfut, divdnpst, divdnfut, resltpst, resltfut):
    eventsum       = []
    bpst           = p4fns.filterdf(bonuspst, PBON, 'SYMBOL', [symbol])
    bfut           = p4fns.filterdf(bonusfut, PBON, 'SYMBOL', [symbol])
    spst           = p4fns.filterdf(splitpst, PSPL, 'SYMBOL', [symbol])
    sfut           = p4fns.filterdf(splitfut, PSPL, 'SYMBOL', [symbol])
    gpst           = p4fns.filterdf(rightpst, PRGT, 'SYMBOL', [symbol])
    gfut           = p4fns.filterdf(rightfut, PRGT, 'SYMBOL', [symbol])
    dpst           = p4fns.filterdf(divdnpst, PDIV, 'SYMBOL', [symbol])
    dfut           = p4fns.filterdf(divdnfut, PDIV, 'SYMBOL', [symbol])
    rpst           = p4fns.filterdf(resltpst, PRES, 'SYMBOL', [symbol])
    rfut           = p4fns.filterdf(resltfut, PRES, 'SYMBOL', [symbol])
    for row in bpst:
        eventsum.append([dp.parse(row[PBON['EXDATE']]), 'Bonus Shares', row[PBON['RATIO']], 'P'])
    for row in bfut:
        eventsum.append([dp.parse(row[PBON['EXDATE']]), 'Bonus Shares', row[PBON['RATIO']], 'F'])
    for row in spst:
        eventsum.append([dp.parse(row[PSPL['EXDATE']]), 'Stock Split', row[PSPL['RATIO']], 'P'])
    for row in sfut:
        eventsum.append([dp.parse(row[PSPL['EXDATE']]), 'Stock Split', row[PSPL['RATIO']], 'F'])
    for row in gpst:
        eventsum.append([dp.parse(row[PRGT['EXDATE']]), 'Rights Issue', row[PRGT['RATIO']], 'P'])
    for row in gpst:
        eventsum.append([dp.parse(row[PRGT['EXDATE']]), 'Rights Issue', row[PRGT['RATIO']], 'F'])
    for row in dpst:
        eventsum.append([dp.parse(row[PDIV['EXDATE']]), 'Dividend Declaration', row[PDIV['DIVIDEND']]+' Rs', 'P'])
    for row in dfut:
        eventsum.append([dp.parse(row[PDIV['EXDATE']]), 'Dividend Declaration', row[PDIV['DIVIDEND']]+' Rs', 'F'])
    for row in rpst:
        eventsum.append([dp.parse(row[PRES['TIMESTAMP']]), 'Result Declaration', '-', 'P'])
    for row in rfut:
        eventsum.append([dp.parse(row[PRES['TIMESTAMP']]), 'Result Declaration', '-', 'F'])
    eventsum.sort(key=lambda x: x[0])
    eventsum       = [[row[0].strftime('%Y-%m-%d')]+row[1:] for row in eventsum]
    fname          = JSONEVNTDIR+symbol+JSON
    with open(fname, 'w') as fjson:
        json.dump(eventsum, fjson)
