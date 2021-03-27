#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#get_ipython().system('pip install mysql-connector-python')


# In[1]:


import pandas as pd 
import numpy as np
#import matplotlib.pyplot as plt
#from sklearn.model_selection import train_test_split
from datetime import datetime
import random


# In[2]:


import mysql.connector
from mysql.connector import Error
records=[]
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='optimatets',
                                         user='root',
                                         password='')
    sql_select_Query=[]
    sql_select_Query.append( "select * from bookings")
    sql_select_Query.append("select * from vehicles")
    for req in sql_select_Query:
        cursor = connection.cursor()
        cursor.execute(req)
        records.append( cursor.fetchall())    

except Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if (connection.is_connected()):
        connection.close()
        cursor.close()
        print("MySQL connection is closed")


# In[3]:


bookings=pd.DataFrame(records[0],columns=['id', 'book_type', 'promo_id' , 'type_id' , 'accept_status', 'total_weight', 'company_id', 'date_time', 'user_id', 'vehicle_id', 'driver_id', 'customer_id', 'pickup', 'dropoff', 'duration', 'pickup_addr', 'dest_addr','note', 'travellers', 'status', 'payment', 'created_at', 'updated_at', 'deleted_at'])
vehicles=pd.DataFrame(records[1],columns=['id', 'department_id', 'company_id', 'make', 'model', 'type', 'year', 'group_id', 'lic_exp_date', 'reg_exp_date', 'vehicle_image', 'engine_type', 'horse_power', 'color', 'vin', 'license_plate', 'mileage', 'in_service', 'user_id', 'created_at', 'updated_at', 'deleted_at', 'int_mileage', 'type_id'])


# <h1> adress data normalisation <h1>

# In[4]:


region=['Tunis','Manouba','ben arous',
        'ariana',' Bizerte','beja', 'jandouba', 'nabeul' , 'zaghouane', 'silana', 'kef' ,
        'kasserine' , 'kairouane' , 'Sousse' , 'monastir', 'Mahdia' , 'Sfax' , 'sidi' 'bouzid' , 'gafsa' ,
        'touzeur', 'kbeli' , 'gabes' , 'mednine' ,'tataouine']
region=[x.upper() for x in region]
destination_adress= bookings['dest_addr'] 
depart_adress = bookings['pickup_addr']

def adressNormalisation(col):
    i=0
    lista=[]
    adr=''
    for phrase in col:
        verif=False
        for adrs in region:
            if adrs in phrase.upper():
                verif=True
                adr=adrs
        if verif==True :
                #lista.append([i,phrase,adr])
                lista.append([adr])

        else : 
                #lista.append([i,phrase,random.choice(region)])
                lista.append([random.choice(region)])


        i=i+1


    return pd.DataFrame(lista, columns=['new_'+col.name])

bookings['pickup_addr']=adressNormalisation(bookings['pickup_addr'])
bookings['dest_addr']=adressNormalisation(bookings['dest_addr'])


# In[5]:


def  maxDate(df):
    lista=[]
    for i in range(len(df['date_time'])):
        lista.append(datetime.timestamp(df['date_time'][i]))
    return max(lista)

def addRow(df1,date_time):
    row = df1.sample()
    row['date_time']=date_time
    df1=df1.append(row)
    return df1
            

def fillDatabase(df1):
    now = datetime.timestamp(datetime.now())
    max_date=maxDate(df1)+ 76522
    day = max_date
    cpt=0
    while now> day :
        day=day+86400
        max_date=day+random.randint(39600,86339)
        df1=addRow(df1,datetime.fromtimestamp(max_date))
        cpt=cpt+1
        
        for i in range(random.randint(0,5)):
            max_date=day+random.randint(21600,39600)
            #print(datetime.fromtimestamp(max_date))
            df1=addRow(df1,datetime.fromtimestamp(max_date))
            cpt=cpt+1
            
            for j in range(random.randint(0,3)):
                max_date=day+random.randint(0,21600)
                #print(datetime.fromtimestamp(max_date))
                df1=addRow(df1,datetime.fromtimestamp(max_date))
                cpt=cpt+1
                
    print(cpt ,"rows added !")        
   
                    
                
       
    return df1
   
def getVihicleByAdress(df2, adress):
    df2=df2.dropna(subset=["vehicle_id"])
    df2=df2.groupby('pickup_addr')['vehicle_id'].apply(list)
    x=list(set(df2[adress]))
    return random.choice(x)
 
