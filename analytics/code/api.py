from flask import Flask, request, jsonify
from flask_cors import CORS
from ariadne.constants import PLAYGROUND_HTML
from ariadne import gql, ObjectType, graphql_sync,make_executable_schema, fallback_resolvers
from ariadne.asgi import GraphQL
import sys

import pandas as pd
from dataclasses import dataclass
import numpy as np
import networkx as nx

# For API server use:
_data_dir = 'analytics/data'
from .datasets import Datasets
from .gql_types import *
from .temporary_generator import TemporaryGenerator
# For Jupyter use:
# _data_dir = '../../data'
# from datasets import Datasets
# from gql_types import *
# from temporary_generator import TemporaryGenerator

_generator = TemporaryGenerator()
_num_payments = 10

# Schema    -------------------------------------------

sdl = gql("""
    type Query {
        staticData: StaticData!
        routes(payment: PaymentInput!): [ Route! ]!
        stats: Stats!
        payments: [ Payment! ]!
    }

    type StaticData {
        origins: [ Party! ]! # 10-20 options
        destinations: [ Destination! ]! # 100-10000 options
        assetCategories: [ String! ]!
    }

    type Party {
         bdp: String!
         bic: String! # 8chars typically
         name: String!
         countryCode: String!
         countryName: String!
         city: String!
    }

    type Destination {
        party: Party!
        accounts: [ String! ]!
    }

    type Payment {
        originBic: String!
        destinationBic: String!
        assetCategory: String!
        currency: String!
        amount: Float!
    }
    
    input PaymentInput {
        originBic: String!
        destinationBic: String!
        assetCategory: String!
        currency: String!
        amount: Float!
    }

    type Hop {
         source: Party!
         target: Party!
         payment: Payment!
         fxRate: Float # optional
         timeTakenMinutes: Int!
         crossBorder: Boolean!
         charge: Float!
    }

    type Route {
        originalPayment: Payment!
        hops: [ Hop! ]!
        risk: RiskLevel!
        totalFee: Float
        totalTimeMinutes: Int
        success: Boolean
    }
    
    enum RiskLevel {
        LO,
        MD,
        HI,
    } 

    type Summary {
         totalVolume: Float!
         averageTimeMinutes: Int!
         pctFailures: Float!
    }

    type Stats {
         summary: Summary!
         map: [ MapEdge! ]!
         opportunities: [ Opportunity! ]!
    }

    type MapEdge {
         sourceCity: String!
         targetCity: String!
         weight: Float!
    }

    type Opportunity {
         source: Party!
         target: Party!
         summary: Summary!
    }
""")

# Resolvers -------------------------------------------

class MockResolvers:
    
    def _fb(self):
        return Party(
            bdp = "BD0000000B8A",
            bic = "FOOBRBIC",
            name = "Foo Bar Corp.",
            countryCode = "FB",
            countryName = "Foo Bar Republic",
            city = "Fooburg",
        )
    
    def staticData(self):
        return StaticData(
            origins = [
                self._fb(),
            ],
            destinations = [
                Destination(
                    party = self._fb(),
                    accounts = [ "F000000000000000000BAAR" ],
                )
            ],
            assetCategories = [ "ANYY" ],
        )
    
    def routes(self, payment):
        pmt = Payment(
            originBic = "FOOBRBIC",
            destinationBic = "FOOBRBIC",
            assetCategory = "ANYY",
            currency = "USD",
            amount = 100_000,
        )
        return [
            Route(
                originalPayment = pmt,
                hops = [
                    Hop(
                        source = self._fb(),
                        target = self._fb(),
                        payment = pmt,
                        fxRate = 1.23,
                        timeTakenMinutes = round(1.25 * 24 * 60),
                        crossBorder = True,
                        charge = 10.0,
                    ),
                ],
                risk = "MD",
                totalFee = 10_000,
                totalTimeMinutes = round(1.25 * 24 * 60),
                success = True,
            ),
        ]
    
    def stats(self):
        return Stats(
            summary = Summary(
                 totalVolume = 100_000_000,
                 averageTimeMinutes = round(1.65 * 24 * 60),
                 pctFailures = 0.03,
            ),
            map = [
                MapEdge(
                    sourceCity = "Singapore",
                    targetCity = "New York",
                    weight = 100,
                ),
                MapEdge(
                    sourceCity = "London",
                    targetCity = "Cape Town",
                    weight = 100,
                ),
                MapEdge(
                    sourceCity = "Saint-Petersburg",
                    targetCity = "Frankfurt",
                    weight = 100,
                ),
            ],
            opportunities = [
                Opportunity(
                    source = self._fb(),
                    target = self._fb(),
                    summary = Summary(
                         totalVolume = 100_000,
                         averageTimeMinutes = round(0.65 * 24 * 60),
                         pctFailures = 0.07,
                    ),
                ),
                Opportunity(
                    source = self._fb(),
                    target = self._fb(),
                    summary = Summary(
                         totalVolume = 1_000_000,
                         averageTimeMinutes = round(2.65 * 24 * 60),
                         pctFailures = 0.01,
                    ),
                ),
            ],
        )
    
    def payments(self):
        return [
            Payment(
                originBic = "FOOOBIC1",
                destinationBic = "FOOBRBIC2",
                assetCategory = "ANYY",
                currency = "USD",
                amount = 200_000,
            ),
            Payment(
                originBic = "FOOOBIC3",
                destinationBic = "FOOBRBIC4",
                assetCategory = "ANYY",
                currency = "USD",
                amount = 300_000,
            ),
            Payment(
                originBic = "FOOOBIC5",
                destinationBic = "FOOBRBIC6",
                assetCategory = "ANYY",
                currency = "USD",
                amount = 400_000,
            ),
            Payment(
                originBic = "FOOOBIC7",
                destinationBic = "FOOBRBIC8",
                assetCategory = "ANYY",
                currency = "USD",
                amount = 500_000,
            ),
        ]

