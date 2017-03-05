## ********************************************************************************************* ##
## The header module contains CONSTANT definitions and type declarations for directory structure ##
## and DATABASE TABLE headers                                                                    ##
## ********************************************************************************************* ##

## ============================================================================================= ##
## NSE DATABASE STRUCTURE                                                                        ##
## ============================================================================================= ##
NSEULDB            = 'NSEUL'
CSV                = '.csv'
JSON               = '.json'
NSEDIR             = '../NSE/'

## Directory Structure and Files for NSE TECH DB
NSETECHDIR         = NSEDIR+'TECH/'
NSEGENLDIR         = NSETECHDIR+'GENL/'
NSEPAIRDIR         = NSETECHDIR+'PAIR/'
NSEJSONDIR         = NSEDIR+'JSON/'
JSONDLYDIR         = NSEJSONDIR+'DAILY/'
JSONGENLDIR        = NSEJSONDIR+'GENL/'
JSONPERFDIR        = NSEJSONDIR+'PERF/'
JSONEVNTDIR        = NSEJSONDIR+'EVENTS/'
JSONPAIRDIR        = NSEJSONDIR+'PAIR/'
JSONRESDIR         = NSEJSONDIR+'RESULT/'

## Directory Structure and Files for IMAGE Dir
NSEIMGDIR          = NSEDIR+'IMG/'
IMGDLYDIR          = NSEIMGDIR+'DAILY/'
IMGVOLDIR          = NSEIMGDIR+'VOL/'
IMGBOBDIR          = NSEIMGDIR+'BOB/'
IMGAURDIR          = NSEIMGDIR+'AUR/'
IMGCRRDIR          = NSEIMGDIR+'CRR/'

## Directory Structure and Files for NSE INDEX DB
NSEIXDIR           = NSEDIR+'INDEX/'
NSEIXRAWDIR        = NSEIXDIR+'RAW/'
NSEIXSDBDIR        = NSEIXDIR+'SDB/'
NSEIXTDBDIR        = NSEIXDIR+'TDB/'
NSEIXCatalog       = NSEIXDIR+'NSEIXCatalog'+CSV
NSEIXTDBFILE       = NSEIXTDBDIR+'IndexDB'+CSV
SQLIXCatalog       = 'IXCatalog'

## Directory Structure and Files for NSE EQUITY DB
NSEEQDIR           = NSEDIR+'EQUITY/'
NSEEQRAWDIR        = NSEEQDIR+'RAW/'
NSEEQRAWCADIR      = NSEEQDIR+'RAWCA/'
NSEEQSDBDIR        = NSEEQDIR+'SDB/'
NSEEQTDBDIR        = NSEEQDIR+'TDB/'
NSEEQCatalog       = NSEEQDIR+'NSEEQCatalog'+CSV
NSEISINCatalog     = NSEEQDIR+'NSEISINCatalog'+CSV
NSESCHCatalog      = NSEEQDIR+'NSESCHCatalog'+CSV
NSEEQTDBFILE       = NSEEQTDBDIR+'EquityDB'+CSV
SQLEQCatalog       = 'EQCatalog'

NSEREQLIST         = NSEEQDIR+'EQUITY_L'+CSV

## Directory Structure and Files for NSE DERIV DB
NSEDVDIR           = NSEDIR+'DERIV/'
NSEDVRAWDIR        = NSEDVDIR+'RAW/'
NSEDVSDBDIR        = NSEDVDIR+'SDB/'
NSEDVTDBDIR        = NSEDVDIR+'TDB/'
NSEDVTDBFILE       = NSEDVTDBDIR+'DerivDB'+CSV

## Directory Structure and Files for NSE CORPORATE ACTIONS
NSERBONUS          = NSEEQRAWCADIR+'RAW_BONUS'+CSV
NSERSPLIT          = NSEEQRAWCADIR+'RAW_SPLIT'+CSV
NSERRIGHT          = NSEEQRAWCADIR+'RAW_RIGHTS'+CSV
NSERDIVIDEND       = NSEEQRAWCADIR+'RAW_DIVIDEND'+CSV
NSERRESULT         = NSEEQRAWCADIR+'RAW_RESULT'+CSV
NSERFBMEET         = NSEEQRAWCADIR+'RAW_FBMEET'+CSV

