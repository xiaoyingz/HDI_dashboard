import dash
from dash import dcc
from dash import html
import database_mongo
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

data = database_mongo.get_movie_by_country("Germany")
def generate_table(data, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(key) for key in data[0].keys()])
        ),
        html.Tbody([
            html.Tr([
                html.Td(data[i][key]) for key in data[i].keys()
            ]) for i in range(min(len(data), 20))
        ])
    ])

def generate_bar(data, max_bars=10):
    length = min(len(data), max_bars)
    bar_data = {"directors": [data[i]["_id"] for i in range(length)],
                "count": [data[i]["total"] for i in range(length)]
                }
    bar_fig = px.bar(bar_data, x="directors", y="count", barmode="group")
    return dcc.Graph(
                id='bar_chart',
                figure=bar_fig
            )

app.layout = html.Div([
    generate_table(data, 10),

    generate_bar(data, 10)
])


# @app.callback(
#     Output(component_id='my-output', component_property='children'),
#     Input(component_id='my-input', component_property='value')
# )
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)
