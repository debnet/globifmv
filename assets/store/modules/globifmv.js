import {startScenario, setChoice, loadSavedGame} from '../../js/utils/requests'

const state = {
    quality: '',
    scenario: null,
    scene: null,
    save: null,
    choice: null,
    choices: [],
    health: null,
    money: null,
    items: []
};

// getters
const getters = {
    quality: (state) => state.quality,
    scenario: (state) => state.scenario,
    scene: (state) => state.scene,
    save: (state) => state.save,
    choice: (state) => state.choice,
    choices: (state) => state.choices,
    health: (state) => state.health,
    money: (state) => state.money,
    items: (state) => state.items
};

// actions
const actions = {
    setQuality({commit}, quality) {
        commit('setQuality', quality)
    },
    setScenario({commit}, scenario) {
        commit('setScenario', scenario)
    },
    setScene({commit}, scene) {
        commit('setScene', scene)
    },
    setChoice({commit}, choice) {
        commit('setChoice', choice)
    },
    startScenario: async function ({commit, state}) {
        var data = await startScenario(state.scenario)
        if (data && data.status === 200) {
            commit('setSave', data.data)
        }
    },
    changeScene: async function ({commit, state}) {
        var data = await setChoice(state.choice, state.save)
        if (data && data.status === 200) {
            commit('setSave', data.data)
        }
    },

    loadSavedGame: async function ({commit}, saveUid) {
        var data = await loadSavedGame(saveUid)
        if(data && data.status === 200 ){
            commit('loadSavedGame', data.data)
        }
    }
};

// mutations
const mutations = {
    setQuality(state, quality) {
        state.quality = quality
        localStorage.setItem('quality', quality);
    },

    setScenario(state, id) {
        state.scenario = id
    },

    setScene(state, id) {
        state.scene = id
    },

    setChoice(state, choice) {
        state.choice = choice
    },

    setSave(state, data) {
        state.save = data.uuid
        state.health = data.health
        state.money = data.money
        state.choices = data.choices
        state.scene = data.scene
        state.items = data.items
        localStorage.setItem(state.scenario, data.uuid);
    },

    loadSavedGame(state, data) {
        state.quality = localStorage.getItem('quality')
        state.scenario = data.scene.scenario_id
        state.save = data.uuid
        state.health = data.health
        state.money = data.money
        state.choices = data.choices
        state.scene = data.scene
        state.items = data.items
    }
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}