NSEBONUS           = NSEEQDIR+'NSEBonus'+CSV
NSESPLIT           = NSEEQDIR+'NSESplit'+CSV
NSERIGHT           = NSEEQDIR+'NSERight'+CSV
NSEDIVIDEND        = NSEEQDIR+'NSEDividend'+CSV
NSERESULT          = NSEEQDIR+'NSEResult'+CSV
NSEFBMEET          = NSEEQDIR+'NSEFBMeet'+CSV

SQLNSEBONUS        = 'NSEBONUS'
SQLNSESPLIT        = 'NSESPLIT'
SQLNSERIGHT        = 'NSERIGHT'
SQLNSEDIVIDEND     = 'NSEDIVIDEND'
SQLNSERESULT       = 'NSERESULT'
SQLNSEFBMEET       = 'NSEFBMEET'

## ============================================================================================= ##
## Log Files
## ============================================================================================= ##
## For IMAGE Dir
IMGDLYLOG          = NSEIMGDIR+'DAILY.log'
IMGVOLLOG          = NSEIMGDIR+'VOL.log'
IMGBOBLOG          = NSEIMGDIR+'BOB.log'
IMGAURLOG          = NSEIMGDIR+'AUR.log'
IMGCRRLOG          = NSEIMGDIR+'CRR.log'

## For JSON Dir
NSEQNTLOG          = NSEJSONDIR+'NSEQnt.log'
## ============================================================================================= ##
## NSE RAW AND GENERATED DATABASE FIELDS                                                         ##
## ============================================================================================= ##
## Column Names/Types for the RAW and Generated NSE INDEX Databases 
RAWIXCOL           = {'Index Name':'NAME','Index Date':'TIMESTAMP','Open Index Value':'OPEN',\
                      'High Index Value':'HIGH','Low Index Value':'LOW',\
                      'Closing Index Value':'CLOSE','Points Change':'CHANGE','Change(%)':'GAIN_C',\
                      'Volume':'VOLUME','Turnover (Rs. Cr.)':'TURNOVER','P/E':'PE','P/B':'PB',\
                      'Div Yield':'DIVYIELD'}
PXR                = {'NAME':0,'TIMESTAMP':1,'OPEN':2,'HIGH':3,'LOW':4,'CLOSE':5,'CHANGE':6,\
                      'GAIN_C':7,'VOLUME':8,'TURNOVER':9,'PE':10,'PB':11,'DIVYIELD':12}
TMIXCOL            = ['TIMESTAMP','SYMBOL','OPEN','HIGH','LOW','CLOSE','PREV',\
                      'GAIN','VOLUME','TURNOVER','PE','PB','DIVYIELD']
PXT                = {'TIMESTAMP':0,'SYMBOL':1,'OPEN':2,'HIGH':3,'LOW':4,'CLOSE':5,'PREV':6,\
                      'GAIN':7,'VOLUME':8,'TURNOVER':9,'PE':10,'PB':11,'DIVYIELD':12}
SYIXCOL            = ['TIMESTAMP','OPEN','HIGH','LOW','CLOSE','PREV',\
                      'GAIN','VOLUME','TURNOVER','PE','PB','DIVYIELD']
PXS                = {'TIMESTAMP':0,'OPEN':1,'HIGH':2,'LOW':3,'CLOSE':4,'PREV':5,\
                      'GAIN':6,'VOLUME':7,'TURNOVER':8,'PE':9,'PB':10,'DIVYIELD':11}
MXS                = {'TIMESTAMP':'DATE','OPEN':'DECIMAL(8,2)','HIGH':'DECIMAL(8,2)',\
                      'LOW':'DECIMAL(8,2)','CLOSE':'DECIMAL(8,2)','PREV':'DECIMAL(8,2)',\
                      'GAIN':'DECIMAL(7,4)','VOLUME':'DECIMAL(11)','TURNOVER':'DECIMAL(8,2)',\
                      'PE':'DECIMAL(6,2)','PB':'DECIMAL(6,2)','DIVYIELD':'DECIMAL(6,2)'}
