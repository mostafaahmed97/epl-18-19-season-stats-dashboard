from maindash import app
from dashboard_layout import generate_layout

app.layout = generate_layout()
app.run_server(debug=True, dev_tools_hot_reload=True)
