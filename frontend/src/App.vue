<template>
  <div id="app">
    <Header />
    <router-view />
    <Toast />
  </div>
</template>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Source+Sans+Pro:wght@400;600&display=swap");

body {
  margin: 0;
  padding: 0;
  font-family: "Source Sans Pro", sans-serif;
  font-weight: 400;
}
h1,
h2,
h3 {
  font-family: "Montserrat", sans-serif;
  font-weight: 700;
}

h1 {
  font-size: 42px;
  line-height: 40px;
  color: #333333;
  letter-spacing: -1px;
}
.text-left {
  text-align: left !important;
}

#app {
  background-color: #f7f9f9;
  min-height: 100vh;
  max-width: 100%;
  overflow: hidden;
}

.blue-text {
  color: #303f9f;
}
.red-text {
  color: #ff5252;
}
.dark-text {
  color: #212121;
}

.dark-primary-color {
  background: #303f9f;
}
.default-primary-color {
  background: #3f51b5;
}
.light-primary-color {
  background: #c5cae9;
}
.text-primary-color {
  color: #ffffff;
}
.accent-color {
  background: #ff5252;
}
.primary-text-color {
  color: #212121;
}
.secondary-text-color {
  color: #757575;
}
.divider-color {
  border-color: #bdbdbd;
}

.card {
  margin: 15px;
  padding: 20px 15px;
  width: 100%;
  box-shadow: rgba(0, 0, 0, 0.08) 0px 1px 12px !important;
  background-color: white;
}
.card-description {
  font-size: 24px;
  line-height: 32px;
  font-weight: 600;
  margin-top: 15px;
  text-align: center;
}
.card-statistic {
  font-family: "Montserrat", sans-serif;
  text-align: center;
  font-size: 42px;
  margin-bottom: 25px;
  margin-top: 18px;
}
.card-title {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 26px;
  font-family: "Montserrat", sans-serif;
  font-weight: 400;
  color: #212121;
}
</style>

<script>
import Header from "@/components/Header.vue";
import Toast from "primevue/toast";

export default {
  components: {
    Header,
    Toast
  }
};
</script>
