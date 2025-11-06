import { createRouter, createWebHistory } from 'vue-router'

// Views
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import UserDashboard from '../views/UserDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  }
  ,
  {
    path: '/user/dashboard',
    name: 'user-dashboard',
    component: UserDashboard
  },

{
  path: '/user/public/:id',
  component: { template: '<div class="p-10 text-center">Public lots page (coming soon)</div>' }
},
{
  path: '/user/private/:id',
  component: { template: '<div class="p-10 text-center">Private lots page (coming soon)</div>' }
},
{
  path: '/book/:id',
  component: { template: '<div class="p-10 text-center">Booking page (coming soon)</div>' }
},
{
  path: '/book-ticket/:id',
  component: { template: '<div class="p-10 text-center">Ticket page (coming soon)</div>' }
},

]

const router = createRouter({
  history: createWebHistory(), // clean URLs
  routes
})

export default router
