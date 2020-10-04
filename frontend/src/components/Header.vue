<template>
  <div class="header">
    <div class="p-grid">
      <div class="p-col-2">
        <img src="../assets/paydaylogosmall.jpeg" />
      </div>
      <div class="p-col-4"></div>
      <div class="p-col-6">
        <div class="nav">
          <div class="nav-item">
            <router-link to="/">Search</router-link>
          </div>
          <div class="nav-item">
            <router-link to="/analytics">Payment History</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.nav {
  text-align: right;
  padding: 25px 50px;
}

.nav-item {
  display: inline;
  margin-right: 25px;

  a {
    text-decoration: none;
    font-weight: 600;
  }
}

.header {
  height: 80px;
  margin-bottom: 80px;
  box-shadow: rgba(0, 0, 0, 0.08) 0px 1px 12px !important;
  background-color: white;
}
img {
    max-height: 60px;
    margin: 8px 30px;
}
</style>