IXCOLTYP           = {'SYMBOL':'S','TIMESTAMP':'T','NAME':'S','OPEN':'F','HIGH':'F','LOW':'F',\
                      'CLOSE':'F','PREV':'F','GAIN':'F4','VOLUME':'I','TURNOVER':'F',\
                      'PE':'F','PB':'F','DIVYIELD':'F','CHANGE':'F'}

## Column Names/Types for the RAW and Generated NSE EQUITY Databases 
VALEQSERIES        = ['EQ','BE','BL','BT','BZ','IL']
REGEQSERIES        = ['EQ','BE']
RAWEQCOL           = {'SYMBOL':'SYMBOL','SERIES':'SERIES','OPEN':'OPEN_U','HIGH':'HIGH_U',\
                      'LOW':'LOW_U','CLOSE':'CLOSE_U','LAST':'LAST_U','PREVCLOSE':'PREV_U',\
                      'TOTTRDQTY':'VOLUME','TOTTRDVAL':'TURNOVER','TIMESTAMP':'TIMESTAMP',\
                      'TOTALTRADES':'CONTRACTS','ISIN':'ISIN'}
PQR                = {'SYMBOL':0,'SERIES':1,'OPEN_U':2,'HIGH_U':3,'LOW_U':4,'CLOSE_U':5,'LAST_U':6,\
                      'PREV_U':7,'VOLUME':8,'TURNOVER':9,'TIMESTAMP':10,'CONTRACTS':11,'ISIN':12}
TMEQCOL            = ['TIMESTAMP','ISIN','SYMBOL','SERIES','OPEN_U','HIGH_U','LOW_U','CLOSE_U',\
                      'LAST_U','PREV_U','VOLUME','TURNOVER','CONTRACTS']
PQT                = {'TIMESTAMP':0,'ISIN':1,'SYMBOL':2,'SERIES':3,'OPEN_U':4,'HIGH_U':5,'LOW_U':6,\
                      'CLOSE_U':7,'LAST_U':8,'PREV_U':9,'VOLUME':10,'TURNOVER':11,'CONTRACTS':12}
SYEQCOL            = ['TIMESTAMP','ISIN','SYMBOL','SERIES','OPEN_U','HIGH_U','LOW_U','CLOSE_U',\
                      'LAST_U','PREV_U','VOLUME','TURNOVER','CONTRACTS','FACTOR','VWAP_U',\
                      'OPEN','HIGH','LOW','CLOSE','VWAP','PREV','GAIN']
PQS                = {'TIMESTAMP':0,'ISIN':1,'SYMBOL':2,'SERIES':3,'OPEN_U':4,'HIGH_U':5,'LOW_U':6,\
                      'CLOSE_U':7,'LAST_U':8,'PREV_U':9,'VOLUME':10,'TURNOVER':11,'CONTRACTS':12,\
                      'FACTOR':13,'VWAP_U':14,'OPEN':15,'HIGH':16,'LOW':17,'CLOSE':18,'VWAP':19,\
                      'PREV':20,'GAIN':21}
MQS                = {'TIMESTAMP':'DATE','ISIN':'VARCHAR(12)','SYMBOL':'VARCHAR(12)',\
                      'SERIES':'VARCHAR(2)','OPEN_U':'DECIMAL(8,2)','HIGH_U':'DECIMAL(8,2)',\
                      'LOW_U':'DECIMAL(8,2)','CLOSE_U':'DECIMAL(8,2)','LAST_U':'DECIMAL(8,2)',\
                      'PREV_U':'DECIMAL(8,2)','VOLUME':'DECIMAL(10)','TURNOVER':'DECIMAL(14,2)',\
                      'CONTRACTS':'DECIMAL(6)','FACTOR':'DECIMAL(8,4)','VWAP_U':'DECIMAL(8,2)',\
                      'OPEN':'DECIMAL(8,2)','HIGH':'DECIMAL(8,2)','LOW':'DECIMAL(8,2)',\
                      'CLOSE':'DECIMAL(8,2)','VWAP':'DECIMAL(8,2)','PREV':'DECIMAL(8,2)',\
                      'GAIN':'DECIMAL(7,4)'}
