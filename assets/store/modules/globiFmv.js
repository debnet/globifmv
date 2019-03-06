import { startScenario } from '../../js/utils/requests'

const state = {
  quality: '',
  scenario: null,
  scene: null,
  save: null,
  health: null,
  money: null,
  displayChoices: false
}

// getters
const getters = {
  quality: (state) => state.quality,
  scenario: (state) => state.scenario,
  scene: (state) => state.scene,
  save: (state) => state.save,
  health: (state) => state.health,
  money: (state) => state.money,
  displayChoices: (state) => state.displayChoices
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
      commit('initSave', data.data.uuid, data.data.health, data.data.money)
    }
  },
  setDisplayChoices ({ commit }, displayChoices) {
    commit('setDisplayChoices', displayChoices)
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
  initSave (state, save, health, money) {
    state.save = save,
    state.health = health,
    state.money = money
  },
  setDisplayChoices (state, displayChoices) {
    state.displayChoices = displayChoices
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}