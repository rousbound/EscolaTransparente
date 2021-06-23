from imports import *
buttonCount = 0
dataPath = "data/"

alunoSelected = ""

dfPersonal = pd.read_csv(dataPath + "personal.csv", sep = ";")
df3201 = pd.read_excel(dataPath + "3201.xlsx", sheet_name=None)
df3202 = pd.read_excel(dataPath + "3202.xlsx", sheet_name=None)

dfs = {'3201':df3201,'3202':df3202}

print(df3201.keys())

currentRoom = "3201"
currentTrimester = "1T"
currentStudentOffset = [0,0]
currentStudentIndex = 0


tableToggleVariable = True

fig = px.line_polar()
fig2= px.bar()
multiPolar = go.Figure()
nclicks = 0


def dfGetTrimestersMeans(currentRoom):
    dfTrimesterMeans = dfs[currentRoom]["Média por Trimestre"].set_index("Trimestres")
    return dfTrimesterMeans

def dfGetTrimester(room=currentRoom, trimester=currentTrimester):
    global currentRoom
    global currentTrimester
    dfTrimester = dfs[room][trimester]
    return dfTrimester


def srGetStudentTrimester(trimester,nrow):
    srStudentTrimester = dfs[currentRoom][trimester].iloc[nrow,1:]
    return srStudentTrimester

def dfGetPersonalActivities():
    fileName = currentRoom + "_personal.csv"
    dfPersonalActivities = pd.read_csv(dataPath + currentRoom + "_personal.csv", sep = ";")
    
    cols = [6,7,8,9,10]
    dfPersonalActivities.drop(dfPersonalActivities.columns[cols],axis=1,inplace=True)
    return dfPersonalActivities


def dfGetPersonalActivities(room=currentRoom):
    global currentRoom
    dfPersonalActivities = pd.read_csv(dataPath +  room + "_personal.csv", sep = ";")
    
    cols = [6,7,8,9,10]
    dfPersonalActivities.drop(dfPersonalActivities.columns[cols],axis=1,inplace=True)
    return dfPersonalActivities

placeHolderInitialDf = dfGetTrimester(currentRoom, currentTrimester)
personalActivities = dfGetPersonalActivities(currentRoom)
activities= ['Tempo de Deslocamento', 'Tempo de Prática de Esportes', 'Tempo Jogando Videogames', 'Tempo Investido em Leitura', 'Tempo Assistindo Séries']
