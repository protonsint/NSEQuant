#!/usr/bin/env python
# Usage ./nseeqdb.py 01-Jan-2010

from   p4defs            import *
import p4fns
import sys
import dateutil.parser   as     dp
import os.path as path
import math

## ============================================================================================= ##
## Date for which database is to be built                                                        ##
## ============================================================================================= ##
tgtdate            = dp.parse(str(sys.argv[1]),dayfirst=True)
timestamp          = tgtdate.strftime('%Y-%m-%d')

raweqfile          = NSEEQRAWDIR+timestamp+CSV

## ============================================================================================= ##
## NSE Temporal Equity DB
## ============================================================================================= ##

## Append the days values to the Temporal EQUITY DB
## ============================================================================================= ##
raweqdf            = p4fns.read_csv(raweqfile) 
eqdf               = []
for rrow in raweqdf:
    if rrow[PQR['SERIES']] in VALEQSERIES:
        trow                   = ['']*len(PQT)
        trow[PQT['TIMESTAMP']] = timestamp
        trow[PQT['ISIN']]      = rrow[PQR['ISIN']]
        trow[PQT['SYMBOL']]    = rrow[PQR['SYMBOL']]
        trow[PQT['SERIES']]    = rrow[PQR['SERIES']]
        trow[PQT['OPEN_U']]    = rrow[PQR['OPEN_U']]
        trow[PQT['HIGH_U']]    = rrow[PQR['HIGH_U']]
        trow[PQT['LOW_U']]     = rrow[PQR['LOW_U']]
        trow[PQT['CLOSE_U']]   = rrow[PQR['CLOSE_U']]
        trow[PQT['LAST_U']]    = rrow[PQR['LAST_U']]
        trow[PQT['PREV_U']]    = rrow[PQR['PREV_U']]
        trow[PQT['VOLUME']]    = rrow[PQR['VOLUME']]
        trow[PQT['TURNOVER']]  = rrow[PQR['TURNOVER']]
        trow[PQT['CONTRACTS']] = rrow[PQR['CONTRACTS']]
        eqdf.append(trow)
eqdlyis            = {row[PQT['SYMBOL']]:row[PQT['ISIN']] for row in eqdf}
eqdlysy            = {row[PQT['ISIN']]:row[PQT['SYMBOL']] for row in eqdf}
eqdlycp            = {row[PQT['SYMBOL']]:row[PQT['CLOSE_U']] for row in eqdf}

p4fns.write_csv(NSEEQTDBFILE, eqdf, 'a')

## Read the Catalog Files
## ============================================================================================= ##
eqc0df             = p4fns.read_csv(NSEEQCatalog) 
eqi0df             = p4fns.read_csv(NSEISINCatalog) 

## Update ISINCatalog with ISIN Changes
## ============================================================================================= ##
eqi1df             = []
for row in eqc0df:
    if row[PCAT['SYMBOL']] in set(eqdlyis.keys()): 
        if row[PCAT['ISIN']] != eqdlyis[row[PCAT['SYMBOL']]]:
            eqi1df.append([row[PCAT['ISIN']], eqdlyis[row[PCAT['SYMBOL']]], timestamp])
eqisdict           = {row[PISN['OLDISIN']]:row[PISN['ISIN']] for row in eqi1df}

p4fns.write_csv(NSEISINCatalog, eqi1df, 'a')

## Update SCHCatalog with Symbol Changes
## ============================================================================================= ##
eqschdf            = []
for row in eqc0df:
    if row[PCAT['ISIN']] in set(eqdlysy.keys()): 
        if row[PCAT['SYMBOL']] != eqdlysy[row[PCAT['ISIN']]]:
            eqschdf.append([row[PCAT['SYMBOL']], eqdlysy[row[PCAT['ISIN']]], timestamp])
eqschdict          = {row[PSCH['OLDSYMBOL']]:row[PSCH['SYMBOL']] for row in eqschdf}

p4fns.write_csv(NSESCHCatalog, eqschdf, 'a')