class DatasetsResolvers:
    
    def __init__(self, datasets = Datasets(
        data_dir = _data_dir,
        generator = _generator,
        num_payments = _num_payments,
    )):
        self._d = datasets
    
    def _fb(self):
        return Party(
            bdp = "BD0000000B8A",
            bic = "FOOBRBIC",
            name = "Foo Bar Corp.",
            countryCode = "FB",
            countryName = "Foo Bar Republic",
            city = "Fooburg",
        )

    def _parties(self, df):
        if len(df) == 0:
            return []
        else:
            return list(df.apply(lambda x: Party(
                bdp = x['RECORD KEY'],
                bic = x['BIC'],
                name = x['INSTITUTION NAME'],
                countryCode = x['ISO COUNTRY CODE'],
                countryName = x['COUNTRY NAME'],
                city = x['CITY'],
            ), axis = 1))
    
    def _parties_by_bdps(self, bdps):
        return self._parties(self._d.bdp[
            lambda x: x['RECORD KEY'].isin(bdps)
        ])
    
    def _client_party(self):
        # return self._parties_by_bdps([ _generator.client_bdp_rk ])[0]
        return _generator.client_party

    def _client_banks(self):
        client_neighbors = nx.neighbors(
            self._d.with_client_ssi_nx,
            _generator.client_bdp_rk,
        )
        return self._parties_by_bdps(client_neighbors)

    def _client_destinations(self):
        party_and_account_numbers_df = self._d.ssi[[
            'RECORD KEY BDP ACCOUNT HOLDING INSTITUTION',
            # 'ISO CURRENCY CODE',
            # 'ASSET CATEGORY',
            'ACCOUNT NBR WITH ACCOUNT HOLDING INSTITUTION',
        ]][
            lambda x: x['RECORD KEY BDP ACCOUNT HOLDING INSTITUTION'].isin(
                _generator.destination_dbp_rks
            )
        ].drop_duplicates().rename(columns = {
            'RECORD KEY BDP ACCOUNT HOLDING INSTITUTION' : 'RECORD KEY',
        }).groupby('RECORD KEY').agg(list).reset_index().merge(
            self._d.bdp[[
                'RECORD KEY',
                'BIC',
                'INSTITUTION NAME',
                'ISO COUNTRY CODE',
                'COUNTRY NAME',
                'CITY',
            ]],
            on = 'RECORD KEY',
        )
        parties = self._parties(party_and_account_numbers_df)
        account_numbers = list(party_and_account_numbers_df[
            'ACCOUNT NBR WITH ACCOUNT HOLDING INSTITUTION'
        ])
        return list(map(lambda row: Destination(
            party = row[0],
            accounts = list(filter(lambda x: x is not np.nan, row[1])),
        ), zip(parties, account_numbers)))
    
    def _asset_categories(self):
        return list(self._d.ssi['ASSET CATEGORY'].drop_duplicates())
    
    def staticData(self):
        return StaticData(
            origins = self._client_banks(),
            destinations = self._client_destinations(),
            assetCategories = self._asset_categories(),
        )
    
    def routes(self, payment):
        routes = self._d.generate_routes(payment)
        for route in routes:
            for hop in route.hops:
                source = self._parties_by_bdps([ hop.source ])
                hop.source = source[0] if len(source) > 0 else self._client_party()
                hop.target = self._parties_by_bdps([ hop.target ])[0]
        return routes
    
    def stats(self):
        payments = self._d.payments_history
        routes = self._d.routes_history

        total_volume = sum([payment.amount for payment in payments])
        average_time_minutes = sum([route.totalTimeMinutes for route in routes]) / len(routes)
        pct_failures = sum([1 for route in routes if not route.success]) / len(routes)
        
        source_cities = [ party.city for party in 
            [ self._parties_by_bdps([payment.originBic])[0] for payment in payments ]
        ]
        target_cities = [ party.city for party in 
            [ self._parties_by_bdps([payment.destinationBic])[0] for payment in payments ]
        ]
        weights = [ route.originalPayment.amount for route in routes ]

        map_edges = pd.DataFrame.from_records(
            zip(source_cities, target_cities, weights),
            columns = [ 'source_city', 'target_city', 'weight' ]
        ).groupby([ 'source_city', 'target_city' ]).sum().reset_index().apply(
            lambda x: MapEdge(x['source_city'], x['target_city'], x['weight']),
            axis = 1
        ).values

        opportunities = pd.DataFrame.from_records(
            [ (route.originalPayment.originBic, route.originalPayment.destinationBic, 
               route.totalTimeMinutes, route.success
              ) for route in routes ],
            columns = [ 'source_bdp', 'target_bdp', 'time_minutes', 'success' ]
        ).assign(
            failure = lambda x: np.where(x['success'], 0.0, 1.0)
        ).groupby([ 'source_bdp', 'target_bdp' ]).agg({
            'time_minutes' : [('average_time_minutes', 'mean')],
            'failure' : [
                 ('total_failures', 'sum'),
                 ('count_failures', 'count')
            ],
        }).reset_index()
        opportunities.columns = [
            'source_bdp', 'target_bdp', 'average_time_minutes', 'total_failures', 'count_failures'
        ]
        opportunities = opportunities.assign(
            pct_failures = lambda x: x['total_failures'] / x['count_failures'] * 100
        )
        opportunities = opportunities.merge(
            pd.DataFrame.from_records(
                [ (payment.originBic, payment.destinationBic, payment.amount) for payment in payments ],
                columns = [ 'source_bdp', 'target_bdp', 'total_amount' ]
            ).groupby([ 'source_bdp', 'target_bdp' ]).sum().reset_index(),
            on = ('source_bdp', 'target_bdp')
        )[[
            'source_bdp', 'target_bdp', 'total_amount', 'average_time_minutes', 'pct_failures'
        ]].apply(
            lambda x: Opportunity(
                self._parties_by_bdps([x['source_bdp']])[0],
                self._parties_by_bdps([x['target_bdp']])[0],
                Summary(
                    x['total_amount'],
                    round(x['average_time_minutes']),
                    x['pct_failures'],
                )
            ),
            axis = 1
        ).values        
        
        return Stats(
            summary = Summary(
                 totalVolume = total_volume,
                 averageTimeMinutes = average_time_minutes,
                 pctFailures = pct_failures,
            ),
            map = map_edges,
            opportunities = opportunities,
        )
    
    def payments(self):
        return self._d.payments_history
    
# Binding   -------------------------------------------

# _resolvers = MockResolvers()
_resolvers = DatasetsResolvers()

_query = ObjectType("Query")

@_query.field("staticData")
def resolve_staticData(_, info):
    obj = _resolvers.staticData()
    print("returning", obj)
    return obj

@_query.field("routes")
def resolve_routes(_, info, payment):
    print("routes requested for payment =", payment)
    obj = _resolvers.routes(Payment(
        originBic = payment['originBic'],
        destinationBic = payment['destinationBic'],
        assetCategory = payment['assetCategory'],
        currency = payment['currency'],
        amount = payment['amount'],
    ))
    print("returning", obj)
    return obj

@_query.field("stats")
def resolve_stats(_, info):
    obj = _resolvers.stats()
    print("returning", obj)
    return obj

@_query.field("payments")
def resolve_payments(_, info):
    obj = _resolvers.payments()
    print("returning", obj)
    return obj

schema = make_executable_schema(sdl, [ _query, fallback_resolvers ])

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return app.send_static_file('index.html')

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(host=sys.argv[1],port=sys.argv[2],debug=True)
    #app.run(debug=True)
