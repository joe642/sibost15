<template>
  <div class="p-grid">
    <div class="p-col-6 p-offset-3">
      <h1>Search Payment Route</h1>
      <div class="p-fluid">
        <div class="p-field">
          <label for="lastname">Origin BIC</label>
          <Dropdown
            v-model="form.assetCategory"
            :options="assetCategories"
            optionLabel="name"
            placeholder="Search for a BIC"
          />
        </div>
        <div class="p-field">
          <label for="lastname">Destination BIC</label>
          <Dropdown
            v-model="form.assetCategory"
            :options="assetCategories"
            optionLabel="name"
            placeholder="Search for a BIC"
          />
        </div>
        <div class="p-field">
          <label for="lastname">Asset Category</label>
          <Dropdown
            v-model="form.assetCategory"
            :options="assetCategories"
            optionLabel="name"
            placeholder="Select an Asset Category"
          />
        </div>
        <div class="p-field">
          <label for="amount">Amount</label>
          <InputText id="amount" type="text" />
        </div>
        <Button
          label="Search" class="p-button-primary"
          @click="handleSubmit"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Button from "primevue/button"
import Dropdown from "primevue/dropdown";
import InputText from "primevue/inputtext";

export default {
  name: "HelloWorld",

  components: {
    Button,
    Dropdown,
    InputText
  },

  props: {
    msg: String
  },

  data() {
    return {
      form: {
        assetCategory: ""
      },
      assetCategories: [{ name: "Cash" }]
    };
  },

  methods: {
    handleSubmit () {
      this.$router.push({ path: 'payment-route' })
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss"></style>
