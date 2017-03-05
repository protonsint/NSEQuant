#!/usr/bin/env python
from   p4defs          import *
import p4fns
import math
import os.path         as     path

cnxlist            = [row[PCAT['SYMBOL']] for row in p4fns.read_csv(NSEEQCatalog)]
ixclist            = ['NIFTY','BANKNIFTY']
count              = 0

for symbol in cnxlist+ixclist:
    count += 1
    print count
    if path.isfile(NSEDVSDBDIR+symbol+CSV):
        dvxdata        = [['TIMESTAMP','AVGIV']]
        eqsdb          = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)

## Volatility
## ============================================== ##
        dvsdb          = p4fns.read_csv(NSEDVSDBDIR+symbol+CSV)
    
        for row in eqsdb:
            timestamp  = row[PQS['TIMESTAMP']]
            dvtdb      = p4fns.filterdf(p4fns.filterdf(p4fns.filterdf(dvsdb,\
                                                                      PDS, 'INSTRUMENT', ['OPTSTK']),\
                                                                      PDS, 'TIMESTAMP', [timestamp]),\
                                                                      PDS, 'T2E', [str(x) for x in range(1,50)])
            ivlist     = [float(row[PDS['IV']]) for row in dvtdb]
            wtlist     = [float(row[PDS['VAL_INLAKH']]) for row in dvtdb]
            if sum(wtlist) >= 100:
                avgiv  = round(p4fns.wmean(ivlist, wtlist), 2)
            else:
                avgiv  = 0
        
            dvxdata.append([timestamp, avgiv])
    
        p4fns.write_csv(NSEDVDIR+'TECH/'+symbol+CSV, dvxdata, 'w')

