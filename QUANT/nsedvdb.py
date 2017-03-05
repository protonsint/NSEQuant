#!/usr/bin/env python
# Usage ./nsedvdb.py 01-Jan-2010

from   p4defs            import *
import p4fns
import sys
import dateutil.parser   as     dp
import os.path as path

## ============================================================================================= ##
## Date for which database is to be built                                                        ##
## ============================================================================================= ##
tgtdate            = dp.parse(str(sys.argv[1]),dayfirst=True)
timestamp          = tgtdate.strftime('%Y-%m-%d')

rawdvfile          = NSEDVRAWDIR+timestamp+CSV

## ============================================================================================= ##
## NSE Temporal Deriv DB
## ============================================================================================= ##

## Append the days values to the Temporal DERIV DB
## ============================================================================================= ##
rawdvdf            = p4fns.read_csv(rawdvfile) 
dvdf               = []
for rrow in rawdvdf:
    if (rrow[PDR['CONTRACTS']] != '0'):
        trow                       = ['']*len(PDT)
        trow[PDT['TIMESTAMP']]     = timestamp
        trow[PDT['INSTRUMENT']]    = rrow[PDR['INSTRUMENT']]
        trow[PDT['SYMBOL']]        = rrow[PDR['SYMBOL']]
        trow[PDT['EXPIRY_DT']]     = dp.parse(rrow[PDR['EXPIRY_DT']],dayfirst=True).strftime('%Y-%m-%d')
        trow[PDT['STRIKE_PR']]     = rrow[PDR['STRIKE_PR']]
        trow[PDT['OPTION_TYP']]    = rrow[PDR['OPTION_TYP']]
        trow[PDT['OPEN']]          = rrow[PDR['OPEN']]
        trow[PDT['HIGH']]          = rrow[PDR['HIGH']]
        trow[PDT['LOW']]           = rrow[PDR['LOW']]
        trow[PDT['CLOSE']]         = rrow[PDR['CLOSE']]
        trow[PDT['SETTLE_PR']]     = rrow[PDR['SETTLE_PR']]
        trow[PDT['CONTRACTS']]     = rrow[PDR['CONTRACTS']]
        trow[PDT['VAL_INLAKH']]    = rrow[PDR['VAL_INLAKH']]
        trow[PDT['OPEN_INT']]      = rrow[PDR['OPEN_INT']]
        trow[PDT['CHG_IN_OI']]     = rrow[PDR['CHG_IN_OI']]
        dvdf.append(trow)

p4fns.write_csv(NSEDVTDBFILE, dvdf, 'a')

## ============================================================================================= ##
## NSE Nominal Deriv DB
## ============================================================================================= ##
ixc0df             = p4fns.read_csv(NSEIXCatalog) 
ixclist            = [row[PXC['SYMBOL']] for row in ixc0df]
eqc0df             = p4fns.read_csv(NSEEQCatalog) 
eqclist            = [row[PCAT['SYMBOL']] for row in eqc0df]

## Append the days values to the Nominal DERIV DB
## ============================================================================================= ##
dvdfsdb            = []
dvlist             = []
for trow in dvdf:
    srow                           = ['']*len(PDS)
    srow[PDS['TIMESTAMP']]         = trow[PDT['TIMESTAMP']]
    srow[PDS['INSTRUMENT']]        = trow[PDT['INSTRUMENT']]
    srow[PDS['SYMBOL']]            = trow[PDT['SYMBOL']]
    srow[PDS['EXPIRY_DT']]         = trow[PDT['EXPIRY_DT']]
    srow[PDS['STRIKE_PR']]         = trow[PDT['STRIKE_PR']]
    srow[PDS['OPTION_TYP']]        = trow[PDT['OPTION_TYP']]
    srow[PDS['OPEN']]              = trow[PDT['OPEN']]
    srow[PDS['HIGH']]              = trow[PDT['HIGH']]
    srow[PDS['LOW']]               = trow[PDT['LOW']]
    srow[PDS['CLOSE']]             = trow[PDT['CLOSE']]
    srow[PDS['SETTLE_PR']]         = trow[PDT['SETTLE_PR']]
    srow[PDS['CONTRACTS']]         = trow[PDT['CONTRACTS']]
    srow[PDS['VAL_INLAKH']]        = trow[PDT['VAL_INLAKH']]
    srow[PDS['OPEN_INT']]          = trow[PDT['OPEN_INT']]
    srow[PDS['CHG_IN_OI']]         = trow[PDT['CHG_IN_OI']]

