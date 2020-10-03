<template>
  <div class="home">
    <Search msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
// @ is an alias to /src
import Search from "@/components/Search.vue";

export default {
  name: "Home",

  components: {
    Search
  }
};
</script>
