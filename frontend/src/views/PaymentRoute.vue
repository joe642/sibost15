<template>
    <div class="payment-route">
        <div class="p-grid">
            <div class="p-col-4">
                <div class="card">
                    <div class="risk-score-wrapper">
                        <span class="risk-score">30</span>
                    </div>
                    <div class="card-description dark-text">
                        Risk Rating
                    </div>
                </div>
            </div>
            <div class="p-col-4">
                <div class="card">
                    <div class="card-statistic blue-text">
                        GBP 200
                    </div>
                    <div class="card-description dark-text">
                        Estimated Fees
                    </div>
                </div>
            </div>
            <div class="p-col-4">
                <div class="card">
                    <div class="card-statistic blue-text">
                        2d 5h 34m
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
                    <PaymentRoute />
                </div>
            </div>
            <div class="p-col-4">
                <div class="filter-wrapper">
                    <div class="card">
                        <div class="card-description text-left">
                            Filters
                        </div>
                        <div class="card-body">
                            <h3>Route Preferences</h3>
                            <div class="p-field-radiobutton">
                                <RadioButton id="city1" name="city" value="Chicago" v-model="city" />
                                <label for="city1">Shortest Route</label>
                            </div>
                            <div class="p-field-radiobutton">
                                <RadioButton id="city2" name="city" value="Los Angeles" v-model="city" />
                                <label for="city2">Lowest Fees</label>
                            </div>

                            <h3>Risk Appetite</h3>
                            <div class="p-field-radiobutton">
                                <RadioButton id="city1" name="city" value="Chicago" v-model="city" />
                                <label for="city1">Least Risk</label>
                            </div>
                            <div class="p-field-radiobutton">
                                <RadioButton id="city2" name="city" value="Los Angeles" v-model="city" />
                                <label for="city2">Medium</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import RadioButton from 'primevue/radiobutton'

import PaymentRoute from "@/components/PaymentRoute.vue"

export default {
  name: "Home",

  components: {
      RadioButton,
      PaymentRoute
  }
};
</script>

<style lang="scss" scoped>
    .payment-route {
        max-width: 1200px;
        display: block;
        margin: auto;
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
        font-family: 'Montserrat', sans-serif;
        text-align: center;
        font-size: 42px;
        margin-bottom: 25px;
        margin-top: 18px;
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
        font-family: 'Montserrat', sans-serif;
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