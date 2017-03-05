## ############################################################################################# ##
## Sub Routines
## ############################################################################################# ##
from   p4defs            import *
import csv
import json
#import MySQLdb           as     mdb
import dateutil.parser   as     dp
import math

## ********************************************************************************************* ##
## CSV Related
## ********************************************************************************************* ##
## Read a csv file and put all lines into list
## =========================================== ##
def readall_csv(fname):
    with open(fname, 'r') as f:
        reader         = csv.reader(f)
        flist          = list(reader)
        return flist

## Read a csv file and put non header lines into list
## =========================================== ##
def read_csv(fname):
    with open(fname, 'r') as f:
        reader         = csv.reader(f)
        next(reader)
        flist          = list(reader)
        return flist

## Read a csv file and put header line into list
## =========================================== ##
def readhdr_csv(fname):
    with open(fname, 'r') as f:
        reader         = csv.reader(f)
        flist          = []
        flist.append(list(next(reader)))
        return flist

## Append / Write a list to a csv file 
## =========================================== ##
def write_csv(fname, flist, mode):
    f        = open(fname, mode)
    fwriter  = csv.writer(f, lineterminator='\n')
    for row in flist:
        fwriter.writerow(row)
    f.close()

## ********************************************************************************************* ##
## Find value among databases
## ********************************************************************************************* ##
def findvalue(timestamp, instrument, symbol, optiontyp, expirydt, strikepr, field):
    if (optiontyp == 'CE'):
       optyp       = ['CE', 'CA']
    elif (optiontyp == 'PE'): 
       optyp       = ['PE', 'PA']
    if (instrument == 'IX') or (instrument == 'FUTIDX') or (instrument == 'FUTIVX') or (instrument == 'OPTIDX'):
        datadf     = read_csv(NSEIXSDBDIR+symbol+CSV)
        datadf     = filterdf(datadf, PXS, 'TIMESTAMP', [timestamp])
        try:
            ulprice    = float(datadf[-1][PXS[field]])
        except:
            print ("FindValue Error: The trading date is not valid")
            exit()
    else:
        datadf     = filterdf(read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)
        datadf     = filterdf(datadf, PXS, 'TIMESTAMP', [timestamp])
        try:
            ulprice    = float(datadf[-1][PQS[field]])
        except:
            print ("FindValue Error: The trading date is not valid")
            exit()
    if (instrument == 'IX') or (instrument == 'EQ'):
        value      = ulprice
    elif (instrument == 'FUTSTK') or (instrument == 'FUTIDX') or (instrument == 'FUTIVX'):
        datadf     = filterdf(read_csv(NSEDVSDBDIR+symbol+CSV), PDS, 'INSTRUMENT', [instrument])
        datadf     = filterdf(datadf, PDS, 'TIMESTAMP', [timestamp])
        datadf     = filterdf(datadf, PDS, 'EXPIRY_DT', [expirydt])
        value      = ulprice if not datadf else float(datadf[-1][PDS[field]])
    else:
        datadf     = filterdf(read_csv(NSEDVSDBDIR+symbol+CSV), PDS, 'TIMESTAMP', [timestamp])
        datadf     = filterdf(datadf, PDS, 'INSTRUMENT', [instrument])
        datadf     = filterdf(datadf, PDS, 'EXPIRY_DT', [expirydt])
        datadf     = filtertdf(datadf, PDS, DVCOLTYP, 'STRIKE_PR', [float(strikepr)])
        datadf     = filterdf(datadf, PDS, 'OPTION_TYP', optyp)
        if (optiontyp == 'CE'):
            value  = max(ulprice-float(strikepr),0) if not datadf else float(datadf[-1][PDS[field]])
        else:
            value  = max(float(strikepr)-ulprice,0) if not datadf else float(datadf[-1][PDS[field]])
    return value

