from imports import *
from overhead import *
import flask
import base64

global means
global values
tabs_styles = {
        'height': '44px'
        }

(styles, legend) = discrete_background_color_bins(placeHolderInitialDf.iloc[:,1:])
styles.append({'if': {'column_id': 'Estudante'}, 'width': '15%'})
external_stylesheets = ['assets/style.css']
app = dash.Dash(__name__,external_stylesheets = external_stylesheets)
app.title= "EscolaTransparente"

def getSeparatedLists(df):
    alunos = df.iloc[:, 0].tolist()
    deslocamento = df.iloc[:, 1].tolist()
    esporte = df.iloc[:, 2].tolist()
    jogo = df.iloc[:, 3].tolist()
    leitura = df.iloc[:, 4].tolist()
    series = df.iloc[:, 5].tolist()
    return alunos, deslocamento, esporte, jogo, leitura, series

def groupedBarPlot(df):
    alunos, deslocamento, esporte, jogo, leitura, series = getSeparatedLists(df)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=alunos,
                    y=deslocamento,
                    name=activities[0],
                    marker_color='rgb(120,198,232)'
                    ))
    fig.add_trace(go.Bar(x=alunos,
                    y=esporte,
                    name=activities[1],
                    marker_color='rgb(85,191,212)'
                    ))
    fig.add_trace(go.Bar(x=alunos,
                    y=jogo,
                    name=activities[2],
                    marker_color='rgb(113,71,181)'
                    ))
    fig.add_trace(go.Bar(x=alunos,
                    y=leitura,
                    name=activities[3],
                    marker_color='rgb(178,131,235)'
                    ))
    fig.add_trace(go.Bar(x=alunos,
                    y=series,
                    name=activities[4],
                    marker_color='rgb(228,141,235)'
                    ))
    fig.update_layout(
        #autosize=False,
        #width=1200,
        title="Extracurricular Activities",
        xaxis_title="Alunos",
        yaxis_title="Tempo em horas"
    )
    
    return fig

def getBarPlotActivities(df1, activities):
    
    figBar = go.Figure()
    figBar.add_trace(go.Bar(
        x=df1.iloc[:, 0],
        y=df1.iloc[:, 1],
        name=activities[0],
        orientation='v',
        marker=dict(
            color='rgba(216,171,242, 0.6)',
            line=dict(color='rgba(216,171,242, 1.0)', width=1)
        )
    ))
    figBar.add_trace(go.Bar(
        #x=df1['Nome_Aluno'],
        x=df1.iloc[:, 0],
        y=df1.iloc[:, 2],
        name=activities[1],
        orientation='v',
        marker=dict(
            color='rgba(154,131,244, 0.6)',
            line=dict(color='rgba(154,131,244, 1.0)', width=1)
        )
    ))
    figBar.add_trace(go.Bar(
        #x=df1['Nome_Aluno'],
        x=df1.iloc[:, 0],
        y=df1.iloc[:, 3],
        name=activities[2],
        orientation='v',
        marker=dict(
            color='rgba(244,150,118, 0.6)',
            line=dict(color='rgba(244,150,118, 1.0)', width=1)
        )
    ))
    figBar.add_trace(go.Bar(
        #x=df1['Nome_Aluno'],
        x=df1.iloc[:, 0],
        y=df1.iloc[:, 4],
        name=activities[3],
        orientation='v',
        marker=dict(
            color='rgba(20,206,163, 0.6)',
            line=dict(color='rgba(20,206,163, 1.0)', width=1)
        )
    ))
    figBar.add_trace(go.Bar(
        #x=df1['Nome_Aluno'],
        x=df1.iloc[:, 0],
        y=df1.iloc[:, 5],
        name=activities[4],
        orientation='v',
        marker=dict(
            color='rgba(166,234,102, 0.6)',
            line=dict(color='rgba(166,234,102, 1.0)', width=1)
        )
    ))
    figBar.update_layout(barmode='stack',
        title="Extracurricular Activities",
        xaxis_title="Alunos",
        yaxis_title="Tempo em horas")
    return figBar

def getMeans(df):
    valuesM = []
    for i in range(1,6):
        valuesM.append(np.mean(df.iloc[:, i].tolist()))
    return valuesM

#means = getMeans(personalActivities)

def createDonutPlot(df):
    means = getMeans(df)
    fig = go.Figure(data=[go.Pie(labels=activities, values=means, hole=.3)])
    return fig

