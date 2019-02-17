import axios from 'axios'

const path = location.origin + '/api/'

// URL scenarii
export const getScenarios = axios.get(path + 'scenario')
export function getNextPageScenarios (page) { return axios.get(path + 'scenario/?page=' + page) }

//URL scenes
export function getScene (sceneId) { return axios.get(path + 'scene/' + sceneId) }

// URL choices
export function getChoices (sceneId) { return axios.get(path + 'scene/' + sceneId + '/choices') }