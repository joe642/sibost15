<template>
  <div class="payment-route">
    <div class="p-grid">
      <div class="p-col-3 filter-wrapper">
        <div class="card">
          <div class="card-title text-left">
            Search
          </div>
          <div class="card-body">
            <Search
              @updated="setSelectedRoute"
            />
          </div>
        </div>
      </div>
      <div class="p-col-5">
        <div v-if="routes.length && routes.length >0" class="route-wrapper">
          <PaymentRoute
            :route="selectedRoute"
          />
        </div>
        <div v-else>
          <p class="no-data">No payment details entered</p>
        </div>
      </div>
      <div class="p-col-4">
        <div class="filter-wrapper">
          <div class="card">
            <div class="card-title text-left">
              Summary
            </div>
            <div class="card-body">
              <div class="p-grid">
                <div class="p-col-6">
                  Risk Rating
                </div>
                <div class="p-col-6" :class="`risk-${selectedRoute.risk}`">
                  <span v-if="routes.length && routes.length >0"  class="summary-stat">{{ riskLabels[selectedRoute.risk] }}</span>
                  <span v-else>No route selected</span>
                </div>
                <div class="p-col-6">
                  Estimated Fees
                </div>
                <div class="p-col-6">
                  <span v-if="routes.length && routes.length >0" class="summary-stat">GBP {{ selectedRoute.totalTimeMinutes }}</span>
                  <span v-else>No route selected</span>
                </div>
                <div class="p-col-6">
                  End-to-End Settlement Time
                </div>
                <div class="p-col-6">
                  <span v-if="routes.length && routes.length >0" class="summary-stat">{{ formatAsHours(selectedRoute.totalTimeMinutes) }}</span>
                  <span v-else>No route selected</span>
                </div>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-title text-left">
              Available Routes
            </div>
            <div class="card-body">
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
                  {{ riskLabels[route.risk] }} risk - {{ formatAsHours(route.totalTimeMinutes) }}*
                  <span
                    v-if="index === 0 && route.risk === 'LO'"
                    class="p-tag p-tag-success"
                    style="margin-left: 20px;"
                  > Reccommended</span>
                </label>
              </div>
              <small>*Estimated time</small>
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
import Search from "@/components/Search.vue"

export default {
  name: "Home",

  components: {
    RadioButton,
    PaymentRoute,
    Search
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
      selectedRoute: {},
      riskLabels: {
        'LO': 'Low',
        'MD': 'Medium',
        'HI': 'High'
      }
    }
  },

  methods: {
    formatAsHours (totalMinutes) {
      const hours = Math.floor(totalMinutes / 60);          
      const minutes = totalMinutes % 60;

      return `${hours}h${minutes}m`
    },
    setSelectedRoute () {
      if (this.routes && this.routes.length > 0) {
        this.selectedRoute = this.routes[0]
      }
    }
  },

  mounted () {
    this.setSelectedRoute()
  }
};
</script>

<style lang="scss" scoped>
.payment-route {
  display: block;
  margin: auto;
  padding-bottom: 50px;
  padding: 0 50px;
}
.no-data {
  font-family: 'Montserrat', sans-serif;
    text-align: center;
    font-size: 24px;
    margin-top: 72px;
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
.summary-stat {
      font-weight: 600;
    font-size: 20px;
}
.risk-HI .summary-stat {
  color: #ff5252;
}
.risk-MD {
  color: orange;
}
.risk-LO {
  color: #689F38;
}
</style>
