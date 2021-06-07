from imports import *
from overhead import *
from layout import *

DEBUG = True

def dfGetTrimestersMeans(trimester):
    dfTrimesterMeans = dfs[currentRoom]["Média por Trimestre"].set_index("Trimestres")
    return dfTrimesterMeans

def dfGetTrimester(trimester=currentTrimester):
    dfTrimester = dfs[currentRoom][currentTrimester]
    return dfTrimester


def srGetStudentTrimester(trimester,nrow):
    srStudentTrimester = dfs[currentRoom][trimester].iloc[nrow,1:]
    return srStudentTrimester

@app.callback(
        [Output('table', 'data'), Output('plotTrimesterDropdown','value'), Output('linePlot','figure')],
        [Input('tableRoomDropdown', 'value'), Input('tableTrimesterDropdown', 'value')])
def tableRoomDropdownClickHandler(selectedRoom,selectedTrimester):
    global currentRoom
    global currentTrimester
    currentRoom = selectedRoom
    currentTrimester = selectedTrimester
    dfTrimestersMeans = dfGetTrimestersMeans(currentTrimester)

    plotLineGraph = px.line(
            dfTrimestersMeans,
            color_discrete_sequence = px.colors.qualitative.Dark24)
    plotLineGraph.update_traces(line=dict(width=4))
    plotLineGraph.update_yaxes(range=[0,10])

    returnTableData = dfGetTrimester(currentTrimester).to_dict('records')
    
    return  returnTableData, selectedTrimester, plotLineGraph


@app.callback(
        Output('studentLinePlot', 'figure'),
        Input('table', 'active_cell'),
        State('table', 'data'))
def updateStudentLine(active_cell,table_data):
    row = active_cell['row'] 
    dfConcat = pd.DataFrame()
    for df in list(dfs[currentRoom].values())[:3]: # Concat first three trimesters 
        dfConcat = pd.concat([dfConcat,df.iloc[row]], axis=1)

    dfConcat = dfConcat\
            .transpose()\
            .set_index("Estudante")\
            .set_axis(["1º Trimestre","2º Trimestre","3º Trimestre"], axis='index')

    studentLinePlot = px.line(dfConcat,
        color_discrete_sequence = px.colors.qualitative.Dark24)
    studentLinePlot.update_traces(line=dict(width=4))

    return studentLinePlot


@app.callback(
        Output('studentHybridPlot', 'figure'),
        Input('table', 'active_cell'),
        Input('plotTrimesterDropdown', 'value'),
        State('table', 'data'))
def updateHybridPlot(active_cell,trimesterFromDropdown,table_data):
    studentSelectedIndex = active_cell['row'] 
    trimester = trimesterFromDropdown if trimesterFromDropdown != currentTrimester else currentTrimester

    srTrimesterMean = dfGetTrimestersMeans(trimester).loc[trimester].iloc[1:]
    srStudentTrimester = srGetStudentTrimester(trimester, studentSelectedIndex)
        

    studentHybridPlot = px.bar(x=srStudentTrimester.index,y=srStudentTrimester.values,
            labels=dict(x="Matérias", y="Nota"),
        color_discrete_sequence = px.colors.qualitative.Dark24)

    studentHybridPlot.add_trace(go.Scatter(x=srTrimesterMean.index,y=srTrimesterMean.values, mode="lines+markers", name="Média da turma"))

    studentHybridPlot.update_yaxes(range=[0,10])

    return studentHybridPlot


@app.callback(
        Output('alunoSelected', 'children'),
        [Input('table', 'active_cell')],
        [State('table', 'data')])
def updateAlunoSelected(active_cell,table_data):
    row = active_cell['row'] 
    name = dfGetTrimester(currentTrimester).iloc[row].iloc[0]
    return f"{name}"

        
if __name__ == '__main__':
    app.run_server(debug=DEBUG, host='0.0.0.0', port="8052")
