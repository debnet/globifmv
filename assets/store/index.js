import Vue from 'vue'
import Vuex from 'vuex'
import globifmv from './modules/globifmv'

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        globifmv
    }
})