## ============================================================================================= ##
## Listing the Corporate Actions that are valid for the target date
## ============================================================================================= ##
## BONUS
## ============================================================================================= ##
bonus0df           = p4fns.read_csv(NSEBONUS) 
bonus0df           = p4fns.symchange(bonus0df, PBON['SYMBOL'], eqschdict)
bonusdf            = []
bonus1df           = p4fns.readhdr_csv(NSEBONUS) 
for row in bonus0df:
    exdate         = dp.parse(row[PBON['EXDATE']])
    symbol         = row[PBON['SYMBOL']]
    done           = row[PBON['DONE']]
    if (exdate<=tgtdate) and (done=='F') and (symbol in list(eqdlyis.keys())):
        bonusdf.append(row)
        row[PBON['DONE']] = 'T'
    bonus1df.append(row)
p4fns.write_csv(NSEBONUS, bonus1df, 'w')
#p4fns.write_sql(NSEULDB, SQLNSEBONUS, bonus1df, MBON, BONUSCOL)
bondict            = {row[PBON['SYMBOL']]:row[PBON['RATIO']] for row in bonusdf}
bontdict           = {row[PBON['SYMBOL']]:row[PBON['EXDATE']] for row in bonusdf}
bonlist            = list(bondict.keys())

## SPLIT
## ============================================================================================= ##
split0df           = p4fns.read_csv(NSESPLIT) 
split0df           = p4fns.symchange(split0df, PSPL['SYMBOL'], eqschdict)
splitdf            = []
split1df           = p4fns.readhdr_csv(NSESPLIT) 
for row in split0df:
    exdate         = dp.parse(row[PSPL['EXDATE']])
    symbol         = row[PSPL['SYMBOL']]
    done           = row[PSPL['DONE']]
    if (exdate<=tgtdate) and (done=='F') and (symbol in list(eqdlyis.keys())):
        splitdf.append(row)
        row[PSPL['DONE']] = 'T'
    split1df.append(row)
p4fns.write_csv(NSESPLIT, split1df, 'w')
#p4fns.write_sql(NSEULDB, SQLNSESPLIT, split1df, MSPL, SPLITCOL)
spldict            = {row[PSPL['SYMBOL']]:row[PSPL['RATIO']] for row in splitdf}
spltdict           = {row[PSPL['SYMBOL']]:row[PSPL['EXDATE']] for row in splitdf}
spllist            = list(spldict.keys())

## RIGHTS ISSUE
## ============================================================================================= ##
right0df           = p4fns.read_csv(NSERIGHT) 
right0df           = p4fns.symchange(right0df, PRGT['SYMBOL'], eqschdict)
rightdf            = []
right1df           = p4fns.readhdr_csv(NSERIGHT) 
for row in right0df:
    exdate         = dp.parse(row[PRGT['EXDATE']])
    symbol         = row[PRGT['SYMBOL']]
    done           = row[PRGT['DONE']]
    if (exdate<=tgtdate) and (done=='F') and (symbol in list(eqdlyis.keys())):
        rightdf.append(row)
        row[PRGT['DONE']] = 'T'
    right1df.append(row)
p4fns.write_csv(NSERIGHT, right1df, 'w')
#p4fns.write_sql(NSEULDB, SQLNSERIGHT, right1df, MRGT, RIGHTCOL)
rgtdict            = {row[PRGT['SYMBOL']]:row[PRGT['RATIO']] for row in rightdf}
rgtissue           = {row[PRGT['SYMBOL']]:row[PRGT['ISSUEPR']] for row in rightdf}
rgttdict           = {row[PRGT['SYMBOL']]:row[PRGT['EXDATE']] for row in rightdf}
rgtlist            = list(rgtdict.keys())
rgtprev            = {}

