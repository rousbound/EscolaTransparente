from imports import *
from overhead import *
from layout import *

DEBUG = True
global df1 
df1 = personalActivities

noMarginTop = go.Layout(margin={
        # 'l':0,
        # 'r':0,
        't':0,
        # 'b':0
        })

def closeLine(s):
    l = s.tolist()
    l.append(l[0])
    return l

@app.callback(
        Output('studentSelectedName','children'),
        Output('studentSelectedAge','children'),
         Input('table', 'active_cell'),
         Input('nextStudentButton', 'n_clicks'),
         Input('previousStudentButton', 'n_clicks'),
         )
def updateStudentHeader(active_cell, nextButton, prevButton):
    global currentStudentIndex
    # studentSelectedIndex = active_cell['row'] if active_cell else 0
    return dfGetTrimester(currentRoom, currentTrimester).iloc[currentStudentIndex,0], "23 Anos"



@app.callback(
        [Output('multiPolar','figure'), Output('clevelandPlot','figure'), Output('indDonutPlot','figure'),
        Output('hybridInd','figure'), Output('radarInd','figure')],
        [Input('table', 'active_cell'),
         Input('tableRoomDropdown', 'value'),
         Input('tableTrimesterDropdown', 'value'),
         Input('plotTrimesterDropdown', 'value'),
         Input('nextStudentButton', 'n_clicks'),
         Input('previousStudentButton', 'n_clicks'),
         ])
def updateMultiPolar(active_cell, selectedTrimester, table_data, trimesterFromDropdown, nextButton, prevButton):
    global df1
    studentSelectedIndex = active_cell['row'] if active_cell else 0
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    studentSelectedIndex = switchStudentsButtonLogic(studentSelectedIndex, button_id,0)

    trimester = trimesterFromDropdown if trimesterFromDropdown != currentTrimester else currentTrimester

    srTrimesterMean = dfGetTrimestersMeans(currentRoom).loc[trimester]
    srStudentTrimester = srGetStudentTrimester(trimester, studentSelectedIndex)

    labels = srStudentTrimester.index
    sRoomMean = dfGetTrimestersMeans(currentRoom).loc[currentTrimester]


    layoutPolar = go.Layout(
            legend=dict(x=1,y=0.85),
      margin=go.layout.Margin(
            #l=20, #left margin
            #r=0, #right margin
            #b=0, #bottom margin
            #t=0, #top margin
         l=100, #left margin
            r=100, #right margin
            b=100, #bottom margin
            t=100, #top margin       
        )
    )
    multiPolar = go.Figure(layout = layoutPolar
           
            )

    multiPolar.add_trace(go.Scatterpolar(
        r=closeLine(sRoomMean),
        theta=closeLine(labels),
        fillcolor='red',
        marker=dict(color='red'),
        opacity=0.5,
        name='Média da Turma'
        ))

    multiPolar.add_trace(go.Scatterpolar(
        r=closeLine(srStudentTrimester.values),
        theta=closeLine(labels),
        fillcolor='blue',
        marker=dict(color = 'blue'),
        opacity=0.7,
        name=f"Notas do Aluno"
        ))


    # fig.update_traces(textposition="middle right")

    multiPolar.update_layout(
            width=900, height=500,
            autosize=False,
            # legend_yanchor='middle',
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                    )),
                showlegend=True
                )

    multiPolar.add_layout_image(
        dict(
            source="assets/polar_background4.png",
            xref="paper",
            yref="paper",
            #sizex=img_width,
            #sizey=img_height,
            #x=-1.9,
            #y=4.5,
            x=0.52,
            y=0.5,
            sizex=1.35,
            sizey=1.35,
            opacity=1.0,
            xanchor="center",
            yanchor="middle",
            layer="below")
)
    multiPolar.update_layout(template="plotly")   

    personalActivities = dfGetPersonalActivities(currentRoom)
    actv = personalActivities.columns[1:].tolist()
    df1 = personalActivities
    means = getMeans(df1)
    alunos, deslocamento, esporte, jogo, leitura, series = getSeparatedLists(df1)
    i = studentSelectedIndex
    values = [deslocamento[i], esporte[i], jogo[i], leitura[i], series[i]]
    nome = alunos[i]
    clevPlot = clevelantPlotIndividual(values, actv, means, nome)

    indDonut = createIndividualDonut(actv, values, nome)
    hybridPlot = hybridPlotIndividual(actv, values, means, nome)
    radarPlot = plotRadarIndividual(actv, values, means, nome)
    return multiPolar, clevPlot, indDonut, hybridPlot, radarPlot

