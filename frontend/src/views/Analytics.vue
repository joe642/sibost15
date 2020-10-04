<template>
    <div class="analytics">
        <div class="p-grid">
            <div class="p-col-4">
                <div class="card">
                <div class="card-statistic blue-text">
                    {{ formatAsHours(data.summary.averageTimeMinutes) }}
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

        <div class="p-grid">
            <div class="p-col-12">
                <div class="card">
                    <h3 class="card-title">Opportunities</h3>
                    <DataTable 
                        :value="opportunities"
                        :expanded-rows="expandedRows"
                        @row-expand="onRowExpand"
                        @row-collapse="onRowCollapse"
                        dataKey="id"
                        :paginator="true" :rows="5"
                        paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
                        currentPageReportTemplate="Showing {first} to {last} of {totalRecords}"
                        class="p-datatable-striped"
                    >
                        <Column :expander="true" headerStyle="width: 3rem" />
                        <Column field="source.name" header="Source" sortable></Column>
                        <Column field="target.name" header="Target" sortable></Column>
                        <Column field="summary.riskLevel" header="Risk" sortable></Column>
                        <Column field="summary.totalVolume" header="Total Volume" sortable></Column>
                        <Column field="summary.timestampMinutes" header="Avg. Duration" :sortable="true">
                            <template #body="slotProps">
                                {{ formatAsHours(slotProps.data.summary.averageTimeMinutes) }}
                            </template>
                        </Column>
                        <template #expansion="slotProps">
                            <div class="orders-subtable">
                                <div class="p-grid">
                                    <div class="p-col-4">
                                        <h4>Source</h4>
                                        <strong>Name: </strong> {{ slotProps.data.source.name }}<br />
                                        <strong>City: </strong> {{ slotProps.data.source.city }}<br />
                                        <strong>Country Code: </strong> {{ slotProps.data.source.countryCode }}<br />
                                        <strong>BIC: </strong> {{ slotProps.data.source.bic }}<br />
                                        <strong>BDP: </strong> {{ slotProps.data.source.bdp }}<br />
                                    </div>
                                    <div class="p-col-4">
                                        <h4>Target</h4>
                                        <strong>Name: </strong> {{ slotProps.data.target.name }}<br />
                                        <strong>City: </strong> {{ slotProps.data.target.city }}<br />
                                        <strong>Country Code: </strong> {{ slotProps.data.target.countryCode }}<br />
                                        <strong>BIC: </strong> {{ slotProps.data.target.bic }}<br />
                                        <strong>BDP: </strong> {{ slotProps.data.target.bdp }}<br />
                                    </div>
                                    <div class="p-col-4">
                                        <h4>Summary</h4>
                                        <strong>Average Duration: </strong> {{ formatAsHours(slotProps.data.summary.averageTimeMinutes) }}<br />
                                        <strong>Percentage Failed: </strong> {{ parseFloat(slotProps.data.summary.pctFailures).toFixed(2)}} %<br />
                                        <strong>Risk Level </strong> {{ slotProps.data.summary.riskLevel }}<br />
                                        <strong>Total Volume </strong> {{ slotProps.data.summary.totalVolume }}<br />
                                    </div>
                                </div>
                            </div>
                        </template>
                    </DataTable>
                </div>
            </div>
        </div>
        <div class="p-grid">
            <div class="p-col-12">
                <div class="card">
                    <h3 class="card-title">Payment History</h3>
                    <DataTable :value="payments" :paginator="true" :rows="10"
                        paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
                        :rowsPerPageOptions="[10,20,50]"
                        currentPageReportTemplate="Showing {first} to {last} of {totalRecords}"
                        class="p-datatable-striped"
                    >
                        <Column field="amount" header="Amount" :sortable="true">
                            <template #body="slotProps">
                                {{formatCurrency(slotProps.data.amount, slotProps.data.currency)}}
                            </template>
                        </Column>
                        <Column field="currency" header="Currency"></Column>
                        <Column field="assetCategory" header="Asset Category"></Column>
                        <Column field="destinationBic" header="Destination BIC"></Column>
                        <Column field="originBic" header="Origin BIC"></Column>
                        <Column field="status" header="Status">
                            <template #body="slotProps">
                                <span 
                                    v-if="slotProps.data.status"
                                    class="p-tag p-tag-success"
                                >Settled</span>
                                <span
                                    v-else
                                    class="p-tag p-tag-danger"
                                >Failed</span>
                            </template>
                             <!--<template #filter>
                                <Dropdown v-model="filters['status']" :options="statuses" placeholder="Select a Status" class="p-column-filter">
                                    <template #option="slotProps">
                                        <span :class="'customer-badge status-' + slotProps.option">{{slotProps.option}}</span>
                                    </template>
                                </Dropdown>
                            </template>-->
                        </Column>
                        <Column field="timestampMinutes" header="Duration" :sortable="true">
                            <template #body="slotProps">
                                {{formatAsHours(slotProps.data.timestampMinutes)}}
                            </template>
                        </Column>
                        <template #paginatorLeft>
                            <Button type="button" icon="pi pi-refresh" class="p-button-text" />
                        </template>
                        <template #paginatorRight>
                            <Button type="button" icon="pi pi-cloud" class="p-button-text" />
                        </template>
                    </DataTable>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Column from "primevue/column";
import DataTable from "primevue/datatable";

import { GET_STATS_QUERY } from "../graphql/Stats";
import { GET_PAYMENTS_DATA_QUERY } from "../graphql/Payments";

import formatters from '../mixins/formatters'

export default {
    components: {
        Column,
        DataTable
    },

    mixins: [formatters],

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
            },
            payments: [],
            statuses: [
                'true', 'false'
            ],
            filters: {},
            expandedRows: []
        }
    },

    computed: {
        opportunities () {
            return this.data.opportunities.map((opportunity, index) => {
                opportunity.id = index
                return opportunity
            })
        }
    },

    async mounted() {
        const queryResponse = await this.$apollo.query({
            query: GET_STATS_QUERY
        });
        this.data = queryResponse.data.stats;

        const paymentQueryResponse = await this.$apollo.query({
            query: GET_PAYMENTS_DATA_QUERY
        });
        this.payments = paymentQueryResponse.data.payments;
    },

    methods: {
        formatCurrency (value, currency) {
            return value.toLocaleString('en-US', {style: 'currency', currency });
        },
        onRowExpand(event) {
            console.log(event.data)
            this.expandedRows = [event.data]
        },
        onRowCollapse() {
            this.expandedRows = []
        },
    }
}
</script>

<style lang="scss" scoped>
.analytics {
  max-width: 1200px;
  display: block;
  margin: auto;
}
h3 {
    margin-bottom: 25px;
}
.card {
    padding: 20px;
}
</style>