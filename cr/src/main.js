// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vueResource from 'vue-resource'

Vue.use(vueResource)
Vue.use(BootstrapVue)

Vue.http.options.root = 'https://courseroad.herokuapp.com/users/juanfajardo/'
Vue.http.headers.common['Authorization'] = 'Basic anVhbmZhamFyZG86YWRtaW4xMjM='
Vue.http.headers.common['Accept'] = 'application/json'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
