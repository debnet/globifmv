import { startScenario } from '../../js/utils/requests'

const state = {
  quality: '',
  scenario: null,
  scene: null,
  save: null,
  health: null,
  money: null
}

// getters
const getters = {
  quality: (state) => state.quality,
  scenario: (state) => state.scenario,
  scene: (state) => state.scene,
  save: (state) => state.save,
  health: (state) => state.health,
  money: (state) => state.money
}

// actions
const actions = {
  setQuality ({ commit }, quality) {
    commit('setQuality', quality)
  },
  setScenario ({ commit }, scenario) {
    commit('setScenario', scenario)
  },
  setScene ({ commit }, scene) {
    commit('setScene', scene)
  },
  startScenario: async function ({ commit, state }) {
    var data = await startScenario(state.scenario)
    if(data && data.status === 200) {
      commit('initSave', data.data)
    }
  }
}

// mutations
const mutations = {
  setQuality (state, quality) {
    state.quality = quality
  },

  setScenario (state, id) {
    state.scenario = id
  },

  setScene (state, id) {
    state.scene = id
  },
  initSave (state, data) {
    state.save = data.uuid,
    state.health = data.health,
    state.money = data.money
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}