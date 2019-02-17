import Vue from 'vue';
import VueRouter from 'vue-router'
import BootstrapVue from 'bootstrap-vue'
import Icon from 'vue-awesome'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { routes } from './router'

Vue.use(BootstrapVue)
Vue.component('icon', Icon)
Vue.use(VueRouter)

const router = new VueRouter({ routes })
const app = new Vue({
    router
}).$mount('#app')