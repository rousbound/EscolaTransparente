import pandas as pd
import numpy as np

def rotateList(l, n):
    return l[n:] + l[:n]

dataPath = "data/"

df3201_1T = pd.read_csv(dataPath + "3201_1T.csv", sep=",").apply(pd.to_numeric).fillna(0)
df3201_2T = pd.read_csv(dataPath + "3201_2T.csv", sep=",").apply(pd.to_numeric).fillna(0)
df3202_1T = pd.read_csv(dataPath + "3202_1T.csv", sep=",").apply(pd.to_numeric).fillna(0)
df3202_2T = pd.read_csv(dataPath + "3202_2T.csv", sep=",").apply(pd.to_numeric).fillna(0)

def get3T(df, df2):
    df3 = (df+df2)/2
    def getR(x):
        rr = float(np.random.randint(-40, 40)) / 10
        if x+rr > 10 or x+rr <0:
            return x
        else:
            return x+rr
    df3 = df3.applymap(getR)
    return df3




    
dfPersonal = pd.read_csv(dataPath + "personal.csv", sep = ";")

disciplinas = ["HIS", "BIO", "QUI", "FIS", "MAT", "DES","FRA","POR", "FIL", "SOC", "GEO"]
disciplinas = rotateList(disciplinas, 8)
new_t = ["Estudante"] + disciplinas

df3201_1T = df3201_1T.reindex(columns=new_t)
df3201_2T = df3201_2T.reindex(columns=new_t)
df3202_1T = df3202_1T.reindex(columns=new_t)
df3202_2T = df3202_2T.reindex(columns=new_t)

df3201_3T = get3T(df3201_1T,df3201_2T).round(1)
df3202_3T = get3T(df3202_1T,df3202_2T).round(1)

sNames = pd.read_csv(dataPath + "names.csv")
sNames2 = pd.read_csv(dataPath + "names2.csv")
df3201_1T.Estudante = sNames.Nomes
df3201_2T.Estudante = sNames.Nomes
df3202_1T.Estudante = sNames2.Nomes
df3202_2T.Estudante = sNames2.Nomes
df3201_3T.Estudante = sNames.Nomes
df3202_3T.Estudante = sNames2.Nomes

mean1 = df3201_1T.mean(axis=0,skipna=True)
mean2 = df3201_2T.mean(axis=0,skipna=True)
mean3 = df3201_3T.mean(axis=0,skipna=True)

df3201_Y = pd.concat([mean1,mean2,mean3],axis=1).transpose().set_axis(['1º Trimestre', '2º Trimestre', '3º Trimestre'],axis=0)

mean1 = df3202_1T.mean(axis=0,skipna=True)
mean2 = df3202_2T.mean(axis=0,skipna=True)
mean3 = df3202_3T.mean(axis=0,skipna=True)

df3202_Y = pd.concat([mean1,mean2,mean3],axis=1).transpose().set_axis(['1º Trimestre', '2º Trimestre', '3º Trimestre'],axis=0)

