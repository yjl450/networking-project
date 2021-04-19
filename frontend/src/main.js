import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

new Vue({
  data() {
    return {
      s: null, //socket
      id: "",
      username: ""
    }
  },
  router,
  render: h => h(App)
}).$mount('#app')
