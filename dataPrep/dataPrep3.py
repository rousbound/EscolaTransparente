import pandas as pd
from appendExcel import *

dataPath = "../data/"

df3201 = pd.read_excel(dataPath + "3201.xlsx", sheet_name=None)
df3202 = pd.read_excel(dataPath + "3202.xlsx", sheet_name=None)

def getRecuperação(df1,df2,df3):
    df1 = df1.iloc[:,1:]
    df2 = df2.iloc[:,1:]
    df3 = df3.iloc[:,1:]
    return (df1*3 + df2*3+df3*4)/10
    
print(df3201)
dfres = df3201["1T"]
dfres.iloc[:,1:] = getRecuperação(df3201["1T"],df3201["2T"],df3201["3T"])
dfres2 = df3202["1T"]
dfres2.iloc[:,1:] = getRecuperação(df3202["1T"],df3202["2T"],df3202["3T"])

#recuperacao = finaldata[finaldata<6].dropna(how="all")

#append_df_to_excel(dataPath + "3201.xlsx", dfres, "MF")
#print(dfres2.iloc[:,:])
#print(dfres2)
#append_df_to_excel(dataPath + "3202.xlsx", dfres2[:,1:], "Média final")

mean1 = df3202['MF'].mean()
print(mean1)

print(df3202['Média por Trimestre'].iloc[:,1:])

df3202['Média por Trimestre'] = df3202['Média por Trimestre'].set_index("Trimestres")
print(df3201['Média por Trimestre'])

df3202['Média por Trimestre'].loc['MF'] = mean1

med = df3202['Média por Trimestre']

append_df_to_excel(dataPath + "3202.xlsx", med, "Média por Trimestre")
