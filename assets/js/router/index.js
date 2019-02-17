module.exports = {
  routes: [
    {
      path: '/',
      name: 'home',
      component: require('../pages/index.vue').default
    },
    {
      path: '/play/:quality/:scenarId/:sceneId',
      name: 'scenar',
      component: require('../pages/game.vue').default
    }
  ]
}