import axios from 'axios'

const path = location.origin + '/api/'

export const getScenarios = axios.get(path + 'scenario')
export function getNextPageScenarios (page) { return axios.get(path + 'scenario/?page=' + page) }