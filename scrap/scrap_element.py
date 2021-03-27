#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import selenium
from selenium import webdriver as wb
import pandas as pd
import time


# In[ ]:

#!pip install selenium

df=pd.read_csv('listOflinks_tayara_voiture.csv')
listOflinks=df["listOflinks"].tolist()


# In[ ]:


test=listOflinks[10:15]


# In[ ]:


def check_data(xpath):
    try:
        return wbD.find_element_by_xpath(xpath).text
    except:
        return ''
        


# In[ ]:


from tqdm import tqdm
wbD=wb.Chrome('chromedriver.exe')
alldetails=[]
brand=""
model=""

for i in tqdm(test):
    try:
        wbD.get(i)
    except:
        break;
    
    name = check_data('//*[@id="app"]/div[3]/div/span/div/div[3]/div/div[3]/div[1]/div[2]/div/h1')
    print("--------------->",name)
    
    price= check_data('//*[@id="app"]/div[3]/div/span/div/div[3]/div/div[3]/div[1]/div[2]/div/h2[1]/span')
    print("--------------->",price)
    
    mile_age= check_data('//*[@id="app"]/div[3]/div/span/div/div[3]/div/div[4]/div/div[2]/div/div/div/div[1]/div[2]/div/p')
    print("--------------->",mile_age)
    
    make= check_data('//*[@id="app"]/div[3]/div/span/div/div[3]/div/div[4]/div/div[2]/div/div/div/div[3]/div[2]/div/p')
    print("--------------->",make)
    
    model= check_data('//*[@id="app"]/div[3]/div/span/div/div[3]/div/div[4]/div/div[2]/div/div/div/div[4]/div[2]/div/p')
    print("--------------->",model)
    
    fuel= check_data('//*[@id="app"]/div[3]/div/span/div/div[3]/div/div[4]/div/div[2]/div/div/div/div[5]/div[2]/div/p')
    print("--------------->",fuel)
    
    power= check_data('//*[@id="app"]/div[3]/div/span/div/div[3]/div/div[4]/div/div[2]/div/div/div/div[6]/div[2]/div/p')
    print("--------------->",power)
    
    transmission= check_data('//*[@id="app"]/div[3]/div/span/div/div[3]/div/div[4]/div/div[2]/div/div/div/div[7]/div[2]/div/p')
    print("--------------->",transmission
         )
    engine_size= check_data('//*[@id="app"]/div[3]/div/span/div/div[3]/div/div[4]/div/div[2]/div/div/div/div[8]/div[2]/div/p')
    print("--------------->",engine_size)
    
    description= check_data('/html/body/div[1]/div/span/div/div/div/div[3]/div/span/div/div[3]/div/div[4]/div/div[3]/div/div/p')
    print("--------------->",description)
    temp ={
        'name':name,
        'price':price,
        'mile_age':mile_age,
        'make':make,
        'model':model,
        'fuel':fuel,
        'power':power,
        'transmission':transmission,
        'engine_size':engine_size,
        'description':description,
        'linkofproduct':i}
    alldetails.append(temp)
df1 = pd.DataFrame(alldetails)

