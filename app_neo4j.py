import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
import database_mysql
import database_mongo
from database_neo4j import App

app = dash.Dash(__name__)



app.layout = html.Div([
    html.H3("Check the movie interests you!"),
    html.Div([
        "Movie Name: ",
        dcc.Input(id='input_movie', value='Million Dollar Baby', type='text')
    ]),
    html.H3("Your vote! (From 1 to 10)"),
    html.Div([
        dcc.Input(id='vote', value=0, type='number'),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    ]),
    html.Div(id='dummy1'),
    dcc.Graph(id='movie_table'),
    html.H3("Give the name of the actor/director/producer/composer interests you!"),
    html.Div([
        "Actor/Director/Producer/Composer Name: ",
        dcc.Input(id='input_name', value='Clint Eastwood', type='text')
    ]),
    
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

@app.callback(
    Output("dummy1", "children"),
    State("input_movie", "value"),
    State("vote", "value"),
    Input("submit-button-state", "n_clicks"))
def update_table(input_movie, vote, n_clicks):
    # print(n_clicks)
    # print(vote)
    if n_clicks>0:
        temp_dict = database_mysql.get_id_by_name("{}".format(input_movie))
        if temp_dict!=None:
            temp_id = temp_dict['imdb_title_id']
            new_rating = database_mongo.update_rating(temp_id, vote)
            res = database_mysql.update_avg_vote(temp_id, new_rating)
            print(res)
            app1 = App()
            app1.update_rating(temp_id, new_rating)
            app1.close()
    return None

        
    
    


@app.callback(
    Output('movie_table', 'figure'),
    Input("input_movie", "value"),
    Input("dummy1", "children"))
def update_table(input_movie, n_clicks):
    movie_dict = database_mysql.get_id_by_name("{}".format(input_movie))
    if movie_dict==None:
        fig1=go.Figure(go.Table(
            header = dict(values=['Movie Not Found'])))
    else:
        del movie_dict['metascore']
        del movie_dict['reviews_from_users']
        del movie_dict['reviews_from_critics']
        del movie_dict['usa_gross_income']
        del movie_dict['imdb_title_id']
        del movie_dict['description']
        movie_dict['global_income'] = movie_dict.pop('worldwide_gross_income')
        movie_dict['company'] = movie_dict.pop('production_company')
        fig1 = go.Figure(data=[go.Table(
            header = dict(values = [[i] for i in movie_dict.keys()], fill_color='paleturquoise',
                    align='left'),
            cells = dict(values = [[i] for i in movie_dict.values()], fill_color='lavender',
                align='left')
            )
            ])
        fig1.update_layout(width=1900)
    return fig1




@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input("input_name", "value"),
    Input("dummy1", "children"))

def update_figure(selected_year, input_name, n_clicks):

    app1 = App()
    df = app1.find_movie_from_person("{}".format(input_name))
    app1.close()

    filtered_df = df[df.year >= selected_year]

    fig = px.scatter(filtered_df, x="year", y="rating",
                 size="rating", color="worktype", hover_name="title",
                 log_x=False, size_max=10)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)