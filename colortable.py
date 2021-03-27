import dash
import dash_table
import dash_html_components as html
import pandas as pd

df = pd.DataFrame(data=dict(COLOR=['#1f77b4', '#d62728', '#e377c2', '#17becf', '#bcbd22'],
                            VALUE=[1, 2, 3, 4, 5]))

app = dash.Dash(__name__)

app.layout = html.Div([

    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        style_data_conditional=[{'if': {'row_index': i, 'column_id': 'COLOR'}, 'color': '#000000', 'color': df['COLOR'][i]} for i in range(df.shape[0])]
    ),

], style=dict(width='100px'))

if __name__ == '__main__':
    app.run_server()
