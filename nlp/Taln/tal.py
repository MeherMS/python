from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import math
import pandas as pd
import numpy as np


#initialiser les listes des critéres
phrases=[]
words=[]
critere0 ={}
critere1 = {}
critere2 ={}
critere3 = {}
critere4 = {}
critere5 = {}
critere6 = {}
critere7 = {}
critere8 = {}
critere9 = {}
critere10 = {}
 

#lire les fichiers nécessaires
f=open("/home/donia/Desktop/Taln/Text.txt", "r" , encoding="utf8")
text = f.read()
f=open("/home/donia/Desktop/Taln/titree.txt", "r" , encoding="utf8")
titre = f.read()
f=open("/home/donia/Desktop/Taln/resume.txt", "r" , encoding="utf8")
resume = f.read()
f=open("/home/donia/Desktop/Taln/bonus.txt", "r" , encoding="utf8")
chB = f.read()
f=open("/home/donia/Desktop/Taln/anapho.txt", "r" , encoding="utf8")
chA = f.read()
f=open("/home/donia/Desktop/Taln/stigma.txt", "r" , encoding="utf8")
chS = f.read()

# definition des fonctions
def label(phrase):
    l={}
    resumes=resume.split("\n")
    if phrase in resumes:
        l[phrase]= 1
    else:
        l[phrase]= 0
    return l
   
def PositionPhTexte(phrase):
    l= {}
    if(text.index(phrase)+1)<=math.ceil(len(text)*1/3):
        l[phrase]=1
    elif(text.index(phrase)+1)<=math.ceil(len(text)*2/3):
        l[phrase]=2
    else:
        l[phrase]=3
    return l
def Nb_mot_titre(phrase,words):
    l={}
    mots=titre.split()
    nb=0
    for w in words:
        nb=nb+mots.count(w)
    l[phrase]=nb
    return l
def Pos_ph_texte():
    l={}
    if text.index(phrase)==0:
        l[phrase]=1
    else:
        l[phrase]=0
    return l
def Pos_ph_parag(phrase):
    l={}
    if text.index(phrase)==0:
        l[phrase]=1
    elif (text.index(phrase)+1)==math.ceil((len(text)*1/3)+1):
        l[phrase]=1
    elif (text.index(phrase)+1)==math.ceil((len(text)*2/3)+1):
        l[phrase]=1
    else:
        l[phrase]=0
    return l
def Nb_exp_bonus(phrase,words):
    l ={}
    nb=0
    for w in words:
        nb=nb+chB.count(w)
    l[phrase]=nb   
    return l
def Nb_exp_stigma(phrase,words):
    l ={}
    nb=0
    for w in words:
        nb=nb+chS.count(w)
    l[phrase]=nb   
    return l
def Mot_anapho(phrase,words):
    l ={}
    if chA.find(words[0]):
        l[phrase]=1
    else:
        l[phrase]=0
    return l
def Idf(phrase,words):
    l={}
    idf=0
    for w in words:
        nb=0
        for p in phrases:
            if p.find(w):
                nb=nb+1
        if nb!=0:
            idf=idf+math.log(nbr_phrase/nb)
    l[phrase]=idf
    return l
def Tf(phrase,words):
    l={}
    nb=0
    t=len(text)
    for w in words:
        nb=nb+(text.count(w)/t)
    l[phrase]=nb
    return l
def IdfTf(tf,idf):
    idfTf ={}
    for key,value in tf.items():
        for k,val in idf.items():
            if key==k:
                idfTf[key]=value*val
    return idfTf
            
#main
phrases=text.split("\n")
nbr_phrase=len(phrases)
for phrase in phrases:
    words=phrase.split(" ")
    critere0.update(label(phrase))
    critere1.update(PositionPhTexte(phrase))
    critere2.update(Nb_mot_titre(phrase,words))
    critere3.update(PositionPhTexte(phrase))
    critere4.update(Pos_ph_parag(phrase))
    critere5.update(Nb_exp_bonus(phrase,words))
    critere6.update(Nb_exp_stigma(phrase,words))
    critere7.update(Mot_anapho(phrase,words))
    critere8.update(Tf(phrase,words))
    critere9.update(Idf(phrase,words))
    critere10.update(IdfTf(critere8,critere9))
#create dataframe
data={"c1":list(critere1.values()),"c2":list(critere2.values()),"c3":list(critere3.values()),"c4":list(critere4.values()),"c5":list(critere5.values()),"c6":list(critere6.values()),"c7":list(critere9.values()),"label":list(critere0.values())}
df= pd.DataFrame.from_dict(data)
df.to_csv(r'data.csv',sep='\t')
X = df.drop('label', axis=1)
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
svclassifier = SVC(kernel='linear')
svclassifier.fit(X_train, y_train)

y_pred = svclassifier.predict(X_test)

f=open("/home/donia/Desktop/Taln/matriceConfusion.txt", "w" , encoding="utf8")
f.write("%s \n" %confusion_matrix(y_test,y_pred))
f.write(" %s" % classification_report(y_test,y_pred))
