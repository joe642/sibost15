import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import "primeflex/primeflex.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";
import "primevue/resources/themes/mdc-light-indigo/theme.css";

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
