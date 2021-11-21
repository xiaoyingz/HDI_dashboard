import dash
import pandas as pd
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import json
from backend import database_mysql
from backend import database_mongo

app = dash.Dash(
    __name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])


class Widget:
    def __init__(self, name, country, genre, lowest_avg_vote, lowest_year, largest_year, group_attribute, chart_type):
        self.name = name
        self.country = country
        self.genre = genre
        self.lowest_avg_vote = lowest_avg_vote
        self.lowest_year = lowest_year
        self.largest_year = largest_year
        self.group_attribute = group_attribute
        self.chart_type = chart_type


def widgetJsonDecod(messageDict):
    return namedtuple('Widget', widgetDict.keys())(*widget.values())


def generate_pie(name, group_key, country, year, avg_vote, genre):
    data = database_mysql.filter_group_movies(group_key, country, year, avg_vote, genre)
    pie_data = {group_key: [], "counts": []}
    for item in data:
        pie_data[group_key].append(item["_id"])
        pie_data["counts"].append(item["total"])
    pie_fig = px.pie(pie_data, values='counts', names=group_key, title=name)
    return pie_fig


def generate_bar(name, group_key, country, year, avg_vote, genre, max_bars=10):
    data = database_mysql.filter_group_movies(group_key, country, year, avg_vote, genre)
    length = min(len(data), max_bars)
    bar_data = {group_key: [data[i]["_id"] for i in range(length)],
                "count": [data[i]["total"] for i in range(length)]
                }
    bar_fig = px.bar(bar_data, x=group_key, y="count", barmode="group", title=name)
    return bar_fig


def generate_table(name, country, year, avg_vote, genre):
    data = database_mysql.filter_movies(country, year, avg_vote, genre)
    #header_values = list(data[0].keys())
    header_values = ["title", "country", "year", "avg_vote", "genre"]
    col_values = [[item[col] for item in data] for col in header_values]
    fig = go.Figure(data=[go.Table(header=dict(values=header_values),
                                   cells=dict(values=col_values))
                          ])
    fig.update_layout(title=name)
    return fig


def dump_widget(name, country, genre, lowest_avg_vote, lowest_year, largest_year, group_attribute, chart_type):
    if country == 'all':
        country = None
    if genre == 'all':
        genre = None
    figure = None
    if chart_type == 'PIE':
        figure = generate_pie(name, group_attribute, country, (lowest_year, largest_year), (lowest_avg_vote, 10),
                              genre)
    elif chart_type == 'BAR':
        figure = generate_bar(name, group_attribute, country, (lowest_year, largest_year), (lowest_avg_vote, 10),
                              genre)
    else:
        figure = generate_table(name, country, (lowest_year, largest_year), (lowest_avg_vote, 10), genre)
    return html.Div(
        className="six columns",
        children=[
            dcc.Graph(
                id='pie_chart',
                figure=figure
            ),
        ])


def get_attributes(col_name):
    values = database_mysql.get_category_attribute_options(col_name)
    return [{"label": "all", 'value': "all"}] + [{"label": value, 'value': value} for value in values]


inputs = ["widget_name", "country", "genre", "lowest_avg_vote", "chart_type_dropdown"]
widgets = []
country_options = get_attributes("country")
genre_options = get_attributes("genre")
create_dash_component = html.Div([
    html.Div([
        "Widget name: ",
        dcc.Input(id='widget_name', value='Widget1', type='text'),
        "Country: ",
        dcc.Dropdown(
            id="country",
            options=country_options,
            value='USA',
            clearable=False
        ),
        "Genre: ",
        dcc.Dropdown(
            id="genre",
            options=genre_options,
            value='Action',
            clearable=False
        ),
        "Lowest Average Vote: ",
        dcc.Input(id='lowest_avg_vote', value='7', type='text'),
        "Year: ",
        dcc.Input(id='lowest_year', value='2008', type='text'),
        "To",
        dcc.Input(id='largest_year', value='2018', type='text'),
        "Group Attribute: ",
        dcc.Dropdown(
            id="group_attribute",
            options=[
                {'label': 'country', 'value': 'country'},
                {'label': 'genre', 'value': 'genre'},
                {'label': 'None', 'value': 'None'},
            ],
            value='country',
            clearable=False
        ),
        "Type: ",
        dcc.Dropdown(
            id="chart_type_dropdown",
            options=[
                {'label': 'bar chart', 'value': 'BAR'},
                {'label': 'pie chart', 'value': 'PIE'},
                {'label': 'table', 'value': 'table'}
            ],
            value='BAR',
            clearable=False
        ),
        html.Button(id='create_state', children='Create', n_clicks=0),
        html.Div(id="drag_container", className="container", children=[
            html.Div(id="create_result"),
            dbc.Card([
                dbc.CardHeader("Card c"),
                dbc.CardBody(
                    "Some more content"
                ),
            ]),
        ]),
    ])
])
