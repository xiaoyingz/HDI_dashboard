import dash_bootstrap_components as dbc
import dash
import pandas as pd
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State, ClientsideFunction, ALL
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import json

from backend import database_mongo
from backend import database_mysql
from backend import database_neo4j
from backend import parser
from frontend import create_dash
from frontend import overview
from frontend import schema

app = dash.Dash(
    __name__,
    external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

filters = ['country_filter', 'year_filter', 'genre_filter', 'low_rating_filter', 'high_rating_filter', 'sort_dropdown']
inputs = ["widget_name", "country", "genre", "lowest_avg_vote", "lowest_year", "largest_year", "group_attribute",
          "target_attribute", "chart_type_dropdown"]
widgets = []

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "Dashboard for IMDB movies", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Create your own", href="/create-your-own", active="exact"),
                dbc.NavLink("More", href="/more", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output("drag_container", "data-drag"),
    [Input("drag_container", "id")],
)


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return overview.overview_component
    elif pathname == "/create-your-own":
        return create_dash.create_dash_component


@app.callback(
    Output('drag_container', 'children'),
    [
        Input('create_state', 'n_clicks'),
        Input({"type": "dynamic-delete", "index": ALL}, "n_clicks"),
    ],
    State("drag_container", "children"), [State(component_id=i, component_property='value') for i in inputs],
)
def create_widget(n_clicks, _, children, name, country, genre, lowest_avg_vote, lowest_year, largest_year,
                  group_attribute, target_attribute, chart_type):
    input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if "index" in input_id:
        delete_chart = json.loads(input_id)["index"]
        children = [
            chart
            for chart in children
            if "'index': " + str(delete_chart) not in str(chart)
        ]
    else:
        new_element = html.Div(
            style={
                "width": "100%",
                "display": "inline-block",
                "outline": "thin lightgrey solid",
                "padding": 10,
            },
            children=[
                html.Button(
                    "X",
                    id={"type": "dynamic-delete", "index": n_clicks},
                    n_clicks=0,
                    style={"display": "block"},
                ),
                dcc.Graph(
                    id={"type": "dynamic-output", "index": n_clicks},
                    style={"height": 500},
                    figure=create_dash.dump_widget(name, country, genre, lowest_avg_vote, lowest_year, largest_year,
                                                   group_attribute, target_attribute, chart_type)
                ),
            ]
        )
        children.append(new_element)
    return [dbc.Card(w) for w in children]

    # return [dbc.Card([html.Button(
    #                 "X",
    #                 id={"type": "dynamic-delete", "index": n_clicks},
    #                 n_clicks=0,
    #                 style={"display": "block"},
    #             ),w]) for w in widgets]


#  html.Div(
#         className="six columns",
#         children=[
#             dcc.Graph(
#                 id='pie_chart',
#                 figure=figure
#             ),
#         ])


@app.callback(
    Output(component_id='search_result', component_property='children'),
    Input(component_id='search_state', component_property='n_clicks'),
    [State(component_id=f, component_property='value') for f in filters],
)
def update_table(n_clicks, country, year, genre, low, high, order):
    return overview.generate_table(country, year, genre, low, high, order)


@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    Input(component_id='submit_state', component_property='n_clicks'),
    State(component_id='country_input', component_property='value')
)
def update_pie(n_clicks, input_country):
    return overview.generate_pie(input_country)


@app.callback(
    Output("dummy1", "children"),
    State("input_movie", "value"),
    State("vote", "value"),
    Input("submit-button-state", "n_clicks"))
def update_table(input_movie, vote, btn1):
    # print(n_clicks)
    # print(vote)
    if btn1 > 0:
        temp_dict = database_mysql.get_id_by_name("{}".format(input_movie))
        if temp_dict != None:
            temp_id = temp_dict['imdb_title_id']
            new_rating = database_mongo.update_rating(temp_id, vote, value=1)
            res = database_mysql.update_avg_vote(temp_id, new_rating)
            print(res)
            app1 = database_neo4j.App()
            app1.update_rating(temp_id, new_rating)
            app1.close()
    return None


if __name__ == '__main__':
    app.run_server(debug=True)
