import dash
import pandas
from dash import dcc
from dash import html
from dash import dash_table
import database_mongo
import database_mysql
import schema
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
filters=['country_filter', 'year_filter', 'genre_filter', 'low_rating_filter', 'high_rating_filter', 'sort_dropdown']
def generate_table(country="China", year=2010, genre="Drama", low=1, high=10, order='DESC'):
    if country == '':
        country = None
    if genre == '':
        genre = None
    data = database_mysql.get_movies(country=country, year=year, avg_vote=(low, high), genre=genre, order=order)
    if len(data) == 0:
        return html.Div([
            "No such movies found."
        ])

    return html.Div(className='scrollable', children=[
        str(len(data)) + " movies found.",
        html.Table([
            html.Thead(
                html.Tr([html.Th(key) for key in schema.DISPLAY])
            ),
            html.Tbody([
                html.Tr(
                    id='table_row',
                    children=[
                        html.Td(data[i][key]) for key in schema.DISPLAY
                    ]) for i in range(len(data))
            ])
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


def generate_pie(country="USA"):
    data = database_mysql.group_movies_by_genre(country)
    pie_data = {"genres": [], "counts": []}
    for g, c in list(data.items()):
        pie_data["genres"].append(g)
        pie_data["counts"].append(c)
    pie_fig = px.pie(pie_data, values='counts', names='genres', title='Genre distribution of '+country)
    return pie_fig


def generate_global():
    raw_data = database_mysql.group_movies_by_country()
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
    return global_fig


app.layout = html.Div([
    html.Div(
        id="world_div",
        children=[
            html.H3(
                "Movies in the world:"
            ),
            dcc.Graph(
                id='choropleth_chart',
                figure=generate_global()
    )]),
    html.Div([
        "Country: ",
        dcc.Input(id='country_input', value='USA', type='text'),
        html.Button(id='submit_state', children='Submit', n_clicks=0),
        # dcc.Graph(
        #     id='bar_chart',
        #     figure=generate_bar(max_bars=10)
        # )
        dcc.Graph(
            id='pie_chart',
            figure=generate_pie()
        )
    ]),
    html.H3(
        "Use filters to find movies:"
    ),
    html.Div([
        "Country: ",
        dcc.Input(id='country_filter', value='China', type='text'),
        "Year: ",
        dcc.Input(id='year_filter', value=2010, type='number'),
        "Genre: ",
        dcc.Input(id='genre_filter', value='Drama', type='text'),
        "Lowest average rating: ",
        dcc.Input(id='low_rating_filter', value=1, type='number', step=1, min=1, max=10),
        "Highest average rating: ",
        dcc.Input(id='high_rating_filter', value=10, type='number', step=1, min=1, max=10),
        "Sort: ",
        dcc.Dropdown(
            id="sort_dropdown",
            options=[
                {'label': 'low to high', 'value': 'ASC'},
                {'label': 'high to low', 'value': 'DESC'}
            ],
            value='DESC',
            clearable=False
        ),
        html.Button(id='search_state', children='Search', n_clicks=0)
    ]),
    html.Div(
        id="search_result",
        children=[
            generate_table()
        ]
    )
])


@app.callback(
    Output(component_id='search_result', component_property='children'),
    Input(component_id='search_state', component_property='n_clicks'),
    [State(component_id=f, component_property='value') for f in filters],
)
def update_table(n_clicks, country, year, genre, low, high, order):
    return generate_table(country, year, genre, low, high, order)

@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    Input(component_id='submit_state', component_property='n_clicks'),
    State(component_id='country_input', component_property='value')
)
def update_pie(n_clicks, input_country):
    return generate_pie(input_country)


if __name__ == '__main__':
    app.run_server(debug=True)
