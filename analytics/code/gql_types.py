from dataclasses import dataclass

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
    charge: object

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