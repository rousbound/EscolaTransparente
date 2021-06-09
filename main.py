from imports import *
from overhead import *
from layout import *

DEBUG = True

noMarginTop = go.Layout(margin={
        # 'l':0,
        # 'r':0,
        't':0,
        # 'b':0
        })

@app.callback(
        [Output('table', 'data'), Output('plotTrimesterDropdown','value'), Output('linePlot','figure')],
        [Input('tableRoomDropdown', 'value'), Input('tableTrimesterDropdown', 'value')])
def tableRoomDropdownClickHandler(selectedRoom, selectedTrimester):
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

    returnTableData = dfGetTrimester(currentRoom, currentTrimester).to_dict('records')
    
    return  returnTableData, selectedTrimester, plotLineGraph

@app.callback(Output('table', 'style_table'),
                #Input('table', 'active_cell'),
                Input('ToggleView','n_clicks'))
def toggleView(btn1):
    global tableToggleVariable
    if btn1 != 1:
        if tableToggleVariable:
            tempTableStyle = tableStyle.copy()
            tempTableStyle['height'] = '100px'
            tableToggleVariable = False
            return tempTableStyle
        else:
            tableToggleVariable = True
            return tableStyle
    else:
        return tableStyle

def switchStudentsButtonLogic(studentSelectedIndex, button_id, plotIdentifier):
    global currentStudentIndex
    global currentStudentOffset
    if studentSelectedIndex != currentStudentIndex:
        currentStudentOffset[plotIdentifier] = 0
        currentStudentIndex = studentSelectedIndex
    else:
        if button_id == "previousStudentButton":
            currentStudentOffset[plotIdentifier] -= 1
        elif button_id == "nextStudentButton":
            currentStudentOffset[plotIdentifier] += 1
        studentSelectedIndex += currentStudentOffset[plotIdentifier]
        studentSelectedIndex = max(studentSelectedIndex,0)
        studentSelectedIndex = min(studentSelectedIndex,len(dfGetTrimester(currentRoom,currentTrimester))-1)
    return studentSelectedIndex

@app.callback(
        Output('studentLinePlot', 'figure'),
        Input('nextStudentButton', 'n_clicks'),
        Input('previousStudentButton', 'n_clicks'),
        Input('table', 'active_cell'),
        State('table', 'data'))
def updateStudentLine(nextButton, prevButton, active_cell, table_data):
    global currentStudentIndex
    global currentStudentOffset

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    studentSelectedIndex = active_cell['row'] 
    studentSelectedIndex = switchStudentsButtonLogic(studentSelectedIndex, button_id,1)
    print(dfGetTrimester().iloc[studentSelectedIndex,0])


    dfConcat = pd.DataFrame()
    for df in list(dfs[currentRoom].values())[:3]: # Concat first three trimesters 
        dfConcat = pd.concat([dfConcat,df.iloc[studentSelectedIndex]], axis=1)

    dfConcat = dfConcat\
            .transpose()\
            .set_index("Estudante")\
            .set_axis(["1º Trimestre","2º Trimestre","3º Trimestre"], axis='index')

    studentLinePlot = px.line(dfConcat,
        color_discrete_sequence = px.colors.qualitative.Dark24)
    studentLinePlot.update_traces(line=dict(width=4))
    studentLinePlot.update_layout(noMarginTop)

    return studentLinePlot



@app.callback(
        Output('studentHybridPlot', 'figure'),
        Input('nextStudentButton', 'n_clicks'),
        Input('previousStudentButton', 'n_clicks'),
        Input('table', 'active_cell'),
        Input('plotTrimesterDropdown', 'value'),
        State('table', 'data'))
def updateHybridPlot(nextButton, prevButton, active_cell,trimesterFromDropdown,table_data):
    studentSelectedIndex = active_cell['row'] 
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    studentSelectedIndex = switchStudentsButtonLogic(studentSelectedIndex, button_id,0)

    trimester = trimesterFromDropdown if trimesterFromDropdown != currentTrimester else currentTrimester

    srTrimesterMean = dfGetTrimestersMeans(trimester).loc[trimester]
    srStudentTrimester = srGetStudentTrimester(trimester, studentSelectedIndex)
        

    studentHybridPlot = make_subplots(specs=[[{"secondary_y": True}]])
    studentHybridPlot.add_trace(go.Bar(x=srStudentTrimester.index,y=srStudentTrimester.values,
        name="Nota do Aluno"
        # color_discrete_sequence = px.colors.qualitative.Dark24)
        ))

    studentHybridPlot.add_trace(
            go.Scatter(
                x=srTrimesterMean.index,
                y=srTrimesterMean.values,
                mode="lines+markers",
                name="Média da turma",
                # marker=dict(
                    # size=20,
                    # line=dict(
                    # width=5
                    # )
                # ),
                line=dict(width=5)
                )
            )

    studentHybridPlot.add_trace(
            go.Scatter(
                x=srTrimesterMean.index,
                y=[random.randint(5,15) for x in range(len(srTrimesterMean.index))],
                mode="lines+markers",
                name="Faltas",
                # marker=dict(line=dict(
                    # width=1
                    # )
                # )
                ),
            secondary_y=True)
    studentHybridPlot.add_trace(
            go.Scatter(
                x=srTrimesterMean.index,
                y=[random.randint(5,15) for x in range(len(srTrimesterMean.index))],
                mode="lines+markers",
                name="Média de Faltas",
                # marker=dict(line=dict(
                    # width=1
                    # )
                # )
                visible="legendonly"
                ),
            secondary_y=True)


    studentHybridPlot.update_layout(noMarginTop)
    studentHybridPlot.update_yaxes(range=[0,10])
    studentHybridPlot.update_yaxes(range=[0,20], secondary_y=True)


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
