#!/usr/bin/env python
import matplotlib.pyplot  as     plt
from   matplotlib.dates   import DateFormatter,MonthLocator,DayLocator,date2num
from   matplotlib.finance import candlestick_ohlc
from   matplotlib         import gridspec
from   datetime           import datetime
import time
import math
import p4fns
from   p4defs             import *

labelc         = 'lightgreen'
textc          = 'lightgreen'
gridc          = 'lightgray'
sitec          = 'goldenrod'
backc          = '#1f242d'
volmc          = 'lightgreen'
candupc        = 'yellowgreen'
canddnc        = 'crimson'
active         = '#e63800'
passive        = '#3e485b'
gbackc         = '#292f3b'
glabelc        = 'w'

today          = time.strftime("%d-%m-%Y")
ixlist         = ['NIFTY', 'BANKNIFTY']

## ********************************************************************************************* ##
## Daily Candlestick with VOlume
## ********************************************************************************************* ##
#def pltcandle(symbol, periods):
#    maxper             = max(periods.values())
#    datadb             = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)[-maxper:]
#    ptimestamp         = [date2num(datetime.strptime(row[PQS['TIMESTAMP']], '%Y-%m-%d')) for row in datadb]
#    popen              = [float(row[PQS['OPEN']]) for row in datadb]
#    phigh              = [float(row[PQS['HIGH']]) for row in datadb]
#    plow               = [float(row[PQS['LOW']]) for row in datadb]
#    pclose             = [float(row[PQS['CLOSE']]) for row in datadb]
#    pvolume            = [round(float(row[PQS['TURNOVER']])/10000000, 2) for row in datadb]
#    
#    for period in periods:
#        days           = periods[period]
#        stimestamp     = ptimestamp[-days:]
#        sopen          = popen[-days:]
#        shigh          = phigh[-days:]
#        slow           = plow[-days:]
#        sclose         = pclose[-days:]
#        svolume        = pvolume[-days:]
#        volmean        = p4fns.smean(svolume)
#        
#        quotes         = [[stimestamp[i], sopen[i], shigh[i], slow[i], sclose[i]] for i in range(len(stimestamp))]
#        
#        if (days == 63):
#            majorl     = DayLocator([1,15])
#            xformat    = DateFormatter('%d-%b')
#        elif (days == 126):
#            majorl     = DayLocator(1)
#            xformat    = DateFormatter('%b')
#        elif (days == 252):
#            majorl     = MonthLocator()
#            xformat    = DateFormatter('%b')
#        elif (days == 504):
#            majorl     = MonthLocator([1,4,7,10])
#            xformat    = DateFormatter('%b-%y')
#        elif (days == 1008):
#            majorl     = MonthLocator([1,7])
#            xformat    = DateFormatter('%b-%y')
#        
#        fig            = plt.figure(figsize=(6,3))
#        gs             = gridspec.GridSpec(2, 1, height_ratios=[5, 1]) 
#        ax1            = plt.subplot(gs[0])
#        plt.title(symbol, loc='left', color=textc, weight='bold', size='small')
#        ax1.xaxis.set_major_locator(majorl)
#        ax1.xaxis.set_major_formatter(xformat)
#        ax1.yaxis.tick_right()
#        ax1.grid(b=True, which='major', color=gridc, linestyle=':')
#        ax1.patch.set_facecolor(backc)
#        ax1.spines['bottom'].set_color(labelc)
#        ax1.spines['top'].set_color(backc) 
#        ax1.spines['right'].set_color(labelc)
#        ax1.spines['left'].set_color(backc)
#        ax1.tick_params(axis='x', colors=labelc)
#        ax1.tick_params(axis='y', colors=labelc)
#        for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
#            label.set_fontsize(6)
#        candlestick_ohlc(ax1, quotes, width=0.8, colorup=candupc, colordown=canddnc)
#        ax1.xaxis_date()
#        ax1.autoscale_view()
#        ax1.set_aspect('auto')
#        plt.setp(ax1.get_xticklabels(), horizontalalignment='center', fontsize=8)
#        
#        ax2            = plt.subplot(gs[1], sharex=ax1)
#        plt.setp(ax2.get_xticklabels(), visible=False)
#        ax2.yaxis.tick_right()
#        max_yticks     = 2
#        yloc           = plt.MaxNLocator(max_yticks)
#        ax2.yaxis.set_major_locator(yloc)
#        ax2.patch.set_facecolor(backc)
#        ax2.spines['bottom'].set_color(labelc)
#        ax2.spines['top'].set_color(backc) 
#        ax2.spines['right'].set_color(labelc)
#        ax2.spines['left'].set_color(backc)
#        ax2.tick_params(axis='x', colors=backc)
#        ax2.tick_params(axis='y', colors=labelc)
#        for label in (ax2.get_yticklabels()):
#            label.set_fontsize(6)
#        plt.ylim(ymax = volmean*3)
#        plt.bar(stimestamp, svolume, color=volmc, edgecolor='none')
#        
#        plt.figtext(0.94, 0.94, '$\copyright$ piby4.com '+today, color=sitec, size='xx-small', ha ='right')
#        gs.tight_layout(fig, h_pad=0)
#        plt.savefig(IMGDLYDIR+symbol+'_'+period+'.png', facecolor=(backc))
#        plt.close(fig)
#
### ********************************************************************************************* ##
### Volume and Volatility Bar
### ********************************************************************************************* ##
#def pltvol(symbol):
#    datadb         = p4fns.read_csv(NSEGENLDIR+symbol+CSV)[0]
#    sg             = float(datadb[8])
#    max_sg         = float(datadb[9])
#    min_sg         = float(datadb[10])
#    vol            = float(datadb[11])
#    max_vol        = float(datadb[12])
#    min_vol        = float(datadb[13])
#
#    sg_per         = (sg-min_sg)*100/(max_sg-min_sg)
#    vol_per        = (vol-min_vol)*100/(max_vol-min_vol)
#
#    N = 2
#    values         = (sg_per, vol_per)
#    padding        = (100-sg_per, 100-vol_per)
#    print values
#    print padding
#    ind            = (0, 1)
#    width          = 0.70
#    
#    fig            = plt.figure(figsize=(3,1))
#    gs             = gridspec.GridSpec(1, 1) 
#    ax1            = plt.subplot(gs[0])
#    pos1           = ax1.get_position()
#    pos2           = [pos1.x0 + 0.1, pos1.y0,  pos1.width / 1.1, pos1.height ] 
#    ax1.set_position(pos2)
#    ax1.patch.set_facecolor(gbackc)
#    ax1.spines['bottom'].set_color(gbackc)
#    ax1.spines['top'].set_color(gbackc) 
#    ax1.spines['right'].set_color(gbackc)
#    ax1.spines['left'].set_color(gbackc)
#    p1 = plt.barh(ind, values, width, color=active, edgecolor='none')
#    p2 = plt.barh(ind, padding, width, color=passive, left=values, edgecolor='none')
#    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off') 
#    plt.yticks((0+width/2, 1+width/2), ('Volatility', 'Volume  '), color=glabelc, size='x-small')
#    plt.tick_params(axis='y', which='both', left='off', right='off') 
#    plt.text(80, (width-0.1)/2, str(sg), size='xx-small', color=textc)
#    plt.text(80, 1+(width-0.1)/2, str(int(vol))+' Cr', size='xx-small', color=textc)
#    
#    plt.savefig(IMGVOLDIR+symbol+'.png', facecolor=(gbackc))
#    plt.close(fig)
#
### ********************************************************************************************* ##
### Bollinger Band
### ********************************************************************************************* ##
#def pltbollinger(symbol, periods, deltaP, deltaN, mawin):
#    maxper             = max(periods.values())+252
#    datadb             = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)[-maxper:]
#    ptimestamp         = [date2num(datetime.strptime(row[PQS['TIMESTAMP']], '%Y-%m-%d')) for row in datadb]
#    popen              = [float(row[PQS['OPEN']]) for row in datadb]
#    phigh              = [float(row[PQS['HIGH']]) for row in datadb]
#    plow               = [float(row[PQS['LOW']]) for row in datadb]
#    pclose             = [float(row[PQS['CLOSE']]) for row in datadb]
#    pvwap              = [float(row[PQS['VWAP']]) for row in datadb]
#    dsize              = len(ptimestamp)
#    
#    for period in periods:
#        samples        = min(dsize, int(periods[period]*1.25))
#        days           = min(int(dsize/1.25), periods[period])
#        window         = min(samples-days, mawin)
#        stimestamp     = ptimestamp[-days:]
#        sopen          = popen[-days:]
#        shigh          = phigh[-days:]
#        slow           = plow[-days:]
#        sclose         = pclose[-days:]
#        svwap          = pvwap[-samples:]
#        mu             = p4fns.rolling_emean(svwap, window)[-days:]
#        sg             = p4fns.rolling_sstdd(svwap, window)[-days:]
#        upl            = [mu[i]+sg[i]*deltaP for i in range(days)]
#        lwl            = [mu[i]-sg[i]*deltaN for i in range(days)]
#        
#        quotes         = [[stimestamp[i], sopen[i], shigh[i], slow[i], sclose[i]] for i in range(days)]
#        
#        if (days <= 63):
#            majorl     = DayLocator([1,15])
#            xformat    = DateFormatter('%d-%b')
#        elif (days <= 126):
#            majorl     = DayLocator(1)
#            xformat    = DateFormatter('%b')
#        elif (days <= 252):
#            majorl     = MonthLocator()
#            xformat    = DateFormatter('%b')
#        elif (days <= 504):
#            majorl     = MonthLocator([1,4,7,10])
#            xformat    = DateFormatter('%b-%y')
#        else:
#            majorl     = MonthLocator([1,7])
#            xformat    = DateFormatter('%b-%y')
#        
#        fig            = plt.figure(figsize=(6,3))
#        gs             = gridspec.GridSpec(1, 1) 
#
#        ax1            = plt.subplot(gs[0])
#        plt.title('Bollinger Bands ['+symbol+']', loc='left', color=textc, weight='bold', size='small')
#        ax1.xaxis.set_major_locator(majorl)
#        ax1.xaxis.set_major_formatter(xformat)
#        ax1.yaxis.tick_right()
#        ax1.grid(b=True, which='major', color=gridc, linestyle=':')
#        ax1.patch.set_facecolor(backc)
#        ax1.spines['bottom'].set_color(labelc)
#        ax1.spines['top'].set_color(backc) 
#        ax1.spines['right'].set_color(labelc)
#        ax1.spines['left'].set_color(backc)
#        ax1.tick_params(axis='x', colors=labelc)
#        ax1.tick_params(axis='y', colors=labelc)
#        for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
#            label.set_fontsize(6)
#        candlestick_ohlc(ax1, quotes, width=0.8, colorup='deepskyblue', colordown='deepskyblue')
#        ax1.xaxis_date()
#        ax1.autoscale_view()
#        ax1.set_aspect('auto')
#        plt.setp(ax1.get_xticklabels(), horizontalalignment='center', fontsize=8)
#
#        ax2            = plt.subplot(gs[0])
#        ax2.plot(stimestamp, mu, color='royalblue', linewidth=1.5)
#        
#        ax3            = plt.subplot(gs[0])
#        ax3.plot(stimestamp, upl, color='yellowgreen')
#        
#        ax4            = plt.subplot(gs[0])
#        ax4.plot(stimestamp, lwl, color='crimson')
#        
#        plt.figtext(0.94, 0.94, '$\copyright$ piby4.com '+today, color=sitec, size='xx-small', ha ='right')
#        gs.tight_layout(fig)
#        plt.savefig(IMGBOBDIR+symbol+'_'+period+'.png', facecolor=(backc))
#        plt.close(fig)
#
### ********************************************************************************************* ##
### Auto Regression
### ********************************************************************************************* ##
#def pltautoregres(symbol, period, deltaP, deltaN, rwindow, mwindow):
#    maxper         = period+rwindow+mwindow-1
#    datadb         = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)[-maxper:]
#    ptimestamp     = [date2num(datetime.strptime(row[PQS['TIMESTAMP']], '%Y-%m-%d')) for row in datadb]
#    pclose         = [math.log(float(row[PQS['CLOSE']])) for row in datadb]
#    pvwap          = [math.log(float(row[PQS['VWAP']])) for row in datadb]
#    dsize          = len(ptimestamp)
#    if (dsize>=rwindow+mwindow+40):
#        reffdb         = p4fns.read_csv(NSEIXSDBDIR+'EIGHTFD'+CSV)[-maxper:]
#        pvwapR         = [math.log(float(row[PXS['CLOSE']])) for row in reffdb]
#        
#        regr           = p4fns.rolling_regress(pvwap[-dsize:], pvwapR[-dsize:], rwindow)
#        rlen           = len(regr)
#        error          = [round((a/b-1)*100, 2) for a, b in zip(pclose[-rlen:], regr[-rlen:])]
#        stimestamp     = ptimestamp[-rlen:]
#        mu             = p4fns.rolling_smean(error, mwindow)
#        sg             = p4fns.rolling_sstdd(error, mwindow)
#        mlen           = len(sg)
#        error          = error[-mlen:]
#        stimestamp     = stimestamp[-mlen:]
#        mu             = mu[-mlen:]
#        sg             = sg[-mlen:]
#        upl            = [mu[i]+sg[i]*deltaP for i in range(mlen)]
#        lwl            = [mu[i]-sg[i]*deltaN for i in range(mlen)]
#        
#        majorl         = MonthLocator()
#        xformat        = DateFormatter('%b')
#        
#        fig            = plt.figure(figsize=(6,3))
#        gs             = gridspec.GridSpec(1, 1) 
#
#        ax1            = plt.subplot(gs[0])
#        plt.title('Auto Regression ['+symbol+']', loc='left', color=textc, weight='bold', size='small')
#        ax1.xaxis.set_major_locator(majorl)
#        ax1.xaxis.set_major_formatter(xformat)
#        ax1.yaxis.tick_right()
#        ax1.grid(b=True, which='major', color=gridc, linestyle=':')
#        ax1.patch.set_facecolor(backc)
#        ax1.spines['bottom'].set_color(labelc)
#        ax1.spines['top'].set_color(backc) 
#        ax1.spines['right'].set_color(labelc)
#        ax1.spines['left'].set_color(backc)
#        ax1.tick_params(axis='x', colors=labelc)
#        ax1.tick_params(axis='y', colors=labelc)
#        for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
#            label.set_fontsize(6)
#        ax1.plot(stimestamp, error, color='deepskyblue', linewidth=1.5)
#        ax1.xaxis_date()
#        ax1.autoscale_view()
#        ax1.set_aspect('auto')
#        plt.setp(ax1.get_xticklabels(), horizontalalignment='center', fontsize=8)
#
#        ax2            = plt.subplot(gs[0])
#        ax2.plot(stimestamp, mu, color='royalblue', linewidth=1.5)
#        
#        ax3            = plt.subplot(gs[0])
#        ax3.plot(stimestamp, upl, color='yellowgreen')
#        
#        ax4            = plt.subplot(gs[0])
#        ax4.plot(stimestamp, lwl, color='orangered')
#        
#        plt.figtext(0.94, 0.94, '$\copyright$ piby4.com '+today, color=sitec, size='xx-small', ha ='right')
#        gs.tight_layout(fig)
#        plt.savefig(IMGAURDIR+symbol+'.png', facecolor=(backc))
#        plt.close(fig)