def createIndividualDonut(actv, values, nome):
    fig = go.Figure(data=[go.Pie(labels=actv, values=values, hole=.3)])
    fig.update_layout(title="Extracurricular Activities - "+nome)
    return fig

def multipleViolinPlots(df, activities):
    fig = go.Figure()
    colors = ['lightcoral', 'lightseagreen', 'aquamarine', 'lightgoldenrodyellow', 'lightsteelblue']
    for i in range(5):
        fig.add_trace(go.Violin(y=df[activities[i]], box_visible=True, line_color='black',
                               meanline_visible=True, fillcolor=colors[i], opacity=0.6,
                               x0=activities[i], name=activities[i]))
    return fig

def ridgelinePlot(df):
    alunos, deslocamento, esporte, jogo, leitura, series = getSeparatedLists(df)

    data = [deslocamento, esporte, jogo, leitura, series]
    colors = n_colors('rgb(5, 200, 200)', 'rgb(113,71,181)', 5, colortype='rgb')
    fig = go.Figure()
    i = 0
    for data_line, color in zip(data, colors):
        fig.add_trace(go.Violin(x=data_line, line_color=color, name = activities[i]))
        i = i+1

    fig.update_traces(orientation='h', side='positive', width=3, points=False)
    fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
    return fig

def clevelantPlotIndividual(values, actv, means, nome):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=actv,
        y=values,
        marker=dict(color="crimson", size=20),
        mode="markers",
        name='Aluno: '+nome,
    ))
    fig.add_trace(go.Scatter(
        x=actv,
        y=means,
        marker=dict(color="darkturquoise", size=20),
        mode="markers",
        name="Média Turma",
    ))
    fig.update_layout(title="Extracurricular Activities",
                      xaxis_title="Atividades",
                      yaxis_title="Tempo em horas")

    return fig

def hybridPlotIndividual(actv, values, means, nome):
    fig = go.Figure()
    colors = ['aqua', 'lightseagreen', 'aquamarine', 'lightgoldenrodyellow', 'lightsteelblue']
    colors1 = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure']
    colors2 = ['beige', 'bisque', 'black', 'blanchedalmond', 'blue']
    for i in range (5):
        fig.add_trace(go.Bar(x=[actv[i]], y=[values[i]],marker_color=colors[i], name=actv[i], marker_line_color='black'))
    fig.add_trace(go.Scatter(
        x=actv,
        y=means,
        marker=dict(color="crimson", size=20),
        mode="markers",
        name="Média Turma")
    )
    fig.update_layout(title="Extracurricular Activities - "+nome)
    return fig

def plotRadarIndividual(actv, values, means, nome):
    fig = go.Figure()
    actv.append(actv[0])
    values.append(values[0])
    means.append(means[0])
    fig.add_trace(go.Scatterpolar(r=values, theta=actv, 
                                  #fill='toself',
                                  name='Aluno: '+ nome))
    
    fig.add_trace(go.Scatterpolar(
          r=means,
          theta=actv,
          #fill='toself',
          name='Média Turma'
    ))
    
    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, max(max(values), max(means))]
        )),
      showlegend=True
    )

    fig.update_layout(title="Extracurricular Activities - "+nome)
    return fig

tableStyle = {
            # 'height': '300px',
            'height': '700px',
            'overflowY': 'auto',
            'margin-left' : '20px',
            # 'margin-right' : '30px'
            }

gradeTable = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in placeHolderInitialDf.columns],
        data=placeHolderInitialDf.to_dict('records'),
        fixed_rows={'headers': True},
        style_table=tableStyle,
        style_cell={'textAlign': 'center',
            'border': '1px solid grey',
            'fontWeight': 'bold'
            },
        style_header={
            'backgroundColor': 'white',
            'width': '30px',
            'maxWidth': '20px',
            },

        editable=False,
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        style_data_conditional=styles
        )


plotLineGraph = px.line(placeHolderInitialDf.iloc[:,1:],
        color_discrete_sequence = px.colors.qualitative.Dark24)

plotLineGraph.update_traces(line=dict(width=4))

studentLinePlot = dcc.Graph(id = "studentLinePlot",
                            style={'width':"100%"},
                            config={
                                    'displayModeBar': False
                                }
                            )
