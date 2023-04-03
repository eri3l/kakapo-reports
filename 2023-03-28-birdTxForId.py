# fixing bug in birdTxForId() 
# given (tx_channel, island, (date)), find bird

import numpy as np
import pandas as pd

records = pd.read_csv("dat/processed/records_for_tx_use02.csv", encoding='ISO-8859-1')
tx = pd.read_csv("dat/processed/tx.csv", encoding='ISO-8859-1')

records_head = records.head(1000)

# want records where tx change occured
# want to remove all rows where the transmitterChange columns are NA - not working
# workaround: think that txFrom is *never NA* when a tx change has happened, so drop based only on that
collist = ['harnessChangeOnly', 'newStatus','prox', 'proxOn', 'recoveryID', 'removed', 'txDocId', 'txFrom', 'txId',
           'txLifeExpectancyWeeks', 'txMortality', 'txTo', 'txchangeid', 'vhfHoursOn', 'newTxFineTune', 'hoursOff', 'hoursOn',
           'addedTxFromStatus', 'removedTxFromLastRecordID', 'removedTxFromStatus', 'addedTxFromLastRecordID', 'addedTxFromTxFineTune']
records_head2 = records_head.dropna(subset=['txFrom'])  # NB! txFrom can be NA
records_head3 = records_head.dropna(subset=['txFrom', 'txTo'], how='all') 
# want to check for NA in ALL cols
roha = records[records['birdName'] == 'Roha']
roha_tx = roha.dropna(subset=['txFrom', 'txTo'], how='all')

#region txIdForTxUniqueId
txFrom = "a8db17a5-49d3-4382-b0d8-36d1ee0d5013"
res = tx[tx['id'] == txFrom]
print(res[['channel', 'txId']])
tx_id = res.iloc[0]['txId']

def getTxId(tx_unique):
    res = tx[tx['id'] == tx_unique]
    tx_id = res.iloc[0]['txId']
    tx_channel = res.iloc[0]['channel']
    return(tx_id, tx_channel)

res2 = getTxId(txFrom)

# hack (not sure how to write to new column with a tuple (tx_id, tx_channel))
def getTxId2(tx_unique):
    res = tx[tx['id'] == tx_unique]
    try:
        tx_id = res.iloc[0]['txId']
        return tx_id
    except IndexError:
        return 0

def getTxId3(tx_unique):
    res = tx[tx['id'] == tx_unique]
    try:
        tx_channel = res.iloc[0]['channel']
        return tx_channel
    except IndexError:
        return 0    
# hack end


res2 = getTxId("a8db17a5-49d3-4382-b0d8-36d1ee0d5013")
mytxid = "a8db17a5-49d3-4382-b0d8-36d1ee0d5013"
mytxid = "89df0830-227f-40fc-a342-46014bb9b25e"
print("txId for %s is:" % mytxid, getTxId2(mytxid))
print("txChannel for %s is:" % mytxid, getTxId3(mytxid))

roha_tx['txFromDuskyId'] = roha_tx['txFrom'].apply(getTxId2)    
roha_tx['txChannel'] = roha_tx['txFrom'].apply(getTxId3)        # FIXME: should really be one function together
roha_tx['txToDuskyId'] = roha_tx['txTo'].apply(getTxId2)
roha_tx = roha_tx.sort_values(by='dateTime', ascending=True)

''' next: for a certain datetime, get transmitter and channel
date == 16/09/2020
return (tx_id, channel)

datetime_range = null
16/08/2020 on = dateTime_range[end]
14/08/2021 off = datetime_range[start]

df.loc[df["date"] == "2005-12-22", "AIR_TEMP"]

date_columns = df.filter(regex='Date').columns
df[date_columns] = df[date_columns].apply(pd.to_datetime, format='%d/%m/%Y')

in_between = df.purchaseDate.between(df.releaseDate, df.ceaseDate)
df['status'] = np.where(in_between, 'Active', 'Inactive')
'''
#region find date
#endregion //find date

#region full records
records_tx = records.dropna(subset=['txFrom', 'txTo'], how='all')

records_tx = records_tx.sort_values(by='dateTime', ascending=False)

records_tx['txFromDuskyId'] = records_tx['txFrom'].apply(getTxId2)    
records_tx['txChannel'] = records_tx['txFrom'].apply(getTxId3)        # FIXME: should really be one function together
records_tx['txToDuskyId'] = records_tx['txTo'].apply(getTxId2)

# write to csv so you don't do this every time
# records_tx.to_csv("31-03-2023-records_tx.csv", sep=',', index=False)
# records_new = pd.read_csv("31-03-2023-records_tx.csv")

# test cases
## 1. given a txDuskyId, return list of all records for it
myTxDuskyId = "1149"
tempres = records_tx[records_tx['txFromDuskyId'] == myTxDuskyId]
tempres['birdName'].values[0]
tempres[['birdName', 'island', 'dateTime']].values[0]
tempres.iloc[0]['birdName']

## 2. given a txChannel, return list (birdName, date, txid)
myTxCh = 93
chres = records_tx[records_tx['txChannel'] == myTxCh]
chres['birdName'].values        # array
chres[['birdName', 'island', 'dateTime']].values

#region print a pretty table
from tabulate import tabulate

print(tabulate(chres, headers = chres.columns, tablefmt = 'psql'))
#endregion // print a pretty table

## 3. given a txChannel (or txDuskyId) and island, return bird list
myIsland = "Whenua Hou"
resCase3 = records_tx[(records_tx['txChannel'] == myTxCh ) & (records_tx['island'] == myIsland)]

## 4. given a txChannel (or txDuskyId), island and date return bird list

''' 
jupyter ibnteractive widget
publishing notebooks with plotly
'''
#endregion // full records
