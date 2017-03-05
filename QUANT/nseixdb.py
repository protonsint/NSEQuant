#!/usr/bin/env python
# Usage ./nseixdb.py

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

rawixfile          = NSEIXRAWDIR+timestamp+CSV

## ============================================================================================= ##
## NSE Index DB                                                                                  ##
## ============================================================================================= ##

## Read the Catalog Files
## ============================================================================================= ##
ixc0df             = p4fns.read_csv(NSEIXCatalog) 
ixc0dict           = {row[PXC['NAME']]:row[PXC['SYMBOL']] for row in ixc0df}
ixclist            = list(ixc0dict.keys())

## Append the days values to the Temporal Index DB
## ============================================================================================= ##
rawixdf            = p4fns.read_csv(rawixfile) 
ixdf               = []
for rrow in rawixdf:
    trow                       = ['']*len(PXT)
    name                       = rrow[PXR['NAME']]
    if name in ixclist:
        trow[PXT['TIMESTAMP']] = timestamp
        trow[PXT['SYMBOL']]    = ixc0dict[rrow[PXR['NAME']]]
        trow[PXT['OPEN']]      = rrow[PXR['OPEN']] if (rrow[PXR['OPEN']] != '-') else ''
        trow[PXT['HIGH']]      = rrow[PXR['HIGH']] if (rrow[PXR['HIGH']] != '-') else ''
        trow[PXT['LOW']]       = rrow[PXR['LOW']] if (rrow[PXR['LOW']] != '-') else ''
        trow[PXT['CLOSE']]     = rrow[PXR['CLOSE']] if (rrow[PXR['CLOSE']] != '-') else ''
        trow[PXT['PREV']]      = "%.2f" %(float(rrow[PXR['CLOSE']])-float(rrow[PXR['CHANGE']]))
        trow[PXT['GAIN']]      = "%.4f" %(math.log(float(rrow[PXR['CLOSE']])/float(trow[PXT['PREV']]))*100) 
        trow[PXT['VOLUME']]    = rrow[PXR['VOLUME']] if (rrow[PXR['VOLUME']] != '-') else ''
        trow[PXT['TURNOVER']]  = rrow[PXR['TURNOVER']] if (rrow[PXR['TURNOVER']] != '-') else ''
        trow[PXT['PE']]        = rrow[PXR['PE']] if (rrow[PXR['PE']] != '-') else ''
        trow[PXT['PB']]        = rrow[PXR['PB']] if (rrow[PXR['PB']] != '-') else ''
        trow[PXT['DIVYIELD']]  = rrow[PXR['DIVYIELD']] if (rrow[PXR['DIVYIELD']] != '-') else ''
        ixdf.append(trow)

p4fns.write_csv(NSEIXTDBFILE, ixdf, 'a')

## Append the days values to the Nominal Index DB
## ============================================================================================= ##
for name in ixclist:
    symbol         = ixc0dict[name]
    sdbdf          = []
    sdbcsv         = NSEIXSDBDIR+symbol+CSV
    newdb          = False
    if not path.isfile(sdbcsv):
        sdbdf.append(SYIXCOL)
        newdb      = True
    for trow in ixdf:
        if (trow[PXT['SYMBOL']]==symbol):
            srow                   = ['']*len(PXS)
            srow[PXS['TIMESTAMP']] = trow[PXT['TIMESTAMP']]
            srow[PXS['OPEN']]      = trow[PXT['OPEN']]
            srow[PXS['HIGH']]      = trow[PXT['HIGH']]
            srow[PXS['LOW']]       = trow[PXT['LOW']]
            srow[PXS['CLOSE']]     = trow[PXT['CLOSE']]
            srow[PXS['PREV']]      = trow[PXT['PREV']]
            srow[PXS['GAIN']]      = trow[PXT['GAIN']]
            srow[PXS['VOLUME']]    = trow[PXT['VOLUME']]
            srow[PXS['TURNOVER']]  = trow[PXT['TURNOVER']]
            srow[PXS['PE']]        = trow[PXT['PE']]
            srow[PXS['PB']]        = trow[PXT['PB']]
            srow[PXS['DIVYIELD']]  = trow[PXT['DIVYIELD']]
            sdbdf.append(srow)
    if (newdb==True):
        p4fns.write_csv(sdbcsv, sdbdf, 'w')
#        p4fns.write_sql(NSEULDB, symbol, sdbdf, MXS, SYIXCOL)
    else:
        p4fns.write_csv(sdbcsv, sdbdf, 'a')
#        p4fns.append_sql(NSEULDB, symbol, sdbdf, MXS, SYIXCOL)

## Create the Fixed fund database
## ============================================================================================= ##
datelist           = [row[PXS['TIMESTAMP']] for row in p4fns.read_csv(NSEIXSDBDIR+'NIFTY'+CSV)]
prev               = 1000
startdate          = '1990-07-02'
outdb              = []
for timestamp in datelist:
    duration       = (dp.parse(timestamp)-dp.parse(startdate)).days
#    gain           = 4.8794/36500*duration
    gain           = 7.6969/36500*duration
    close          = (1+gain)*prev
    price          = round(close,2)
    startdate      = timestamp
    lngain         = math.log(close/prev)
    row            = [startdate,price,price,price,price,round(prev,2),round(lngain*100,4)]
    prev           = close
    outdb.append(row)
outdb              = [['TIMESTAMP','OPEN','HIGH','LOW','CLOSE','PREV','GAIN']]+outdb
p4fns.write_csv(NSEIXSDBDIR+'EIGHTFD'+CSV, outdb, 'w')
