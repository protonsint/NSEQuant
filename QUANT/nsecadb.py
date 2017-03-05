#!/usr/bin/env python
# Usage ./nsecadb.py

from   p4defs            import *
import p4fns
from   datetime          import datetime
import dateutil.parser   as     dp
import re

## ============================================================================================= ##
## General 
## ============================================================================================= ##
eqschdf            = p4fns.read_csv(NSESCHCatalog) 
eqschdict          = {row[PSCH['OLDSYMBOL']]:row[PSCH['SYMBOL']] for row in eqschdf}
## ============================================================================================= ##
## Parsing NSE Corporate Actions and Updating the Corporate Actions Catalogs
## ============================================================================================= ##
def cadates(row):
    try:
        rcdate     = (datetime.strptime(row[PRCA['RECDATE']], '%d-%b-%Y')).strftime('%Y-%m-%d')
    except:
        try:
            rcdate = (datetime.strptime(row[PRCA['BCSTART']], '%d-%b-%Y')).strftime('%Y-%m-%d')
        except:
            rcdate = ''
    try:
        bcdate     = (datetime.strptime(row[PRCA['BCEND']], '%d-%b-%Y')).strftime('%Y-%m-%d')
    except:
        try:
            bcdate = (datetime.strptime(row[PRCA['RECDATE']], '%d-%b-%Y')).strftime('%Y-%m-%d')
        except:
            bcdate = ''
    try:
        exdate     = (datetime.strptime(row[PRCA['EXDATE']], '%d-%b-%Y')).strftime('%Y-%m-%d')
        valid      = True
    except:
        exdate     = ''
        valid      = False
    return valid, exdate, rcdate, bcdate

## BONUS
## ============================================================================================= ##
def parsebonus(purpose):
    extract        = re.search('[Bb]onus[^0-9]+([0-9]+)\s*:\s*([0-9]+)', purpose)
    if extract:
         bonus     = float(extract.group(1))
         origl     = float(extract.group(2))
    else:
         bonus     = 0
         origl     = 0
    return bonus, origl

def genbonus(bonus0df, bonusrdf):
    for row in bonusrdf:
        valid, exdate, rcdate, bcdate = cadates(row)
        exist          = False
        if (valid==True):
            for bon in bonus0df:
                if ((bon[PBON['SYMBOL']]==row[PRCA['SYMBOL']]) and (bon[PBON['EXDATE']]==exdate)):
                     exist     = True
            if (row[PRCA['SERIES']] in REGEQSERIES) and (exist==False):
                bonus, origl   = parsebonus(row[PRCA['PURPOSE']])
                if bonus and origl:
                    ratio      =  "%.4f" %((bonus+origl)/origl)
                    bonus0df.append([row[PRCA['SYMBOL']], row[PRCA['FACEVALUE']], ratio, exdate, rcdate, bcdate, 'F'])
    return bonus0df

bonus0df           = p4fns.read_csv(NSEBONUS) 
bonus0df           = p4fns.symchange(bonus0df, PBON['SYMBOL'], eqschdict)
bonusrdf           = p4fns.read_csv(NSERBONUS) 
bonusrdf           = p4fns.symchange(bonusrdf, PRCA['SYMBOL'], eqschdict)
bonus1df           = p4fns.readhdr_csv(NSEBONUS) 
bonus1df.extend(genbonus(bonus0df, bonusrdf))
p4fns.write_csv(NSEBONUS, bonus1df, 'w')
#p4fns.write_sql(NSEULDB, SQLNSEBONUS, bonus1df, MBON, BONUSCOL)

## SPLIT
## ============================================================================================= ##
def parsesplit(purpose):
    extract        = re.search('([Ff]ace|[Ss]plit|[Ff]rom)[^0-9]+([0-9]+)[^0-9]+([Tt]o|\-)+[^0-9]+([0-9]+)', purpose)
    if extract:
         split     = float(extract.group(4))
         origl     = float(extract.group(2))
    else:
         split     = 0
         origl     = 0
    return split, origl

def gensplit(split0df, splitrdf):
    for row in splitrdf:
        valid, exdate, rcdate, bcdate = cadates(row)
        exist          = False
        if (valid==True):
            for spl in split0df:
                if ((spl[PSPL['SYMBOL']]==row[PRCA['SYMBOL']]) and (spl[PSPL['EXDATE']]==exdate)):
                     exist = True
            if (row[PRCA['SERIES']] in REGEQSERIES) and (exist==False):
                split, origl   = parsesplit(row[PRCA['PURPOSE']])
                if split and origl:
                    ratio      =  "%.4f" %(origl/split)
                    split0df.append([row[PRCA['SYMBOL']], row[PRCA['FACEVALUE']], ratio, exdate, rcdate, bcdate, 'F'])
    return split0df