## Find the strike price and expiry date of an option for given OPDIST and T2E constraint
## ======================================================================================== ##
def findopparam(timestamp, instrument, symbol, optiontyp, opdist):
    if (optiontyp == 'CE'):
       optyp       = ['CE', 'CA']
    elif (optiontyp == 'PE'): 
       optyp       = ['PE', 'PA']
    datadf         = filterdf(read_csv(NSEDVSDBDIR+symbol+CSV), PDS, 'INSTRUMENT', [instrument])
    datadf         = filterdf(datadf, PDS, 'TIMESTAMP', [timestamp])
    datadf         = filterdf(datadf, PDS, 'OPTION_TYP', optyp)
    datadf         = filterdf(datadf, PDS, 'OPDIST', [opdist])
    datadf         = filterdf(datadf, PDS, 'T2E', [str(i) for i in list(range(1,60))])
    datadf.sort(key=lambda x: float(x[PDS['VAL_INLAKH']]))
    expirydt       = 'XX' if not datadf else datadf[-1][PDS['EXPIRY_DT']]
    strikepr       = 0 if not datadf else float(datadf[-1][PDS['STRIKE_PR']])
    return expirydt, strikepr

## Find trading day at a delta days from given timestamp
## ======================================================================================== ##
def tradingday(timestamp, delta):
    datadf         = read_csv(NSEIXSDBDIR+'NIFTY'+CSV)
    if (delta < 0):
        niftydf    = filterts(datadf, PXS, 'TIMESTAMP', timestamp, 'LT')
        marker     = min(len(niftydf)-1, -delta)
        deltats    = niftydf[-marker][PXS['TIMESTAMP']]
    else:
        niftydf    = filterts(datadf, PXS, 'TIMESTAMP', timestamp, 'GTE')
        marker     = min(len(niftydf)-1, delta)
        deltats    = niftydf[marker][PXS['TIMESTAMP']]
    return deltats

## ********************************************************************************************* ##
## Dataframe Manipulation
## ********************************************************************************************* ##
## Change the symbol name from a DF
## =========================================== ##
def symchange(indf, spos, schdict):
    outdf               = []
    for row in indf:
        if row[spos] in list(schdict.keys()):
            row[spos]   = schdict[row[spos]]
        outdf.append(row)
    return outdf

## Read a DF and rearrange and subset columns
## =========================================== ##
def rearrange(inputdf, inpos, outcol):
    outdf            = []
    for row in inputdf:
        outrow       = []     
        for i in range(0,len(outcol)):
            outrow.append(row[inpos[outcol[i]]])
        outdf.append(outrow)
    return outdf

## Filter a DF 
## =========================================== ##
def filterdf(inputdf, inpos, filcol, fillist):
    outdf            = []
    for row in inputdf:
        if (row[inpos[filcol]] in fillist):
            outdf.append(row)
    return outdf

## Filter a DF using type
## =========================================== ##
def filtertdf(inputdf, inpos, intyp, filcol, fillist):
    outdf            = []
    for row in inputdf:
        if (intyp[filcol] == 'F' or intyp[filcol] == 'F4'):
            if (float(row[inpos[filcol]]) in fillist):
                outdf.append(row)
        elif (intyp[filcol] == 'I'):
            if (int(row[inpos[filcol]]) in fillist):
                outdf.append(row)
        else:
            if (row[inpos[filcol]] in fillist):
                outdf.append(row)
    return outdf

## Filter a DF based on timestamp
## =========================================== ##
def filterts(inputdf, inpos, filcol, timestamp, operator):
    outdf            = []
    for row in inputdf:
        if (operator == 'GT'):
            if (dp.parse(row[inpos[filcol]]) > dp.parse(timestamp)):
                outdf.append(row)
        elif (operator == 'GTE'):
            if (dp.parse(row[inpos[filcol]]) >= dp.parse(timestamp)):
                outdf.append(row)
        elif (operator == 'LT'):
            if (dp.parse(row[inpos[filcol]]) < dp.parse(timestamp)):
                outdf.append(row)
        elif (operator == 'LTE'):
            if (dp.parse(row[inpos[filcol]]) <= dp.parse(timestamp)):
                outdf.append(row)
        else:
            if (dp.parse(row[inpos[filcol]]) == dp.parse(timestamp)):
                outdf.append(row)
    return outdf

## Select data beginning at a timestamp
## =========================================== ##
def blockdf(inputdf, inpos, timestamp, blocksize, direction):
    marker           = len(inputdf)
    for i in range(0, len(inputdf)):
        if (direction=='bi') or (direction=='fe'):
            if (dp.parse(inputdf[i][inpos['TIMESTAMP']]) <= dp.parse(timestamp)):
                marker   = i
        else:
            if (dp.parse(inputdf[i][inpos['TIMESTAMP']]) >= dp.parse(timestamp)):
                marker   = i
                break
    if (direction=='bi'):
        outdf        = inputdf[max((marker-blocksize+1),0):(marker+1)]
    elif (direction=='be'):
        outdf        = inputdf[max((marker-blocksize),0):marker]
    elif (direction=='fi'):
        outdf        = inputdf[marker:(marker+blocksize)]
    else:
        outdf        = inputdf[(marker+1):(marker+blocksize+1)]
    return outdf

