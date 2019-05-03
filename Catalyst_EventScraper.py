#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:37:56 2019

@author: josephquigley
"""

import requests as r
from bs4 import BeautifulSoup
import pandas as pd
from ast import literal_eval

sitePages = ['https://www.belsomra.com/belsomra-works-differently/',
             'https://www.belsomra.com/',
             'https://www.belsomra.com/clinical-study-results/',
             'https://www.belsomra.com/savings-coupon/',
             'https://www.belsomra.com/how-to-take-belsomra/',
             'https://www.belsomra.com/side-effects/',
             'https://www.belsomra.com/belsomra-beginnings/',
             'https://www.belsomra.com/belsomra-beginnings/interested/',
             'https://www.belsomra.com/belsomra-beginnings/sleep-habits-quiz/',
             'https://www.belsomra.com/belsomra-beginnings/for-patients/',
             'https://www.belsomra.com/risk-information/',
             'https://www.belsomra.com/how-does-belsomra-work/',
             'https://www.belsomra.com/sitemap/',
             'https://www.belsomra.com/belsomra-beginnings/interested/talk-to-your-doctor/',
             'https://www.belsomra.com/insomnia-treatment/',
             'https://www.belsomra.com/patient',
             'https://www.belsomra.com/savings']
             

descriptions = []
sitePageURLs = []
urls = []
EventDatalayers = []
events = []
actions = []
labels  = []

def PullEvents(sitePage):
    html = r.get(sitePage)
    soup = BeautifulSoup(html.text,'html.parser')
    links = soup.find_all('a')
    for l in links:
        description = l.text
        descriptions.append(description)
        sitePageURLs.append(sitePage)
        url = l.get('href')
        urls.append(url)
        EventDatalayer = l.get('data-tracking-datalayer')
        try:
            EventDatalayer = literal_eval(EventDatalayer)
        except ValueError:
            EventDatalayer = 'No Datalayer'
        EventDatalayers.append(EventDatalayer)

for s in sitePages:
    PullEvents(s)
print('Initial Events Pulled!')

TaggingSheet = pd.DataFrame({"Page URL":sitePageURLs,
                             "Link Text":descriptions,
                             "Link URL":urls,
                             "Event Datalayer":EventDatalayers})

def eventColumns(js_string):
    try:
        events.append(js_string['event_category'])
        actions.append(js_string['event_action'])
        labels.append(js_string['event_label'])
    except TypeError:
        events.append('No Datalayer')
        actions.append('No Datalayer')
        labels.append('No Datalayer')

js_list = TaggingSheet['Event Datalayer']

for js in js_list:
    eventColumns(js)

TaggingSheet['Event'] = events     
TaggingSheet['Action'] = actions
TaggingSheet['Label'] = labels

print('Done!')
        
TaggingSheet.to_csv('/Users/josephquigley/Desktop/Belsomra_Events_20190501.csv')