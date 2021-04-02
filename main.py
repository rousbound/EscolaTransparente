import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from colorTableHandling import *
# from dataPrep import *

buttonCount = 0
dataPath = "data/"

alunoSelected = ""

external_stylesheets = ['assets/style.css']


dfPersonal = pd.read_csv(dataPath + "personal.csv", sep = ";")
df3201 = pd.read_excel(dataPath + "3201.xlsx", sheet_name=None)
df3202 = pd.read_excel(dataPath + "3202.xlsx", sheet_name=None)
print("df3201:",df3201['1T'])

dfs = {'3201':df3201,'3202':df3202}

currentRoom = "3201"
currentTrimester = "1T"

fig = px.line_polar()
fig2= px.bar()
multiPolar = go.Figure()

(styles, legend) = discrete_background_color_bins(dfs[currentRoom][currentTrimester].iloc[:,1:])
app = dash.Dash(__name__,external_stylesheets = external_stylesheets)

gradeTable = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dfs[currentRoom][currentTrimester].columns],
        data=dfs[currentRoom][currentTrimester].to_dict('records'),
        fixed_rows={'headers': False},
        style_table={'height': '300px',
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
            'width': '50px',
            },

        editable=False,
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        style_data_conditional=styles)

plotLineGraph = px.line(dfs[currentRoom]['Média por Trimestre'].iloc[:,1:], color_discrete_sequence = px.colors.qualitative.Dark24)
plotLineGraph.update_traces(line=dict(width=4))
barGraph = dcc.Graph(id="barPlot", style={'display': 'inline-block', 'width':'33%', 'margin-bottom':'25px'})
multiPolarGraph = dcc.Graph(id="multiPolar", style={'display': 'inline-block', 'width':'50%'})
lineGraph = dcc.Graph(figure = plotLineGraph,
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
dropdown3 = dcc.Dropdown(
        id='dropdown3',
        options=[
            {'label': '1º Trimestre', 'value': '1T'},
            {'label': '2º Trimestre', 'value': '2T'},
            {'label': '3º Trimestre', 'value': '3T'}

            ],
        value=None,
        placeholder= "Escolha o Trimestre",
        style={'float': 'left','width':'200px'}
        )


alunoHeader = html.H1("",id="alunoSelected",
        style={'margin-top':'50px',
            # 'margin-left':'230px',
            # 'margin-bottom':'-50px',
            'text-align':'center'})

        # LAYOUT

app.layout = html.Div(children=[
    html.Div([dropdown,
        dropdown2],
        className = 'row',
        style = {
            "margin-left":"30px",
            "margin-bottom":"30px",
            "margin-top":"30px"}),
        html.Div([gradeTable,lineGraph], id = "gradeTable"),
        html.Div(id = "studentGraphs", children=[
            alunoHeader,
            html.Div( className = 'row',children=[
                html.Div(personalTable, className = 'five columns'),
                html.Div([multiPolarGraph,html.Div(dropdown3,
                    style={
                        'margin-left': '160px',
                        'margin-right': 'auto'})],
                    className = 'five columns'),
                html.Button("Voltar", id='closeStudent', n_clicks=0)
                ])], style={'display':'inline'}),

            ])

@app.callback([Output('studentGraphs', 'style'),
    Output('gradeTable', 'style')],
    [Input('closeStudent', 'n_clicks'),
        Input('table', 'active_cell')])
def studentGraphHandler(btn, active_cell):
    global buttonCount
    print(active_cell)
    print(btn,buttonCount)
    if btn == buttonCount:
        buttonCount += 1
        print("Hiding studentGraphs")
        return {'display':'none'}, {'display':'block'}
    elif active_cell != None:
        print("Displaying studentGraphs")
        return {'display': 'block'},{'display':'none'}

@app.callback(
        [Output('table', 'data'), Output('dropdown3','value'), Output('linePlot','figure')],
        [Input('dropdown', 'value'), Input('dropdown2', 'value')])
def update_table(selectedRoom,selectedTrimester):
    global currentRoom
    global currentTrimester
    currentRoom = selectedRoom
    currentTrimester = selectedTrimester

    plotLineGraph = px.line(dfs[currentRoom]['Média por Trimestre'].iloc[:,1:], color_discrete_sequence = px.colors.qualitative.Dark24)
    plotLineGraph.update_traces(line=dict(width=4))

    return dfs[currentRoom][currentTrimester].to_dict('records'), {'value':selectedTrimester}, plotLineGraph


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
    name = dfs[currentRoom][currentTrimester].iloc[row].iloc[0]
    return f"{name}"


@app.callback(
        Output('multiPolar', 'figure'),
        [Input('table', 'active_cell')],
        [State('table', 'data')])
def update_figure3(active_cell, table_data):
    row = active_cell['row'] 
    global currentTrimester
    multiPolar = go.Figure()

    labels = dfs[currentRoom]['Média por Trimestre'].columns[1:]
    sRoomMean = dfs[currentRoom]['Média por Trimestre'].iloc[int(currentTrimester[:1])-1].iloc[1:]
    print(sRoomMean)

    multiPolar.add_trace(go.Scatterpolar(
        r=closeLine(sRoomMean),
        theta=closeLine(labels),
        fillcolor='red',
        marker=dict(color='red'),
        opacity=0.5,
        name='Média da Turma'
        ))

    multiPolar.add_trace(go.Scatterpolar(
        r=closeLine(dfs[currentRoom][currentTrimester].iloc[row].iloc[1:]),
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
