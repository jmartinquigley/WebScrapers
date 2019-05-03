#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:37:56 2019

@author: josephquigley
"""

import requests as r
from bs4 import BeautifulSoup
from json import loads
import re
import pandas as pd

sitePages = ['https://www.januvia.com/',
             'https://www.januvia.com/sitagliptin/what-is-januvia/',
             'https://www.januvia.com/sitagliptin/blood-sugar/',
             'https://www.januvia.com/sitagliptin/how-does-januvia-work/',
             'https://www.januvia.com/sitagliptin/understanding-low-blood-sugar/',
             'https://www.januvia.com/safety-information/',
             'https://www.januvia.com/questions-to-ask-your-doctor/',
             'https://www.januvia.com/special-offers/',
             'https://www.januvia.com/type-2-diabetes/',
             'https://www.januvia.com/type-2-diabetes/information/',
             'https://www.januvia.com/type-2-diabetes/living-with-diabetes/']

siteURLs = []
datalayers = []
page_titles =[]
page_engagementtypes = []
page_contentclassifications = []
page_therapeuticareas = []
page_globalproductnames = []
page_audiences = []
page_regions = []

def PullDatalayer(sitePage):
    html = r.get(sitePage)
    soup = BeautifulSoup(html.text,'html.parser')
    script_text = soup.find('script',text=re.compile('var\s+utag_data')).text.split('=',1)[1]
    datalayer = loads(script_text)
    #datalayers.append(datalayer)
    #return(datalayer)
    page_titles.append(datalayer['page_title'])
    page_engagementtypes.append(datalayer['page_engagementtype'])
    page_contentclassifications.append(datalayer['page_contentclassification'])
    page_therapeuticareas.append(datalayer['page_therapeuticarea'])
    page_globalproductnames.append(datalayer['page_globalproductname'])
    page_audiences.append(datalayer['page_audience'])
    page_regions.append(datalayer['page_region'])
    
for s in sitePages:
    PullDatalayer(s)
    siteURLs.append(s)
    #datalayers.append(datalayer)
print('Initial Datalayers Pulled!')

df = pd.DataFrame({'page_url':siteURLs,
                   'page_title':page_titles,
                   'page_engagementtype':page_engagementtypes,
                   'page_contentclassification':page_contentclassifications,
                   'page_therapeuticarea':page_therapeuticareas,
                   'page_globalproductname':page_globalproductnames,
                   'page_audience':page_audiences,
                   'page_region':page_regions})
        
df.to_csv('/Users/josephquigley/Desktop/Januvia_Datalayer_20190429.csv')