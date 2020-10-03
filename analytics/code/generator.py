import pandas as pd
import networkx as nx

class Generator:
    
    def __init__(self):
        self.SEED = 100500
    
    # smart things happen here !
    def generate_client_data(self, ssi, bdp):
        return pd.DataFrame({
            # BDP ID
            'RECORD KEY BDP OWNER' : [],
            'RECORD KEY BDP ACCOUNT HOLDING INSTITUTION' : [],
            # EDGE PAYLOAD
            'ISO CURRENCY CODE' : [],
            'ASSET CATEGORY' : [],
            'ACCOUNT NBR WITH ACCOUNT HOLDING INSTITUTION' : [],

        })
    
    # smart things happen here !
    def generate_route(self, current_nx, origin, destination):
        return []
    