EQCOLTYP           = {'SYMBOL':'S','ISIN':'S','SERIES':'S','TIMESTAMP':'T','NAME':'S','OPEN_U':'F',\
                      'HIGH_U':'F','LOW_U':'F','CLOSE_U':'F','LAST_U':'F','PREV_U':'F',\
                      'FACTOR':'F4','OPEN':'F','HIGH':'F','LOW':'F','CLOSE':'F','LAST':'F',\
                      'VWAP_U':'F','VWAP':'F','VOLUME':'I','TURNOVER':'F','CONTRACTS':'I',\
                      'PREV':'F','GAIN':'F4'}

## Column Names/Types for the RAW and Generated NSE DERIV Databases 
RAWDVCOL           = {'INSTRUMENT':'INSTRUMENT','SYMBOL':'SYMBOL','EXPIRY_DT':'EXPIRY_DT',\
                      'STRIKE_PR':'STRIKE_PR','OPTION_TYP':'OPTION_TYP',\
                      'OPEN':'OPEN','HIGH':'HIGH','LOW':'LOW','CLOSE':'CLOSE','SETTLE_PR':'SETTLE_PR',\
                      'CONTRACTS':'CONTRACTS','VAL_INLAKH':'VAL_INLAKH',\
                      'OPEN_INT':'OPEN_INT','CHG_IN_OI':'CHG_IN_OI','TIMESTAMP':'TIMESTAMP'}
PDR                = {'INSTRUMENT':0,'SYMBOL':1,'EXPIRY_DT':2,'STRIKE_PR':3,'OPTION_TYP':4,\
                      'OPEN':5,'HIGH':6,'LOW':7,'CLOSE':8,'SETTLE_PR':9,'CONTRACTS':10,\
                      'VAL_INLAKH':11,'OPEN_INT':12,'CHG_IN_OI':13,'TIMESTAMP':14}
TMDVCOL            = ['TIMESTAMP','INSTRUMENT','SYMBOL','EXPIRY_DT','STRIKE_PR','OPTION_TYP',\
                      'OPEN','HIGH','LOW','CLOSE','SETTLE_PR','CONTRACTS','VAL_INLAKH','OPEN_INT','CHG_IN_OI']
PDT                = {'TIMESTAMP':0,'INSTRUMENT':1,'SYMBOL':2,'EXPIRY_DT':3,'STRIKE_PR':4,\
                      'OPTION_TYP':5,'OPEN':6,'HIGH':7,'LOW':8,'CLOSE':9,'SETTLE_PR':10,\
                      'CONTRACTS':11,'VAL_INLAKH':12,'OPEN_INT':13,'CHG_IN_OI':14}
SYDVCOL            = ['TIMESTAMP','INSTRUMENT','SYMBOL','EXPIRY_DT','STRIKE_PR','OPTION_TYP',\
                      'OPEN','HIGH','LOW','CLOSE','SETTLE_PR','CONTRACTS','VAL_INLAKH',\
                      'OPEN_INT','CHG_IN_OI','T2E','OPDIST','IV']
PDS                = {'TIMESTAMP':0,'INSTRUMENT':1,'SYMBOL':2,'EXPIRY_DT':3,'STRIKE_PR':4,\
                      'OPTION_TYP':5,'OPEN':6,'HIGH':7,'LOW':8,'CLOSE':9,'SETTLE_PR':10,\
                      'CONTRACTS':11,'VAL_INLAKH':12,'OPEN_INT':13,'CHG_IN_OI':14,\
                      'T2E':15,'OPDIST':16,'IV':17}
DVCOLTYP           = {'TIMESTAMP':'T','INSTRUMENT':'S','SYMBOL':'S','EXPIRY_DT':'T','STRIKE_PR':'F',\
                      'OPTION_TYP':'S','OPEN':'F','HIGH':'F','LOW':'F','CLOSE':'F','SETTLE_PR':'F',\
                      'CONTRACTS':'F','VAL_INLAKH':'F','OPEN_INT':'I','CHG_IN_OI':'I',\
                      'T2E':'I','OPDIST':'S','IV':'F'}

