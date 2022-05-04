from maindash import app
from dash import html, dcc, dash_table
from dash.dependencies import Output, Input
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc

df = pd.read_csv("data/epl-matches-18-19.csv")

allowed_cols = {
    # "timestamp": "Timestamp",
    "home_team_name": "Home Team",
    "away_team_name": "Away Team",
    "date_GMT": "Date (GMT)",
    "Game Week": "Game Week",
    "home_team_goal_count": "Home Team Goals",
    "away_team_goal_count": "Away Team Goals",
    "home_team_goal_timings": "Home Team Goal Timings",
    "away_team_goal_timings": "Away Team Goal Timings",
    "home_team_possession": "Home Team Possession",
    "away_team_possession": "Away Team Possession",
    "home_team_shots": "Home Shots",
    "away_team_shots": "Away Shots",
    "home_team_shots_off_target": "Home Shots (On target)",
    "away_team_shots_off_target": "Away Shots (On target)",
    "home_team_corner_count": "Home Team Corners",
    "away_team_corner_count": "Away Team Corners",
    "home_team_fouls": "Home Fouls",
    "away_team_fouls": "Away Fouls",
    "home_team_yellow_cards": "Home Team Yellow Cards",
    "away_team_yellow_cards": "Home Team Corners",
    "home_team_red_cards": "Home Team Red Cards",
    "away_team_red_cards": "Away Team Red Cards",
    "stadium_name": "Stadium",
    "attendance": "Attendance",
}

for col in df.columns:
    if not col in allowed_cols:
        df = df.drop(col, axis=1)

# Rearrange columns to match allowed cols
df = df.reindex(columns=list(allowed_cols.keys()))

matches_table = html.Div(
    [
        html.Div(
            [
                html.H5("Match Statistics Table", className="mx-auto"),
            ],
            className="row",
        ),
        html.Div(
            [
                dash_table.DataTable(
                    df.to_dict("records"),
                    [{"name": allowed_cols[i], "id": i} for i in df.columns],
                    filter_action="native",
                    sort_action="native",
                    page_action="native",
                    page_size=10,
                    style_cell={
                        "textAlign": "left",
                        "padding": "1rem",
                    },
                    style_header={
                        "textAlign": "left",
                        "padding": "1rem",
                    },
                    style_table={"overflowX": "scroll", "minWidth": "100%"},
                    fixed_columns={"headers": True, "data": 2},
                ),
            ],
            className="w-100 overflow-auto",
        ),
    ],
    className="col-12 rounded bg-white p-4 mt-2",
)
