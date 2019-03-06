import Vue from 'vue'
import Vuex from 'vuex'
import globiFmv from './modules/globiFmv'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    globiFmv
  }
})