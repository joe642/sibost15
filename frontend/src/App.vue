<template>
  <div id="app">
    <Header />
    <router-view />
  </div>
</template>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Source+Sans+Pro:wght@400;600&display=swap');

body {
  margin: 0;
  padding: 0;
  font-family: 'Source Sans Pro', sans-serif;
  font-weight: 400;
}
h1, h2, h3 {
  font-family: 'Montserrat', sans-serif;
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
}

.blue-text {
  color: #303F9F;
}
.red-text {
  color: #FF5252;
}
.dark-text {
  color: #212121;
}

.dark-primary-color    { background: #303F9F; }
.default-primary-color { background: #3F51B5; }
.light-primary-color   { background: #C5CAE9; }
.text-primary-color    { color: #FFFFFF; }
.accent-color          { background: #FF5252; }
.primary-text-color    { color: #212121; }
.secondary-text-color  { color: #757575; }
.divider-color         { border-color: #BDBDBD; }
</style>

<script>
import Header from "@/components/Header.vue";

export default {
  components: {
    Header
  }
}
</script>