## ********************************************************************************************* ##
## SQL Related
## ********************************************************************************************* ##
## Write a list to a SQL DB Table
## =========================================== ##
#def write_sql(dbname, tablename, datalist, hdrdict, hdrlist):
#    hdrstr             = 'Id INT PRIMARY KEY AUTO_INCREMENT'
#    for l in hdrlist:
#        hdrstr         = hdrstr+', '+l+' '+hdrdict[l]
#    data               = [tuple(l) for l in datalist[1:]]
#    hdrstmt            = 'CREATE TABLE `'+tablename+'` ('+hdrstr+');'
#    collist            = ",".join(hdrlist)
#    stmt               = 'INSERT INTO `'+tablename+'` ('+collist+') VALUES (%s'+', %s'*(len(hdrlist)-1)+');'
#    
#    con = mdb.connect(host=HOSTNM, user=USERNM, passwd=PASSWDNM, db=dbname, read_default_file=CNFFILE);
#    with con:
#        cur = con.cursor()
#        cur.execute('DROP TABLE IF EXISTS `'+tablename+'`;')
#        cur.execute(hdrstmt)
#        cur.executemany(stmt, data)

## Append a list to a SQL DB Table
## =========================================== ##
#def append_sql(dbname, tablename, datalist, hdrdict, hdrlist):
#    data               = [tuple(l) for l in datalist]
#    collist            = ",".join(hdrlist)
#    stmt               = 'INSERT INTO `'+tablename+'` ('+collist+') VALUES (%s'+', %s'*(len(hdrlist)-1)+');'
#    
#    con = mdb.connect(host=HOSTNM, user=USERNM, passwd=PASSWDNM, db=dbname, read_default_file=CNFFILE);
#    with con:
#        cur = con.cursor()
#        cur.executemany(stmt, data)

## Drop an SQL Table
## =========================================== ##
#def drop_sql(dbname, tablename):
#    stmt               = 'DROP TABLE IF EXISTS `'+tablename+'`;'
#    
#    con = mdb.connect(host=HOSTNM, user=USERNM, passwd=PASSWDNM, db=dbname, read_default_file=CNFFILE);
#    with con:
#        cur = con.cursor()
#        cur.execute(stmt)

## ********************************************************************************************* ##
## JSON Related
## ********************************************************************************************* ##
## Write a list to a JSON File
## =========================================== ##
def write_json(fname, datalist, hdrtyp):
    data             = datalist[1:]
    jsonhdr          = datalist[0]
    jsondata         = []
    jsondata.append(jsonhdr)
    for row in data:
        jrow         = []
        for i in range(0,len(row)):
            if (jsonhdr[i] not in hdrtyp):
                jrow.append(row[i])
            elif (hdrtyp[jsonhdr[i]] == 'I'):
                jrow.append(int(row[i]) if row[i]!='' else 0)
            elif ((hdrtyp[jsonhdr[i]] == 'F') or (hdrtyp[jsonhdr[i]] == 'F4')):
                jrow.append(float(row[i]) if row[i]!='' else 0)
            else:
                jrow.append(row[i])
        jsondata.append(jrow)
       
    with open(fname, 'w') as fjson:
        json.dump(jsondata, fjson, indent=4)

