from imports import *
from overhead import *
from layout import *

DEBUG = True


@app.callback(
        [Output('table', 'data'), Output('dropdown3','value'), Output('linePlot','figure')],
        [Input('dropdown', 'value'), Input('dropdown2', 'value')])
def dropdownClickHandler(selectedRoom,selectedTrimester):
    global currentRoom
    global currentTrimester
    currentRoom = selectedRoom
    currentTrimester = selectedTrimester
    dfPlotting = dfs[currentRoom]['Média por Trimestre'].set_index("Trimestres")

    plotLineGraph = px.line(
            dfPlotting,
            color_discrete_sequence = px.colors.qualitative.Dark24)
    plotLineGraph.update_traces(line=dict(width=4))

    returnTableData = dfs[currentRoom][currentTrimester].to_dict('records')
    
    return  returnTableData, selectedTrimester, plotLineGraph

def closeLine(s):
    l = s.tolist()
    l.append(l[0])
    return l

def updateMultiPolar(active_cell, selectedTrimester, table_data):
    row = active_cell['row'] 
    global currentTrimester

    layoutPolar = go.Layout(
            legend=dict(x=1,y=0.85),
      margin=go.layout.Margin(
            l=20, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=0, #top margin
        )
    )
    multiPolar = go.Figure(layout = layoutPolar)

    labels = dfs[currentRoom]['Média por Trimestre'].columns[1:]
    sRoomMean = dfs[currentRoom]['Média por Trimestre'].iloc[int(currentTrimester[:1])-1].iloc[1:]

    multiPolar.add_trace(go.Scatterpolar(
        r=closeLine(sRoomMean),
        theta=closeLine(labels),
        fillcolor='red',
        marker=dict(color='red'),
        opacity=0.5,
        name='Média da Turma'
        ))

    multiPolar.add_trace(go.Scatterpolar(
        r=closeLine(dfs[currentRoom][selectedTrimester].iloc[row].iloc[1:]),
        theta=closeLine(labels),
        fillcolor='blue',
        marker=dict(color = 'blue'),
        opacity=0.7,
        name=f"Notas do Aluno"
        ))


    # fig.update_traces(textposition="middle right")

    multiPolar.update_layout(
            width=500, height=500,
            autosize=False,
            # legend_yanchor='middle',
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                    )),
                showlegend=True
                )

    return multiPolar

def updateMultiPolar2(active_cell, table_data):
    row = active_cell['row'] 
    global currentTrimester
    multiPolar2 = go.Figure()

    # labels = dfs[currentRoom]['Gostos pessoais'].loc[:,'Tempo de deslocamento diário':'Tempo investido em séries semanalmente'].columns
    labels = ['Deslocamento','Esportes','Jogos','Leitura(lazer)','Séries/Televisão', 'Deslocamento']
    sRoomMean = dfs[currentRoom]['Gostos pessoais'].loc[:,'Tempo de deslocamento diário':'Tempo investido em séries semanalmente'].mean()
    sGostos = dfs[currentRoom]['Gostos pessoais'].iloc[row].loc['Tempo de deslocamento diário':'Tempo investido em séries semanalmente']

    multiPolar2.add_trace(go.Scatterpolar(
        r=closeLine(sRoomMean),
        theta=labels,
        fillcolor='red',
        marker=dict(color='red'),
        opacity=0.5,
        name='Média da Turma'
        ))

    multiPolar2.add_trace(go.Scatterpolar(
        r=closeLine(sGostos),
        theta=labels,
        fillcolor='blue',
        marker=dict(color = 'blue'),
        opacity=0.7,
        name=f"Aluno"
        ))


    multiPolar2.update_layout(
            width=600, height=600,
            autosize=False,
            polar=dict(
                radialaxis=dict(
                    visible=True
                    # range=[0, 10]
                    )),
                showlegend=True
                )

    return multiPolar2

@app.callback(
        Output('studentLinePlot', 'figure'),
        Input('table', 'active_cell'),
        State('table', 'data'))
def updateStudentLine(active_cell,table_data):
    row = active_cell['row'] 
    dfConcat = pd.DataFrame()
    for el in list(dfs[currentRoom].values())[:-2]:
        dfConcat = pd.concat([dfConcat,el.iloc[row]], axis=1)

    dfConcat = dfConcat.transpose().set_index("Estudante").set_axis(["1º Trimestre","2º Trimestre","3º Trimestre"], axis='index')

    studentLinePlot = px.line(dfConcat,
        color_discrete_sequence = px.colors.qualitative.Dark24)
    studentLinePlot.update_traces(line=dict(width=4))

    return studentLinePlot

@app.callback(
        Output('studentHybridPlot', 'figure'),
        Input('table', 'active_cell'),
        State('table', 'data'))
def updateHybridPlot(active_cell,table_data):
    nrow = active_cell['row'] 
    srTrimesterMean = dfs[currentRoom]["Média por Trimestre"].iloc[int(currentTrimester[0])-1].iloc[1:]
    dfStudent = dfs[currentRoom][currentTrimester].iloc[nrow,1:]
    print(dfStudent.values)
    print(dfStudent.index)

    studentHybridPlot = px.bar(x=dfStudent.index,y=dfStudent.values,
            labels=dict(x="Matérias", y="Nota"),
        color_discrete_sequence = px.colors.qualitative.Dark24)

    studentHybridPlot.add_trace(go.Scatter(x=srTrimesterMean.index,y=srTrimesterMean.values, mode="lines+markers", name="Média da turma"))
    #studentLinePlot.update_traces(line=dict(width=4))

    return studentHybridPlot


@app.callback(
        Output('multiPolar', 'figure'),
        # Output('tabHandler', 'value'),
        Input('table', 'active_cell'),
        Input('dropdown2', 'value'),
        Input('dropdown3', 'value'),
        Input('dropdown', 'value'),
        State('tabHandler', 'value'),
        State('table', 'data'),
        )
def tableClickHandler(active_cell, selectedTrimester, selectedTrimester2, selectedRoom, tabValue, table_data):
    if selectedTrimester != selectedTrimester2:
        trimester = selectedTrimester2
    if tabValue == 'room':
        tabreturn = 'student'
    else:
        tabreturn = tabValue

    return updateMultiPolar(active_cell, selectedTrimester2, table_data)

@app.callback(
        Output('studentPersonalPolar', 'figure'),
        Input('table', 'active_cell'),
        State('table', 'data'))
def personalInfoHandler(active_cell, table_data):
    fig = updateMultiPolar2(active_cell,table_data)

    return fig





@app.callback(
        Output('alunoSelected', 'children'),
        [Input('table', 'active_cell')],
        [State('table', 'data')])
def updateAlunoSelected(active_cell,table_data):
    row = active_cell['row'] 
    name = dfs[currentRoom][currentTrimester].iloc[row].iloc[0]
    return f"{name}"

# @app.callback(Output('tabOutput', 'children'),
              # Input('tabHandler', 'value'))
# def renderTabContent(tab):
    # if tab == 'room':
        # return lineGraph
    # elif tab == 'student':
        # return studentDetail
        
if __name__ == '__main__':
    app.run_server(debug=DEBUG, host='0.0.0.0', port="8052")
