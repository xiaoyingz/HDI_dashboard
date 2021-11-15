import dash
import pandas as pd
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import json

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

class Widget:
	def __init__(self, name, query, chart_type):
		self.name = name
		self.query = query
		self.chart_type = chart_type

def widgetJsonDecod(messageDict):
	return namedtuple('Widget', widgetDict.keys())(*widget.values())

def dump_widget(name, query, chart_type):
	widget = Widget(name, query, chart_type)
	return json.dumps(widget.__dict__)

inputs = ["widget_name", "query", "chart_type_dropdown"]
widgets = []
create_dash_component = html.Div([
    html.Div([
        "Widget name: ",
        dcc.Input(id='widget_name', value='Widget1', type='text'),
        "Query: ",
        dcc.Input(id='query', value="select * from movies", type='text'),
        "Type: ",
        dcc.Dropdown(
            id="chart_type_dropdown",
            options=[
                {'label': 'bar chart', 'value': 'BAR'},
                {'label': 'pie chart', 'value': 'PIE'}
            ],
            value='BAR',
            clearable=False
        ),
        html.Button(id='create_state', children='Create', n_clicks=0),
        html.Div(id="create_result", children=[
            html.H2("empty")
        ])
    ]),
])

# @app.callback(
#     Output(component_id='create_result', component_property='children'),
#     Input(component_id='create_state', component_property='n_clicks'),
#     [State(component_id=i, component_property='value') for i in inputs],
# )
# def create_widget(n_clicks, name, query, chart_type):
#     widget_json = dump_widget(name, query, chart_type)
#     widgets.append(widget_json)
#     print(widgets)
#     return html.Div([
#         w for w in widgets
#     ])
