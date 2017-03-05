#!/usr/bin/env python
# -*- coding: utf-8 -*-

from   p4defs  import *
import p4fns
import sys

mode               = str(sys.argv[1])
csvdb              = str(sys.argv[2])

ixc0df             = p4fns.read_csv(NSEIXCatalog) 
ixclist            = [row[PXC['SYMBOL']] for row in ixc0df]

eqc0df             = p4fns.read_csv(NSEEQCatalog) 
eqclist            = [row[PCAT['SYMBOL']] for row in eqc0df]

if (mode=='WRITE'):
    if (csvdb==SQLEQCatalog):
        inputdf            = p4fns.readall_csv(NSEEQCatalog) 
        p4fns.write_sql(NSEULDB, csvdb, inputdf, MCAT, EQCATCOL)
    elif (csvdb==SQLIXCatalog):
        inputdf            = p4fns.readall_csv(NSEIXCatalog) 
        p4fns.write_sql(NSEULDB, csvdb, inputdf, MXC, IXCATCOL)
    elif (csvdb in ixclist):
        inputdf            = p4fns.readall_csv(NSEIXSDBDIR+csvdb+CSV) 
        p4fns.write_sql(NSEULDB, csvdb, inputdf, MXS, SYIXCOL)
    elif (csvdb in eqclist):
        inputdf            = p4fns.readall_csv(NSEEQSDBDIR+csvdb+CSV) 
        p4fns.write_sql(NSEULDB, csvdb, inputdf, MQS, SYEQCOL)
    elif (csvdb==SQLNSEBONUS):
        inputdf            = p4fns.readall_csv(NSEBONUS) 
        p4fns.write_sql(NSEULDB, csvdb, inputdf, MBON, BONUSCOL)
    elif (csvdb==SQLNSESPLIT):
        inputdf            = p4fns.readall_csv(NSESPLIT) 
        p4fns.write_sql(NSEULDB, csvdb, inputdf, MSPL, SPLITCOL)
    elif (csvdb==SQLNSERIGHT):
        inputdf            = p4fns.readall_csv(NSERIGHT) 
        p4fns.write_sql(NSEULDB, csvdb, inputdf, MRGT, RIGHTCOL)
    elif (csvdb==SQLNSEDIVIDEND):
        inputdf            = p4fns.readall_csv(NSEDIVIDEND) 
        p4fns.write_sql(NSEULDB, csvdb, inputdf, MDIV, DIVCOL)
    elif (csvdb==SQLNSERESULT):
        inputdf            = p4fns.readall_csv(NSERESULT) 
        p4fns.write_sql(NSEULDB, csvdb, inputdf, MRES, RESCOL)
    else:
        print ('The given csv database is not part of Catalog')
elif (mode=='DROP'):
    if (csvdb==SQLEQCatalog):
        p4fns.drop_sql(NSEULDB, csvdb)
    elif (csvdb==SQLIXCatalog):
        p4fns.drop_sql(NSEULDB, csvdb)
    elif (csvdb in ixclist):
        p4fns.drop_sql(NSEULDB, csvdb)
    elif (csvdb in eqclist):
        p4fns.drop_sql(NSEULDB, csvdb)
    elif (csvdb==SQLNSEBONUS):
        p4fns.drop_sql(NSEULDB, csvdb)
    elif (csvdb==SQLNSESPLIT):
        p4fns.drop_sql(NSEULDB, csvdb)
    elif (csvdb==SQLNSERIGHT):
        p4fns.drop_sql(NSEULDB, csvdb)
    elif (csvdb==SQLNSEDIVIDEND):
        p4fns.drop_sql(NSEULDB, csvdb)
    elif (csvdb==SQLNSERESULT):
        p4fns.drop_sql(NSEULDB, csvdb)
    else:
        print ('The given csv database is not part of Catalog')
else:
    print ('The given mode is not supported')
