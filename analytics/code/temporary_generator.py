import pandas as pd
import networkx as nx
import random

# For API server use:
from .gql_types import *
# For Jupyter use:
# from gql_types import *

# smart things do not happen here.
class TemporaryGenerator:
    
    def __init__(self, seed = 100500):
        self.seed = seed
        self.r = random.Random(self.seed)
        
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
        self.num_client_bank_bdp_rks = 5
        self.supplier_dbp_rks = [
            self._generate_bdp_rk()
            for i in range(len(self.destination_dbp_rks))
        ]
        
        self.asset_categories = [
            'ANYY', 'WHLS', 'COPA',
            'TREA', 'FOEX', 'NDLF', 'OPTI', 'DERI', 'MMKT',
            'LOAN', 'SECU', 'COLL',
            'GUAR', 'COMM', 'LETT', 'TFIN', 'DOCC', 'CASH',
        ]
        self.currencies = [
            'USD', 'EUR', 'GBP', 'JPY',
            'AUD', 'NZD', 'CAD',
            'CHF', 'NOK', 'SEK',
        ]
    
    def _generate_account_number(self):
        return ''.join(self.r.choices(
            '0000000000000000000000000' + \
            '0000000000000000000000000' + \
            'QWERTYUIOPASDFGHJKLZXCVBNM' + \
            '1234567890' + \
            '----------',
            k = 25
        ))
    
    def _generate_bdp_rk(self):
        return 'BD_12345_' + ''.join(self.r.choices(
            'QWERTYUIOPASDFGHJKLZXCVBNM' + \
            '1234567890',
            k = 3
        ))
    
    def generate_client_data(self, ssi, bdp):
        return pd.DataFrame.from_records(
            [
                [ 
                    self.client_bdp_rk,
                    client_bank_bdp_rk,
                    self.r.choice(self.currencies),
                    self.r.choice(self.asset_categories),
                    self._generate_account_number(),
                ]
                for client_bank_bdp_rk in self.r.choices(
                    ssi['RECORD KEY BDP OWNER'].drop_duplicates().values,
                    k = self.num_client_bank_bdp_rks,
                )
            ] + [
                [
                    supplier_bank_bdp_rk,
                    supplier_dbp_rk,
                    self.r.choice(self.currencies),
                    self.r.choice(self.asset_categories),
                    self._generate_account_number(),
                ]
                for (supplier_bank_bdp_rk, supplier_dbp_rk) in zip(
                    self.destination_dbp_rks,
                    self.supplier_dbp_rks,
                )
            ],
            columns = [
                # BDP ID
                'RECORD KEY BDP OWNER',
                'RECORD KEY BDP ACCOUNT HOLDING INSTITUTION',
                # EDGE PAYLOAD
                'ISO CURRENCY CODE',
                'ASSET CATEGORY',
                'ACCOUNT NBR WITH ACCOUNT HOLDING INSTITUTION',
            ]
        )
    
    def generate_route(self, ssi_nx, origin_bdp_rk, destination_bdp_rk):
        return []
    
    def generate_payment(
        self,
        origin_bdp_rks = None, 
        destination_bdp_rks = None,
        asset_categories = None,
        currencies = None,
        amount_range = (1_000, 5_000_000),
    ):
        if origin_bdp_rks is None:
            origin_bdp_rks = [ self.client_bdp_rk ]
        if destination_bdp_rks is None:
            destination_bdp_rks = self.destination_dbp_rks
        if asset_categories is None:
            asset_categories = self.asset_categories
        if currencies is None:
            currencies = self.currencies

        min_amount, max_amount = amount_range
        return Payment(
                originBic = self.r.choice(origin_bdp_rks),
                destinationBic = self.r.choice(destination_bdp_rks),
                assetCategory = self.r.choice(asset_categories),
                currency = self.r.choice(currencies),
                amount = round(self.r.triangular(
                    min_amount,
                    max_amount,
                    (max_amount - min_amount) * 0.01
                )),
        )
    
