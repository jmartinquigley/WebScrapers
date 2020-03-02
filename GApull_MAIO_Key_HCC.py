#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:39:07 2020

@author: josephquigley
"""
import requests as r
import pandas as pd
import sys

token = ''

dates = [['2019-01-01','2019-06-30'],
         ['2019-07-01','2019-12-2']]

indications = {'nonSmallCellLung': 'non-small-cell-lung-cancer',
               'melanoma': 'melanoma',
               'headNeckSquamous': 'head-and-neck-cancer',
               #'nonMuscleInvasiveBladder': 'non-muscle-invasive-bladder-cancer', doesn't return any results in first half of the year
               'urothelialBladder': 'advanced-urothelial-bladder-cancer',
               'kidney': 'advanced-kidney-cancer',
               'microsatelliteInstability': 'msi-h',
               'classicalHodgkinLymphoma': 'classical-hodgkin-lymphoma',
               'gastric': 'gastric-cancer',
               'cervical': 'cervical-cancer',
               'mediastinalBcell': 'primary-mediastinal-b-cell-lymphoma',
               'liver': 'advanced-hepatocellular-liver-cancer',
               'merkelCellCarcinoma': 'merkel-cell-carcinoma'}
               #'esophageal': 'esophageal-cancer'} doesn't return any results in first half of the year

indicationList = list(indications.keys())
pathList = list(indications.values())

index = 0

def MAIOpull(indication):    
    dataList = []
    flatList = []    
    
    for d in dates:
        startDate = d[0]
        endDate = d[1]
        call = 'https://www.googleapis.com/analytics/v3/data/ga?ids=ga%3A147651117&start-date='+startDate+'&end-date='+endDate+'&metrics=ga%3AnewUsers%2Cga%3ApercentNewSessions%2Cga%3Asessions%2Cga%3AbounceRate%2Cga%3AsessionDuration&dimensions=ga%3Aregion%2Cga%3Ametro%2Cga%3Acity%2Cga%3Ayear%2Cga%3Amonth%2Cga%3AchannelGrouping&filters=ga%3ApagePath!%40hcp%3Bga%3ApagePath%3D%40'+indication+'&max-results=10000&output=json&access_token='+token
        report = r.get(call)
        
        if report.status_code == 200:
            jsonReport = report.json()
            columnNames = []
            for h in jsonReport['columnHeaders']:
                columnNames.append(h['name'])
                data = jsonReport['rows']
                dataList.append(data)
        else:
            print(str(report.status_code)+ ' is the status. Try refreshing your token and try again.')
            sys.exit()
   
    for subList in dataList:
        for item in subList:
            flatList.append(item)
        
    brandframe = pd.DataFrame(flatList,columns=columnNames)    
    brandframe.to_csv('/Users/josephquigley/Desktop/'+indicationList[index]+'_HCC.csv')

for p in pathList:
    MAIOpull(p)   
    print(indicationList[index] + ' generated!')
    index = index+1