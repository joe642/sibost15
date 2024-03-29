<template>
  <div class="p-fluid">
    <div class="p-field">
      <label for="lastname">Destination BIC</label>
      <Dropdown
        v-model="form.destinationBic"
        :options="destinationBics"
        optionLabel="name"
        optionValue="bdp"
        placeholder="Search for a BIC"
      >
        <template #option="slotProps">
          <span
            >{{ slotProps.option.bic }} - {{ slotProps.option.name }}</span
          >
        </template>
      </Dropdown>
    </div>
    <div class="p-field">
      <label for="lastname">Asset Category</label>
      <Dropdown
        v-model="form.assetCategory"
        :options="data.assetCategories"
        placeholder="Select an Asset Category"
      />
    </div>
    <div class="p-field">
      <label for="amount">Amount</label>
      <InputNumber
        v-model="form.amount"
        id="amount"
        mode="decimal"
        :minFractionDigits="2"
      />
    </div>
    <div class="p-field">
      <label for="currency">Currency</label>
      <AutoComplete
        v-model="selectedCurrency"
        @item-select="selectCurrency($event)"
        :suggestions="filteredCurrencies"
        @complete="searchCurrency($event)"
        :dropdown="true"
        field="code"
        placeholder="Search for a currency"
      >
        <template #item="slotProps">
          <div>{{ slotProps.item.code }} - {{ slotProps.item.name }}</div>
        </template>
      </AutoComplete>
    </div>
    <Button label="Search" class="p-button-primary" @click="handleSubmit" />
  </div>
</template>

<script>
import AutoComplete from "primevue/autocomplete";
import Button from "primevue/button";
import Dropdown from "primevue/dropdown";
import InputNumber from "primevue/inputnumber";
import { required } from "vuelidate/lib/validators";

import currencies from "../assets/currencies.json";
import { GET_STATIC_DATA_QUERY } from "../graphql/StaticData";

export default {
  name: "Search",

  components: {
    AutoComplete,
    Button,
    Dropdown,
    InputNumber
  },

  props: {
    msg: String
  },

  computed: {
    destinationBics() {
      return this.data.destinations.map(destination => {
        return destination.party;
      });
    }
  },

  validations: {
    form: {
      assetCategory: {
        required
      },
      amount: {
        required
      },
      destinationBic: {
        required
      },
      currency: {
        required
      }
    }
  },

  data() {
    return {
      form: {
        assetCategory: "",
        originBic: "BD_CLIENT_Z2",
        amount: 0,
        destinationBic: "",
        currency: ""
      },
      data: {
        assetCategories: [],
        origins: [],
        destinations: []
      },
      currencies: [],
      filteredCurrencies: [],
      selectedCurrency: null
    };
  },

  methods: {
    async handleSubmit () {
      this.$v.$touch();

      console.log(JSON.stringify(this.form));
      if (this.$v.$invalid) {
        this.$toast.add({
          severity: "error",
          summary: "Validation Error",
          detail: "Please complete all required fields",
          life: 3000
        });
      } else {
        this.$store.commit('updateOriginalPayment', this.form)
        
        
        try {
          const response = await this.$store.dispatch('getPaymentRoute', this.$apollo)

          if (response.data) {
            if (this.$router.currentRoute.path === "/") {
              this.$router.push({ path: "payment-route" });
            }
            this.$emit('updated')
          }
        } catch (err) {
          this.$toast.add({
            severity: "error",
            summary: "API Error",
            detail: "No results found",
            life: 3000
          });
          console.log(err)
        }
      }
    },
    searchCurrency(event) {
      setTimeout(() => {
        if (!event.query.trim().length) {
          this.filteredCurrencies = [...this.currencies];
        } else {
          this.filteredCurrencies = this.currencies.filter(currency => {
            return currency.code
              .toLowerCase()
              .startsWith(event.query.toLowerCase());
          });
        }
      }, 10);
    },
    selectCurrency(event) {
      this.form.currency = event.value.code;
    }
  },

  async mounted() {
    const queryResponse = await this.$apollo.query({
      query: GET_STATIC_DATA_QUERY
    });
    this.data = queryResponse.data.staticData;
    this.currencies = Object.values(currencies);
    this.form = this.$store.state.originalPayment
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss"></style>
