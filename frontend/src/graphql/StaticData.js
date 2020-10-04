import gql from "graphql-tag";

export const GET_STATIC_DATA_QUERY = gql`
  query {
    staticData {
      assetCategories
      destinations {
        party {
          bdp
          bic
          name
          countryCode
          countryName
          city
        }
        accounts
      }
      origins {
        bdp
        bic
        name
        countryCode
        countryName
        city
      }
    }
  }
`;
