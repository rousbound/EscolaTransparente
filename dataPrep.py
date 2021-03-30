import pandas as pd

dataPath = "data/"

df3201_1T = pd.read_csv(dataPath + "3201_1T.csv", sep=",")
df3201_1T = df3201_1T.apply(pd.to_numeric)
df3201_1T = df3201_1T.rename(columns={'Numero':'Estudante'})

dfPolar = pd.DataFrame(dict(
    r=df3201_1T.iloc[0],
    theta= df3201_1T.columns))
    
dfPersonal = pd.read_csv(dataPath + "personal.csv", sep = ";")

new_t = ["Estudante", "HIS", "BIO", "QUI", "FIS", "MAT", "DES","FRA","POR", "FIL", "SOC", "GEO"]
df3201_1T = df3201_1T.reindex(columns=new_t)