studentPersonalPolar = dcc.Graph(id = "studentPersonalPolar",
                                style={'width':"50%"},
                                
                                )
studentHybridPlot = dcc.Graph(id="studentHybridPlot",
        style={'margin-left':'-90px'},
        config={
                'displayModeBar': False
            }
        )

barGraph = dcc.Graph(id="barPlot",
        style={'display': 'inline-block',
            'width':'33%',
            'margin-bottom':'25px'})
multiPolarGraph = dcc.Graph(id="multiPolar",
        style={'display': 'inline-block',
                'width':'50%'},
                config={
                        'displayModeBar': False
                    }
        )
lineGraph = dcc.Graph(figure = plotLineGraph,
        id="linePlot",
        style={'display': 'inline-block',
            'width':'50%',
            'margin-left':'450px',
            'margin-right':'100px'})

lineChart = dcc.Graph(id="line-chart",
        style={'display': 'inline-block',
        'width':'100%'})

barPlotActivities = dcc.Graph(figure=getBarPlotActivities(personalActivities, personalActivities.columns[1:].tolist()),
        id = 'barPlotActivities',
        style={'display': 'inline-block',
        'width':'100%'})

groupedBPlot = dcc.Graph(figure=groupedBarPlot(personalActivities),
        id = 'groupedBarPlotActivities',
        style={'display': 'inline-block',
        'width':'100%'})

checkListActivities = dcc.Checklist(
            id="checklist",
            options=[{"label": x, "value": x} for x in personalActivities.columns[1:].tolist()],
            value= personalActivities.columns[1:].tolist()[3:],
            labelStyle={'display': 'inline-block'})

donutPlot = dcc.Graph(figure=createDonutPlot(personalActivities),
        id = 'donutPlot',
        style={'display': 'inline-block',
        'width':'65%'})

violinPlot = dcc.Graph(figure=multipleViolinPlots(personalActivities, personalActivities.columns[1:].tolist()),
        id = 'violinPlot',
        style={'display': 'inline-block',
        'width':'50%'})

ridgedPlot = dcc.Graph(figure=ridgelinePlot(personalActivities),
        id = 'ridgePlot',
        style={'display': 'inline-block',
        'width':'50%'})
clevelandPlot = dcc.Graph(id="clevelandPlot",
        style={'display': 'inline-block',
                'width':'50%'},
        config={
            'displayModeBar': False
        })
individualDonutPlot = dcc.Graph(id="indDonutPlot",
        style={'display': 'inline-block',
                'width':'50%'},
        config={
            'displayModeBar': False
        })
individualHybridPlot = dcc.Graph(id="hybridInd",
        style={'display': 'inline-block',
                'width':'50%'},
        config={
            'displayModeBar': False
        })
individualRadarPlot = dcc.Graph(id="radarInd",
        style={'display': 'inline-block',
                'width':'50%'},
        config={
            'displayModeBar': False
        })

toggleViewButton = html.Button('Ocultar/Mostrar Tabela', id='ToggleView', n_clicks=1, style={'margin-left':'10px'})

nextStudentButton = html.Button('Próximo Aluno', id='nextStudentButton', n_clicks=1, style={'margin-left':'10px'})
previousStudentButton = html.Button('Aluno Anterior', id='previousStudentButton', n_clicks=1, style={'margin-left':'10px'})



tableRoomDropdown = dcc.Dropdown(
        id='tableRoomDropdown',
        options=[
            {'label': 'Turma 3201', 'value': '3201'},
            {'label': 'Turma 3202', 'value': '3202'}

            ],
        value = "3201",
        placeholder= "Escolha a Turma",
        style={'float': 'left', 'width':'200px', 'margin-right':'10px'}
        )
tableTrimesterDropdown = dcc.Dropdown(
        id='tableTrimesterDropdown',
        options=[
            {'label': '1º Trimestre', 'value': '1T'},
            {'label': '2º Trimestre', 'value': '2T'},
            {'label': '3º Trimestre', 'value': '3T'}

            ],
        value="1T",
        placeholder= "Escolha o Trimestre",
        style={'float': 'left','width':'200px'}
        )
plotTrimesterDropdown = dcc.Dropdown(
        id='plotTrimesterDropdown',
        options=[
            {'label': '1º Trimestre', 'value': '1T'},
            {'label': '2º Trimestre', 'value': '2T'},
            {'label': '3º Trimestre', 'value': '3T'}

            ],
        value='1T',
        placeholder= "Escolha o Trimestre",
        style={'float': 'center','width':'200px', 'margin-left':'40px'}
        )


    # LAYOUT