split0df           = p4fns.read_csv(NSESPLIT) 
split0df           = p4fns.symchange(split0df, PSPL['SYMBOL'], eqschdict)
splitrdf           = p4fns.read_csv(NSERSPLIT) 
splitrdf           = p4fns.symchange(splitrdf, PRCA['SYMBOL'], eqschdict)
split1df           = p4fns.readhdr_csv(NSESPLIT) 
split1df.extend(gensplit(split0df, splitrdf))
p4fns.write_csv(NSESPLIT, split1df, 'w')
#p4fns.write_sql(NSEULDB, SQLNSESPLIT, split1df, MSPL, SPLITCOL)

## RIGHTS ISSUE
## ============================================================================================= ##
def parseright(purpose, facevalue):
    extractr       = re.search('[Rr]ight[^0-9]+([0-9]+)\s*:\s*([0-9]+)', purpose)
    right          = 0
    origl          = 0
    issuepr        = 0
    if extractr:
         right     = float(extractr.group(1))
         origl     = float(extractr.group(2))
         extractp  = re.search('[Pp]remium[^0-9]+([0-9]*\.?[0-9]*)', purpose)
         if extractp:
              issuepr  = float(extractp.group(1))
         else:
              issuepr  = float(facevalue)
    return right, origl, issuepr

def genright(right0df, rightrdf):
    for row in rightrdf:
        valid, exdate, rcdate, bcdate = cadates(row)
        exist          = False
        if (valid==True):
            for rgt in right0df:
                if ((rgt[PRGT['SYMBOL']]==row[PRCA['SYMBOL']]) and (rgt[PRGT['EXDATE']]==exdate)):
                     exist = True
            if (row[PRCA['SERIES']] in REGEQSERIES) and (exist==False):
                right, origl, issuepr = parseright(row[PRCA['PURPOSE']], row[PRCA['FACEVALUE']])
                if right and origl and issuepr:
                    ratio      =  "%.4f" %(origl/right)
                    right0df.append([row[PRCA['SYMBOL']], row[PRCA['FACEVALUE']], ratio, issuepr, exdate, rcdate, bcdate, 'F'])
    return right0df

right0df           = p4fns.read_csv(NSERIGHT) 
right0df           = p4fns.symchange(right0df, PRGT['SYMBOL'], eqschdict)
rightrdf           = p4fns.read_csv(NSERRIGHT) 
rightrdf           = p4fns.symchange(rightrdf, PRCA['SYMBOL'], eqschdict)
right1df           = p4fns.readhdr_csv(NSERIGHT) 
right1df.extend(genright(right0df, rightrdf))
p4fns.write_csv(NSERIGHT, right1df, 'w')
#p4fns.write_sql(NSEULDB, SQLNSERIGHT, right1df, MRGT, RIGHTCOL)

## DIVIDENDS
## ============================================================================================= ##
def parsediv(purpose):
    extractr       = re.search('[Dd]iv[^0-9]+([0-9]*\.?[0-9]*)[^0-9]*([Dd]iv|Special)[^0-9]+([0-9]*\.?[0-9]*)[^0-9]+[Ss]hare', purpose)
    div            = 0
    if extractr:
        div        = float(extractr.group(1)) + float(extractr.group(3))
    else:
        extractr   = re.search('[Dd]iv[^0-9]+([0-9]+\.?[0-9]*)[^0-9]+([Pp]er|Share)', purpose)
        if extractr:
             div   = float(extractr.group(1))
    return div

def gendiv(div0df, divrdf):
    for row in divrdf:
        valid, exdate, rcdate, bcdate = cadates(row)
        exist          = False
        if (valid==True):
            for ref in div0df:
                if ((ref[PDIV['SYMBOL']]==row[PRCA['SYMBOL']]) and (ref[PDIV['EXDATE']]==exdate)):
                     exist = True
            if (row[PRCA['SERIES']] in REGEQSERIES) and (exist==False):
                div        = "%.2f" %(parsediv(row[PRCA['PURPOSE']]))
                if div:
                    div0df.append([row[PRCA['SYMBOL']], div, exdate, rcdate, bcdate])
    return div0df

div0df           = p4fns.read_csv(NSEDIVIDEND) 
div0df           = p4fns.symchange(div0df, PDIV['SYMBOL'], eqschdict)
divrdf           = p4fns.read_csv(NSERDIVIDEND) 
divrdf           = p4fns.symchange(divrdf, PRCA['SYMBOL'], eqschdict)
div1df           = p4fns.readhdr_csv(NSEDIVIDEND) 
div1df.extend(gendiv(div0df, divrdf))
p4fns.write_csv(NSEDIVIDEND, div1df, 'w')
#p4fns.write_sql(NSEULDB, SQLNSEDIVIDEND, div1df, MDIV, DIVCOL)

