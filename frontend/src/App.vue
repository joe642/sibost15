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
</style>

<script>
import Header from "@/components/Header.vue";

export default {
  components: {
    Header
  }
}
</script>