## Generate List of symbols
## ============================================================================================= ##
    symbol                         = trow[PDT['SYMBOL']]
    if (symbol not in dvlist):
        dvlist.append(symbol)

## Calculate Time to Expiry
## ============================================================================================= ##
    srow[PDS['T2E']]               = (dp.parse(trow[PDT['EXPIRY_DT']])-dp.parse(trow[PDT['TIMESTAMP']])).days

## Calculate Implied Volatility
## ============================================================================================= ##
    instrument                     = trow[PDT['INSTRUMENT']]
    strikepr                       = float(trow[PDT['STRIKE_PR']])
    optyp                          = trow[PDT['OPTION_TYP']]
    expirydt                       = trow[PDT['EXPIRY_DT']]
    opprice                        = float(trow[PDT['CLOSE']])
    days2exp                       = srow[PDS['T2E']]
    if (instrument == 'OPTSTK') and (symbol in eqclist):
        ulprice                    = float(p4fns.filterdf(p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV),\
                                     PQS, 'SERIES', REGEQSERIES), PQS, 'TIMESTAMP', [timestamp])[-1][PQS['CLOSE']])
        impvol                     = p4fns.ivcalc(optyp, ulprice, strikepr, opprice, days2exp)
    elif (instrument == 'OPTIDX') and (symbol in ixclist):
        ulprice                    = float(p4fns.filterdf(p4fns.read_csv(NSEIXSDBDIR+symbol+CSV),\
                                     PXS, 'TIMESTAMP', [timestamp])[-1][PXS['CLOSE']])
        impvol                     = p4fns.ivcalc(optyp, ulprice, strikepr, opprice, days2exp)
    else:
        impvol                     = 0
    srow[PDS['IV']]                = impvol

## Calculate Option Distance
## ============================================================================================= ##
    if ((instrument == 'OPTSTK') and (symbol in eqclist)) or \
       ((instrument == 'OPTIDX') and (symbol in ixclist)):
        subdf                      = []
        for xrow in dvdf:
            if (xrow[PDT['INSTRUMENT']]==instrument) and (xrow[PDT['SYMBOL']]==symbol) and \
               (xrow[PDT['EXPIRY_DT']]==expirydt) and (xrow[PDT['OPTION_TYP']]==optyp):
                subdf.append(float(xrow[PDT['STRIKE_PR']]))
        if (optyp=='CE') or (optyp=='CA'):
            if (ulprice <= strikepr):
                opdist             = 'OTM'+str(sum(1 for i in subdf if (i >= ulprice) and (i < strikepr)))
            else:
                opdist             = 'ITM'+str(sum(1 for i in subdf if (i < ulprice) and (i >= strikepr)))
        else:
            if (ulprice >= strikepr):
                opdist             = 'OTM'+str(sum(1 for i in subdf if (i <= ulprice) and (i > strikepr)))
            else:
                opdist             = 'ITM'+str(sum(1 for i in subdf if (i > ulprice) and (i <= strikepr)))
    else:
        opdist                     = 'NA'
    srow[PDS['OPDIST']]            = opdist

    dvdfsdb.append(srow)

## In case of SYMBOL Change copy the Prev SYMBOL File to the new one
## ============================================================================================= ##
eqschdf            = p4fns.read_csv(NSESCHCatalog)
eqschdict          = {row[PSCH['OLDSYMBOL']]:row[PSCH['SYMBOL']] for row in eqschdf}
for oldsymbol in set(eqschdict.keys()): 
    oldcsv         = NSEDVSDBDIR+oldsymbol+CSV
    if path.isfile(oldcsv):
         newsymbol      = eqschdict[oldsymbol]
         newcsv         = NSEDVSDBDIR+newsymbol+CSV
         if not path.isfile(newcsv):
             sdbdf      = p4fns.readall_csv(oldcsv) 
             p4fns.write_csv(newcsv, sdbdf, 'w')

## Append the days values to the Nominal DERIV DB
## ============================================================================================= ##
for symbol in dvlist:
    sdbdf          = []
    sdbcsv         = NSEDVSDBDIR+symbol+CSV
    if not path.isfile(sdbcsv):
        sdbdf.append(SYDVCOL)
        for row in dvdfsdb:
            if (row[PDS['SYMBOL']]==symbol):
                sdbdf.append(row)
        p4fns.write_csv(sdbcsv, sdbdf, 'w')
    else:
        for row in dvdfsdb:
            if (row[PDS['SYMBOL']]==symbol):
                sdbdf.append(row)
        p4fns.write_csv(sdbcsv, sdbdf, 'a')
