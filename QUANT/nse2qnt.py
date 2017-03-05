#!/usr/bin/env python
from   p4defs            import *
import p4fns
import q4fns
import json

cnx500             = p4fns.read_csv(NSEEQDIR+'CNX500.csv') 
cnxlist            = [row[PXL['SYMBOL']] for row in cnx500]
ixclist            = ['NIFTY','BANKNIFTY']
catalog            = p4fns.read_csv(NSEEQCatalog) 
eqnamdict          = {}
eqsecdict          = {}
eqinddict          = {}
eqmkcdict          = {}
eqmkclist          = []
for row in catalog:
    eqnamdict[row[PCAT['SYMBOL']]]   = row[PCAT['NAME']]
    eqsecdict[row[PCAT['SYMBOL']]]   = row[PCAT['SECTOR']]
    eqinddict[row[PCAT['SYMBOL']]]   = row[PCAT['INDUSTRY']]
    mktcap                           = float(row[PCAT['MKT_CAP']]) if row[PCAT['MKT_CAP']] else 0
    eqmkcdict[row[PCAT['SYMBOL']]]   = mktcap
    eqmkclist.append(mktcap)

donelist           = [row[0] for row in p4fns.read_csv(NSEQNTLOG)]
## ********************************************************************************************* ##
## Catalog 
## ********************************************************************************************* ##
if 'CATALOG' not in donelist:
    eqcatdf            = p4fns.read_csv(NSEEQCatalog) 
    catdf              = []
    for item in ixclist:
        catdf.append(item+' ['+item+']')
    fname = NSEJSONDIR+'NSEIXCatalog'+JSON
    with open(fname, 'w') as fjson:
        json.dump(catdf, fjson)
    
    catdf              = []
    for row in eqcatdf:
        if row[PCAT['SYMBOL']] in cnxlist:
             catdf.append(row[2]+' ['+row[1]+']')
    fname = NSEJSONDIR+'NSECatalog'+JSON
    with open(fname, 'w') as fjson:
        json.dump(catdf, fjson)

    p4fns.write_csv(NSEQNTLOG, [['CATALOG']], 'a')

## ********************************************************************************************* ##
## Daily Closing Data
## ********************************************************************************************* ##
#if 'DAILY' not in donelist:
#    for symbol in cnxlist:
#        q4fns.qntdaily(symbol)
#    p4fns.write_csv(NSEQNTLOG, [['DAILY']], 'a')

## ********************************************************************************************* ##
## General Information
## ********************************************************************************************* ##
if 'GENL' not in donelist:
    techhover      = ['Symbol','Company Name','Sector','Industry','Closing Price','% Change',\
                      'Market Capitalization (Rs Cr)','Volume (Rs Cr)','Volatility']
    techtitle      = ['Symbol','Name','Sector','Industry','Price','%','MC','TO','SG']
    p4fns.write_csv(NSETECHDIR+'NSEGenl'+CSV, [techhover]+[techtitle], 'w')
    for symbol in cnxlist:
        name           = eqnamdict[symbol]
        sector         = eqsecdict[symbol]
        industry       = eqinddict[symbol]
        mktcap         = p4fns.approxify(eqmkcdict[symbol], 2)
        mcpercent      = int(sum(i < mktcap for i in eqmkclist)*100/len(eqmkclist))
        q4fns.qntgenl(symbol, name, sector, industry, mktcap, mcpercent)
    p4fns.write_json(NSEJSONDIR+'NSEGenl'+JSON, p4fns.readall_csv(NSETECHDIR+'NSEGenl'+CSV), '')
    p4fns.write_csv(NSEQNTLOG, [['GENL']], 'a')
    
## ********************************************************************************************* ##
## Performance Information
## ********************************************************************************************* ##
if 'PERF' not in donelist:
    techhover      = ['Symbol','Company Name','1 Week Return','1 Month Return','3 Month Return',\
                      '6 Month Return','1 Year Return','2 Year Return','4 Year Return','1 Week Volatility',\
                      '1 Month Volatility','3 Month Volatility','6 Month Volatility','1 Year Volatility',\
                      '2 Year Volatility','4 Year Volatility']
    techtitle      = ['Symbol','Name','1W','1M','3M','6M','1Y','2Y','4Y',\
                     '1W','1M','3M','6M','1Y','2Y','4Y']
    p4fns.write_csv(NSETECHDIR+'NSEPerf'+CSV, [techhover]+[techtitle], 'w')
    for symbol in cnxlist:
        name           = eqnamdict[symbol]
        q4fns.qntperf(symbol, name)
    p4fns.write_json(NSEJSONDIR+'NSEPerf'+JSON, p4fns.readall_csv(NSETECHDIR+'NSEPerf'+CSV), '')
    p4fns.write_csv(NSEQNTLOG, [['PERF']], 'a')

## ********************************************************************************************* ##
## Performance Information
## ********************************************************************************************* ##
if 'TECH' not in donelist:
    techhover      = ['Symbol','Company Name','1 Month Price Band','3 Month Price Band','6 Month Price Band',\
                      '1 Year Price Band','1 Month Bollinger Band','3 Month Bollinger Band',\
                      '6 Month Bollinger Band','1 Year Bollinger Band']
    techtitle      = ['Symbol','Name','1M PB','3M PB','6M PB','1Y PB',\
                     '1M BB','3M BB','6M BB','1Y BB']
    p4fns.write_csv(NSETECHDIR+'NSETech'+CSV, [techhover]+[techtitle], 'w')
    for symbol in cnxlist:
        name           = eqnamdict[symbol]
        q4fns.qnttech(symbol, name)
    p4fns.write_json(NSEJSONDIR+'NSETech'+JSON, p4fns.readall_csv(NSETECHDIR+'NSETech'+CSV), '')
    p4fns.write_csv(NSEQNTLOG, [['TECH']], 'a')

