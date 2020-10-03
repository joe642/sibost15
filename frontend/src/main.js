import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import "primeflex/primeflex.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";
import "primevue/resources/themes/mdc-light-indigo/theme.css";
import { createProvider } from "./vue-apollo";

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  apolloProvider: createProvider(),
  render: h => h(App)
}).$mount("#app");
