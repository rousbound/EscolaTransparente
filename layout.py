from imports import *
from overhead import *
import flask
import base64

tabs_styles = {
        # 'height': '44px'
        }

(styles, legend) = discrete_background_color_bins(dfs[currentRoom][currentTrimester].iloc[:,1:])
external_stylesheets = ['assets/style.css']
app = dash.Dash(__name__,external_stylesheets = external_stylesheets)

gradeTable = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dfs[currentRoom][currentTrimester].columns],
        data=dfs[currentRoom][currentTrimester].to_dict('records'),
        fixed_rows={'headers': False},
        style_table={'height': '700px',
            'overflowY': 'auto',
            'margin-left' : '20px',
            # 'margin-right' : '30px'
            },
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

# personalTable = dash_table.DataTable(
        # id='studentPersonal',
        # columns=[{"name": i, "id":i} for i in dfs[currentRoom]['Gostos pessoais'].iloc[0,:].to_frame().columns],
            # data=dfs[currentRoom]['Gostos pessoais'].iloc[0,:].to_frame().to_dict('records'),
        # # fixed_rows={'headers': True},
        # style_table={ 'display':'inline-block',
            # 'width':'50%',
            # 'margin-top':'150px',
            # 'margin-left': '300px'},
        # style_cell={'textAlign': 'center',
            # 'border': '1px solid grey'},
        # style_header={
            # 'backgroundColor': 'white',
            # 'width': '50px',
            # },

        # editable=False,
        # sort_action="native",
        # sort_mode="multi",
        # column_selectable="single",
        # style_data_conditional=styles)



plotLineGraph = px.line(dfs[currentRoom]['Média por Trimestre'].iloc[:,1:],
                        color_discrete_sequence = px.colors.qualitative.Dark24)
plotLineGraph.update_traces(line=dict(width=4))

studentLinePlot = dcc.Graph(id = "studentLinePlot",
                            style={'width':"100%",
                            'margin-top':'80px'})
studentPersonalPolar = dcc.Graph(id = "studentPersonalPolar",
                                style={'width':"50%"})
studentHybridPlot = dcc.Graph(id="studentHybridPlot",
        style={})

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


dropdown = dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Turma 3201', 'value': '3201'},
            {'label': 'Turma 3202', 'value': '3202'}

            ],
        value = "3201",
        placeholder= "Escolha a Turma",
        style={'float': 'left', 'width':'200px', 'margin-right':'10px'}
        )
dropdown2 = dcc.Dropdown(
        id='dropdown2',
        options=[
            {'label': '1º Trimestre', 'value': '1T'},
            {'label': '2º Trimestre', 'value': '2T'},
            {'label': '3º Trimestre', 'value': '3T'}

            ],
        value="1T",
        placeholder= "Escolha o Trimestre",
        style={'float': 'left','width':'200px'}
        )
dropdown3 = dcc.Dropdown(
        id='dropdown3',
        options=[
            {'label': '1º Trimestre', 'value': '1T'},
            {'label': '2º Trimestre', 'value': '2T'},
            {'label': '3º Trimestre', 'value': '3T'}

            ],
        value='1T',
        placeholder= "Escolha o Trimestre",
        style={'float': 'left','width':'200px'}
        )


alunoHeader = html.Center(html.H1("",id="alunoSelected",
    style={'margin-top':'50px',
        # 'margin-left':'230px',
        # 'margin-bottom':'-50px',
        #'text-align':'center'
        }))

    # LAYOUT

studentDetail = html.Div(style = {}, children=[
    html.Div(id = "studentGraphs", children=[
        # alunoHeader,
        # html.Div(
        # html.Button("<< Voltar", id='closeStudent', n_clicks=0),
        # style={#'float':'right',
        # 'margin-left':'160px',
        # 'margin-bottom':'50px'
        # }
        # ),
        # html.Div(
        # html.Center(
        # html.Img(src=app.get_asset_url('student.jpg'),
        # style={'width':'10%','height':'10%'}
        # ),
        # style={'display':'block',
        # 'margin-bottom': '100px',
        # 'margin-top':'100px'})
        # ),
        html.Div( # Student
            className = 'row',children=[
                html.Div([
                    # html.Center(html.H2("Acadêmico"), style={'margin-bottom':'-100px'}),
                    html.Div(
                        [multiPolarGraph,html.Div(dropdown3,
                            style={
                                'margin-top':'-50px',
                                'margin-left': '95px',
                                })],
                            className = 'five columns',
                            style={'margin-left':'300px',
                                'margin-top':'30px'
                                }
                            ),
                    html.Div(
                        html.Center(studentLinePlot,
                            style={
                                'margin-top': '-20px',
                                'margin-right': '260px',
                                'margin-left': '-200px'
                                }
                            ),
                        className= 'five columns'
                        )],style={
                            # 'margin-left':'-100px'
                            'margin-top':'-0px'
                            }
                        ),

                ]
            ),
        ])
    ]
            )


studentPersonal = html.Div([
    # html.Center(html.H2("Pessoal"), style={}),
    html.Div(studentPersonalPolar, style={'display':'block',
        'margin-left':'300px',
        # 'margin-top':'-30px'
        })
    ], style={'display':'block'}
    )

app.layout = html.Div(children=[
    html.Div([dropdown,
        dropdown2],
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
