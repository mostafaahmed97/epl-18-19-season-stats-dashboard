from maindash import app
from dash.dependencies import Output, Input, State
from dash import html, dcc

from graphs.player_stats_bar import bar_plot


def make_layout():
    return html.Div(
        [
            html.H3(
                "Premier League Statistics Season 18/19",
                className="text-center py-2",
            ),
            bar_plot,
        ],
        className="p-4",
    )
