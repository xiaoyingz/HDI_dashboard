import dash
import pandas as pd
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc

from database_neo4j import App
import database_mongo
import database_mysql
import schema

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

filters=['country_filter', 'year_filter', 'genre_filter', 'low_rating_filter', 'high_rating_filter', 'sort_dropdown']
def generate_table(country="China", year=2008, genre='Action', low=1, high=10, order='DESC'):
    if country == '':
        country = None
    if genre == '':
        genre = None
    data = database_mysql.get_movies(country=country, year=year, avg_vote=(low, high), genre=genre, order=order)
    if len(data) == 0:
        return html.Div([
            "No such movies found."
        ])
    figure = go.Figure(data=[go.Table(
        header = dict(values = [key for key in schema.DISPLAY], fill_color='paleturquoise',
                align='left'),
        cells = dict(values = [[data[i][key] for i in range(len(data))] for key in schema.DISPLAY], fill_color='lavender',
            align='left')
        )
    ])
    figure.update_layout(width=1900, margin=dict(l=20, r=20, t=20, b=20))
    return html.Div(className='scrollable', children=[
        str(len(data)) + " movies found.",
        dcc.Graph(
            id = 'filter_table',
            figure = figure
        )
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
    country_group = pd.DataFrame(raw_data)

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


overview_component = html.Div([
    html.Div(
        className="row",
        children=[
            html.Div(
                id="world_div",
                className="six columns",
                children=[
                    html.H3(
                        "Movies in the world:"
                    ),
                    dcc.Graph(
                        id='choropleth_chart',
                        figure=generate_global()
            )]),
            html.Div(
                className="six columns",
                children=[
                    dcc.Graph(
                        id='pie_chart',
                        figure=generate_pie()
                    ),
                    "Country: ",
                    dcc.Input(id='country_input', value='USA', type='text'),
                    html.Button(id='submit_state', children='Submit', n_clicks=0)
            ])]
    ),
    html.H3(
        "Use filters to find movies:"
    ),
    html.Div([
        "Country: ",
        dcc.Input(id='country_filter', value='China', type='text'),
        "Year: ",
        dcc.Input(id='year_filter', value=2008, type='number'),
        "Genre: ",
        dcc.Input(id='genre_filter', value='Action', type='text'),
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
    ),
    # html.H3("Check the movie interests you!"),
    # html.Div(id='dummy1'),
    # html.Div(id='dummy2'),
    # html.Div([
    #     "Movie Name: ",
    #     dcc.Input(id='input_movie', value='Million Dollar Baby', type='text')
    # ]),
    # html.H3("Your vote! (From 1 to 10)"),
    # html.Div([
    #     dcc.Input(id='vote', value=0, type='number'),
    #     html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    #     html.Button(id='revoke-button-state', n_clicks=0, children='Revoke'),
    # ]),
    # html.Div(className='row', children=[
    #     html.Div(className='eight columns', children=[
    #         html.H3("Movie details"),
    #         dcc.Graph(id='movie_table')
    #     ]),
    #     html.Div(className='four columns', children=[
    #         html.H3("Vote Distribution"),
    #         dcc.Graph(id="vote_distribution")
    #     ])
    # ]),
    # html.H3("Give the name of the actor/director/producer/composer interests you!"),
    # html.Div([
    #     "Actor/Director/Producer/Composer Name: ",
    #     dcc.Input(id='input_name', value='Clint Eastwood', type='text')
    # ]),
    # dcc.Graph(id='graph-with-slider'),
    # dcc.Slider(
    #     id='year-slider',
    #     min=1900,
    #     max=2021,
    #     value=1990,
    #     marks={str(year): str(year) for year in range(1900,2021,10)},
    #     step=None,
    #     included=False
    # )
])

# @app.callback(
#     Output(component_id='search_result', component_property='children'),
#     Input(component_id='search_state', component_property='n_clicks'),
#     [State(component_id=f, component_property='value') for f in filters],
# )
# def update_table(n_clicks, country, year, genre, low, high, order):
#     return generate_table(country, year, genre, low, high, order)
#
# @app.callback(
#     Output(component_id='pie_chart', component_property='figure'),
#     Input(component_id='submit_state', component_property='n_clicks'),
#     State(component_id='country_input', component_property='value')
# )
# def update_pie(n_clicks, input_country):
#     return generate_pie(input_country)
#
# @app.callback(
#     Output("dummy1", "children"),
#     State("input_movie", "value"),
#     State("vote", "value"),
#     Input("submit-button-state", "n_clicks"))
# def update_table(input_movie, vote, btn1):
#     # print(n_clicks)
#     # print(vote)
#     if btn1>0:
#         temp_dict = database_mysql.get_id_by_name("{}".format(input_movie))
#         if temp_dict!=None:
#             temp_id = temp_dict['imdb_title_id']
#             new_rating = database_mongo.update_rating(temp_id, vote,value = 1)
#             res = database_mysql.update_avg_vote(temp_id, new_rating)
#             print(res)
#             app1 = App()
#             app1.update_rating(temp_id, new_rating)
#             app1.close()
#     return None

# @app.callback(
#     Output("dummy2", "children"),
#     State("input_movie", "value"),
#     State("vote", "value"),
#     Input("revoke-button-state", "n_clicks"))
# def update_table(input_movie, vote, btn2):
#     # print(n_clicks)
#     # print(vote)
#     if btn2>0:
#         temp_dict = database_mysql.get_id_by_name("{}".format(input_movie))
#         if temp_dict!=None:
#             temp_id = temp_dict['imdb_title_id']
#             new_rating = database_mongo.update_rating(temp_id, vote,value = -1)
#             res = database_mysql.update_avg_vote(temp_id, new_rating)
#             print(res)
#             app1 = App()
#             app1.update_rating(temp_id, new_rating)
#             app1.close()
#     return None


# @app.callback(
#     Output('movie_table', 'figure'),
#     Input("input_movie", "value"),
#     Input("dummy1", "children"),
#     Input("dummy2", "children"))
# def update_table(input_movie, n_clicks, adas):
#     movie_dict = database_mysql.get_id_by_name("{}".format(input_movie))
#     if movie_dict==None:
#         fig1=go.Figure(go.Table(
#             header = dict(values=['Movie Not Found'])))
#     else:
#         del movie_dict['metascore']
#         del movie_dict['reviews_from_users']
#         del movie_dict['reviews_from_critics']
#         del movie_dict['usa_gross_income']
#         del movie_dict['imdb_title_id']
#         del movie_dict['description']
#         movie_dict['global_income'] = movie_dict.pop('worldwide_gross_income')
#         movie_dict['company'] = movie_dict.pop('production_company')
#         fig1 = go.Figure(data=[go.Table(
#             header = dict(values = [[i] for i in movie_dict.keys()], fill_color='paleturquoise',
#                     align='left'),
#             cells = dict(values = [[i] for i in movie_dict.values()], fill_color='lavender',
#                 align='left')
#             )
#             ])
#         # fig1.update_layout(width=1900)
#         fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20))
#     return fig1

# @app.callback(
#     Output('vote_distribution', 'figure'),
#     Input("input_movie", "value"),
#     Input("dummy1", "children"),
#     Input("dummy2", "children"))
#
# def update_figure1(input_movie, dummy1,adfasf):
#     temp_dict = database_mysql.get_id_by_name("{}".format(input_movie))
#     if temp_dict==None:
#         fig =  px.bar()
#     else:
#         temp_id = temp_dict['imdb_title_id']
#         data = database_mongo.get_votes_by_id(temp_id)
#         fig =  px.bar(data, x="field", y="value")
#         fig.update_layout(margin=dict(l=0, r=20, t=20, b=20), paper_bgcolor="LightSteelBlue")
#     return fig


# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     Input('year-slider', 'value'),
#     Input("input_name", "value"),
#     Input("dummy1", "children"),
#     Input("dummy2", "children"))
#
# def update_figure(selected_year, input_name, n_clicks,adfds):
#
#     app1 = App()
#     df = app1.find_movie_from_person("{}".format(input_name))
#     app1.close()
#
#     filtered_df = df[df.year >= selected_year]
#
#     fig = px.scatter(filtered_df, x="year", y="rating",
#                  size="rating", color="worktype", hover_name="title",
#                  log_x=False, size_max=10)
#
#     fig.update_layout(transition_duration=500)
#
#     return fig
