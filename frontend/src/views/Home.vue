<template>
  <div class="home">
    <div class="p-grid">
      <div class="p-col-6 p-offset-3">
        <h1>Search Payment Route</h1>
        <Search />
      </div>
    </div>
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
