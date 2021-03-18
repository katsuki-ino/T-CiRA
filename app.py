import pickle
import json
import os
import glob
import re
import csv
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

# from cytograph import cytograph
from edge_generator import DataVersion_Manager
from my_style import generate_stylesheet
# from edge_generator import make_drug_table, make_indications_tabledata

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

dm = DataVersion_Manager()
nodes, edges = dm.paging()
es = nodes+edges


cytograph =  cyto.Cytoscape(
                    id='cytoscape',
                    layout={
                        'name': 'dagre',
                        'padding': 1,
                        'spacingFactor': 1.7,
                        'animate': True,
                        'animationDuration': 1000
                    },
                    stylesheet=generate_stylesheet(),
                    style={'width': '100%',
                            'height': '350px',
                            'background-color':'#fafafa',
                            'border': 'solid thin #cedded',
                            'border-radius': '5px',
                            'border-color': '#3498DB'
                            },
                    elements=es,
                    boxSelectionEnabled=True,
            )

app.layout = html.Div(
    [
    html.Div(
        [
            dcc.RadioItems(
                options=[
                    {'label': 'Ver1', 'value': 'v1'},
                    {'label': 'Ver2', 'value': 'v2'},
                ],
                value='v1',
                id='version_selector',
            ),
        ],
        style={'margin-bottom':'20px'}
    ),
    cytograph,
    html.P('EdgeScore:', id='edge_score'),
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
                    style_table={'height': 'auto', 'overflowY': 'auto'},
                ),
            ]) 
        ], style={'width':'25%'}),
        html.Div([
            html.Div([
                html.H3(id='ind_name'),
                dash_table.DataTable(
                    columns=[{'id': c, 'name': c} for c in ['mesh_heading', 'efo_term','max_phase']],
                    id='indication_table',
                    # style_cell_conditional=[
                    #     {'if': {'column_id': 'mesh_heading'},
                    #     'width': '85%'},
                    #     {'if': {'column_id': 'max_phase'},
                    #     'width': '15%'},
                    # ],
                    page_action='none',
                    style_cell={
                        'minWidth':'30px',
                        'maxWidth': '200px',
                    },
                    fixed_rows={'headers': True},
                    style_table={'height': 'auto', 'overflowY': 'auto'})
            ])
        ], style={'width':'70%', 'margin-left':'40px'}),
    ], style={'display':'flex'}),
    ]
)


@app.callback([Output('drug_table', 'data'), Output('drug_table', 'style_data_conditional'), Output('drug_name', 'children')],
            [Input('cytoscape', 'tapNodeData')])           
def update_janbotron_by_tap(target):
    target = target['id']
    data, style = dm.make_drug_table(target)
    return data, style, target


@app.callback([Output('indication_table', 'data'), Output('ind_name', 'children')],
            [Input('drug_table', 'selected_cells')],
            [State('drug_table', 'data')])           
def update_indications(cells, data):
    cell = cells[0]
    row = cell['row']

    df = pd.DataFrame.from_dict(data)
    target = df.iloc[row, 0]
    return dm.make_indications_tabledata(target), 'Drug Indication: '+target


@app.callback([Output('edge_score', 'children')],
            [Input('cytoscape', 'tapEdgeData')])           
def display_score_by_tap(target):
    score = target['score']
    return ['EdgeScore:{}'.format(score)]


@app.callback([Output('cytoscape', 'elements')],
            [Input('version_selector', 'value')])   
def update_cytoscape_by_version(version):
    dm.update_selfvalue(version)
    nodes, edges = dm.paging()
    es = nodes+edges
    return [es]

if __name__ == "__main__":
    app.run_server(debug=True)
    # app.run_server()
