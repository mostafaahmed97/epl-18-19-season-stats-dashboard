from re import template
from turtle import title
from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_daq as daq

df = pd.read_csv("epl-players-18-19.csv")

teams = sorted(df["Current Club"].unique())

positions = df["position"].unique()

bar_plot_statistics_opts = {
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


app = Dash(
    name="EPLStats",
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css",
    ],
)


# team_picker = dcc.RadioItems(
#     teams,
#     inline=True,
#     value=teams[0],
#     id="barTeamPicker",
#     labelClassName="mr-4 p-2 text-muted bg-light rounded",
#     inputClassName="mr-1",
# )
team_picker = dcc.Dropdown(
    teams,
    [],
    id="barTeamPicker",
    multi=True,
    clearable=True,
    placeholder="Choose Teams",
)


bar_bot_ctrls = html.Div(
    [
        html.Div(
            [
                html.P("Hide zeros"),
                daq.BooleanSwitch(id="barCtrlsSwitch", on=True),
            ],
            className="row align-self-center col-md-4 col-12",
        ),
        html.Div(
            [
                html.P("Sort"),
                dcc.Dropdown(
                    ["asc", "desc", "no"],
                    id="barCtrlsOrder",
                    value="desc",
                    clearable=False,
                ),
            ],
            className="col-md-4 col-12",
        ),
        html.Div(
            [
                html.P("Statistic"),
                dcc.Dropdown(
                    bar_plot_statistics_opts,
                    id="barCtrlsStatistic",
                    value="goals_overall",
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
    ],
    className="row wrap",
)

bar_plot = html.Div(
    [
        team_picker,
        dcc.Graph(id="barPlot"),
        bar_bot_ctrls,
    ],
    className="col-12",
)

app.layout = html.Div(
    [
        html.H3(
            "Premier League Statistics Season 18/19",
            className="text-center py-2",
        ),
        bar_plot,
    ],
    className="p-4",
)


@app.callback(
    Output("barPlot", "figure"),
    Input("barCtrlsSwitch", "on"),
    Input("barCtrlsOrder", "value"),
    Input("barCtrlsStatistic", "value"),
    Input("barCtrlsPos", "value"),
    Input("barTeamPicker", "value"),
)
def update_bar_plot(hide_zeros, order, statistic, player_pos, team):

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

    if order != "no":
        filtered_df = filtered_df.sort_values(
            by=statistic,
            ascending=True if order == "asc" else False,
        )

    print("updating ", order, statistic, player_pos, team)

    fig = px.bar(
        filtered_df,
        x="full_name",
        y=statistic,
        color="Current Club",
        hover_data=["age", "position", "Current Club"],
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


app.run_server(debug=True, dev_tools_hot_reload=True)
