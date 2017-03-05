#!/usr/bin/env python
from   p4defs          import *
import p4fns
import math
import os.path         as     path

cnx500             = p4fns.read_csv(NSEEQDIR+'CNX500.csv') 
cnxlist            = [row[PXL['SYMBOL']] for row in cnx500]
ixclist            = ['NIFTY','BANKNIFTY']

# General: Prices, Turnover, Volatility
# ============================================== ##
#for symbol in cnxlist:
#    genldata       = [['TIMESTAMP','OPEN','HIGH','LOW','CLOSE','TURNOVER','VOLATILITY']]
#    eqsdb          = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)
#
#    if path.isfile(NSEDVDIR+'TECH/'+symbol+CSV):
#        dvsdb      = p4fns.read_csv(NSEDVDIR+'TECH/'+symbol+CSV)
#        ivdict     = {row[0]:float(row[1]) for row in dvsdb}
#    else:
#        ivdict     = {}
#
#    timestamp      = [row[PQS['TIMESTAMP']] for row in eqsdb]
#    avgiv          = []
#    for i in range (0, len(timestamp)):
#       if timestamp[i] in ivdict:
#           avgiv.append(ivdict[timestamp[i]])
#       else:
#           avgiv.append(0)
#    gain           = [float(row[PQS['GAIN']]) for row in eqsdb]
#    cum_gain       = p4fns.rolling_sum(gain, 21)
#    volatility     = [round(row*math.sqrt(12), 2) for row in p4fns.rolling_sstdd(cum_gain, 21)]
#    dsize          = len(volatility)
#    eqsdb          = eqsdb[-dsize:]
#    avgiv          = avgiv[-dsize:]
#
#    for i in range(0, dsize):
#       srow        = []
#       srow.append(eqsdb[i][PQS['TIMESTAMP']])
#       srow.append(eqsdb[i][PQS['OPEN']])
#       srow.append(eqsdb[i][PQS['HIGH']])
#       srow.append(eqsdb[i][PQS['LOW']])
#       srow.append(eqsdb[i][PQS['CLOSE']])
#       srow.append(round(float(eqsdb[i][PQS['TURNOVER']])/10000000, 2))
#       srow.append(avgiv[i] if avgiv[i] != 0 else volatility[i])
#       genldata.append(srow)
#
#    p4fns.write_csv(NSEDIR+'TECHNICAL/GENL/'+symbol+CSV, genldata, 'w')

# Bollinger Bands + AutoRegression + Nifty Regression
# =================================================== ##
#for symbol in cnxlist:
for symbol in ['HDFCBANK']:

    eqsdb          = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)
    eqsize         = len(eqsdb)
    dsize          = 252
