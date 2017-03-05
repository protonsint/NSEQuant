#!/usr/bin/env bash
# Usage: ./nsecron.sh 01-Oct-2014
curdate="$1"
#curdate=$(date +"%d-%b-%Y");
echo "=========== $curdate ================" >> cron_nse.log;
day=$(echo $curdate |& awk -F'-' '{print $1}');
month=$(echo $curdate |& awk -F'-' '{print $2}' |& tr '[:lower:]' '[:upper:]');
year=$(echo $curdate |& awk -F'-' '{print $3}');
numdate=$(date --date="$curdate" +"%Y-%m-%d");
ixdate=$(date --date="$curdate" +"%d%m%Y");

# Download the Equity Raw Catalog from NSE
# ===========================================================
wget -U firefox -O ../DATABASE/EQUITY/EQUITY_L.csv www.nseindia.com/content/equities/EQUITY_L.csv;

# Download the Index Constituent List from NSE
# ===========================================================
wget -U firefox -O ../DATABASE/EQUITY/CNX500.csv www.nseindia.com/content/indices/ind_cnx500list.csv;

# Download the Previous Corporate Actions Information from NSE
# ===========================================================
wget -U firefox -P ../DATABASE/EQUITY/RAWCA http://www.nseindia.com/corporates/datafiles/CA_LAST_1_MONTH_BONUS.csv;
if [ -f ../DATABASE/EQUITY/RAWCA/CA_LAST_1_MONTH_BONUS.csv ]; then
    mv ../DATABASE/EQUITY/RAWCA/CA_LAST_1_MONTH_BONUS.csv ../DATABASE/EQUITY/RAWCA/RAW_BONUS.csv;
    echo "Success: Done BONUS File Download" >> cron_nse.log;
else
    echo "Failure: BONUS File download" >> cron_nse.log;
fi
wget -U firefox -P ../DATABASE/EQUITY/RAWCA http://www.nseindia.com/corporates/datafiles/CA_LAST_1_MONTH_SPLIT.csv;
if [ -f ../DATABASE/EQUITY/RAWCA/CA_LAST_1_MONTH_SPLIT.csv ]; then
    mv ../DATABASE/EQUITY/RAWCA/CA_LAST_1_MONTH_SPLIT.csv ../DATABASE/EQUITY/RAWCA/RAW_SPLIT.csv;
    echo "Success: Done SPLIT File Download" >> cron_nse.log;
else
    echo "Failure: SPLIT File download" >> cron_nse.log;
fi
wget -U firefox -P ../DATABASE/EQUITY/RAWCA http://www.nseindia.com/corporates/datafiles/CA_LAST_1_MONTH_RIGHTS.csv;
if [ -f ../DATABASE/EQUITY/RAWCA/CA_LAST_1_MONTH_RIGHTS.csv ]; then
    mv ../DATABASE/EQUITY/RAWCA/CA_LAST_1_MONTH_RIGHTS.csv ../DATABASE/EQUITY/RAWCA/RAW_RIGHTS.csv;
    echo "Success: Done RIGHTS File Download" >> cron_nse.log;
else
    echo "Failure: RIGHTS File download" >> cron_nse.log;
fi
wget -U firefox -P ../DATABASE/EQUITY/RAWCA http://www.nseindia.com/corporates/datafiles/CA_LAST_1_MONTH_DIVIDEND.csv;
if [ -f ../DATABASE/EQUITY/RAWCA/CA_LAST_1_MONTH_DIVIDEND.csv ]; then 
    mv ../DATABASE/EQUITY/RAWCA/CA_LAST_1_MONTH_DIVIDEND.csv ../DATABASE/EQUITY/RAWCA/RAW_DIVIDEND.csv;
    echo "Success: Done DIVIDEND File Download" >> cron_nse.log;
else
    echo "Failure: DIVIDEND File download" >> cron_nse.log;
