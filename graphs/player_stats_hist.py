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
    "age": "Age",
    "position": "Position",
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
                    value="age",
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

players_hist_plot = html.Div(
    [
        html.Div(
            [
                html.H5("Player Statistics Distribution", className="mx-auto"),
            ],
            className="row",
        ),
        dcc.Graph(
            id="histPlot",
        ),
        hist_ctrls,
    ],
    className="col-12 bg-white rounded p-4 mt-2",
)


@app.callback(
    Output("histPlot", "figure"),
    Input("histCtrlsStatistic", "value"),
    Input("histTeamPicker", "value"),
)
def update_hist(statistic, teams):
    fig = px.histogram(
        df,
        x=statistic,
        opacity=0.69,
        template="simple_white",
    )

    fig.update_layout(
        plot_bgcolor="#fafafa",
        xaxis_title=statistic.title().replace("_", " "),
    )

    return fig
