import pandas as pd
import plotly.express as px
from dash import html, Dash, dcc
from dash.dependencies import Input, Output

from app.main import logger

logger.debug("read cases into dataframe")
category = ["server", "kernel", "openstack", "ceph", "all"]
count = [123, 90, 200, 58, 500]
df = pd.DataFrame({"category": category, "count": count})
logger.debug(df.head())


app_layout = html.Div([
    html.H4('Cases by Category'),
    dcc.Dropdown(
        id="dropdown",
        options=["All", "Ceph", "Kernel", "Openstack", "Server"],
        value="All",
        clearable=False,
    ),
    dcc.Graph(id="graph", figure=px.bar(data_frame=df, x="category", y="count", barmode="group")),
])

graph = html.Div([
    html.H3('Table content'),
])


# @app.callback(dash.dependencies.Output('graph', [dash.dependencies.Input('dropdown', 'value')]))
def render_content():
    return graph


def init_callbacks(app):
    app.callback(
        Output("bar-graph", "figure"),
        [
            Input("x-variable", "value"),
            Input("y-variable", "value"),
        ],
    )(render_content)
    app.callback(Output("x-variable", "options"), [Input("y-variable", "value")], )
    app.callback(Output("y-variable", "options"), [Input("x-variable", "value")], )

    return app


def init_dash(server):
    """Create a Plotly dashboard."""
    app = Dash(server=server, routes_pathname_prefix="/cases-example/", )

    # create dash layout
    app.layout = app_layout

    # initialize callbacks
    init_callbacks(app)
    app.logger.info("in init dash")
    return app.server


if __name__ == '__main__':
    # main isn't called at all?
    logger.info("in main cases example app")
    dash = Dash(__name__)
    init_callbacks(dash)
    dash.run_server(debug=True, port=8080)
