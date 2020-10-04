<template>
  <div class="payment-route">
    <div class="p-grid">
      <div class="p-col-4">
        <div class="card">
          <div class="risk-score-wrapper">
            <span class="risk-score">{{ selectedRoute.risk }}</span>
          </div>
          <div class="card-description dark-text">
            Risk Rating
          </div>
        </div>
      </div>
      <div class="p-col-4">
        <div class="card">
          <div class="card-statistic blue-text">
            GBP {{ selectedRoute.totalTimeMinutes }}
          </div>
          <div class="card-description dark-text">
            Estimated Fees
          </div>
        </div>
      </div>
      <div class="p-col-4">
        <div class="card">
          <div class="card-statistic blue-text">
            {{ formateAsHours(selectedRoute.totalTimeMinutes) }}
          </div>
          <div class="card-description dark-text">
            End-to-End Settlement Time
          </div>
        </div>
      </div>
    </div>
    <div class="p-grid">
      <div class="p-col-8">
        <div class="route-wrapper">
          <PaymentRoute
            :route="selectedRoute"
          />
        </div>
      </div>
      <div class="p-col-4">
        <div class="filter-wrapper">
          <div class="card">
            <div class="card-description text-left">
              Filters
            </div>
            <div class="card-body">
              <h3>Available Routes</h3>
              <div 
                v-for="(route, index) in routes"
                :key="index"
                class="p-field-radiobutton"
              >
                <RadioButton
                  :id="`route${index}`"
                  :name="`route${index}`"
                  :value="route"
                  v-model="selectedRoute"
                />
                <label :for="`route${index}`">
                  {{ route.risk }} risk - Est. Time {{ formateAsHours(route.totalTimeMinutes) }} 
                  <span
                    v-if="index === 0"
                    class="p-tag p-tag-success"
                    style="margin-left: 20px;"
                  > Reccomended</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RadioButton from "primevue/radiobutton";

import PaymentRoute from "@/components/PaymentRoute.vue";

export default {
  name: "Home",

  components: {
    RadioButton,
    PaymentRoute
  },

  computed: {
    routes () {
      const routes = this.$store.state.routes.map((route) => {
        const riskScoreMapping = {
          'LO': 1,
          'MD': 2,
          'HI': 3
        }

        route.riskScore = riskScoreMapping[route.risk]
        return route
      })

      let sortBy = [{
        prop:'riskScore',
        direction: 1
      },{
        prop:'totalTimeMinutes',
        direction: 1
      }];

      return routes.sort(function(a, b){
        let i = 0, result = 0;
        while(i < sortBy.length && result === 0) {
          result = sortBy[i].direction*(a[ sortBy[i].prop ].toString() < b[ sortBy[i].prop ].toString() ? -1 : (a[ sortBy[i].prop ].toString() > b[ sortBy[i].prop ].toString() ? 1 : 0));
          i++;
        }
        return result;
      })
    }
  },

  data () {
    return {
      selectedRoute: {}
    }
  },

  methods: {
    formateAsHours (totalMinutes) {
      const hours = Math.floor(totalMinutes / 60);          
      const minutes = totalMinutes % 60;

      return `${hours}h${minutes}m`
    }
  },

  mounted () {
    if (this.routes.length > 0) {
      this.selectedRoute = this.routes[0]
    } else {
      this.$router.push({ path: "/" });
    }
  }
};
</script>

<style lang="scss" scoped>
.payment-route {
  max-width: 1200px;
  display: block;
  margin: auto;
  padding-bottom: 50px;
}

.risk-score-wrapper {
  border: 2px solid red;
  border-radius: 50%;
  height: 80px;
  width: 80px;
  text-align: center;
  padding: 17px;
  display: block;
  margin: auto;
}
.risk-score {
  font-family: "Montserrat", sans-serif;
  width: 80px;
  font-size: 32px;
  font-weight: 600;
}

.route-wrapper {
  padding-top: 100px;
}
.filter-wrapper {
  padding-top: 50px;
}
</style>
