#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 10:07:57 2020
@author: josephquigley
"""

import requests as r
import pandas as pd

#token only lasts one hour
token = ''

dates = [['2019-01-01','2019-06-30'],
         ['2019-07-01','2019-12-31']]

ConsumerProfiles = {'GardasilHCC':'ga%3A133491887',
                    'NexplanonHCC': 'ga%3A119847739',
                    'JanuviaHCC': 'ga%3A116291317',
                    'SteglatroHCC': 'ga%3A194954087',
                    'P23HCC': 'ga%3A132111985',
                    'BelsomraHCC': 'ga%3A119760146'}

brandList = list(ConsumerProfiles.keys())
idList = list(ConsumerProfiles.values())


#keytruda and hcc will require other scripts

payload = {'ids':'ga%3A133491887',
           'start-date':'2019-01-01',
           'end-date':'2019-12-31',''
           'metrics':'ga%3Asessions',
           'dimensions':'ga%3Ametro%2Cga%3AyearMonth%2Cga%3AchannelGrouping',
           'max-results':'10000',
           'output':'json',
           'access_token':token}

#call = 'https://www.googleapis.com/analytics/v3/data/ga'
#report = r.get(call,params=payload)
index = 0
def MAIOpull(brand):
    
    dataList = []
    flatList = []    
    
    for d in dates:
        startDate = d[0]
        endDate = d[1]
        call = 'https://www.googleapis.com/analytics/v3/data/ga?ids='+brand+'&start-date='+startDate+'&end-date='+endDate+'&metrics=ga%3AnewUsers%2Cga%3ApercentNewSessions%2Cga%3Asessions%2Cga%3AbounceRate%2Cga%3AsessionDuration&dimensions=ga%3Aregion%2Cga%3Ametro%2Cga%3Acity%2Cga%3Ayear%2Cga%3Amonth%2Cga%3AchannelGrouping&max-results=10000&output=json&access_token='+token
        report = r.get(call)
        jsonReport = report.json()
        columnNames = []
        for h in jsonReport['columnHeaders']:
            columnNames.append(h['name'])
        data = jsonReport['rows']
        dataList.append(data)
    
    for subList in dataList:
        for item in subList:
            flatList.append(item)
        
    brandframe = pd.DataFrame(flatList,columns=columnNames)    
    brandframe.to_csv('/Users/josephquigley/Desktop/'+brandList[index]+'test.csv')

print('All good up until here!')
    
for b in idList:
    MAIOpull(b)    
    print(brandList[index] + ' generated!')
    index = index + 1