## Write a list to a JSON File (Old dictionary format)
## =========================================== ##
def write_jsondict(fname, datalist, hdrtyp):
    data             = datalist[1:]
    hdr              = datalist[0]
    jsondict         = {}
    jsoncols         = []
    count            = 0
    for item in hdr:
        itemdict          = {}
        itemdict['id']    = count
        itemdict['label'] = item
        itemdict['type']  = JSONTYP[hdrtyp[item]]
        jsoncols.append(itemdict)
        count             = count+1
    jsondict['cols']      = jsoncols
    
    jsondata              = []
    for row in data:
        rowdict           = {}
        jsonrow           = []
        for i in range(0,len(row)):
            itemdict      = {}
            if (hdrtyp[hdr[i]] == 'I'):
                itemdict['v'] = int(row[i]) if row[i]!='' else 0
            elif ((hdrtyp[hdr[i]] == 'F') or (hdrtyp[hdr[i]] == 'F4')):
                itemdict['v'] = float(row[i]) if row[i]!='' else 0
            elif (hdrtyp[hdr[i]] == 'T'):
                ts        = dp.parse(row[i])
                itemdict['v'] = ts.strftime('Date(%Y,')+str(int(ts.strftime('%m'))-1)+ts.strftime(',%d)')
            else:
                itemdict['v'] = row[i]
            jsonrow.append(itemdict)
        rowdict['c']      = jsonrow
        jsondata.append(rowdict)
    jsondict['rows']      = jsondata
    
    with open(fname, 'w') as fjson:
        json.dump(jsondict, fjson)

## ********************************************************************************************* ##
## Statistics
## ********************************************************************************************* ##
## Find mean of a list
## =========================================== ##
def smean(data):
    mean           = sum(data)/len(data)
    return mean

## Find ewma 
## =========================================== ##
def emean(data, ewma, span):
    a              = 2.0/(span + 1) 
    ewma           = data*a + (1-a)*ewma
    return ewma

## Find weighted mean of a list
## =========================================== ##
def wmean(data, weights):
    mean           = sum([a*b for a,b in zip(data,weights)])/sum(weights)
    return mean

## Find standard deviation
## =========================================== ##
def sstdd(data):
    mean           = smean(data)
    error          = [(x-mean)**2 for x in data]
    variance       = sum(error) / (len(data)-1)
    stdd           = variance**0.5
    return stdd

## Find weighted standard deviation
## =========================================== ##
def wstdd(data, weights):
    mean           = wmean(data, weights)
    error          = [(x-mean)**2 for x in data]
    variance       = sum([a*b for a,b in zip(error,weights)])/(smean(weights)*(len(data)-1))
    stdd           = variance**0.5
    return stdd

## Find RMS Error between two lists
## =========================================== ##
def rmse(data, prediction):
    error          = [math.log(b/a)**2 for a, b in zip(data, prediction)]
    rmse           = math.sqrt(smean(error))
    return rmse*100

## Find rolling sum of a list
## =========================================== ##
def rolling_sum(data, window):
    rsum           = []
    for i in range(0, len(data)-window+1):
        rsum.append(sum(data[i:i+window])) 
    return rsum    

## Find rolling gains of a list
## =========================================== ##
def rolling_gain(data):
    rgain          = []
    for i in range(0, len(data)-1):
        rgain.append(math.log(data[i+1]/data[i])*100) 
    return rgain    

## Find rolling sma of a list
## =========================================== ##
def rolling_smean(data, window):
    rsmean          = []
    for i in range(window, len(data)):
        rsmean.append(round(smean(data[i-window:i]), 2)) 
    return rsmean    

## Find rolling ewma of a list
## =========================================== ##
def rolling_emean(data, span):
    remean          = []
    ewma            = data[0]
    for i in range(0, len(data)):
        ewma        = emean(data[i], ewma, span)
        remean.append(round(ewma, 2)) 
    return remean

## Find rolling stdd of a list
## =========================================== ##
def rolling_sstdd(data, window):
    rsstdd          = []
    for i in range(window, len(data)):
        rsstdd.append(round(sstdd(data[i-window:i]), 2)) 
    return rsstdd    

## Sample a list
## =========================================== ##
def sample(data, intervals):
    sampledata     = []
    for i in range(0, len(data)):
        if (i%intervals == (len(data)-1)%intervals):
            sampledata.append(data[i])
    return sampledata    

## Find cumulative normal distribution
## =========================================== ##
def cumnormdist(x):
    b1             = 0.319381530
    b2             = -0.356563782
    b3             = 1.781477937
    b4             = -1.821255978
    b5             = 1.330274429
    p              = 0.2316419
    c              = 0.39894228
    if (x >= 0):
        t          = 1/(1 + p * x)
        nd         = (1-c*math.exp(-x*x/2)*t*(t*(t*(t*(t*b5+b4)+b3)+b2)+b1))
    else:
        t          = 1/(1 - p * x)
        nd         = (c*math.exp(-x*x/2)*t*(t*(t*(t*(t*b5+b4)+b3)+b2)+b1))
    return nd

