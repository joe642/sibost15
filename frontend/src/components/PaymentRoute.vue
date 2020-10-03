<template>
  <ul class="route">
    <li>
      <span>&nbsp;</span>
      <div><strong>GBP 200</strong> 2d 12h 15m</div>
    </li>
    <li>
      <span>&nbsp;</span>
      <div><strong>GBP 200</strong> 2d 12h 15m</div>
    </li>
    <li>
      <span>USD 50000</span>
      <div><strong>GBP 200</strong> 2d 12h 15m</div>
    </li>
    <li>
      <span></span>
      <div><strong>GBP 200</strong> 2d 12h 15m</div>
    </li>
    <li>
      <span></span>
      <div><strong>GBP 200</strong> 2d 12h 15m</div>
    </li>
    <li>
      <span></span>
      <div><strong>GBP 200</strong> 2d 12h 15m</div>
    </li>
  </ul>
</template>

<style lang="scss" scoped>
.route li {
  display: flex;
}

.route span {
  position: relative;
  color: #ff5252;
  padding: 11px 38px 0 0;
  min-width: 175px;
  text-align: right;
  font-size: 20px;
}

.route span::after {
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
}

.route div {
  padding: 4px 0.5em 6.5em 47px;
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

.route strong {
  display: block;
  font-weight: bolder;
}

.route {
  margin: 1em;
  width: 100%;
  display: block;
  margin: auto;
  max-width: 500px;
}
.route,
.route *::before,
.route *::after {
  box-sizing: border-box;
}
</style>