## ********************************************************************************************* ##
## Cross Regression
## ********************************************************************************************* ##
def pltcrosregres(symbol, period, deltaP, deltaN, rwindow, mwindow):
    maxper         = period+rwindow+mwindow-1
    datadb         = p4fns.filterdf(p4fns.read_csv(NSEEQSDBDIR+symbol+CSV), PQS, 'SERIES', REGEQSERIES)[-maxper:]
    ptimestamp     = [date2num(datetime.strptime(row[PQS['TIMESTAMP']], '%Y-%m-%d')) for row in datadb]
    pclose         = [math.log(float(row[PQS['CLOSE']])) for row in datadb]
    pvwap          = [math.log(float(row[PQS['VWAP']])) for row in datadb]
    dsize          = len(ptimestamp)
    if (dsize>=rwindow+mwindow+40):
#        pairlist   = [row[0] for row in p4fns.read_csv(NSEPAIRDIR+symbol+CSV)]+['NIFTY']
        pairlist   = ['NIFTY']
        for pair in pairlist:
            if pair in ixlist:
                reffdb     = p4fns.read_csv(NSEIXSDBDIR+pair+CSV)[-maxper:]
                pvwapR     = [math.log(float(row[PXS['CLOSE']])) for row in reffdb]
            else:
                reffdb     = p4fns.read_csv(NSEEQSDBDIR+pair+CSV)[-maxper:]
                pvwapR     = [math.log(float(row[PQS['VWAP']])) for row in reffdb]
            
            regr           = p4fns.rolling_regress(pvwap[-dsize:], pvwapR[-dsize:], rwindow)
            rlen           = len(regr)
            error          = [round((a/b-1)*100, 2) for a, b in zip(pclose[-rlen:], regr[-rlen:])]
            stimestamp     = ptimestamp[-rlen:]
            mu             = p4fns.rolling_smean(error, mwindow)
            sg             = p4fns.rolling_sstdd(error, mwindow)
            mlen           = len(sg)
            error          = error[-mlen:]
            stimestamp     = stimestamp[-mlen:]
            mu             = mu[-mlen:]
            sg             = sg[-mlen:]
            upl            = [mu[i]+sg[i]*deltaP for i in range(mlen)]
            lwl            = [mu[i]-sg[i]*deltaN for i in range(mlen)]
            
            majorl         = MonthLocator()
            xformat        = DateFormatter('%b')
            
            fig            = plt.figure(figsize=(6,3))
            gs             = gridspec.GridSpec(1, 1) 
        
            ax1            = plt.subplot(gs[0])
            plt.title(symbol, loc='left', color=textc, weight='bold')
            plt.title('StatArb ['+symbol+' vs '+pair+']', loc='left', color=textc, weight='bold', size='small')
            ax1.xaxis.set_major_locator(majorl)
            ax1.xaxis.set_major_formatter(xformat)
            ax1.yaxis.tick_right()
            ax1.grid(b=True, which='major', color=gridc, linestyle=':')
            ax1.patch.set_facecolor(backc)
            ax1.spines['bottom'].set_color(labelc)
            ax1.spines['top'].set_color(backc) 
            ax1.spines['right'].set_color(labelc)
            ax1.spines['left'].set_color(backc)
            ax1.tick_params(axis='x', colors=labelc)
            ax1.tick_params(axis='y', colors=labelc)
            for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
                label.set_fontsize(6)
            ax1.plot(stimestamp, error, color='deepskyblue', linewidth=1.5)
            ax1.xaxis_date()
            ax1.autoscale_view()
            ax1.set_aspect('auto')
            plt.setp(ax1.get_xticklabels(), horizontalalignment='center', fontsize=8)
        
            ax2            = plt.subplot(gs[0])
            ax2.plot(stimestamp, mu, color='royalblue', linewidth=1.5)
            
            ax3            = plt.subplot(gs[0])
            ax3.plot(stimestamp, upl, color='yellowgreen')
            
            ax4            = plt.subplot(gs[0])
            ax4.plot(stimestamp, lwl, color='orangered')
            
            plt.figtext(0.94, 0.94, '$\copyright$ piby4.com '+today, color=sitec, size='xx-small', ha ='right')
            gs.tight_layout(fig)
#            plt.savefig(IMGCRRDIR+symbol+'_'+pair+'.png', facecolor=(backc))
            plt.savefig('aaa.png', facecolor=(backc))
            plt.close(fig)
