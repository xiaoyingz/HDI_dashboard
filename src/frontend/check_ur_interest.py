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

# from database_neo4j import App
from backend import database_mongo
from backend  import database_mysql
from backend  import database_neo4j
from frontend import schema



app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

interest_component = html.Div([
    html.H3("Check the movie interests you!"),
    html.Div(id='dummy1'),
    html.Div(id='dummy2'),
    html.Div([
        html.Div(id="movie_title"),
        "Movie Name: ",
        dcc.Input(id='input_movie', value='Million Dollar Baby', type='text')
    ]),
    html.H5("Your vote! (From 1 to 10)"),
    html.Div([
        dcc.Input(id='vote', value=0, type='number'),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
        html.Button(id='revoke-button-state', n_clicks=0, children='Revoke'),
    ]),
    html.Div(className='row', children=[
        html.Div(className='eight columns', children=[
            html.H5("Movie details"),
            dcc.Graph(id='movie_table')
        ]),
        html.Div(className='four columns', children=[
            html.H5("Vote Distribution"),
            dcc.Graph(id="vote_distribution")
        ])
    ]),
    html.Br(),
    html.Br(),
    html.H3("Give the name of the actor/director/producer/composer interests you!"),
    html.Div([
        "Type in Actor/Director/Producer/Composer Name: ",
        dcc.Input(id='input_name', value='Clint Eastwood', type='text')
    ]),
    "(You may toggle the slider to view movies after a certain year.)",
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=1900,
        max=2021,
        value=1990,
        marks={str(year): str(year) for year in range(1900,2021,10)},
        step=None,
        included=False
    )
])






# @app.callback(
#     Output(component_id='search_result', component_property='children'),
#     Input(component_id='search_state', component_property='n_clicks'),
#     [State(component_id=f, component_property='value') for f in filters],
# )
# def update_table(n_clicks, country, year, genre, low, high, order):
#     return generate_table(country, year, genre, low, high, order)

# @app.callback(
#     Output(component_id='pie_chart', component_property='figure'),
#     Input(component_id='submit_state', component_property='n_clicks'),
#     State(component_id='country_input', component_property='value')
# )
# def update_pie(n_clicks, input_country):
#     return generate_pie(input_country)

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
#             app1 = database_neo4j.App()
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
#             app1 = database_neo4j.App()
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

# def update_figure(selected_year, input_name, n_clicks,adfds):

#     app1 = database_neo4j.App()
#     df = app1.find_movie_from_person("{}".format(input_name))
#     app1.close()

#     filtered_df = df[df.year >= selected_year]

#     fig = px.scatter(filtered_df, x="year", y="rating",
#                  size="rating", color="worktype", hover_name="title",
#                  log_x=False, size_max=10)

#     fig.update_layout(transition_duration=500)

#     return fig
