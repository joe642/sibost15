<template>
    <div class="analytics">
        <div class="p-grid">
            <div class="p-col-4">
                <div class="card">
                <div class="card-statistic blue-text">
                    {{ data.summary.averageTimeMinutes }}
                </div>
                <div class="card-description dark-text">
                    Average Payment Time
                </div>
                </div>
            </div>
            <div class="p-col-4">
                <div class="card">
                <div class="card-statistic blue-text">
                    {{ data.summary.pctFailures }}
                </div>
                <div class="card-description dark-text">
                    % Failed
                </div>
                </div>
            </div>
            <div class="p-col-4">
                <div class="card">
                <div class="card-statistic blue-text">
                    {{ data.summary.totalVolume }}
                </div>
                <div class="card-description dark-text">
                    Total Volume
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { GET_STATS_QUERY } from "../graphql/Stats";

export default {
    data () {
        return {
            data: {
                map: [],
                opportunities: [],
                summary: {
                    averageTimeMinutes: null,
                    pctFailures: null,
                    totalVolume: null
                }
            }
        }
    },
    async mounted() {
        const queryResponse = await this.$apollo.query({
            query: GET_STATS_QUERY
        });
        this.data = queryResponse.data.stats;
    }
}
</script>

<style lang="scss" scoped>
.analytics {
  max-width: 1200px;
  display: block;
  margin: auto;
}
</style>