import pandas as pd
import networkx as nx
import numpy as np

# For API server use:
from .generator import Generator
# For Jupyter use:
# from generator import Generator

def _read_tsv(path):
    print('reading TSV:', path)
    return pd.read_csv(path, sep = '\t')

class Datasets:
    
    def __init__(
        self,
        data_dir,
        generator = Generator(),
        num_payments = 10000
    ):
        self._data_dir = data_dir
        self._generator = generator

        self._path_gcp_datasets = self._data_dir + '/raw/gcp/datasets'
        self.ssi = self._read_gcp('StandingSettlementInstructions', 'SSIPLUS_V3_MONTHLY_FULL_20200828.txt')
        self.bdp = self._read_gcp('StandingSettlementInstructions', 'BANKDIRECTORYPLUS_V3_FULL_20200828.txt')
        self.edges = self._calc_edges(self.ssi, self.bdp)
        self.ssi_nx = self._calc_ssi_nx(self.edges)
        
        self.with_client_ssi_nx = self._onboard_client(self.ssi, self.bdp)
        
        self.payments_history = self._generate_payments(n = num_payments)
    
    def _read_gcp(self, dir_name, file_name):
        return _read_tsv(self._path_gcp_datasets + '/' + dir_name + '/' + file_name)
    
    def _onboard_client(self, ssi, bdp):
        
        ssi_cols = [
            # BDP ID
            'RECORD KEY BDP OWNER',                        # for Source side -- same constant, imaginary;   for Target side -- one of bdp dataset BDP IDs
            'RECORD KEY BDP ACCOUNT HOLDING INSTITUTION',  # for Source side -- one of bdp dataset BDP IDs; for Target side -- unique, imaginary
            # EDGE PAYLOAD                                 -- just random
            'ISO CURRENCY CODE',
            'ASSET CATEGORY',
            'ACCOUNT NBR WITH ACCOUNT HOLDING INSTITUTION',
        ]
        
        # smart things happenning here
        client_edges_df = self._generator.generate_client_data(ssi, bdp)[ssi_cols]
        
        with_client_edges = self._calc_edges(
            pd.concat([ ssi[ssi_cols], client_edges_df ]),
            bdp
        )
        
        return self._calc_ssi_nx(
            with_client_edges
        )
    
    def generate_routes(self, payment):
        current_nx = self.with_client_ssi_nx
        origins = nx.neighbors(payment.origin)
        routes = []
        for origin in origins:
            route = self._generator.generate_route(current_nx, origin, payment.destination)
            routes.append(route)
            current_nx = nx.remove_nodes(current_nx, route)
        return routes
    
    def _generate_payments(self, n = 10000):
        return [
            self._generator.generate_payment(
                origin_bdp_rks = list(nx.neighbors(
                    self.with_client_ssi_nx,
                    self._generator.client_bdp_rk,
                )),
                destination_bdp_rks = self._generator.destination_dbp_rks,
            )
            for i in range(n)
        ]
    
    def _calc_edges(self, ssi, bdp):
        
        ssi_df = ssi[[
            # BDP ID
            'RECORD KEY BDP OWNER',
            'RECORD KEY BDP ACCOUNT HOLDING INSTITUTION',
            # EDGE PAYLOAD
            'ISO CURRENCY CODE',
            'ASSET CATEGORY',
            'ACCOUNT NBR WITH ACCOUNT HOLDING INSTITUTION',
        ]]
        
        bdp_df = bdp[[
            # BDP ID
            'RECORD KEY',
            # NODE PAYLOAD
            'ISO COUNTRY CODE',
            'TIMEZONE',
        ]]
        
        return ssi_df.merge(
            bdp_df,
            left_on = 'RECORD KEY BDP OWNER',
            right_on = 'RECORD KEY',
            how = 'left', # so we don't have to add client to BDP
        ).assign(**{
            'RECORD KEY' : lambda x: np.where(
                x['RECORD KEY'].isna(),
                x['RECORD KEY BDP OWNER'],
                x['RECORD KEY'],
            )
        }).merge(
            bdp_df,
            left_on = 'RECORD KEY BDP ACCOUNT HOLDING INSTITUTION',
            right_on = 'RECORD KEY',
            suffixes = (' of OWNER', ' of HOLDER'),
        ).drop(columns = [
            'RECORD KEY BDP OWNER',
            'RECORD KEY BDP ACCOUNT HOLDING INSTITUTION',
        ])

    def _calc_ssi_nx(self, edges):
        raw_ssi_nx = nx.from_pandas_edgelist(
            edges,
            source = 'RECORD KEY of OWNER',  # BDP RECORD KEY
            target = 'RECORD KEY of HOLDER', # BDP RECORD KEY
            edge_attr = True,
        )
        connected_components = nx.connected_components(raw_ssi_nx)
        # exploration shows that this graph has just one significantly non-trivial connected component, the first one
        first_connected_component_as_list_of_tuples = list(zip(range(1), connected_components))
        if len(first_connected_component_as_list_of_tuples) > 0:
            first_connected_component = first_connected_component_as_list_of_tuples[0][1]
            return nx.subgraph(raw_ssi_nx, first_connected_component)
        else:
            return nx.empty_graph(0)
