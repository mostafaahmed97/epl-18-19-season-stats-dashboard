from maindash import app
from layout import make_layout

app.layout = make_layout()
app.run_server(debug=True, dev_tools_hot_reload=True)
