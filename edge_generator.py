import pandas as pd 
import numpy as np
import pickle
import csv

import dash_table

# # phase_df = pd.read_json('phase_data.json')
# with open('data/noVCP/gene_drug_report.pkl', 'rb') as f:
#     phase_df = pickle.load(f)

# # phase_df = phase_df.set_index('Gene')
# with open('data/noVCP/drug_properties.pkl', 'rb') as f:
#     drug_properties = pickle.load(f)




class DataVersion_Manager:
    def __init__(self):
        with open('data/v2/gene_drug_report.pkl', 'rb') as f:
            self.phase_df = pickle.load(f)

        with open('data/v2/drug_properties.pkl', 'rb') as f:
            self.drug_properties = pickle.load(f)

        self.path_data = pd.read_table('data/v1/plot_graph_data.txt')

        with open('data/share_genes.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                self.share_gene = row

        with open('data/share_drug.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                self.share_drug = row


    def update_selfvalue(self, ver):
        # with open('data/'+ver+'/gene_drug_report.pkl', 'rb') as f:
        #     self.phase_df = pickle.load(f)

        # with open('data/'+ver+'/drug_properties.pkl', 'rb') as f:
        #     self.drug_properties = pickle.load(f)

        self.path_data = pd.read_table('data/'+ver+'/plot_graph_data.txt')


    def paging(self):
        path = self.path_data
        kamei = ['DRD2','KCNN3', 'SLC6A3', 'COMT', 'ATP4', 'ADRA2C', 'GABRG2', 'OPRM1', 'MAOA', 'MAOB', 'DRD4', 'HTR1A', 'DRD3']
        # path = pd.read_table('data/' + ver + 'NGLY1_plot_graph_data_20201214_no_VCP.txt')
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
            score = flow
            if flow > 0.1:
                flow = 0.1
            if source=='S' or target=='E':
                continue
            else:
                edges.append({'data':{'source': source, 'target': target, 'weight':flow, 'score':score}, 'selectable': 'True'})

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

            if name in list(self.phase_df.index) and self.phase_df.loc[name, 'max_phase']==4:
                if 'classes' not in node.keys():
                    node['classes'] = 'havedrug'
                else:
                    node['classes'] = node['classes']+' havedrug'

            if name in kamei:
                if 'classes' not in node.keys():
                    node['classes'] = 'kamei'
                else:
                    node['classes'] = node['classes']+' kamei'

            if name in self.share_gene:
                if 'classes' not in node.keys():
                    node['classes'] = 'share'
                else:
                    node['classes'] = node['classes']+' share'
            
            page_nodes.append(node)
                
        return page_nodes, edges


    def make_drug_table(self, target):
        drugs = self.phase_df.loc[target, 'Drug']
        phases = self.phase_df.loc[target, 'Phase']
        df = pd.DataFrame({'Drug':drugs, 'Phase':phases})
        df = df.sort_values(['Phase','Drug'], ascending=[False, True])
        
        # gene table style
        drugs = [i.upper() for i in drugs]
        index_list = [i for i, v in enumerate(drugs) if v in self.share_drug]
        table_condition_data = []
        # print('share', self.share_drug)
        # print('drugs', drugs)
        # print('index_lsit', index_list)
        for i in index_list:
            table_condition_data.append(
                    {
                        'if': {
                            'row_index': i,
                            'column_id': 'Drug',
                        },
                        'backgroundColor': 'tomato',
                        'color': 'white'
                    } 
            )

        return df.to_dict('records'), table_condition_data

    def make_indications_tabledata(self, target):
        indications = self.drug_properties[self.drug_properties['compound_name']==target].sort_values(['max_phase_for_ind', 'efo_term', 'mesh_heading'], ascending=[False, True, True])

        if len(indications)==0:
            return [{'mesh_heading':'-', 'efo_term': '-', 'max_phase':'-'}]
        res_df = indications[['mesh_heading', 'efo_term','max_phase_for_ind']]
        res_df.columns = ['mesh_heading', 'efo_term','max_phase']
        return res_df.to_dict('records')