#    # Bollinger Bands 
#    # --------------------------------------------------- #
#    genldata       = p4fns.read_csv(NSEDIR+'TECHNICAL/GENL/'+symbol+CSV)
#    title          = ['TIMESTAMP','CLOSE','MEAN','SIGMA']
#    dsize          = min(252, len(genldata))
#    vwap           = [float(row[PQS['VWAP']]) for row in eqsdb]
#    emean          = p4fns.rolling_emean(vwap, 21)[-dsize:]
#    eqdata         = eqsdb[-dsize:]
#    genldata       = genldata[-dsize:]
#    vwap           = vwap[-dsize:]
#    table          = []
#    sigma          = [round(float(genldata[i][6])*vwap[i]/(math.sqrt(252)*100),2) for i in range(dsize)]
#
#    for i in range(0, dsize):
#       
#       srow        = []
#       srow.append(eqdata[i][PQS['TIMESTAMP']])
#       srow.append(eqdata[i][PQS['CLOSE']])
#       srow.append(emean[i])
#       srow.append(sigma[i])
#       table.append(srow)
#
#    # Auto Regression
#    # ---------------------------------------------- #
#    rwindow        = 252
#    mwindow        = 94
#    close          = [float(row[PQS['CLOSE']]) for row in eqsdb]
#    pvwap          = [math.log(float(row[PQS['VWAP']])) for row in eqsdb]
#    if (eqsize>=rwindow+mwindow+40):
#        title      = title + ['AURMU','AURSG']
#        reffdb     = p4fns.read_csv(NSEIXSDBDIR+'EIGHTFD'+CSV)[-eqsize:]
#        pvwapR     = [math.log(float(row[PXS['CLOSE']])) for row in reffdb]
#        regr       = p4fns.rolling_regress(pvwap[-eqsize:], pvwapR[-eqsize:], rwindow)
#        predict    = [round(math.exp(x),2) for x in regr]
#        rlen       = len(regr)
#        error      = [round((a - b), 2) for a, b in zip(close[-rlen:], predict[-rlen:])]
#        sg         = p4fns.rolling_sstdd(error, mwindow)
#        mlen       = len(sg)
#        predict    = predict[-mlen:]
#        timestamp  = [row[PQS['TIMESTAMP']] for row in eqsdb[-mlen:]]
#        mudict     = {timestamp[i]:predict[i] for i in range(mlen)}
#        sgdict     = {timestamp[i]:sg[i] for i in range(mlen)}
#        for i in range(0, dsize):
#            table[i].append(mudict[table[i][0]] if table[i][0] in mudict else '')
#            table[i].append(sgdict[table[i][0]] if table[i][0] in sgdict else '')
#
    # Regression with NIFTY
    # ---------------------------------------------- #
    rwindow        = 252
    mwindow        = 94
    close          = [float(row[PQS['CLOSE']]) for row in eqsdb]
    pvwap          = [math.log(float(row[PQS['VWAP']])) for row in eqsdb]
    if (eqsize>=rwindow+mwindow+40):
        title      = ['TIMESTAMP','CLOSE','MEAN','SIGMA']
        reffdb     = p4fns.read_csv(NSEIXSDBDIR+'NIFTY'+CSV)[-eqsize:]
        pvwapR     = [math.log(float(row[PXS['CLOSE']])) for row in reffdb]
        regr       = p4fns.rolling_regress(pvwap[-eqsize:], pvwapR[-eqsize:], rwindow)
        predict    = [round(math.exp(x),2) for x in regr]
        mu         = p4fns.rolling_smean(predict, mwindow)
        rlen       = len(predict)
        error      = [round((a - b), 2) for a, b in zip(close[-rlen:], predict[-rlen:])]
        sg         = p4fns.rolling_sstdd(error, mwindow)
        mu         = mu[-dsize:]
        sg         = sg[-dsize:]
        eqdata     = eqsdb[-dsize:]
        table      = []
        for i in range(0, dsize):
            srow   = []
            srow.append(eqdata[i][PQS['TIMESTAMP']])
            srow.append(eqdata[i][PQS['CLOSE']])
            srow.append(mu[i])
            srow.append(sg[i])
            table.append(srow)

    p4fns.write_csv(NSEDIR+'TECHNICAL/CRR/'+symbol+'_NIFTY'+CSV, [title]+table, 'w')

# Correlelation between pairs of stocks
# =================================================== ##
#for symbol in cnxlist:
#
#    eqsdb          = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)
#    symclose       = [float(row[PQS['CLOSE']]) for row in eqsdb]
#    eqsize         = len(eqsdb)
#    title          = ['SYMBOL', 'CORR126']
#    table          = []
#
#    for pair in [x for x in cnxlist if x != symbol]:
#        pairsdb    = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+pair+CSV), PQS, 'SERIES', REGEQSERIES)
#        pairclose  = [float(row[PQS['CLOSE']]) for row in pairsdb]
#        pairsize   = len(pairsdb)
#        dsize      = min(pairsize, eqsize, 756)
#        window     = 126
#        interval   = 21
#        corr       = p4fns.mean_corr(symclose[-dsize:], pairclose[-dsize:], window, interval)
#        table.append([pair, corr])
#
#    table.sort(key=lambda x: x[1], reverse=True)
#    p4fns.write_csv(NSEDIR+'TECHNICAL/CORR/'+symbol+CSV, [title]+table, 'w')
