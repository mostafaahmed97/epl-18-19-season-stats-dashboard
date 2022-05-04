from maindash import app
from dash import html, dcc
from dash.dependencies import Output, Input
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

import plotly.express as px
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc

df = pd.read_csv("data/epl-players-18-19.csv")
teams = sorted(df["Current Club"].unique())
positions = df["position"].unique()

players_bar_plot_statistics_opts = {
    "goals_overall": "Goals",
    "goals_away": "Goals (Away)",
    "goals_home": "Goals (Home)",
    "appearances_overall": "Appearances",
    "appearances_home": "Appearances (Home)",
    "appearances_away": "Appearances (Away)",
    "assists_overall": "Assists",
    "assists_home": "Assists (Home)",
    "assists_away": "Assists (Away)",
    "penalty_goals": "Penalties Scored",
    "penalty_misses": "Penalties Missed",
    "yellow_cards_overall": "Yellow Cards",
    "red_cards_overall": "Red Cards",
}

bar_ctrls = html.Div(
    [
        html.Div(
            [
                dcc.Dropdown(
                    teams,
                    [],
                    id="barTeamPicker",
                    multi=True,
                    clearable=True,
                    placeholder="Choose Teams",
                )
            ],
            className="col-12 mb-2",
        ),
        html.Div(
            [
                html.P("Hide zeros"),
                dbc.Checkbox(id="barCtrlsSwitch", value=True, className="ml-2"),
            ],
            className="col-md-4 col-12 row align-items-center align-center",
        ),
        html.Div(
            [
                html.P("Statistic"),
                dcc.Dropdown(
                    players_bar_plot_statistics_opts,
                    id="barCtrlsStatistic",
                    value="goals_overall",
                    clearable=False,
                ),
            ],
            className="col-md-4 col-12",
        ),
        html.Div(
            [
                html.P("Position"),
                dcc.Dropdown(positions, id="barCtrlsPos"),
            ],
            className="col-md-4 col-12",
        ),
        html.Div(
            [
                html.P("Show Top 10 Only"),
                dbc.Checkbox(id="barCtrlsTopOnly", value=False, className="ml-2"),
            ],
            className="col-md-4 col-12 row align-items-center align-center",
        ),
    ],
    className="row wrap",
)

players_bar_plot = html.Div(
    [
        html.Div(
            [
                html.H5(
                    "Player Statistics",
                    className="mx-auto",
                )
            ],
            className="row mt-4",
        ),
        dcc.Graph(id="barPlot"),
        bar_ctrls,
    ],
    className="col-12 bg-white p-4 rounded mt-4",
)


@app.callback(
    Output("barPlot", "figure"),
    Input("barCtrlsSwitch", "value"),
    Input("barCtrlsTopOnly", "value"),
    Input("barCtrlsStatistic", "value"),
    Input("barCtrlsPos", "value"),
    Input("barTeamPicker", "value"),
)
def update_players_bar_plot(hide_zeros, top_only, statistic, player_pos, team):

    # Init filter
    if hide_zeros:
        filter = df[statistic] != 0
    else:
        filter = df[statistic] | True

    if team:
        filter = filter & df["Current Club"].isin(team)

    if player_pos:
        filter = filter & (df["position"] == player_pos)

    filtered_df = df[filter]

    filtered_df = filtered_df.sort_values(
        by=statistic,
        ascending=False,
    )

    if top_only:
        filtered_df = filtered_df.head(10)

    fig = px.bar(
        filtered_df,
        x="full_name",
        y=statistic,
        text=statistic,
        color="Current Club",
        hover_data=[
            "age",
            "position",
            "Current Club",
        ],
        template="simple_white",
    )

    fig.update_layout(xaxis_categoryorder="total descending")

    fig.update_layout(
        plot_bgcolor="#fafafa",
        yaxis_title=statistic.title().replace("_", " "),
        xaxis_title="Player Name",
        xaxis_type="category",
    )

    return fig