#,Output('checklist', 'value')
@app.callback(
        [Output('table', 'data'), Output('table','columns'), Output('plotTrimesterDropdown','value'), Output('linePlot','figure'),
        Output('checklist', 'value'), Output('barPlotActivities','figure'), Output('groupedBarPlotActivities', 'figure')],
        [Input('tableRoomDropdown', 'value'), Input('tableTrimesterDropdown', 'value')])
def tableRoomDropdownClickHandler(selectedRoom, selectedTrimester):
    global currentRoom
    global currentTrimester
    global df1
    currentRoom = selectedRoom
    currentTrimester = selectedTrimester
    dfTrimestersMeans = dfGetTrimestersMeans(currentRoom)
    print(currentRoom)
    print(dfTrimestersMeans)

    plotLineGraph = px.line(
            dfTrimestersMeans,
            color_discrete_sequence = px.colors.qualitative.Dark24)
    plotLineGraph.update_traces(line=dict(width=4))
    plotLineGraph.update_yaxes(range=[0,10])

    sortedDf = dfTrimestersMeans\
                    .loc[currentTrimester]\
                    .sort_values(ascending=False)

    sortedLabels = sortedDf.index.tolist()
    print(sortedDf)
    print(sortedLabels)

    dfTable = dfGetTrimester(currentRoom, currentTrimester)[['Estudante'] + sortedLabels]
    print(dfTable)
    returnTableData = dfTable.to_dict('records')
    
    columns = [{"name": i, "id": i} for i in dfTable.columns]
    
    personalActivities = dfGetPersonalActivities(currentRoom)
    df1 = personalActivities
    value= df1.columns[1:].tolist()[3:]

    figStackedBarPlot=getBarPlotActivities(personalActivities, personalActivities.columns[1:].tolist())

    figGroupedBP = groupedBarPlot(personalActivities)
    

    return  returnTableData, columns, selectedTrimester, plotLineGraph, value, figStackedBarPlot, figGroupedBP

@app.callback(Output('table', 'style_table'),
                #Input('table', 'active_cell'),
                Input('ToggleView','n_clicks'))
def toggleView(btn1):
    global tableToggleVariable
    if btn1 != 1:
        if tableToggleVariable:
            tempTableStyle = tableStyle.copy()
            tempTableStyle['height'] = '0px'
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
    # currentStudentIndex = studentSelectedIndex
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
    studentSelectedIndex = active_cell['row'] if active_cell else 0
    studentSelectedIndex = switchStudentsButtonLogic(studentSelectedIndex, button_id,1)


    dfConcat = pd.DataFrame()
    for df in list(dfs[currentRoom].values())[:3]: # Concat first three trimesters 
        dfConcat = pd.concat([dfConcat,df.iloc[studentSelectedIndex]], axis=1)

    dfConcat = dfConcat\
            .transpose()\
            .set_index("Estudante")\
            .set_axis(["1º Trimestre","2º Trimestre","3º Trimestre"], axis='index')

    print("CONCAT:",dfConcat)
    dfConcat.index.name = "Trimestres"
    studentLinePlot = px.line(dfConcat, 
        color_discrete_sequence = px.colors.qualitative.Dark24)
    studentLinePlot.update_traces(line=dict(width=4))
    studentLinePlot.update_layout(noMarginTop)
    studentLinePlot.update_yaxes(title_text="Nota do aluno")

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

    srTrimesterMean = dfGetTrimestersMeans(currentRoom).loc[trimester]
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
    name = dfGetTrimester(currentRoom, currentTrimester).iloc[row].iloc[0]
    return f"{name}"

@app.callback(
    Output("line-chart", "figure"), 
    [Input("checklist", "value")])
def update_line_chart(activity):
    global df1
    #fig = px.line(df1, x="Nome_Aluno", y=activity)
    fig = px.scatter(df1, x="Nome_Aluno", y=activity,
        title="Atividades Extracurriculares",
        labels={"value":"Tempo em horas", "Nome_Aluno":"Alunos"})
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=DEBUG, host='0.0.0.0', port="8052")
