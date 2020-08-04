import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.min.css'
import Vuetify from 'vuetify'

Vue.use(Loading)
Vue.use(Vuetify)
Vue.use(BootstrapVue)
Vue.component('Loading', Loading)
Vue.config.productionTip = false

new Vue({
  vuetify: new Vuetify({
    icons: {
      iconfont: 'mdi'// default - only for display purposes
    }
  }),
  render: h => h(App)
}).$mount('#app')
