import axios from 'axios'

const path = location.origin + '/api/'

// URL scenarii
export const getScenarios = axios.get(path + 'scenario')
export function getNextPageScenarios (page) { return axios.get(path + 'scenario/?page=' + page) }
export function startScenario (id) { return axios.get(path + 'scenario/' + id + '/start/')}

//URL scenes
export function getScene (sceneId) { return axios.get(path + 'scene/' + sceneId) }

// URL choices
export function getChoices (sceneId, saveUid) { return axios.get(path + 'scene/' + sceneId + '/choices/?save_uid=' + saveUid) }
export function setChoice (choiceId, saveUid) { return axios.get(path + 'choice/' + choiceId + '/select/?=save_uid=' + saveUid) }