import pandas as pd 
import numpy as np
import pickle

import dash_table
# phase_df = pd.read_json('phase_data.json')
with open('data/noVCP/gene_drug_report.pkl', 'rb') as f:
    phase_df = pickle.load(f)
# phase_df = phase_df.set_index('Gene')

with open('data/noVCP/drug_properties.pkl', 'rb') as f:
    drug_properties = pickle.load(f)


def paging():
    kamei = ['DRD2','KCNN3', 'SLC6A3', 'COMT', 'ATP4', 'ADRA2C', 'GABRG2', 'OPRM1', 'MAOA', 'MAOB', 'DRD4', 'HTR1A', 'DRD3']
    path = pd.read_table('NGLY1_plot_graph_data_20201214_no_VCP.txt')
    # phase_df = pd.read_json('phase_data.json')

    # edge処理
    path = path[path['sources']!='S']
    path = path[path['targets']!='E']
    s = list(path['sources'].unique())
    t = list(path['targets'].unique())
    starts = [n for n in s if n not in t]
    ends = [n for n in t if n not in s]

    edges = []
    for source, target, flow in zip(path['sources'], path['targets'], path['flow']):
        if source=='S' or target=='E':
            continue
        else:
            edges.append({'data':{'source': source, 'target': target, 'weight':flow}, 'selectable': 'True'})

    # node処理
    nodes = []
    for edge in edges:
        data = edge['data']
        nodes.append(data['source'])
        nodes.append(data['target'])
    
    nodes = list(set(nodes))

    page_nodes = []
    # for name in nodes:
    #     if phase_df.loc[name, 'max_phase']==4:
    #         page_nodes.append({'data': {'id': name, 'label': name}, 'classes': 'havedrug'})
    #     elif name in starts:
    #         page_nodes.append({'data': {'id': name, 'label': name}, 'classes': 'causality'})
    #     elif name in ends:
    #         page_nodes.append({'data': {'id': name, 'label': name},  'classes': 'responsive'})
    #     else:
    #         page_nodes.append({'data': {'id': name, 'label': name}})


    for name in nodes:
        node = {}
        node['data'] = {'id': name, 'label': name}
        if name in starts:
            node['classes'] = 'causality'
        elif name in ends:
            node['classes'] = 'responsive'

        if phase_df.loc[name, 'max_phase']==4:
            if 'classes' not in node.keys():
                node['classes'] = 'havedrug'
            else:
                node['classes'] = node['classes']+' havedrug'

        if name in kamei:
            if 'classes' not in node.keys():
                node['classes'] = 'kamei'
            else:
                node['classes'] = node['classes']+' kamei'
        
        page_nodes.append(node)
            
    return page_nodes, edges


def make_drug_table(target):
    drugs = phase_df.loc[target, 'Drug']
    phases = phase_df.loc[target, 'Phase']
    df = pd.DataFrame({'Drug':drugs, 'Phase':phases})

    df = df.sort_values(['Phase','Drug'], ascending=[False, True])
    return df.to_dict('records')

def make_indications_tabledata(target):
    indications = drug_properties[drug_properties['compound_name']==target].sort_values(['max_phase_for_ind', 'mesh_heading'], ascending=[False, True])

    if len(indications)==0:
        return [{'mesh_heading':'Nothing', 'max_phase':'-'}]
    res_df = indications[['mesh_heading', 'max_phase_for_ind']]
    res_df.columns = ['mesh_heading', 'max_phase']
    return res_df.to_dict('records')
