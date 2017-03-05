#!/usr/bin/env python
from   p4defs            import *
import p4fns

clearlog           = p4fns.readhdr_csv(NSEQNTLOG)
p4fns.write_csv(NSEQNTLOG, clearlog, 'w')

clearlog           = p4fns.readhdr_csv(IMGDLYLOG)
p4fns.write_csv(IMGDLYLOG, clearlog, 'w')

clearlog           = p4fns.readhdr_csv(IMGVOLLOG)
p4fns.write_csv(IMGVOLLOG, clearlog, 'w')

clearlog           = p4fns.readhdr_csv(IMGBOBLOG)
p4fns.write_csv(IMGBOBLOG, clearlog, 'w')

clearlog           = p4fns.readhdr_csv(IMGAURLOG)
p4fns.write_csv(IMGAURLOG, clearlog, 'w')

clearlog           = p4fns.readhdr_csv(IMGCRRLOG)
p4fns.write_csv(IMGCRRLOG, clearlog, 'w')
