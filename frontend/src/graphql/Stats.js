import gql from "graphql-tag";

export const GET_STATS_QUERY = gql`
  query {
    stats {
      summary {
        totalVolume
        averageTimeMinutes
        pctFailures
      }
      map {
        sourceCity
        targetCity
        weight
      }
      opportunities {
        source {
          bdp
          bic
          name
          countryCode
          city
        }
        target {
          bdp
          bic
          name
          countryCode
          city
        }
        summary {
          totalVolume
          averageTimeMinutes
          pctFailures
          riskLevel
        }
      }
    }
  } 
`