## Find slope and intercept of linear regression
## =========================================== ##
def regress(x, y):
    xmu            = smean(x)
    ymu            = smean(y)
    num            = [(x[i]-xmu)*(y[i]-ymu) for i in range(0,len(x))]
    den            = [(x[i]-xmu)*(x[i]-xmu) for i in range(0,len(x))]
    slope          = sum(num)/sum(den)
    intercept      = ymu - slope*xmu
    return slope, intercept

## Find regression expected value of a list
## =========================================== ##
def regpred(data, indep):
    slope, intercept   = regress(indep, data)
    predict            = indep[-1]*slope + intercept
    return predict

## Find rolling regression expected value of a list
## ================================================ ##
def rolling_regress(data, indep, window):
    rpred          = []
    for i in range(0, len(data)-window+1):
        rpred.append(regpred(data[i:i+window], indep[i:i+window])) 
    return rpred    

## Find mean Pearson correlation coefficient of the sample
## ========================================================================== ##
def corr(dataX, dataY):
    meanX          = smean(dataX)
    meanY          = smean(dataY)
    stddX          = sstdd(dataX)
    stddY          = sstdd(dataY)
    scoreX         = [(x-meanX)/stddX for x in dataX]
    scoreY         = [(y-meanY)/stddY for y in dataY]
    score          = [(a*b) for a,b in zip(scoreX, scoreY)]
    corrcoeff      = round(sum(score)*100/(len(dataX)-1), 2)
    return corrcoeff

## Find mean correlation between two lists with given window and intervals
## ========================================================================== ##
def mean_corr(data1, data2, window, interval):
    samples        = sample(range(0,len(data1)), interval) 
    corrc          = []
    for i in samples:
        if (i>=window):
            corrc.append(corr(data1[i-window:i+1],data2[i-window:i+1]))
    mean_corrcoeff = round(smean(corrc), 2)
    return mean_corrcoeff

## ********************************************************************************************* ##
## Simple Algebra
## ********************************************************************************************* ##
## Approximate a numer to N digits
## =========================================== ##
def approxify(number, N):
    factor = 0
    for i in reversed(range(N,6)):
         if (number > math.pow(10,i)):
              factor = i-N
              break
    number = int(int(number/math.pow(10,factor))*math.pow(10,factor))
    return number

## ********************************************************************************************* ##
## Option Related Calculations
## ********************************************************************************************* ##
## Opton Price Calculation
## =========================================== ##
def optionprice(optyp, ulprice, strikeprice, volatility, riskfree, days2exp, dividend):
    if (days2exp==0):
        opprice    = 0
    else:
        t2e        = days2exp/365.0
        d1         = (math.log(ulprice/strikeprice) + t2e*(riskfree - dividend + volatility*volatility/2))/(volatility*math.sqrt(t2e))
        d2         = d1 - volatility*math.sqrt(t2e)
        if (optyp == 'call'):
            nd1        = cumnormdist(d1)
            nd2        = cumnormdist(d2)
            opprice    = ulprice*nd1*math.exp(-dividend*t2e) - strikeprice*nd2*math.exp(-riskfree*t2e)
        else:
            nd1        = cumnormdist(-d1)
            nd2        = cumnormdist(-d2)
            opprice    = strikeprice*nd2*math.exp(-riskfree*t2e) - ulprice*nd1*math.exp(-dividend*t2e)
    return opprice

## IV Calculation
## =========================================== ##
def ivcalc(optiontyp, ulprice, strikeprice, opprice, days2exp):
    if (days2exp==0):
        volatility   = 0
    else:
        riskfree         = 0.10
        dividend         = 0
        vol_floor        = 0.049
        vol_ceiling      = 1.01
        volatility       = round(((vol_ceiling + vol_floor)/2.0),4)
        while (volatility-vol_floor > 0.001) :
            if (optiontyp=='CE') or (optiontyp=='CA'):
                optyp        = 'call'
            else:
                optyp        = 'put'
            calcprice        = optionprice(optyp, ulprice, strikeprice, volatility, riskfree, days2exp, dividend)
            if (calcprice > opprice):
                vol_ceiling  = volatility
            else:
                vol_floor    = volatility
            volatility       = round(((vol_ceiling + vol_floor)/2.0),4)
        volatility       = min(max(volatility, 0.05), 1)
    return round(volatility*100,2)
