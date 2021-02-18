import json
import pickle
import pandas as pd
import dash
import dash_cytoscape as cyto

from my_style import generate_stylesheet
from edge_generator import paging

nodes, edges = paging()
es = nodes+edges

cytograph =  cyto.Cytoscape(
                    id='cytoscape-elements-classes',
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