for i in range(len(bookings['vehicle_id'])):
    if np.isnan(bookings['vehicle_id'].values[i]):
        bookings['vehicle_id'].values[i]=getVihicleByAdress(bookings,bookings['pickup_addr'].iloc[i])    
  


# In[6]:


bookings=fillDatabase(bookings)  
bookings.shape


# In[7]:


df = pd.DataFrame()
df['Datetime'] = bookings['date_time']
for i in range(len(bookings)):
    
    bookings['Year'] = df.Datetime.dt.year
    bookings['Month'] = df.Datetime.dt.month
    bookings['Day'] = df.Datetime.dt.day


# In[8]:


bookings[["Month"]]


# In[9]:


def filter_by_date(dataframe,date):
    filtred_df =pd.DataFrame()
    date1=date.split("-")
    if len(date1) == 3 :
        filtred_df=dataframe.loc[(dataframe["Year"] == int(date1[0])) & (dataframe["Month"] == int(date1[1])) & (dataframe["Day"] == int(date1[2]))]
    if len(date1) == 2 :
        filtred_df=dataframe.loc[(dataframe["Year"] == int(date1[0])) & (dataframe["Month"] == int(date1[1]))]
    if len(date1) == 1 :
        filtred_df=dataframe.loc[(dataframe["Year"] == int(date1[0]))]
   
    return filtred_df    
    


# In[10]:



import mysql.connector
from mysql.connector import Error

def get_best_vehicles(dataframe):
    best_vehicle=dataframe.groupby(['vehicle_id']).count().reset_index()[['vehicle_id','id']].sort_values(by=['id'],ascending=False).reset_index()
    return best_vehicle

def get_vehicle(id):
    try:
        connection = mysql.connector.connect(host='localhost',
                                         database='optimatets',
                                         user='root',
                                         password='')
        records=[]  
        sql_select_Query=[]
        vihicle=[]     
        reqet = "SELECT department_id,company_id,make,model,type_id FROM vehicles WHERE id='" + str(id) + "';"
        sql_select_Query.append(reqet)
        for req in sql_select_Query:
            cursor = connection.cursor()
            cursor.execute(req)
            ex=cursor.fetchall()[0]
            msg="this vihicle of the company : "+str(ex[1])+" , departement : "+str(ex[0]) +" with the make : "+ ex[2]+" and a model : "+ex[3]
            records.append(ex)    
            vihicle.append({'message':msg,'type_id':ex[4]})
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
    return(vihicle)


def get_vehicles(ids,vtn):
    try:
        connection = mysql.connector.connect(host='localhost',
                                         database='optimatets',
                                         user='root',
                                         password='')
        records=[]  
        sql_select_Query=[]
        vihicle=[]
        for i in ids:        
            reqet = "SELECT department_id,company_id,make,model,type_id FROM vehicles WHERE id='" + str(i) + "';"
            sql_select_Query.append(reqet)
        c=0
        for req in sql_select_Query:
            cursor = connection.cursor()
            cursor.execute(req)
            ex=cursor.fetchall()[0]
            msg= ex[2]+" departement "+str(ex[0]) +" company "+str(ex[1])
            records.append(ex)    
            vihicle.append({'message':msg,'numberTransaction':int(vtn[c])})
            c=c+1
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
    
    return(vihicle)


def getBestVehicles(dataframe,date):
    ids=[]
    date1=date.split("-") 
    vehicles_transaction_number=[]
    df=filter_by_date(dataframe,date)    
    best_vehicle=get_best_vehicles(df)
    i=0
    while (i<6) and (i<len(best_vehicle)): 
        ids.append(best_vehicle['vehicle_id'][i])
        vehicles_transaction_number.append(best_vehicle['id'][i])
        i=i+1
    if len(best_vehicle)> 0:
        return get_vehicles(ids, vehicles_transaction_number)
    else: 
        return [{}]





getBestVehicles(bookings,"2020-2") 


# In[11]:


