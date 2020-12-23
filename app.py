import pickle
import json
import os
import glob
import re
import base64

import pandas as pd
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
from edge_generator import make_drug_table, make_indications_tabledata

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
        html.Div([
            html.Div([
                html.H3(id='drug_name'),
                dash_table.DataTable(
                    columns=[{'id': c, 'name': c} for c in ['Drug', 'Phase']],
                    id='drug_table',
                    style_cell_conditional=[
                        {'if': {'column_id': 'Drug'},
                        'width': '85%'},
                        {'if': {'column_id': 'Phase'},
                        'width': '15%'}
                    ],
                    page_action='none',
                    fixed_rows={'headers': True},
                    style_table={'height': 'auto', 'overflowY': 'auto'}
                ),
            ]) 
        ], style={'width':'40%'}),
        html.Div([
            html.Div([
                html.H3(id='ind_name'),
                dash_table.DataTable(
                    columns=[{'id': c, 'name': c} for c in ['efo_term', 'max_phase']],
                    id='indication_table',
                    style_cell_conditional=[
                        {'if': {'column_id': 'efo_term'},
                        'width': '85%'},
                        {'if': {'column_id': 'max_phase'},
                        'width': '15%'},
                    ],
                    page_action='none',
                    style_cell={
                        'maxWidth':'350px'
                    },
                    fixed_rows={'headers': True},
                    style_table={'height': 'auto', 'overflowY': 'auto'})
            ])
        ], style={'width':'40%', 'margin-left':'40px'}),
    ], style={'display':'flex'}),
    ]
)


@app.callback([Output('drug_table', 'data'), Output('drug_name', 'children')],
            [Input('cytoscape-elements-classes', 'tapNodeData')])           
def update_janbotron_by_tap(target):
    target = target['id']
    return make_drug_table(target), target


@app.callback([Output('indication_table', 'data'), Output('ind_name', 'children')],
            [Input('drug_table', 'selected_cells')],
            [State('drug_table', 'data')])           
def update_indications(cells, data):
    cell = cells[0]
    row = cell['row']

    df = pd.DataFrame.from_dict(data)
    target = df.iloc[row, 0]
    return make_indications_tabledata(target), 'Drug Indication: '+target


if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server()