fi
wget -U firefox -P ../DATABASE/EQUITY/RAWCA http://www.nseindia.com/corporates/datafiles/FR_QuarterlyLast_1_Month.csv;
if [ -f ../DATABASE/EQUITY/RAWCA/FR_QuarterlyLast_1_Month.csv ]; then 
    mv ../DATABASE/EQUITY/RAWCA/FR_QuarterlyLast_1_Month.csv ../DATABASE/EQUITY/RAWCA/RAW_RESULT.csv;
    echo "Success: Done RESULT File Download" >> cron_nse.log;
else
    echo "Failure: RESULT File download" >> cron_nse.log;
fi

# Integrate the Corporate Actions
python ../QUANT/nsecadb.py >> cron_nse.log;
if [ $? -eq 0 ]; then
    echo "Success: Python CORP-ACTIONS Integration" >> cron_nse.log;
else
    echo "Failure: Python CORP-ACTIONS Integration" >> cron_nse.log;
fi

# Download the Forthcoming Corporate Actions Information from NSE
# ===============================================================
wget -U firefox -P ../DATABASE/EQUITY/RAWCA http://www.nseindia.com/corporates/datafiles/CA_ALL_FORTHCOMING_BONUS.csv;
if [ -f ../DATABASE/EQUITY/RAWCA/CA_ALL_FORTHCOMING_BONUS.csv ]; then
    mv ../DATABASE/EQUITY/RAWCA/CA_ALL_FORTHCOMING_BONUS.csv ../DATABASE/EQUITY/RAWCA/RAW_BONUS.csv;
    echo "Success: Done Future BONUS File Download" >> cron_nse.log;
else
    echo "Failure: Future BONUS File download" >> cron_nse.log;
fi
wget -U firefox -P ../DATABASE/EQUITY/RAWCA http://www.nseindia.com/corporates/datafiles/CA_ALL_FORTHCOMING_SPLIT.csv;
if [ -f ../DATABASE/EQUITY/RAWCA/CA_ALL_FORTHCOMING_SPLIT.csv ]; then
    mv ../DATABASE/EQUITY/RAWCA/CA_ALL_FORTHCOMING_SPLIT.csv ../DATABASE/EQUITY/RAWCA/RAW_SPLIT.csv;
    echo "Success: Done Future SPLIT File Download" >> cron_nse.log;
else
    echo "Failure: Future SPLIT File download" >> cron_nse.log;
fi
wget -U firefox -P ../DATABASE/EQUITY/RAWCA http://www.nseindia.com/corporates/datafiles/CA_ALL_FORTHCOMING_RIGHTS.csv;
if [ -f ../DATABASE/EQUITY/RAWCA/CA_ALL_FORTHCOMING_RIGHTS.csv ]; then
    mv ../DATABASE/EQUITY/RAWCA/CA_ALL_FORTHCOMING_RIGHTS.csv ../DATABASE/EQUITY/RAWCA/RAW_RIGHTS.csv;
    echo "Success: Done Future RIGHTS File Download" >> cron_nse.log;
else
    echo "Failure: Future RIGHTS File download" >> cron_nse.log;
fi
wget -U firefox -P ../DATABASE/EQUITY/RAWCA http://www.nseindia.com/corporates/datafiles/CA_ALL_FORTHCOMING_DIVIDEND.csv;
if [ -f ../DATABASE/EQUITY/RAWCA/CA_ALL_FORTHCOMING_DIVIDEND.csv ]; then 
    mv ../DATABASE/EQUITY/RAWCA/CA_ALL_FORTHCOMING_DIVIDEND.csv ../DATABASE/EQUITY/RAWCA/RAW_DIVIDEND.csv;
    echo "Success: Done Future DIVIDEND File Download" >> cron_nse.log;
else
    echo "Failure: Future DIVIDEND File download" >> cron_nse.log;
fi
wget -U firefox -P ../DATABASE/EQUITY/RAWCA http://www.nseindia.com/corporates/datafiles/BM_All_Forthcoming.csv
if [ -f ../DATABASE/EQUITY/RAWCA/BM_All_Forthcoming.csv ]; then 
    mv ../DATABASE/EQUITY/RAWCA/BM_All_Forthcoming.csv ../DATABASE/EQUITY/RAWCA/RAW_FBMEET.csv;
    echo "Success: Done Future BMEET File Download" >> cron_nse.log;
