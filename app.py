from maindash import app
from dashboard_layout import generate_layout

app.layout = generate_layout()

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
