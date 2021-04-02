import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

from colorTableHandling import *
from dataPrep import *

buttonCount = 0

alunoSelected = ""

external_stylesheets = ['assets/style.css']

dfCurrentRoom = df3201_1T

fig = px.line_polar()
fig2= px.bar()
multiPolar = go.Figure()

(styles, legend) = discrete_background_color_bins(dfCurrentRoom.iloc[:,1:])
app = dash.Dash(__name__,external_stylesheets = external_stylesheets)

gradeTable = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dfCurrentRoom.columns],
        data=dfCurrentRoom.to_dict('records'),
        fixed_rows={'headers': False},
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center',
            'border': '1px solid grey'},
        style_header={
            'backgroundColor': 'white',
            'width': '90px'
            },

        editable=False,
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        style_data_conditional=styles
        )

personalTable = dash_table.DataTable(
        id='studentPersonal',
        columns=[{"name": i, "id":i} for i in dfPersonal.columns],
        data=dfPersonal.to_dict('records'),
        # fixed_rows={'headers': True},
        style_table={ 'display':'inline-block',
            'width':'50%',
            'margin-top':'150px',
            'margin-left': '300px'},
        style_cell={'textAlign': 'center',
            'border': '1px solid grey'},
        style_header={
            'backgroundColor': 'white',
            },

        editable=False,
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        style_data_conditional=styles)


barGraph = dcc.Graph(id="barPlot", style={'display': 'inline-block', 'width':'33%', 'margin-bottom':'25px'})
multiPolarGraph = dcc.Graph(id="multiPolar", style={'display': 'inline-block', 'width':'50%'})
lineGraph = dcc.Graph(figure = px.line(df3201_Y),
        id="linePlot", style={'display': 'inline-block', 'width':'50%', 'margin-left':'450px', 'margin-right':'100px'})

dropdown = dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Turma 3201', 'value': '3201'},
            {'label': 'Turma 3202', 'value': '3202'}

            ],
        value = "3201",
        placeholder= "Escolha a Turma",
        style={'float': 'left', 'width':'200px'}
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


alunoHeader = html.H1("",id="alunoSelected",
        style={'margin-top':'50px',
            'margin-left':'230px',
            'margin-bottom':'-50px'})

# linePlot = px.line(df3201_Y)

app.layout = html.Div(children=[
    html.Div([dropdown,
        dropdown2],
        className = 'row',
        style = {"margin-bottom":"30px", "margin-top":"30px"}),
    html.Div([gradeTable]),
    html.Div(id = "studentGraphs", children=[
        alunoHeader,
        html.Div( className = 'row',children=[
            html.Div(personalTable, className = 'five columns'),
            html.Div(multiPolarGraph, className = 'five columns'),
            html.Button("Fechar", id='closeStudent', n_clicks=0)
            ])], style={'display':'inline'}),
    lineGraph

        ])

sRoomMean = dfCurrentRoom.iloc[:,1:].mean()

@app.callback(Output('studentGraphs', 'style'),
        [Input('closeStudent', 'n_clicks'),
            Input('table', 'active_cell')])
def studentGraphHandler(btn, active_cell):
    global buttonCount
    if btn == buttonCount:
        buttonCount += 1
        return {'display':'none'}
    elif active_cell != None:
        return {'display': 'block'}

@app.callback(
        Output('table', 'data'),
        [Input('dropdown', 'value'), Input('dropdown2', 'value')])
def update_table(value1,value2):
    global dfCurrentRoom
    if value1 == "3201":
        if value2 == "1T":
            dfCurrentRoom = df3201_1T
        elif value2 == "2T":
            dfCurrentRoom = df3201_2T
        elif value2 == "3T":
            dfCurrentRoom = df3201_3T
    elif value1 == "3202":
        if value2 == "1T":
            dfCurrentRoom = df3202_1T
        elif value2 == "2T":
            dfCurrentRoom = df3202_2T
        elif value2 == "3T":
            dfCurrentRoom = df3202_3T

    return dfCurrentRoom.to_dict('records')

@app.callback(
        Output('barPlot', 'figure'),
        [Input('table', 'active_cell')],
        [State('table', 'data')])
def update_figure2(active_cell, table_data):
    row = active_cell['row'] 
    notasEstudante = pd.to_numeric(dfCurrentRoom.iloc[row].iloc[1:])
    dfBar = pd.concat([notasEstudante,sRoomMean],axis=1).set_axis(['Média do Estudante','Média da Turma'],axis=1)
    fig2 = px.bar(dfBar, width=800, height=500,range_y=[0,10], labels=True, barmode="group")
    fig2.update_layout(transition_duration=500)

    return fig2

def closeLine(s):
    l = s.tolist()
    l.append(l[0])
    return l


@app.callback(
        Output('alunoSelected', 'children'),
        [Input('table', 'active_cell')],
        [State('table', 'data')])
def updateAlunoSelected(active_cell,table_data):
    row = active_cell['row'] 
    name = dfCurrentRoom.iloc[row].iloc[0]
    return f"Aluno: {name}"


@app.callback(
        Output('multiPolar', 'figure'),
        [Input('table', 'active_cell')],
        [State('table', 'data')])
def update_figure3(active_cell, table_data):
    row = active_cell['row'] 
    multiPolar = go.Figure()

    labels = dfCurrentRoom.columns[1:]

    multiPolar.add_trace(go.Scatterpolar(
        r=closeLine(sRoomMean),
        theta=closeLine(labels),
        fillcolor='red',
        marker=dict(color='red'),
        opacity=0.5,
        name='Média da Turma'
        ))

    multiPolar.add_trace(go.Scatterpolar(
        r=closeLine(dfCurrentRoom.iloc[row].iloc[1:]),
        theta=closeLine(labels),
        fillcolor='blue',
        marker=dict(color = 'blue'),
        opacity=0.7,
        name=f"Notas do Aluno"
        ))


    multiPolar.update_layout(
            width=600, height=600,
            autosize=False,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                    )),
                showlegend=True
                )



    return multiPolar

if __name__ == '__main__':
    app.run_server(debug=True)
