import axios from 'axios'

const path = location.origin + '/api/';

// URL scenarii
export const getScenarios = axios.get(path + 'scenario');

export function getNextPageScenarios(page) {
    return axios.get(path + 'scenario/?page=' + page)
}

export function startScenario(id) {
    return axios.get(path + 'start/' + id)
}

// URL save
export function setChoice(choiceId, saveUid) {
    return axios.get(path + saveUid + '/' + choiceId)
}

// URL load game from save
export function loadSavedGame(saveUid) {
    return axios.get(path + 'save/?uuid=' + saveUid)
}
