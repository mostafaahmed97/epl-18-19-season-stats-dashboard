from dash import html
from graphs import players_bar_plot, players_hist_plot, banner, matches_table


def generate_layout():
    print("Creating layout")
    return html.Div(
        [
            html.H3(
                "Premier League Statistics Season 18/19",
                className="text-center py-2",
            ),
            banner,
            players_bar_plot,
            html.Br(),
            players_hist_plot,
            html.Br(),
            matches_table,
        ],
        className="p-4 bg-light",
    )
