import dash
import pandas
from dash import dcc
from dash import html
import database_mongo
import schema
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)

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

def generate_bar(country="USA", max_bars=10):
    data = database_mongo.get_movie_by_country(country)
    length = min(len(data), max_bars)
    bar_data = {"directors": [data[i]["_id"] for i in range(length)],
                "count": [data[i]["total"] for i in range(length)]
                }
    bar_fig = px.bar(bar_data, x="directors", y="count", barmode="group")
    return bar_fig

def generate_global():
    raw_data = database_mongo.group_movie_by_country()
    for d in raw_data:
        prev_key = d['_id']
        d['iso_alpha'] = schema.NAME_ISO[prev_key]
    country_group = pandas.DataFrame(raw_data)

    global_fig = px.choropleth(country_group, locations="iso_alpha",
                    locationmode="ISO-3",
                    scope="world",
                    color=np.log10(country_group['total']),
                    hover_name="_id",
                    hover_data=["total"],
                    color_continuous_scale=px.colors.diverging.BrBG_r,
                    custom_data=["_id"])

    max_total = max(country_group["total"])
    global_fig.update_layout(coloraxis_colorbar=dict(
        title="Number of movies",
        tickvals=[0,1,2,3,np.log10(max_total)],
        ticktext=["1", "10", "100", "1000", str(max_total)],
    ))
    # global_widget = go.FigureWidget(global_fig)
    # global_widget.on_click(updata_bar)
    return global_fig

app.layout = html.Div([
    dcc.Graph(
        id='choropleth_chart',
        figure=generate_global()
    ),
    html.Div([
        "Country: ",
        dcc.Input(id='country_input', value='USA', type='text'),
        html.Button(id='submit_state', children='Submit', n_clicks=0),
        dcc.Graph(
            id='bar_chart',
            figure=generate_bar(max_bars=10)
        )
    ])
])


@app.callback(
    Output(component_id='bar_chart', component_property='figure'),
    Input(component_id='submit_state', component_property='n_clicks'),
    State(component_id='country_input', component_property='value')
)
def update_bar(n_clicks, input_country):
    return generate_bar(input_country, 10)


if __name__ == '__main__':
    app.run_server(debug=True)
