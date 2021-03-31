import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

from colorTableHandling import *
from dataPrep import *



dfCurrentRoom = df3201_1T

fig = px.line_polar()
fig2= px.bar()
multiPolar = go.Figure()
print(dfCurrentRoom.loc[:,'HIS':].mean(axis=0))

(styles, legend) = discrete_background_color_bins(dfCurrentRoom.iloc[:,1:])
app = dash.Dash(__name__)

gradeTable = dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in dfCurrentRoom.columns],
            data=dfCurrentRoom.to_dict('records'),
            fixed_rows={'headers': True},
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'center',
                        'border': '1px solid grey'},
            style_header={
            'backgroundColor': 'white',
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
                style_table={ 'display':'inline-block', 'width':'33%'},
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


polarGraph = dcc.Graph(id="polarPlot", style={'display': 'inline-block', 'width':'33%'})
barGraph = dcc.Graph(id="barPlot", style={'display': 'inline-block', 'width':'33%'})
multiPolarGraph = dcc.Graph(id="multiPolar", style={'display': 'inline-block', 'width':'33%'})

app.layout = html.Div(children=[
    html.Div([gradeTable]),
        html.Div(children=[
            multiPolarGraph,
            polarGraph,
            barGraph])
        ])

@app.callback(
    Output('polarPlot', 'figure'),
    [Input('table', 'active_cell')],
    [State('table', 'data')])
def update_figure(active_cell, table_data):
    row = active_cell['row']
    value = row+1
    dfPolar = pd.DataFrame(dict(
        r=dfCurrentRoom.iloc[value][1:],
        theta= dfCurrentRoom.columns[1:]))

    fig = px.line_polar(dfPolar, range_r=[0,10], r='r', theta='theta', line_close=True)

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('barPlot', 'figure'),
    [Input('table', 'active_cell')],
    [State('table', 'data')])
def update_figure2(active_cell, table_data):
    row = active_cell['row']
    value = row+1
    dfBar =dfCurrentRoom.iloc[value].iloc[1:]

    fig2 = px.bar(dfBar, width=600, height=400,range_y=[0,10], labels=False)

    fig2.update_layout(transition_duration=500)

    return fig2

def closeLine(s):
    s['LAST'] = s[0]
    print(s.tolist())
    return s.tolist()

@app.callback(
    Output('multiPolar', 'figure'),
    [Input('table', 'active_cell')],
    [State('table', 'data')])
def update_figure3(active_cell, table_data):
    row = active_cell['row']
    value = row+1
    multiPolar = go.Figure()

    multiPolar.add_trace(go.Scatterpolar(
          r=closeLine(dfCurrentRoom.iloc[:,1:].mean()),
          theta=dfCurrentRoom.columns[1:],
          fill='toself',
          fillcolor='red',
          # color='red',
          opacity=0.7,
          name='Média da Turma'
    ))

    multiPolar.add_trace(go.Scatterpolar(
          r=closeLine(dfCurrentRoom.iloc[value].iloc[1:]),
          theta=dfCurrentRoom.columns[1:],
          fill='toself',
          fillcolor='blue',
          # color='blue',
          opacity=0.7,
          name=f"Estudante: {dfCurrentRoom.iloc[value].Estudante-1}"
    ))


    multiPolar.update_layout(
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