## ============================================================================================= ##
## Updating Temporal DB with Bonus / Split Info
## ============================================================================================= ##
## Generate the Adjustment Factors and the Adjusted Prices for SDB
## ============================================================================================= ##
eqdfsdb            = []
for trow in eqdf:
    symbol                 = trow[PQT['SYMBOL']]
    srow                   = ['']*len(PQS)
    srow[PQS['TIMESTAMP']] = trow[PQT['TIMESTAMP']]
    srow[PQS['ISIN']]      = trow[PQT['ISIN']]
    srow[PQS['SYMBOL']]    = trow[PQT['SYMBOL']]
    srow[PQS['SERIES']]    = trow[PQT['SERIES']]
    srow[PQS['OPEN_U']]    = trow[PQT['OPEN_U']]
    srow[PQS['HIGH_U']]    = trow[PQT['HIGH_U']]
    srow[PQS['LOW_U']]     = trow[PQT['LOW_U']]
    srow[PQS['CLOSE_U']]   = trow[PQT['CLOSE_U']]
    srow[PQS['LAST_U']]    = trow[PQT['LAST_U']]
    srow[PQS['PREV_U']]    = trow[PQT['PREV_U']]
    srow[PQS['VOLUME']]    = trow[PQT['VOLUME']]
    srow[PQS['TURNOVER']]  = trow[PQT['TURNOVER']]
    srow[PQS['CONTRACTS']] = trow[PQT['CONTRACTS']]
    srow[PQS['FACTOR']]    = str(1)
    srow[PQS['VWAP_U']]    = "%.2f" %(float(trow[PQT['TURNOVER']])/float(trow[PQT['VOLUME']]))
    srow[PQS['OPEN']]      = trow[PQT['OPEN_U']] 
    srow[PQS['HIGH']]      = trow[PQT['HIGH_U']] 
    srow[PQS['LOW']]       = trow[PQT['LOW_U']]  
    srow[PQS['CLOSE']]     = trow[PQT['CLOSE_U']]
    srow[PQS['VWAP']]      = srow[PQS['VWAP_U']] 
    srow[PQS['PREV']]      = trow[PQT['PREV_U']] 
    if symbol in bonlist:
        srow[PQS['PREV']]  = "%.2f" %(float(srow[PQS['PREV']])/float(bondict[symbol])) 
    if symbol in spllist:
        srow[PQS['PREV']]  = "%.2f" %(float(srow[PQS['PREV']])/float(spldict[symbol]))
    if symbol in rgtlist:
        rgtprev[symbol]    = trow[PQT['PREV_U']]
        adjmult            = float(rgtprev[symbol])*(1+float(rgtdict[symbol]))/\
                             (float(rgtissue[symbol])+float(rgtprev[symbol])*float(rgtdict[symbol]))
        srow[PQS['PREV']]  = "%.2f" %(float(srow[PQS['PREV']])/float(adjmult))
    srow[PQS['GAIN']]      = "%.4f" %(math.log(float(srow[PQS['CLOSE']])/float(srow[PQS['PREV']]))*100) 
    eqdfsdb.append(srow)

## ============================================================================================= ##
## Updating Catalog Files
## ============================================================================================= ##
## Read the EQUITY List File for Stock Information
## ============================================================================================= ##
eqltdf             = p4fns.read_csv(NSEREQLIST) 

eqnamdict          = {}
eqlisdict          = {}
eqpyddict          = {}
eqlotdict          = {}
eqfacdict          = {}
for row in eqltdf:
    if row[PRQL['SERIES']] in REGEQSERIES:
        eqnamdict[row[PRQL['ISIN']]]   = row[PRQL['NAME']]
        eqlisdict[row[PRQL['ISIN']]]   = (dp.parse(row[PRQL['LISTING_DATE']], dayfirst=True)).strftime('%Y-%m-%d')
        eqpyddict[row[PRQL['ISIN']]]   = row[PRQL['PAID_UP_VALUE']]
        eqlotdict[row[PRQL['ISIN']]]   = row[PRQL['MARKET_LOT']]
        eqfacdict[row[PRQL['ISIN']]]   = row[PRQL['FACEVALUE']]

