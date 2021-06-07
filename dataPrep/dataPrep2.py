import pandas as pd
import random 


def generatePersonal(dfRoom, roomName):

    dfPersonal = pd.read_csv(dataPath + "personal.csv", sep = ";")

    print(dfRoom)


# print(sNames.tolist())

    columns = dfPersonal.transpose().loc['Chave'].tolist()
    columns.append('Tempo investido em leitura(lazer) semanalmente')
    columns.append('Tempo investido em séries semanalmente')
    rows = dfRoom.iloc[:,0].tolist()
    df = pd.DataFrame(index=rows, columns = columns)
    df = df.fillna(0)

    new_columns = ['Tempo de deslocamento diário',  'Tempo de prática de esportes semanal',  'Tempo de jogo semanal', 'Tempo investido em leitura(lazer) semanalmente', 'Tempo investido em séries semanalmente','Meio de Transporte', 'Matérias preferidas', 'Séries preferidas', 'Preferência exercício físico/esportes','Preferência VideoGames']

    df = df.reindex(columns=new_columns)

    def randomize(x):
        return random.randint(0,30)
    df = df.applymap(randomize)

    transporte = ['Ônibus','A pé','Van','Metrô','Carro','Uber', 'Bicicleta']
    matérias = ["HIS", "BIO", "QUI", "FIS", "MAT", "DES","FRA","POR", "FIL", "SOC", "GEO"]
    series = ["The Office", "Game of Thrones", "Greys anatomy", "Avatar"]
    esportes = ["Futebol", "Vôlei", "Natação", "Nenhum", "Balé", "Academia", "Corrida"]
    jogos = ["DotA2","Lol","Fifa","Fortnite","Minecraft","Xadrez"]

    L = [transporte,matérias,series,esportes,jogos]

    def randList(l):
        return ", ".join(random.sample(l,random.randint(1,len(l)-3)))



    for i in range(0,len(L)):
        df.iloc[:,i+5] = df.iloc[:,i+5].map(lambda x: randList(L[i]))

    df.to_csv(dataPath + f"{roomName}_personal.csv", sep=";")


dataPath = "data/"

df3201 = pd.read_excel(dataPath + "3201.xlsx")
df3202 = pd.read_excel(dataPath + "3202.xlsx")

generatePersonal(df3201, "3201")
generatePersonal(df3202, "3202")
