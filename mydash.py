import dash
import dash_table
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

def discrete_background_color_bins(df, n_bins=9, columns='all'):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]

    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
        color = 'white' if i > len(bounds) / 2. else 'inherit'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))



data = pd.read_csv("3201_1c2.csv", sep=",")
data = data.apply(pd.to_numeric)
#new_t = [ "FRA","BIO", "GEO", "HIS", "FIS", "QUI", "FIL",  "SOC", "POR", "MAT", "DES"]
data = data.rename(columns={'Numero':'Estudante'})

dfPolar = pd.DataFrame(dict(
    r=data.iloc[0],
    theta= data.columns))
    
dfPersonal = pd.read_csv("personal.csv", sep = ";")

fig = px.line_polar()
fig2= px.bar()
new_t = ["Estudante", "HIS", "BIO", "QUI", "FIS", "MAT", "DES","FRA","POR", "FIL", "SOC", "GEO"]
data = data.reindex(columns=new_t)
print("reindexed:", data)
print(data.columns)


(styles, legend) = discrete_background_color_bins(data.iloc[:,1:])
app = dash.Dash(__name__)

app.layout = html.Div(children=[
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
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
            ),
        html.Div(children=[
            html.H1(id='studentName'),
                dash_table.DataTable(
                id='studentPersonal',
                columns=[{"name": i, "id":i} for i in dfPersonal.columns],
                data=dfPersonal.to_dict('records'),
                fixed_rows={'headers': True},
                style_table={'height': '300px'},
                style_cell={'textAlign': 'center',
                            'border': '1px solid grey'},
                style_header={
                'backgroundColor': 'white',
                },

                editable=False,
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                style_data_conditional=styles,
                ),
                

            dcc.Graph(id="polarPlot", style={'display': 'inline-block'}),
            dcc.Graph(id="barPlot", style={'display': 'inline-block'})
            ])
        ])

@app.callback(
    Output('polarPlot', 'figure'),
    [Input('table', 'active_cell')],
    [State('table', 'data')])
def update_figure(active_cell, table_data):
    row = active_cell['row']
    value = row+1
    # col = active_cell['column_id']
    dfPolar = pd.DataFrame(dict(
        r=data.iloc[value].loc['HIS':],
        theta= data.columns[1:]))

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
    dfBar =data.iloc[value].loc['HIS':]

    fig2 = px.bar(dfBar, width=600, height=400,range_y=[0,10], labels=False)

    fig2.update_layout(transition_duration=500)

    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)
