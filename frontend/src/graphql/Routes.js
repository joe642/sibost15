import gql from "graphql-tag";

export const GET_ROUTES_QUERY = gql`
  query($payment: PaymentInput!) {
    routes(payment: $payment) {
      originalPayment {
        originBic
        destinationBic
        assetCategory
        currency
        amount
        timestampMinutes
        status
        gCaseId
      }
      risk
      totalFee
      totalTimeMinutes
      success
      hops {
        source {
          bdp
          bic
          name
          countryCode
          countryName
          city
        }
        target {
          bdp
          bic
          name
          countryCode
          countryName
          city
        }
        payment {
          originBic
          destinationBic
          assetCategory
          currency
          amount
          timestampMinutes
          status
          gCaseId
        }
        fxRate
        timeTakenMinutes
        crossBorder
        charge
      }
    }
  }
`;