## FINANCIAL RESULT DATES
## ============================================================================================= ##
def genres(res0df, resrdf, resfdf):
    res1df             = []
    for row in resrdf:
        try:
            resdatime  = (datetime.strptime(row[PRRS['TIMESTAMP']], '%d-%b-%Y %H:%M')).strftime('%Y-%m-%d %H:%M')
            valid      = True
        except:
            resdatime  = ''
            valid      = False
        exist          = False
        if (valid==True):
            resdate    = (datetime.strptime(row[PRRS['TIMESTAMP']], '%d-%b-%Y %H:%M')).strftime('%Y-%m-%d')
            for ref in resfdf:
                refdate    = (datetime.strptime(ref[PRES['TIMESTAMP']], '%Y-%m-%d %H:%M')).strftime('%Y-%m-%d')
                if ((ref[PRES['SYMBOL']]==row[PRRS['SYMBOL']]) and (refdate==resdate)):
                     exist = True
            if (exist==False):
                res1df.append([row[PRRS['SYMBOL']], resdatime])
                resfdf.append([row[PRRS['SYMBOL']], resdatime])
    return res1df
res0df           = p4fns.read_csv(NSERESULT) 
res0df           = p4fns.symchange(res0df, PRES['SYMBOL'], eqschdict)
resrdf           = p4fns.read_csv(NSERRESULT) 
resrdf           = p4fns.symchange(resrdf, PRRS['SYMBOL'], eqschdict)
resrdf.sort(key=lambda x: dp.parse(x[PRRS['TIMESTAMP']],dayfirst=True))
resfdf           = [row for row in res0df if (dp.parse(row[PRES['TIMESTAMP']])>=dp.parse(resrdf[0][PRRS['TIMESTAMP']],dayfirst=True))]
res1df           = p4fns.readhdr_csv(NSERESULT) 
res1df.extend(res0df)
res1df.extend(genres(res0df, resrdf, resfdf))
p4fns.write_csv(NSERESULT, res1df, 'w')
#p4fns.write_sql(NSEULDB, SQLNSERESULT, res1df, MRES, RESCOL)

## FORTHCOMING BUSINESS MEETING DATES (For Results Declaration)
## ============================================================================================= ##
def parsebmeet(purpose):
    extractr       = re.search('[Rr]esult', purpose)
    if extractr:
        resday     = True
    else:
        resday     = False
    return resday

def genfbm(fbm0df, fbmrdf, fbmfdf):
    fbm1df             = []
    for row in fbmrdf:
        try:
            fbmdate    = (datetime.strptime(row[PRBM['TIMESTAMP']], '%d-%b-%Y')).strftime('%Y-%m-%d')
            valid      = True
        except:
            fbmdate    = ''
            valid      = False
        exist          = False
        if (valid==True):
            for ref in fbmfdf:
                refdate    = ref[PFBM['TIMESTAMP']]
                if ((ref[PFBM['SYMBOL']]==row[PRBM['SYMBOL']]) and (refdate==fbmdate)):
                     exist = True
            if (exist==False) and (parsebmeet(row[PRBM['PURPOSE']])):
                fbm1df.append([row[PRBM['SYMBOL']], fbmdate])
                fbmfdf.append([row[PRBM['SYMBOL']], fbmdate])
    return fbm1df
fbm0df           = p4fns.read_csv(NSEFBMEET) 
fbm0df           = p4fns.symchange(fbm0df, PFBM['SYMBOL'], eqschdict)
fbmrdf           = p4fns.read_csv(NSERFBMEET) 
fbmrdf           = p4fns.symchange(fbmrdf, PRBM['SYMBOL'], eqschdict)
fbmrdf.sort(key=lambda x: dp.parse(x[PRBM['TIMESTAMP']],dayfirst=True))
fbmfdf           = [row for row in fbm0df if (dp.parse(row[PFBM['TIMESTAMP']])>=dp.parse(fbmrdf[0][PRBM['TIMESTAMP']],dayfirst=True))]
fbm1df           = p4fns.readhdr_csv(NSEFBMEET) 
fbm1df.extend(fbm0df)
fbm1df.extend(genfbm(fbm0df, fbmrdf, fbmfdf))
p4fns.write_csv(NSEFBMEET, fbm1df, 'w')
#p4fns.write_sql(NSEULDB, SQLNSEFBMEET, fbm1df, MFBM, FBMCOL)
