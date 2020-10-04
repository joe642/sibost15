import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Analytics from "../views/Analytics.vue"
import PaymentRoute from "../views/PaymentRoute.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/payment-route",
    name: "PaymentRoute",
    component: PaymentRoute
  },
  {
    path: "/analytics",
    name: "Analytics",
    component: Analytics
  }
];

const router = new VueRouter({
  routes
});

export default router;