## Column Names/Types for the RAW and Generated NSE Corporate Actions Databases 
RAWCACOL           = {'Symbol':'SYMBOL','Face Value(Rs.)':'FACEVALUE','Purpose':'PURPOSE',\
                      'Ex-Date':'EXDATE','Record Date':'RECDATE','BC Start Date':'BCSTART',\
                      'BC End Date':'BCEND'}
PRCA               = {'SYMBOL':0,'SERIES':3,'FACEVALUE':4,'PURPOSE':5,'EXDATE':6,'RECDATE':7,\
                      'BCSTART':8,'BCEND':9}
BONUSCOL           = ['SYMBOL','FACEVALUE','RATIO','EXDATE','RECDATE','BCEND','DONE']
BONCOLTYP          = {'SYMBOL':'S','FACEVALUE':'I','RATIO':'F4','EXDATE':'T','RECDATE':'T','BCEND':'T','DONE':'S'}
PBON               = {'SYMBOL':0,'FACEVALUE':1,'RATIO':2,'EXDATE':3,'RECDATE':4,'BCEND':5,'DONE':6}
MBON               = {'SYMBOL':'VARCHAR(12)','FACEVALUE':'DECIMAL(3)','RATIO':'DECIMAL(7,4)',\
                      'EXDATE':'DATE','RECDATE':'DATE','BCEND':'DATE','DONE':'VARCHAR(1)'}
SPLITCOL           = ['SYMBOL','FACEVALUE','RATIO','EXDATE','RECDATE','BCEND','DONE']
SPLCOLTYP          = {'SYMBOL':'S','FACEVALUE':'I','RATIO':'F4','EXDATE':'T','RECDATE':'T','BCEND':'T','DONE':'S'}
PSPL               = {'SYMBOL':0,'FACEVALUE':1,'RATIO':2,'EXDATE':3,'RECDATE':4,'BCEND':5,'DONE':6}
MSPL               = {'SYMBOL':'VARCHAR(12)','FACEVALUE':'DECIMAL(3)','RATIO':'DECIMAL(7,4)',\
                      'EXDATE':'DATE','RECDATE':'DATE','BCEND':'DATE','DONE':'VARCHAR(1)'}
RIGHTCOL           = ['SYMBOL','FACEVALUE','RATIO','ISSUEPR','EXDATE','RECDATE','BCEND','DONE']
RGTCOLTYP          = {'SYMBOL':'S','FACEVALUE':'I','RATIO':'F4','ISSUEPR':'F','EXDATE':'T','RECDATE':'T','BCEND':'T','DONE':'S'}
PRGT               = {'SYMBOL':0,'FACEVALUE':1,'RATIO':2,'ISSUEPR':3,'EXDATE':4,'RECDATE':5,'BCEND':6,'DONE':7}
MRGT               = {'SYMBOL':'VARCHAR(12)','FACEVALUE':'DECIMAL(3)','ISSUEPR':'DECIMAL(8,2)',\
                      'RATIO':'DECIMAL(7,4)','EXDATE':'DATE','RECDATE':'DATE','BCEND':'DATE','DONE':'VARCHAR(1)'}
DIVCOL             = ['SYMBOL','DIVIDEND','EXDATE','RECDATE','BCEND']
DIVCOLTYP          = {'SYMBOL':'S','DIVIDEND':'F','EXDATE':'T','RECDATE':'T','BCEND':'T'}
PDIV               = {'SYMBOL':0,'DIVIDEND':1,'EXDATE':2,'RECDATE':3,'BCEND':4}
MDIV               = {'SYMBOL':'VARCHAR(12)','DIVIDEND':'DECIMAL(8,2)','EXDATE':'DATE',\
                      'RECDATE':'DATE','BCEND':'DATE'}
