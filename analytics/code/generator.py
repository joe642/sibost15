import pandas as pd
import networkx as nx

# For API server use:
from .gql_types import *
# For Jupyter use:
# from gql_types import *

class Generator:
    
    def __init__(self):
        self.SEED = 100500
        
        self.client_bdp_rk = 'BD_CLIENT_Z2'
        self.destination_dbp_rks = [
            'BD00000005G6',
            'BD00000006O3',
            'BD0000000HUQ',
        ]
        self.client_party = Party(
            bdp = self.client_bdp_rk,
            bic = "BDABLABX840",
            name = "Z2 Corp.",
            countryCode = "SG",
            countryName = "United Kingdom",
            city = "London",
        )


    
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
    def generate_route(self, ssi_nx, origin_bdp_rk, destination_bdp_rk):
        return []
    
    def generate_payment(
        self, 
        origin_bdp_rks, 
        destination_bdp_rks,
        asset_categories,
        currencies,
        amount_range,
    ):
        return Payment(
            originBic = "FOOBRBIC",
            destinationBic = "FOOBRBIC",
            assetCategory = "ANYY",
            currency = "USD",
            amount = 100_000,
        )