## Update EQCatalog with ISIN and Symbol Changes
## ============================================================================================= ##
eqc1df             = p4fns.readhdr_csv(NSEEQCatalog) 
eqc1isin           = []
for row in eqc0df:
    if row[PCAT['ISIN']] in set(eqisdict.keys()): 
        row[PCAT['ISIN']]              = eqisdict[row[PCAT['ISIN']]]
    if row[PCAT['SYMBOL']] in set(eqschdict.keys()):
        row[PCAT['SYMBOL']]            = eqschdict[row[PCAT['SYMBOL']]]
    if row[PCAT['ISIN']] in set(eqnamdict.keys()): 
        row[PCAT['NAME']]              = eqnamdict[row[PCAT['ISIN']]]
        row[PCAT['LISTING_DATE']]      = eqlisdict[row[PCAT['ISIN']]]
        row[PCAT['PAID_UP_VALUE']]     = eqpyddict[row[PCAT['ISIN']]]
        row[PCAT['MARKET_LOT']]        = eqlotdict[row[PCAT['ISIN']]]
        row[PCAT['FACEVALUE']]         = eqfacdict[row[PCAT['ISIN']]]
    symbol         = row[PCAT['SYMBOL']]
    if (row[PCAT['SHARES']]):
        if symbol in bonlist:
            row[PCAT['SHARES']]  = "%.2f" %(float(row[PCAT['SHARES']])*float(bondict[symbol])) 
        if symbol in spllist:
            row[PCAT['SHARES']]  = "%.2f" %(float(row[PCAT['SHARES']])*float(spldict[symbol])) 
        if symbol in rgtlist:
            adjmult              = float(rgtprev[symbol])*(1+float(rgtdict[symbol]))/\
                                   (float(rgtissue[symbol])+float(rgtprev[symbol])*float(rgtdict[symbol]))
            row[PCAT['SHARES']]  = "%.2f" %(float(row[PCAT['SHARES']])*float(adjmult)) 
        if row[PCAT['SYMBOL']] in set(eqdlycp.keys()):
            row[PCAT['MKT_CAP']] = "%.0f" %(float(row[PCAT['SHARES']])*float(eqdlycp[symbol])/100) 
    eqc1df.append(row)
    eqc1isin.append(row[PCAT['ISIN']])

for newisin in set(eqdlysy.keys()): 
    if newisin not in eqc1isin:
        if newisin in set(eqnamdict.keys()): 
            eqc1df.append([newisin, eqdlysy[newisin], eqnamdict[newisin], eqlisdict[newisin],\
                           eqpyddict[newisin], eqlotdict[newisin], eqfacdict[newisin], '', '', '', ''])
        else:
            eqc1df.append([newisin, eqdlysy[newisin], '', '', '', '', '', '', '', '', ''])
        eqc1isin.append(newisin)
eqc1list           = [row[PCAT['SYMBOL']] for row in eqc1df if row[PCAT['ISIN']] in eqc1isin]

p4fns.write_csv(NSEEQCatalog, eqc1df, 'w')
#p4fns.write_sql(NSEULDB, SQLEQCatalog, eqc1df, MCAT, EQCATCOL)

## ============================================================================================= ##
## NSE Nominal Equity DB
## ============================================================================================= ##
## In case of SYMBOL Change copy the Prev SYMBOL File to the new one
## ============================================================================================= ##
for oldsymbol in set(eqschdict.keys()): 
    newsymbol      = eqschdict[oldsymbol]
    sdbdf          = p4fns.readall_csv(NSEEQSDBDIR+oldsymbol+CSV) 
    p4fns.write_csv(NSEEQSDBDIR+newsymbol+CSV, sdbdf, 'w')
#    p4fns.write_sql(NSEULDB, newsymbol, sdbdf, MQS, SYEQCOL)

