import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from app.main import logger


class Cases_Category:

    def __init__(self):
        logger.debug("in search csv")
        category = ["server", "kernel", "openstack", "ceph", "all"]
        df = pd.read_csv('./app/data/cases.csv')
        logger.debug(df.head)
        logger.debug(df.info)
        count = None
        # df['Escalated_Time__c'] = [pd.to_datetime(index, format='%Y-%m-%d').date() for index in df['Escalated_Time__c']]
        # self.df = pd.DataFrame({"category": category, "count": count})
        # clean datetime stamp
        df['Escalated_Time__c'] = [pd.to_datetime(index, format='%Y-%m-%d').date() for index in df['Escalated_Time__c']]
        # convert dtypes
        df['Escalated_Time__c'] = df['Escalated_Time__c'].astype('datetime64[ns]')
        df['Subject'] = df['Subject'].astype("string")
        df['Status'] = df['Status'].astype("string")
        df['Description'] = df['Description'].astype("string")
        df['CaseComment'] = df['CaseComment'].astype("string")
        df['modifiedDescription'] = df['Description'].copy()
        df['modifiedCaseComment'] = df['CaseComment'].copy()
        print(df.dtypes)
        print(f"number of na's found: \n", df.isnull().value_counts().sum())

        df["modifiedDescription"] = [str(x).replace('\n', '') for x in df["modifiedDescription"]]
        df["modifiedDescription"] = [str(x).replace('\r', '') for x in df["modifiedDescription"]]
        df["modifiedCaseComment"] = [str(x).replace('\n', '') for x in df["modifiedCaseComment"]]
        df["modifiedCaseComment"] = [str(x).replace('\r', '') for x in df["modifiedCaseComment"]]
        df["modifiedCaseNumber"] = [int(x) for x in df['CaseNumber']]


category = ["server", "kernel", "openstack", "ceph", "all"]
count = [123, 90, 200, 58, 500]
df = pd.DataFrame({"category": category, "count": count})

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


def render_content():
    return graph


def init_callbacks(app):
    app.callback(
        Output("graph", "figure"),
        [
            Input("x-variable", "value"),
            Input("y-variable", "value"),
        ],
    )(render_content)
    category_cases = Cases_Category()
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

    app.callback(Output("graph", "figure"), Input("selection", "value"))

    return app.server
