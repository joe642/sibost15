from ariadne import gql, ObjectType, make_executable_schema, fallback_resolvers
from ariadne.asgi import GraphQL

from dataclasses import dataclass


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

# Binding   -------------------------------------------

_resolvers = MockResolvers()

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

_schema = make_executable_schema(sdl, [ _query, fallback_resolvers ])
app = GraphQL(_schema, debug=True)
