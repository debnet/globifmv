module.exports = {
  routes: [
    {
      path: '/',
      name: 'home',
      component: require('../pages/index.vue').default
    },
    {
      path: '/play/',
      name: 'scenar',
      component: require('../pages/game.vue').default
    }
  ]
}