import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

import { GET_ROUTES_QUERY } from "../graphql/Routes";

export default new Vuex.Store({
  state: {
    originalPayment: {
      assetCategory: "",
      originBic: "BD_CLIENT_Z2",
      amount: 0,
      destinationBic: "",
      currency: ""
    },
    routes: [],
    loading: false
  },
  mutations: {
    updateOriginalPayment (state, payload) {
      state.originalPayment = payload
    },
    updateRoutes (state, payload) {
      state.routes = payload
    }
  },
  actions: {
    async getPaymentRoute (context, apolloInstance) {
      const queryResponse = await apolloInstance.query({
        query: GET_ROUTES_QUERY,
        variables: { payment: context.state.originalPayment }
      });

      context.commit('updateRoutes', queryResponse.data.routes)
      console.log(context)

      return queryResponse
    }
  },
  modules: {}
});
