from maindash import app
from dash import html, dcc, dash_table
from dash.dependencies import Output, Input
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc

with open("data/cumulative-season-stats.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame.from_dict(data)
game_weeks = [*range(1, 39)]


cumulative_stats_plot = html.Div(
    [
        html.Div(
            [
                html.H5("Team Cumulative Statistics", className="mx-auto"),
            ],
            className="row",
        ),
        html.Div(
            [
                dcc.Graph(id="trendGraph"),
            ],
            className="w-100 overflow-auto",
        ),
        dcc.Dropdown(
            df.index.tolist(),
            id="statPicker",
            value="goals",
        ),
    ],
    className="col-12 rounded bg-white p-4 mt-2",
)


@app.callback(Output("trendGraph", "figure"), Input("statPicker", "value"))
def update_cumulative_graph(stat):
    fig = go.Figure()

    for team in df:
        fig.add_trace(
            go.Scatter(
                x=game_weeks,
                y=df[team][stat],
                name=team,
                mode="lines+markers",
            )
        )

    fig.update_layout(
        xaxis_title="Game Week",
        yaxis_title=stat,
        legend_title="Teams",
    )

    return fig
