import gql from "graphql-tag";

export const GET_PAYMENTS_DATA_QUERY = gql`
  query {
    payments(fromIdx: null, toIdx: 1000) {
      originBic
      destinationBic
      assetCategory
      currency
      amount
      timestampMinutes
      status
      gCaseId
    }
  }
`;


