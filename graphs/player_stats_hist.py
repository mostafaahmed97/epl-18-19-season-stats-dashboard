from maindash import app
from dash import html, dcc
from dash.dependencies import Input, Output

# Not used but they fix circualr import bug
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

import pandas as pd
import plotly.express as px

df = pd.read_csv("data/epl-players-18-19.csv")
teams = sorted(df["Current Club"].unique())

hist_opts = {
    "goals_overall": "Goals",
    "appearances_overall": "Appearances",
    "assists_overall": "Assists",
    "yellow_cards_overall": "Yellow Cards",
    "red_cards_overall": "Red Cards",
}

hist_ctrls = html.Div(
    [
        html.Div(
            [
                html.P("Choose statistic"),
                dcc.Dropdown(
                    hist_opts,
                    id="histCtrlsStatistic",
                    value="goals_overall",
                    clearable=False,
                ),
            ]
        ),
        dcc.Dropdown(
            teams,
            [],
            id="histTeamPicker",
            multi=True,
            clearable=True,
            placeholder="Choose Teams",
            className="my-2",
        ),
    ]
)

hist_plot = html.Div(
    [
        dcc.Graph(
            id="histPlot",
        ),
        hist_ctrls,
    ],
    className="col-12",
)


@app.callback(
    Output("histPlot", "figure"),
    Input("histCtrlsStatistic", "value"),
    Input("histTeamPicker", "value"),
)
def update_hist(statistic, teams):
    hist_figure = px.histogram(df, x=statistic, histnorm="probability density")
    return hist_figure