else
    echo "Failure: Future BMEET File download" >> cron_nse.log;
fi

# Integrate the Corporate Actions
python ../QUANT/nsecadb.py >> cron_nse.log;
if [ $? -eq 0 ]; then
    echo "Success: Python CORP-ACTIONS Integration" >> cron_nse.log;
else
    echo "Failure: Python CORP-ACTIONS Integration" >> cron_nse.log;
fi

# Download the Daily (Equity / Index / Deriv) Information from NSE
# ====================================================================
wget -U firefox -P ../DATABASE/INDEX/RAW www.nseindia.com/content/indices/ind_close_all_"$ixdate".csv;
if [ -f ../DATABASE/INDEX/RAW/ind_close_all_"$ixdate".csv ]; then
    mv ../DATABASE/INDEX/RAW/ind_close_all_"$ixdate".csv ../DATABASE/INDEX/RAW/"$numdate".csv;
    echo "Success: Done INDEX File Download for $curdate" >> cron_nse.log;
    python ../QUANT/nseixdb.py $curdate >> cron_nse.log;
    if [ $? -eq 0 ]; then
        echo "Success: Python INDEX Integration" >> cron_nse.log;
    else
        echo "Failure: Python INDEX Integration" >> cron_nse.log;
    fi
    wget -U firefox -P ../DATABASE/EQUITY/RAW www.nseindia.com/content/historical/EQUITIES/"$year"/"$month"/cm"$day$month$year"bhav.csv.zip;
    if [ -f ../DATABASE/EQUITY/RAW/cm"$day$month$year"bhav.csv.zip ]; then
        mv ../DATABASE/EQUITY/RAW/cm"$day$month$year"bhav.csv.zip ../DATABASE/EQUITY/RAW/"$numdate".csv.gz;
        gunzip ../DATABASE/EQUITY/RAW/"$numdate".csv.gz;
        echo "Success: Done EQUITY File Download for $curdate" >> cron_nse.log;
        python ../QUANT/nseeqdb.py $curdate >> cron_nse.log;
        if [ $? -eq 0 ]; then
            echo "Success: Python EQUITY Integration" >> cron_nse.log;
        else
            echo "Failure: Python EQUITY Integration" >> cron_nse.log;
        fi
    else
        echo "Failure: Could not Download EQUITY File from NSE for $curdate" >> cron_nse.log;
    fi
    wget -U firefox -P ../DATABASE/DERIV/RAW www.nseindia.com/content/historical/DERIVATIVES/"$year"/"$month"/fo"$day$month$year"bhav.csv.zip
    if [ -f ../DATABASE/DERIV/RAW/fo"$day$month$year"bhav.csv.zip ]; then
        mv ../DATABASE/DERIV/RAW/fo"$day$month$year"bhav.csv.zip ../DATABASE/DERIV/RAW/"$numdate".csv.gz;
        gunzip ../DATABASE/DERIV/RAW/"$numdate".csv.gz;
        echo "Success: Done DERIV File Download for $curdate" >> cron_nse.log;
        python ../QUANT/nsedvdb.py $curdate >> cron_nse.log;
        if [ $? -eq 0 ]; then
            echo "Success: Python DERIV Integration" >> cron_nse.log;
        else
            echo "Failure: Python DERIV Integration" >> cron_nse.log;
        fi
    else
        echo "Failure: Could not Download DERIV File from NSE for $curdate" >> cron_nse.log;
    fi
else
    echo "Note: NO TRADING ON $curdate" >> cron_nse.log;
fi

# Update JSON Database
# ====================================================================
#python ../QUANT/nse2qnt.py
#if [ $? -eq 0 ]; then
#    echo "Success: Python JSON Database Update" >> cron_nse.log;
#else
#    echo "Failure: Python JSON Database Update" >> cron_nse.log;
#fi
#python ../QUANT/nse2img.py
#if [ $? -eq 0 ]; then
#    echo "Success: Python IMG Database Update" >> cron_nse.log;
#else
#    echo "Failure: Python IMG Database Update" >> cron_nse.log;
#fi
#python ../QUANT/nseclear.py
