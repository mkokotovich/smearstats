import os
from math import ceil

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_csv('game-stats.csv')
df['date_played'] = pd.to_datetime(df['date_played'])

dates = df.date_played.dt.normalize().value_counts().sort_index().keys()
counts = df.date_played.dt.normalize().value_counts().sort_index()
smear_vs_time = dcc.Graph(
    id='smear_day_of_week',
    figure={
        'data': [
            go.Scatter(
                x=dates,
                y=counts,
                opacity=0.7,
                #mode='markers',
                #marker={
                #    'size': 15,
                #    'line': {'width': 0.5, 'color': 'white'}
                #},
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Smear Games Over Time'},
            yaxis={'title': 'Number of Games'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='x'
        )
    }
)

daysofweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
first_day = df.date_played.dt.normalize().sort_index()[0]
last_day = df.date_played.dt.normalize().sort_index().iloc[-1]
num_days = last_day - first_day
num_weeks = ceil(num_days.days/7)
dow_counts = df.date_played.dt.dayofweek.value_counts().sort_index()
dow_averages = [count/num_weeks for count in dow_counts]

day_of_week_avg = dcc.Graph(
    id='day_of_week_avg',
    figure={
        'data': [
            go.Bar(
                x=daysofweek,
                y=dow_averages,
                opacity=0.7,
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Average Number of Games Per Day'},
            yaxis={'title': 'Number of Games'},
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='x'
        )
    }
)

num_hands = df.num_hands.value_counts().sort_index().keys()
num_hands_games = df.num_hands.value_counts().sort_index()
num_hands_in_game = dcc.Graph(
    id='num_hands_in_game',
    figure={
        'data': [
            go.Scatter(
                x=num_hands,
                y=num_hands_games,
                opacity=0.7,
                #mode='markers',
                #marker={
                #    'size': 15,
                #    'line': {'width': 0.5, 'color': 'white'}
                #},
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Number of Hands'},
            yaxis={'title': 'Number of Games'},
            margin={'l': 50, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='x'
        )
    }
)


app.layout = html.Div([
    html.Div([
        html.Div([
            smear_vs_time,
        ], className="twelve columns"),
    ], className="row", style={'padding': 10}),
    html.Div([
        html.Div([
            day_of_week_avg,
        ], className="six columns"),
        html.Div([
            num_hands_in_game,
        ], className="six columns"),
    ], className="row", style={'padding': 10}),
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':

    app.run_server(debug=True)

