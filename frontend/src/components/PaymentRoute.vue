<template>
  <ul class="route">
    <li
      v-if="route.hops.length > 0"
    >
      <span>&nbsp;</span>
      <div>
        <strong v-tooltip.right="`BIC: ${route.hops[0].source.bic}`" class="bank-name">{{ route.hops[0].source.name }}</strong>
        <i>{{ route.hops[0].target.countryName }} - {{ route.hops[0].target.city }}</i><br/>
      </div>
    </li>
    <li
      v-for="(hop, index) in route.hops"
      :key="index"
    >
      <span>
        <span class="fx-rate" v-if="hop.fxRate" v-tooltip.right="'FX Rate'">
          {{ parseFloat(hop.fxRate).toFixed(2) }} {{ hop.payment.currency }}
        </span>
      </span>
      <div>
        <strong v-tooltip.right="`BIC: ${hop.target.bic}`" class="bank-name">{{ hop.target.name }}</strong> 
        <i>{{ hop.target.countryName }} - {{ hop.target.city }}</i><br/>
        <p class="time">{{ formatAsHours(hop.timeTakenMinutes) }}<br/></p>
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  props: {
    route: {
      type: Object,
      required: true
    }
  },

  methods: {
    formatAsHours (totalMinutes) {
      const hours = Math.floor(totalMinutes / 60);          
      const minutes = totalMinutes % 60;

      return `${hours}h${minutes}m`
    }
  },
}
</script>
<style lang="scss" scoped>
.route li {
  display: flex;
}

.route li > span {
  position: relative;
  color: #ff5252;
  padding: 11px 38px 0 0;
  min-width: 175px;
  text-align: right;
  font-size: 20px;
}

.route li > span::after {
  content: "";
  position: absolute;
  z-index: 2;
  right: 0;
  top: 0;
  transform: translateX(50%);
  border-radius: 50%;
  background: #fff;
  border: 4px #bdbdbd solid;
  width: 50px;
  height: 50px;
  font-family: "FontAwesome";
  content: "\f19c";
  line-height: 40px;
  letter-spacing: 9px;
  color: #212121;
  box-shadow: rgba(0, 0, 0, 0.08) 0px 1px 12px !important;
}

.route div {
  padding: 4px 0.5em 4.5em 47px;
  position: relative;
  min-width: 200px;
  display: block;
}

.route div::before {
  content: "";
  position: absolute;
  z-index: 1;
  left: 0;
  height: 100%;
  border-left: 1px #ccc solid;
}

.route li:last-of-type div::before {
  border: none;
}

.route strong {
  display: block;
  font-weight: bolder;
}

.route {
  margin: 1em;
  width: 100%;
  display: block;
  margin: auto;
  max-width: 550px;
}
.route,
.route *::before,
.route *::after {
  box-sizing: border-box;
}
.time {
  margin-top: 5px;
    font-size: 20px;
    color: #303f9f;
}
.bank-name {
  font-size: 20px;
}
</style>
