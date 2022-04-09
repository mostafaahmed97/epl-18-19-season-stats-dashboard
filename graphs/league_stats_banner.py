from maindash import app
from dash import html, dcc
from dash.dependencies import Input, Output

# Not used but they fix circualr import bug
# from plotly.graph_objects import Layout
# from plotly.validator_cache import ValidatorCache

import pandas as pd

df = pd.read_csv("data/epl-18-19.csv")


banner = html.Div(
    [
        html.Div(
            [
                html.H5("Clubs"),
                html.P(df["number_of_clubs"]),
            ],
            className="col-md-4 col-6 text-center",
        ),
        html.Div(
            [
                html.H5("Matches"),
                html.P(df["total_matches"]),
            ],
            className="col-md-4 col-6 text-center",
        ),
        html.Div(
            [
                html.H5("Avg. Goals / Match"),
                html.P(df["average_goals_per_match"]),
            ],
            className="col-md-4 col-6 text-center",
        ),
    ],
    className="mx-auto row wrap outlined rounded border bg-light",
)
