import logging
from logging.config import DEFAULT_LOGGING_CONFIG_PORT, dictConfig

import dash_bootstrap_components as dbc
from collections import namedtuple
import flask
import pandas
import plotly.graph_objs as go
import pandas as pd
from dash import html, Dash
from dash.dependencies import Input, Output, State

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def create_dataframe():
    """Prepare data for Plotly Dash."""
    casesdf = pd.read_csv('app/data/cases.csv')

    return casesdf


app_layout = html.Div([
    # html.Div(dcc.Input(id='Historical salesforce case data', type='text')),
    # html.Canvas(children='cases_example'),
    html.Div(id='container-button-basic',
             children='Historical salesforce case data'),
    html.Button('All', id='all-val', n_clicks=0),
    html.Button('Ceph', id='ceph-val', n_clicks=0),
    html.Button('Kernel', id='kernel-val', n_clicks=0),
    html.Button('Openstack', id='openstack-val', n_clicks=0),
    html.Button('Server', id='server-val', n_clicks=0),

])


def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


def create_categorical_scatter():
    pass


def create_all_bar(df):
    return {
        "data": [go.Bar(x=df[""])],
        "layout": {
            "height": 400,
            "annotations": [{
                "x": 0,
                "y": 0,
                "xanchor": "left",
                "yanchor": "right",
                "text": "All Demo Cases"
            }]
        }
    }


# def create_time_series(dff, axis_type, title):
#     return {
#         "data": [go.Scatter(x=dff["Escalated_Time__c"], y=dff["Id"], mode="lines+markers")],
#         "layout": {
#             "height": 225,
#             "margin": {"l": 40, "b": 60, "r": 20, "t": 20},
#             "annotations": [
#                 {
#                     "x": 0,
#                     "y": 0.85,
#                     "xanchor": "left",
#                     "yanchor": "bottom",
#                     "xref": "paper",
#                     "yref": "paper",
#                     "showarrow": False,
#                     "align": "left",
#                     "bgcolor": "rgba(255, 255, 255, 0.5)",
#                     "text": title,
#                 }
#             ],
#             "yaxis": {"type": "linear"},
#             "xaxis": {"showgrid": False},
#         },
#     }

# def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
#     caseNumber = hoverData["points"][0]["CaseNumber"]
#     dff = casesdf[casesdf["Id"] == caseNumber]
#     dff = dff[dff["Months"] == xaxis_column_name]
#     title = "<b>{}</b><br>{}".format(caseNumber, xaxis_column_name)
#     return create_time_series(dff, axis_type, title)
#
#
# def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
#     dff = casesdf[casesdf["Country Name"] == hoverData["points"][0]["customdata"]]
#     dff = dff[dff["Indicator Name"] == yaxis_column_name]
#     return create_time_series(dff, axis_type, yaxis_column_name)

def init_callbacks(dash_app):
    # input is the kernel query specific cases to salesforce
    # output a list of those cases
    dash_app.callback()
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('query-for-sf-cases', 'value')

    return dash_app


def init_dash(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(server=server, routes_pathname_prefix="/cases-example/", )

    # create dash layout
    dash_app.layout = app_layout

    # initialize callbacks
    init_callbacks(dash_app)

    return dash_app.server


@app.route("/")
def main():
    # logging config setup
    FORMAT = '%(asctime)s %(levelname)s  %(message)s'
    logging.basicConfig(filename='cases.log', filemode='w',
                        level=logging.DEBUG, format=FORMAT)
    logger = logging.getLogger()
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    # TODO figure out logging in dash app
    init_callbacks(app)
    app.logger.setLevel(level='DEBUG')
    casesdf = create_dataframe()
    app.logger.debug(casesdf.head())
    app.logger.debug(casesdf["Id"].unique())
    # Only for debugging while developing
    app.run_server(debug=True, port=8080)


if __name__ == '__main__':
    main()
