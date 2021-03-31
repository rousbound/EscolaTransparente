import pandas as pd

def rotateList(l, n):
    return l[n:] + l[:n]

dataPath = "data/"

df3201_1T = pd.read_csv(dataPath + "3201_1T.csv", sep=",")
df3201_1T = df3201_1T.apply(pd.to_numeric)
df3201_1T = df3201_1T.rename(columns={'Numero':'Estudante'})

dfPolar = pd.DataFrame(dict(
    r=df3201_1T.iloc[0],
    theta= df3201_1T.columns))
    
dfPersonal = pd.read_csv(dataPath + "personal.csv", sep = ";")

disciplinas = ["HIS", "BIO", "QUI", "FIS", "MAT", "DES","FRA","POR", "FIL", "SOC", "GEO"]

disciplinas = rotateList(disciplinas, 8)
new_t = ["Estudante"] + disciplinas

df3201_1T = df3201_1T.reindex(columns=new_t)
