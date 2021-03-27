#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd 
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from datetime import datetime
import random


# <h1> get data from database</h1>

# In[6]:


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
    sql_select_Query.append("select * from driver_vehicle")
    sql_select_Query.append("select * from tracking")
    sql_select_Query.append("select * from vehicles")
    sql_select_Query.append("select * from vehicle_types")
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


# In[7]:


bookings=pd.DataFrame(records[0],columns=['id', 'book_type', 'promo_id' , 'type_id' , 'accept_status', 'total_weight', 'company_id', 'date_time', 'user_id', 'vehicle_id', 'driver_id', 'customer_id', 'pickup', 'dropoff', 'duration', 'pickup_addr', 'dest_addr','note', 'travellers', 'status', 'payment', 'created_at', 'updated_at', 'deleted_at'])


# In[8]:


df1=bookings


# <h1> adress data normalisation <h1>

# In[9]:



region=['Tunis','Manouba','ben arous',
        'ariana',' Bizerte','beja', 'jandouba', 'nabeul' , 'zaghouane', 'silana', 'kef' ,
        'kasserine' , 'kairouane' , 'Sousse' , 'monastir', 'Mahdia' , 'Sfax' , 'sidi' 'bouzid' , 'gafsa' ,
        'touzeur', 'kbeli' , 'gabes' , 'mednine' ,'tataouine']
region=[x.upper() for x in region]
destination_adress= df1['dest_addr'] 
depart_adress = df1['pickup_addr']


# In[10]:



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


# In[11]:



def adressToNan(col):
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
                lista.append([np.nan])


        i=i+1


    return pd.DataFrame(lista, columns=['new_'+col.name])


# In[12]:


df1['pickup_addr']=adressNormalisation(df1['pickup_addr'])
df1['dest_addr']=adressNormalisation(df1['dest_addr'])


# In[ ]:





# <h1> fill the nan vehicle_id </h1>
# <h4>this method return a random vihicle_id by adress </h4>

# In[13]:


df2=df1
def getVihicleByAdress(df2, adress):
    df2=df2.dropna(subset=["vehicle_id"])
    df2=df2.groupby('pickup_addr')['vehicle_id'].apply(list)
    x=list(set(df2[adress]))
    return random.choice(x)
 


# In[14]:


df2.groupby('pickup_addr')['vehicle_id'].apply(list)


# In[15]:


for i in range(len(df1['vehicle_id'])):
    if np.isnan(df1['vehicle_id'].iloc[i]):
        df1['vehicle_id'].iloc[i]=getVihicleByAdress(df1,df1['pickup_addr'].iloc[i])


# <h1> prepare train and test data </h1>

# In[16]:


vihicule_id=df1['vehicle_id'].unique()


# In[17]:


df = pd.DataFrame()
df['Datetime'] = df1['date_time']
for i in range(len(df1)):
    
    df['Year'] = df.Datetime.dt.year
    df['Month'] = df.Datetime.dt.month
    df['Day'] = df.Datetime.dt.day
    df['Hour'] = df.Datetime.dt.hour
    #df['Minute'] = df.Datetime.dt.minute


# In[18]:


y=df1[['dest_addr','pickup_addr']]


# In[19]:


x=pd.concat([df[['Year','Day','Month','Hour']],df1['vehicle_id']],sort=False,axis=1)


# In[20]:


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state=1)


# <h1>train model</h1>

# In[21]:



# Compare Algorithms

import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.multioutput import MultiOutputClassifier
# load dataset

# prepare configuration for cross validation test harness
seed = 7
# prepare models
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
# evaluate each model in turn
results = []
names = []
scores = []
scoring = 'accuracy'

for name, model in models:
  
    cv_results = MultiOutputClassifier(model).fit(x_train,y_train)
   
    results.append(cv_results)
    names.append(name)
    msg = "the score of %s  is : %s " % (name, cv_results.score(x_test,y_test))
    scores.append(cv_results.score(x_test,y_test))
    print(msg)
# boxplot algorithm comparison


# In[22]:


def get_model(model):
    models = {
        'LR': 0,
        'LDA': 1,
        'KNN': 2,
        "DT": 3,
        'GNB': 4,
        'SVM': 5,
    }
    return (models.get(model, "Invalid model")) 


# In[23]:



import mysql.connector
from mysql.connector import Error

def get_vehicle(ids,model_name):

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
       
        for req in sql_select_Query:
            cursor = connection.cursor()
            cursor.execute(req)
            ex=cursor.fetchall()[0]
            msg="this vihicle of the company : "+str(ex[1])+" , departement : "+str(ex[0]) +" with the make : "+ ex[2]+" and a model : "+ex[3]
            records.append(ex)    
            vihicle.append({'message':msg,'type_id':ex[4],"score":scores[get_model(model_name)]})
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
    
    return(vihicle)
      


# In[24]:


from flask import Flask, request, make_response
import json
app = Flask(__name__)
@app.route('/', methods=['POST'])
def index():
    
    d = request.form.to_dict() # data recived from form
    date=d['date'].split("T")
    date1=date[0].split("-")
    hours=date[1].split(':')
    date2=list(map(int, date1)) 
    hours2= list(map(int, hours)) 
   
    
    df=pd.DataFrame(columns=['Datatime'],data=np.array(range(len(vihicule_id))))
   
    for i in range(len(vihicule_id)):  
    
        df['Year'] =date1[0]
        df['Month'] =date1[1]
        df['Day'] = date1[2]
        df['Hour'] =int(hours[0])
        
        
    

    xx=pd.concat([df[['Year','Day','Month','Hour']],pd.Series(vihicule_id).rename("id")],sort=False,axis=1) #input data
    result=pd.concat([pd.DataFrame(results[get_model(d['model'])].predict(np.array(xx))),xx],sort=False,axis=1)                 #result of prediction
    result=result.rename(columns={0: 'destination',1:'pickup'})
    ms=result[(result.destination == str( d['destination']).upper()) & (result.pickup == str(d['retour']).upper())] # return only the result of our destination and pickup
        
    if ms.empty:
        vehicles=[{'message': 'there is no vehicles , please change the time or pickup/destination','type_id': -1,'score':scores[get_model(d['model'])]}]
    else:
        
        vehicles= get_vehicle(ms['id'].tolist(),d['model'])       # return the data of vehicles predicted                                                
    
    
   
    
   
    
    print(d)        # data recived from form
    print(result)    # result of the prediction of all vehicles
    print(ms)        # result of the prediction of  vehicle who strat of our pickup and go to destination
    print(vehicles) # the data of vehicle predicted
    
    
    data=make_response(json.dumps(vehicles)) # transform final result to json
    resp=data
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*' # configiration 
    return resp


    
    
    
if __name__ == "__main__":
    app.run()
    


# In[ ]:





# In[ ]:





# In[38]:





# In[ ]:




