import pickle
import json
import os
import glob
import re
import base64

import flask
import dash_auth
import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output, State

from cytograph import cytograph
from edge_generator import make_drug_table

# Load extra layouts
cyto.load_extra_layouts()

# app initialize
app = dash.Dash(__name__,
                # url_base_pathname='/interactive_cascade/',
                # external_stylesheets=[dbc.themes.DARKLY],
                # serve_locally=False,
                prevent_initial_callbacks=True, 
                # suppress_callback_exceptions=True
                )
server = app.server

VALID_USERNAME_PASSWORD_PAIRS = {
    'ngly1': 'fronteo2020'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div(
    [
    cytograph,
    html.Div([
        dash_table.DataTable(
        columns=[{'id': c, 'name': c} for c in ['Drug', 'Phase']],
        page_size=5,
        id='drug_table',
        style_cell_conditional=[
            {'if': {'column_id': 'Drug'},
            'width': '70%'},
            {'if': {'column_id': 'Phase'},
            'width': '10%'},
        ],
        tooltip_delay=0,
        tooltip_duration=None
        )
    ], style={'width':'80%'})
    ]
)


@app.callback([Output('drug_table', 'data'), Output('drug_table', 'tooltip_data')],
            [Input('cytoscape-elements-classes', 'tapNodeData')])           
def update_janbotron_by_tap(target):
    target = target['id']
    return make_drug_table(target)


if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server()