PRRS               = {'SYMBOL':0,'TIMESTAMP':9}
RESCOL             = ['SYMBOL','TIMESTAMP']
RESCOLTYP          = {'SYMBOL':'S','TIMESTAMP':'T'}
PRES               = {'SYMBOL':0,'TIMESTAMP':1}
MRES               = {'SYMBOL':'VARCHAR(12)','TIMESTAMP':'DATETIME'}
PRBM               = {'SYMBOL':0,'PURPOSE':3,'TIMESTAMP':4}
FBMCOL             = ['SYMBOL','TIMESTAMP']
FBMCOLTYP          = {'SYMBOL':'S','TIMESTAMP':'T'}
PFBM               = {'SYMBOL':0,'TIMESTAMP':1}
MFBM               = {'SYMBOL':'VARCHAR(12)','TIMESTAMP':'DATE'}

## Column Names/Types for the IX Catalog 
IXCATCOL           = ['SYMBOL','NAME']
PXC                = {'SYMBOL':0,'NAME':1}
MXC                = {'SYMBOL':'VARCHAR(15)','NAME':'VARCHAR(50)'}
IXCATCOLTYP        = {'SYMBOL':'S','NAME':'S'}
## Column Names/Types for the RAW and Generated EQ Catalog 
PRQL               = {'SYMBOL':0,'NAME':1,'SERIES':2,'LISTING_DATE':3,'PAID_UP_VALUE':4,\
                      'MARKET_LOT':5,'ISIN':6,'FACEVALUE':7}
EQCATCOL           = ['ISIN','SYMBOL','NAME','LISTING_DATE','PAID_UP_VALUE','MARKET_LOT','FACEVALUE'\
                      'SECTOR','INDUSTRY','MKT_CAP','SHARES']
PCAT               = {'ISIN':0,'SYMBOL':1,'NAME':2,'LISTING_DATE':3,'PAID_UP_VALUE':4,\
                      'MARKET_LOT':5,'FACEVALUE':6,'SECTOR':7,'INDUSTRY':8,'MKT_CAP':9,'SHARES':10}
MCAT               = {'ISIN':'VARCHAR(12)','SYMBOL':'VARCHAR(12)','NAME':'VARCHAR(75)',\
                      'LISTING_DATE':'DATE','PAID_UP_VALUE':'DECIMAL(3)',\
                      'MARKET_LOT':'DECIMAL(3)','FACEVALUE':'DECIMAL(3)'}
EQCATCOLTYP        = {'ISIN':'S','SYMBOL':'S','NAME':'S','LISTING_DATE':'T',\
                      'PAID_UP_VALUE':'F','MARKET_LOT':'F','FACEVALUE':'F','STOCKCODE':'S'}
PISN               = {'OLDISIN':0,'ISIN':1,'TIMESTAMP':2}
PSCH               = {'OLDSYMBOL':0,'SYMBOL':1,'TIMESTAMP':2}
PXL                = {'NAME':0,'INDUSTRY':1,'SYMBOL':2,'SERIES':3,'ISIN':4}

## ============================================================================================= ##
## JSON GENERATED FILES
## ============================================================================================= ##
## Column Names for the JSON Files
JSONTYP            = {'S':'string','T':'string','I':'number','F':'number','F4':'number','T':'string'}
JSONCOL            = ['TIMESTAMP','LOW','OPEN','CLOSE','HIGH','GAIN','VOLUME','TURNOVER']
PJS                = {'TIMESTAMP':0,'LOW':1,'OPEN':2,'CLOSE':3,'HIGH':4,'GAIN':5,'VOLUME':6,'TURNOVER':7}

## ============================================================================================= ##
## LEDGER and PORTFOLIO
## ============================================================================================= ##
LEDGERCOL          = ['TIMESTAMP','SYMBOL','INSTRUMENT','OPTION_TYP','EXPIRY_DT','STRIKE_PR','VOLUME','TURNOVER']
PLS                = {'TIMESTAMP':0,'SYMBOL':1,'INSTRUMENT':2,'OPTION_TYP':3,\
                      'EXPIRY_DT':4,'STRIKE_PR':5,'VOLUME':6,'TURNOVER':7}
PORTFCOL           = ['SYMBOL','INSTRUMENT','OPTION_TYP','EXPIRY_DT','STRIKE_PR','VOLUME','VALUE']
PPS                = {'SYMBOL':0,'INSTRUMENT':1,'OPTION_TYP':2,'EXPIRY_DT':3,\
                      'STRIKE_PR':4,'VOLUME':5,'VALUE':6}

