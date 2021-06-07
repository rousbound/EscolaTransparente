from imports import *
buttonCount = 0
dataPath = "data/"

alunoSelected = ""

dfPersonal = pd.read_csv(dataPath + "personal.csv", sep = ";")
df3201 = pd.read_excel(dataPath + "3201.xlsx", sheet_name=None)
df3202 = pd.read_excel(dataPath + "3202.xlsx", sheet_name=None)

dfs = {'3201':df3201,'3202':df3202}

currentRoom = "3201"
currentTrimester = "1T"

fig = px.line_polar()
fig2= px.bar()
multiPolar = go.Figure()


def dfGetTrimestersMeans(trimester):
    dfTrimesterMeans = dfs[currentRoom]["Média por Trimestre"].set_index("Trimestres")
    return dfTrimesterMeans

def dfGetTrimester(trimester=currentTrimester):
    dfTrimester = dfs[currentRoom][currentTrimester]
    return dfTrimester


def srGetStudentTrimester(trimester,nrow):
    srStudentTrimester = dfs[currentRoom][trimester].iloc[nrow,1:]
    return srStudentTrimester

