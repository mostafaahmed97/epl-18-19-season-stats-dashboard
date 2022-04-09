from dash import html
from graphs import bar_plot, hist_plot


def generate_layout():
    print("Creating layout")
    return html.Div(
        [
            html.H3(
                "Premier League Statistics Season 18/19",
                className="text-center py-2",
            ),
            bar_plot,
            html.Br(),
            hist_plot,
        ],
        className="p-4",
    )
