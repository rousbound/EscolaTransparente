from imports import *
from overhead import *
import flask
import base64

tabs_styles = {
        'height': '44px'
        }

(styles, legend) = discrete_background_color_bins(placeHolderInitialDf.iloc[:,1:])
external_stylesheets = ['assets/style.css']
app = dash.Dash(__name__,external_stylesheets = external_stylesheets)


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
        fixed_rows={'headers': False},
        style_table=tableStyle,
        style_cell={'textAlign': 'center',
            'border': '1px solid grey',
            'fontWeight': 'bold'
            },
        style_header={
            'backgroundColor': 'white',
            'width': '60px'
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
                                style={'width':"50%"})
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
                'width':'50%'})
lineGraph = dcc.Graph(figure = plotLineGraph,
        id="linePlot",
        style={'display': 'inline-block',
            'width':'50%',
            'margin-left':'450px',
            'margin-right':'100px'})


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
        style={'float': 'center','width':'200px'}
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
                        [html.H3("Gráfico Híbrido",style={'text-align':'center'}),
                            studentHybridPlot,
                            plotTrimesterDropdown],
                            className = 'five columns',
                            style={'margin-left':'200px',
                                'margin-top':'10px'
                                }
                            ),
                    html.Div(
                        html.Center([
                            html.H3("Gráfico de Linha", style={'text-align':'center'}),
                            studentLinePlot],
                            style={
                                #'margin-top': '-60px',
                                'margin-top':'30px',
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
                    children = [html.Div(lineGraph, style={})]
                    ),
                dcc.Tab(label='Aluno - Acadêmico', value='student',
                    children = [studentDetail]
                    ),
                dcc.Tab(label='Aluno - Pessoal', value='studentPersonal',
                    children = [studentPersonal]
                    )
                ]
            )
        ])