## Adjust for Corporate Actions in the Nominal EQUITY DB
## ============================================================================================= ##
## BONUS
## ============================================================================================= ##
for symbol in bonlist:
    bontime            = dp.parse(bontdict[symbol])
    if symbol in eqc1list:
        nomecsv        = NSEEQSDBDIR+symbol+CSV
        if path.isfile(nomecsv):
             eqn0df    = p4fns.read_csv(nomecsv) 
             eqn1df    = p4fns.readhdr_csv(nomecsv) 
             for row in eqn0df:
                 rowtime                   = dp.parse(row[PQS['TIMESTAMP']])
                 if (rowtime<bontime):
                     row[PQS['FACTOR']]    = "%.4f" %(float(row[PQS['FACTOR']])*float(bondict[symbol]))
                     row[PQS['OPEN']]      = "%.2f" %(float(row[PQS['OPEN_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['HIGH']]      = "%.2f" %(float(row[PQS['HIGH_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['LOW']]       = "%.2f" %(float(row[PQS['LOW_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['CLOSE']]     = "%.2f" %(float(row[PQS['CLOSE_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['VWAP']]      = "%.2f" %(float(row[PQS['VWAP_U']])/float(row[PQS['FACTOR']]))
                 eqn1df.append(row)
             p4fns.write_csv(nomecsv, eqn1df, 'w')
#             p4fns.write_sql(NSEULDB, symbol, eqn1df, MQS, SYEQCOL)
## SPLIT
## ============================================================================================= ##
for symbol in spllist:
    spltime            = dp.parse(spltdict[symbol])
    if symbol in eqc1list:
        nomecsv        = NSEEQSDBDIR+symbol+CSV
        if path.isfile(nomecsv):
             eqn0df    = p4fns.read_csv(nomecsv) 
             eqn1df    = p4fns.readhdr_csv(nomecsv) 
             for row in eqn0df:
                 rowtime                   = dp.parse(row[PQS['TIMESTAMP']])
                 if (rowtime<spltime):
                     row[PQS['FACTOR']]    = "%.4f" %(float(row[PQS['FACTOR']])*float(spldict[symbol]))
                     row[PQS['OPEN']]      = "%.2f" %(float(row[PQS['OPEN_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['HIGH']]      = "%.2f" %(float(row[PQS['HIGH_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['LOW']]       = "%.2f" %(float(row[PQS['LOW_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['CLOSE']]     = "%.2f" %(float(row[PQS['CLOSE_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['VWAP']]      = "%.2f" %(float(row[PQS['VWAP_U']])/float(row[PQS['FACTOR']]))
                 eqn1df.append(row)
             p4fns.write_csv(nomecsv, eqn1df, 'w')
#             p4fns.write_sql(NSEULDB, symbol, eqn1df, MQS, SYEQCOL)
## RIGHTS ISSUE
## ============================================================================================= ##
for symbol in rgtlist:
    rgttime            = dp.parse(rgttdict[symbol])
    if symbol in eqc1list:
        nomecsv        = NSEEQSDBDIR+symbol+CSV
        if path.isfile(nomecsv):
             eqn0df    = p4fns.read_csv(nomecsv) 
             eqn1df    = p4fns.readhdr_csv(nomecsv) 
             for row in eqn0df:
                 rowtime                   = dp.parse(row[PQS['TIMESTAMP']])
                 if (rowtime<rgttime):
                     adjmult               = float(rgtprev[symbol])*(1+float(rgtdict[symbol]))/\
                                             (float(rgtissue[symbol])+float(rgtprev[symbol])*float(rgtdict[symbol]))
                     row[PQS['FACTOR']]    = "%.4f" %(float(row[PQS['FACTOR']])*float(adjmult))
                     row[PQS['OPEN']]      = "%.2f" %(float(row[PQS['OPEN_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['HIGH']]      = "%.2f" %(float(row[PQS['HIGH_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['LOW']]       = "%.2f" %(float(row[PQS['LOW_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['CLOSE']]     = "%.2f" %(float(row[PQS['CLOSE_U']])/float(row[PQS['FACTOR']]))
                     row[PQS['VWAP']]      = "%.2f" %(float(row[PQS['VWAP_U']])/float(row[PQS['FACTOR']]))
                 eqn1df.append(row)
             p4fns.write_csv(nomecsv, eqn1df, 'w')
#             p4fns.write_sql(NSEULDB, symbol, eqn1df, MQS, SYEQCOL)

## Append the days values to the Nominal EQUITY DB
## ============================================================================================= ##
for symbol in eqc1list:
    sdbdf          = []
    sdbcsv         = NSEEQSDBDIR+symbol+CSV
    if not path.isfile(sdbcsv):
        sdbdf.append(SYEQCOL)
        for row in eqdfsdb:
            if (row[PQS['SYMBOL']]==symbol):
                sdbdf.append(row)
        p4fns.write_csv(sdbcsv, sdbdf, 'w')
#        p4fns.write_sql(NSEULDB, symbol, sdbdf, MQS, SYEQCOL)
    else:
        for row in eqdfsdb:
            if (row[PQS['SYMBOL']]==symbol):
                sdbdf.append(row)
        p4fns.write_csv(sdbcsv, sdbdf, 'a')
#        p4fns.append_sql(NSEULDB, symbol, sdbdf, MQS, SYEQCOL)
