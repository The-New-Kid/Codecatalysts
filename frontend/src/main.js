import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// FIX: Create Pinia instance separately so DevTools detects it
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')

// Refresh animations after navigation
router.afterEach(() => {
  if (window.AOS) {
    window.AOS.refreshHard()
  }
})