## ********************************************************************************************* ##
### Best Candidates for Statistical Arbitrage for each (Sector, Industry)
## ********************************************************************************************* ##
if 'PAIR' not in donelist:
    eqvoldict      = {}
    for symbol in cnxlist:
        eqvoldict[symbol]  = p4fns.read_csv(NSEGENLDIR+symbol+CSV)[0][8]
    
    eqlendict      = {}
    for symbol in cnxlist:
        eqlendict[symbol]  = len(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV))
    deltaP         = 1.5
    deltaN         = 1.5
    period         = 252
    rwindow        = 252
    mwindow        = 94
    for symbol in cnxlist:
        categ      = (eqsecdict[symbol], eqinddict[symbol]) 
        sector     = eqsecdict[symbol]
        categstk   = {sym:eqmkcdict[sym] for sym in cnxlist if (eqsecdict[sym], eqinddict[sym])==categ and sym!=symbol and eqlendict[sym]>600}
        categlist  = sorted(categstk, key=categstk.get, reverse=True)[:10]
        categstk   = {sym:eqvoldict[sym] for sym in categlist}
        categlist  = sorted(categstk, key=categstk.get)[:5]
        sectstk    = {sym:eqmkcdict[sym] for sym in cnxlist if eqsecdict[sym]==sector and sym!=symbol and sym not in categstk and eqlendict[sym]>600}
        sectlist   = sorted(sectstk, key=sectstk.get, reverse=True)[:10]
        sectstk    = {sym:eqvoldict[sym] for sym in sectlist}
        sectlist   = sorted(sectstk, key=sectstk.get)[:10-len(categlist)]
        if (len(sectlist)+len(categlist)<10):
             sectlist.append('ITC')
        if (len(sectlist)+len(categlist)<10):
             sectlist.append('HINDUNILVR')
        if (len(sectlist)+len(categlist)<10):
             sectlist.append('DABUR')
        pairlist   = [item for item in categlist+sectlist]

        q4fns.qntpair(symbol, period, deltaP, deltaN, rwindow, mwindow, pairlist)
    p4fns.write_csv(NSEQNTLOG, [['PAIR']], 'a')

## ********************************************************************************************* ##
## Result effect
## ********************************************************************************************* ##
#if 'RESULT' not in donelist:
#    resdf          = p4fns.read_csv(NSERESULT)
#    for symbol in cnxlist:
#        q4fns.qntresult(symbol, resdf)
#    p4fns.write_csv(NSEQNTLOG, [['RESULT']], 'a')

## ********************************************************************************************* ##
## Event Catalog
## ********************************************************************************************* ##
#if 'EVENT' not in donelist:
#    past3m             = p4fns.read_csv(NSEIXSDBDIR+'NIFTY'+CSV)[-63][PXS['TIMESTAMP']]
#    today              = p4fns.read_csv(NSEIXSDBDIR+'NIFTY'+CSV)[-1][PXS['TIMESTAMP']]
#    bonusdf            = p4fns.filterts(p4fns.read_csv(NSEBONUS), PBON, 'EXDATE', past3m, 'GTE')
#    bonuspst           = p4fns.filterts(bonusdf, PBON, 'EXDATE', today, 'LTE')
#    bonusfut           = p4fns.filterts(bonusdf, PBON, 'EXDATE', today, 'GT')
#    splitdf            = p4fns.filterts(p4fns.read_csv(NSESPLIT), PSPL, 'EXDATE', past3m, 'GTE')
#    splitpst           = p4fns.filterts(splitdf, PSPL, 'EXDATE', today, 'LTE')
#    splitfut           = p4fns.filterts(splitdf, PSPL, 'EXDATE', today, 'GT')
#    rightdf            = p4fns.filterts(p4fns.read_csv(NSERIGHT), PRGT, 'EXDATE', past3m, 'GTE')
#    rightpst           = p4fns.filterts(rightdf, PRGT, 'EXDATE', today, 'LTE')
#    rightfut           = p4fns.filterts(rightdf, PRGT, 'EXDATE', today, 'GT')
#    divdndf            = p4fns.filterts(p4fns.read_csv(NSEDIVIDEND), PDIV, 'EXDATE', past3m, 'GTE')
#    divdnpst           = p4fns.filterts(divdndf, PDIV, 'EXDATE', today, 'LTE')
#    divdnfut           = p4fns.filterts(divdndf, PDIV, 'EXDATE', today, 'GT')
#    resltpst           = p4fns.filterts(p4fns.read_csv(NSERESULT), PRES, 'TIMESTAMP', past3m, 'GTE')
#    resltfut           = p4fns.filterts(p4fns.read_csv(NSEFBMEET), PFBM, 'TIMESTAMP', today, 'GT')
#    for symbol in cnxlist:
#        q4fns.qntevent(symbol, bonuspst, bonusfut, splitpst, splitfut, rightpst, rightfut, divdnpst, divdnfut, resltpst, resltfut)
#    p4fns.write_csv(NSEQNTLOG, [['EVENT']], 'a')