studentDetail = html.Div(style = {
                # 'margin-top':'-30px'
                    }, 
    children=[
    html.Div(id = "studentGraphs", children=[
        html.Div( # Student
            className = 'row',children=[
                html.Div([
                    html.Div(
                        [html.H3("Gráfico Polar",style={'text-align':'center'}),
                            multiPolarGraph,
                            plotTrimesterDropdown],
                            className = 'five columns',
                            style={'margin-left':'100px',
                                'margin-top':'10px',
                                'border': '1px solid-black'
                                }
                            ),
                    html.Div(
                        html.Center([
                            html.H3("Gráfico de Linha", style={'text-align':'center'}),
                            studentLinePlot],
                            style={
                                #'margin-top': '-60px',
                                'margin-top':'60px',
                                'margin-right': '20px',
                                'margin-left': '-60px'
                                }
                            ),
                        className= 'five columns'
                        )],style={
                            'margin-top':'-0px'
                            }
                        ),

                ]
            ),
        ])
    ]
            )


studentPersonal = html.Div([
    html.Div(studentPersonalPolar, style={'display':'block',
        'margin-left':'300px',
        })
    ], style={'display':'block'}
    )

alunoHeader = html.Div(style={'display':'inline-block'},
                    children= [html.Img(src=app.get_asset_url('student.jpg'), style={'height':"10%",'width':"10%"}),
                        html.H3("",id="studentSelectedName"),
                        html.H3("",id="studentSelectedAge"),
                        ])

app.layout = html.Div(children=[
    html.Div([tableRoomDropdown,
        tableTrimesterDropdown,
        toggleViewButton,
        previousStudentButton,
        nextStudentButton
        ],
        className = 'row',
        style = {
            "margin-left":"30px",
            "margin-bottom":"20px",
            "margin-top":"20px"}),
        # Room
        html.Div([gradeTable], id = "gradeTable"),
        dcc.Tabs(id = "tabHandler", style= tabs_styles, value='room', children = 
            [
                dcc.Tab(label='Sala', value='room',
                    #children = [html.Div(lineGraph, style={})]
                    children = [html.Div(lineGraph, style={}),
                        html.H3(
                            children='Atividades Extracurriculares',
                            style={
                                'textAlign': 'center',
                                'color': '#7FDBFF'
                            }
                        ),
                        html.Div([
                            checkListActivities,
                            lineChart
                        ]), 
                        html.Div([
                            html.H5(
                                children='Stacked Bar Plot - Atividades Extracurriculares em Horas x Aluno',
                                style={
                                    'textAlign': 'center',
                                    'color': '#9a83f4'
                                }
                            ),
                            barPlotActivities
                        ]),
                        html.Div([
                            html.H5(
                                children='Grouped Bar Plot - Atividades Extracurriculares em Horas x Aluno',
                                style={
                                    'textAlign': 'center',
                                    'color': '#9a83f4'
                                }
                            ),
                            groupedBPlot
                        ]),
                        html.Div([
                            html.Center([
                            html.H5(
                                children='Donut Plot - Atividades Extracurriculares da Turma',
                                style={
                                    'textAlign': 'center',
                                    'color': '#9a83f4'
                                }
                            ),
                            donutPlot])
                        ]),
                        html.Div([
                            html.H5(
                                children='Violin e Rigged Plot - Atividades Extracurriculares da Turma',
                                style={
                                    'textAlign': 'center',
                                    'color': '#9a83f4'
                                }
                            )
                        ]),
                        violinPlot, ridgedPlot
                    ]
                    ),
                dcc.Tab(label='Aluno - Acadêmico', value='student',
                    children = [
                        #alunoHeader,
                        studentDetail]
                    ),
                dcc.Tab(label='Aluno - Pessoal', value='studentPersonal',
                    #children = [studentPersonal]
                    children = [clevelandPlot, individualDonutPlot,
                    html.Div([
                            html.H5(
                                children='Hybrid e Radar Plot - Atividades Extracurriculares do Aluno',
                                style={
                                    'textAlign': 'center',
                                    'color': '#9a83f4'
                                }
                            )
                        ]),
                        individualHybridPlot,individualRadarPlot]
                    )
                ]
            )
        ])
