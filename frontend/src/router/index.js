import { createRouter, createWebHistory } from 'vue-router'

// Importa tus componentes (ajusta las rutas según tus necesidades)
const Home = { template: '<div>Home</div>' }
const About = { template: '<div>About</div>' }

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/about', component: About },
  ]
})

export default router