# import modules    
import json    
import pandas as pd    
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.express as px



df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dfColor = pd.DataFrame(data=dict(COLOR=['#1f77b4', '#d62728', '#e377c2', '#17becf', '#bcbd22'],
                                VALUE=[1, 2, 3, 4, 5]))

print(df2)

# prepare dash_table    
size = 2
df = pd.DataFrame([], index=range(size))
df['num'] = range(size)
df['char'] = ['1952','1967']
tab = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    style_data_conditional=[{'if': {'row_index': i, 'column_id': 'COLOR'}, 'background-color': dfColor['COLOR'][i], 'color': dfColor['COLOR'][i]} for i in range(dfColor.shape[0])],
    tooltip_data=[
        {
            # (B) multiply cell value by 10 for demonstration purpose
            column: {'value': str(value*10), 'type': 'markdown'}
            for column, value in row.items()
        } for row in df.to_dict('records')
    ],
    tooltip_delay=0,
    tooltip_duration=None
)

# set layout    
app = dash.Dash('SimpleExample', external_stylesheets=external_stylesheets)     
app.layout = html.Div([
    tab,
    dcc.Graph(id='graph-with-slider'),
    html.Div(id='click-data', style={'whiteSpace': 'pre-wrap'}),

])

# define callback        
@app.callback(
    Output('click-data', 'children'),
    [Input('table', 'active_cell')],
    [State('table', 'data')]
)
def display_click_data(active_cell, table_data):
    if active_cell:
        cell = json.dumps(active_cell, indent=2)    
        row = active_cell['row']
        col = active_cell['column_id']
        value = table_data[row][col]
        out = '%s' % (value)
    else:
        out = 'no cell selected'
    return out
 
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('table', 'active_cell')],
    [State('table', 'data')])
def update_figure(active_cell, table_data):
    row = active_cell['row']
    col = active_cell['column_id']
    value = table_data[row][col]
    print(value, type(value))
    filtered_df = df2[df2.year == int(value)]
    print(filtered_df)

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

# run app    
if __name__ == '__main__':
    app.run_server(debug=True)
