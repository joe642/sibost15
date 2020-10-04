from flask import Flask, request, jsonify
from flask_cors import CORS
from ariadne.constants import PLAYGROUND_HTML
from ariadne import gql, ObjectType, graphql_sync,make_executable_schema, fallback_resolvers
from ariadne.asgi import GraphQL

from dataclasses import dataclass

import sys
import numpy as np
import networkx as nx

# For API server use:
_data_dir = '/mnt/gcp_data'
from datasets import Datasets
# For Jupyter use:
# from datasets import Datasets
# _data_dir = '../../data'

# Schema    -------------------------------------------

sdl = gql("""
    type Query {
        staticData: StaticData!
        routes(payment: PaymentInput!): [ Route! ]!
        stats: Stats!
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
    }

    type Route {
        originalPayment: Payment!
        hops: [ Hop! ]!
        risk: RiskLevel!
        totalFee: Float
        totalTimeMinutes: Int
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

# Types     -------------------------------------------

@dataclass
class StaticData:
    origins: object
    destinations: object
    assetCategories: object

@dataclass
class Party:
    bdp: object
    bic: object
    name: object
    countryCode: object
    countryName: object
    city: object

@dataclass
class Destination:
    party: object
    accounts: object

@dataclass
class Payment:
    originBic: object
    destinationBic: object
    assetCategory: object
    currency: object
    amount: object

@dataclass
class Hop:
    source: object
    target: object
    payment: object
    fxRate: object
    timeTakenMinutes: object
    crossBorder: object

@dataclass
class Route:
    originalPayment: object
    hops: object
    risk: object
    totalFee: object
    totalTimeMinutes: object

@dataclass
class Summary:
    totalVolume: object
    averageTimeMinutes: object
    pctFailures: object

@dataclass
class Stats:
    summary: object
    map: object
    opportunities: object

@dataclass
class MapEdge:
    sourceCity: object
    targetCity: object
    weight: object

@dataclass
class Opportunity:
    source: object
    target: object
    summary: object

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
                    ),
                ],
                risk = "MD",
                totalFee = 10_000,
                totalTimeMinutes = round(1.25 * 24 * 60),
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

class DatasetsResolvers:
    
    def __init__(self, datasets = Datasets(_data_dir)):
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
        return self._parties_by_bdps([ self._d.client_bdp_rk ])[0]

    def _client_banks(self):
        client_neighbors = nx.neighbors(self._d.ssi_nx, self._d.client_bdp_rk)
        return self._parties_by_bdps(client_neighbors)

    def _client_destinations(self):
        party_and_account_numbers_df = self._d.ssi[[
            'RECORD KEY BDP ACCOUNT HOLDING INSTITUTION',
            # 'ISO CURRENCY CODE',
            # 'ASSET CATEGORY',
            'ACCOUNT NBR WITH ACCOUNT HOLDING INSTITUTION',
        ]][
            lambda x: x['RECORD KEY BDP ACCOUNT HOLDING INSTITUTION'].isin(
                self._d.destination_dbp_rks
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
                    ),
                ],
                risk = "MD",
                totalFee = 10_000,
                totalTimeMinutes = round(1.25 * 24 * 60),
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
    obj = _resolvers.routes(payment)
    print("returning", obj)
    return obj

@_query.field("stats")
def resolve_stats(_, info):
    obj = _resolvers.stats()
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