def getBookingsTransaction(dataframe,date):
    result=[]
    date1=date.split("-")
    booking=pd.DataFrame()
    
    if len(date1) == 3 :
        df=filter_by_date(dataframe,date1[0]+"-"+date1[1])
        booking=df['Day'].value_counts()
        transaction=df[(df.status == 3)]
        trans=transaction['Day'].value_counts()
        trans1= pd.Series(trans, index =booking.index).replace(np.nan,0)
        if trans1.empty:
            trans1 = pd.Series(0, index =booking.index)
        for i in range(len(booking)) :
            result.append({"day":int(booking.index[i]),"booking":int(booking.values[i]),"transaction":int(trans1.values[i])})
        result = sorted(result, key=lambda k: k['day'])
    
    
    if len(date1) == 2 :
        df=filter_by_date(dataframe,date)
        booking=df['Day'].value_counts()
        transaction=df[(df.status == 3)]
        trans=transaction['Day'].value_counts()
        trans1= pd.Series(trans, index =booking.index).replace(np.nan,0)
        if trans1.empty:
            trans1 = pd.Series(0, index =booking.index)
        for i in range(len(booking)) :
            result.append({"day":int(booking.index[i]),"booking":int(booking.values[i]),"transaction":int(trans1.values[i])})
        result = sorted(result, key=lambda k: k['day']) 
    
        
    if len(date1) == 1 :
        booking=dataframe['Year'].value_counts()
        transaction=dataframe[(dataframe.status == 3)]
        trans=transaction['Year'].value_counts()
        for i in range(len(booking)) :
            result.append({"year":int(booking.index[i]),"booking":int(booking.values[i]),"transaction":int(trans.values[i])})
        result = sorted(result, key=lambda k: k['year'])    
            
    
    
    return result

getBookingsTransaction(bookings,'2019-7')
    


# In[12]:


def getReg(dataframe,date,l):
    result=[]
    switcher={1:'Year',2:'Month',3:'Day',}
    df=filter_by_date(dataframe,date)
    dest_number=df['dest_addr'].value_counts()
    pick_number=df['pickup_addr'].value_counts()
    frame = {'des': dest_number, 'pick': pick_number } 
    region_frame=pd.DataFrame(frame).fillna(0)
    for i in range(len(region_frame)):
        result.append({switcher[l]:date,"region":region_frame.index[i],"destination_number":int(region_frame.des[i]),"pickup_number":int(region_frame.pick[i])})
    return result
    
def getRegion(dataframe,date):
    result=[]
    date1=date.split("-")
    region_frame=pd.DataFrame()
    
    if len(date1) == 3 :
        result=getReg(dataframe,date,len(date1))
        
    if len(date1) == 2 :
        result=getReg(dataframe,date,len(date1))
        
    if len(date1) == 1 :
        result=getReg(dataframe,date,len(date1))
        
    return result
            
getRegion(bookings,"2019")     


# In[13]:


def getGoodWeight(dataframe,date):
    result=[]
    date1=date.split("-")
    df=filter_by_date(dataframe,date)
    total=df['total_weight'].sum()
    
    if len(date1) == 3 :
        result.append({"day":date,"total_weight":total})
        
    if len(date1) == 2 :
        goo=df[['Day','total_weight']].groupby(['Day']).sum()
        for i in range(len(goo)) :
            result.append({"day":int(goo.index[i]),"total_weight":int(goo.values[i])})
        result = sorted(result, key=lambda k: k['day'])  
        
    if len(date1) == 1 :
        goo=df[['Month','total_weight']].groupby(['Month']).sum()
        for i in range(len(goo)) :
            result.append({"month":int(goo.index[i]),"total_weight":int(goo.values[i])})
        result = sorted(result, key=lambda k: k['month']) 
        
    return result
getGoodWeight(bookings,"2020")    


# In[ ]:


from flask import Flask, request, make_response
import json
import sys
app = Flask(__name__)
@app.route('/', methods=['POST'])
def index():
    
    sys.stdout.flush()
    res=[]
    d = request.form.to_dict() # data recived from form
    d1=d
    if (d1['typy'] =='transaction'):
        res=getBookingsTransaction(bookings,d1['date'])
    if (d1['typy'] =='region'):
        res=getRegion(bookings,d1['date'])
    if (d1['typy'] =='goods'):
        res=getGoodWeight(bookings,d1['date'])
    if (d1['typy'] =='vehicle'):
        res=getBestVehicles(bookings,d1['date'])
    
    else:
        print("verif type of chart ")
    data=make_response(json.dumps(res))
 
    resp=data
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*' # configiration 
   
    print(d, flush=True)

    print(res)
    return resp


    
    
    
if __name__ == "__main__":
    app.run()
    

