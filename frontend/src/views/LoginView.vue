<template>
  <div class="h-screen flex items-center justify-center bg-gradient-to-br from-orange-400 via-amber-300 to-yellow-100 relative overflow-hidden">
    <!-- Decorative saffron glow circles -->
    <div class="absolute w-72 h-72 bg-orange-500 rounded-full opacity-20 -top-20 -left-20 animate-float"></div>
    <div class="absolute w-96 h-96 bg-amber-400 rounded-full opacity-20 -bottom-32 -right-32 animate-float"></div>

    <!-- Card -->
    <div class="w-full max-w-md p-10 bg-white/95 rounded-3xl shadow-2xl border border-orange-200 backdrop-blur-sm" data-aos="fade-up">
      <!-- Title -->
      <h1 class="text-3xl font-extrabold text-center mb-8 text-orange-700 glow-text">🛕 User Login</h1>

      <!-- Form -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block mb-2 text-gray-700 font-medium">Email Address</label>
          <input
            type="email"
            v-model="email"
            placeholder="name@example.com"
            required
            class="w-full px-5 py-3 rounded-xl border border-gray-300 shadow-inner focus:ring-2 focus:ring-orange-300 transition"
          />
        </div>

        <div class="relative">
          <label class="block mb-2 text-gray-700 font-medium">Password</label>
          <div class="relative flex items-center">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="Enter password"
              required
              class="w-full px-5 py-3 pr-12 rounded-xl border border-gray-300 shadow-inner focus:ring-2 focus:ring-orange-300 transition"
            />
            <button type="button" class="absolute right-3 text-gray-400 hover:text-orange-600" @click="togglePassword">
              <i data-feather="eye"></i>
            </button>
          </div>
        </div>

        <button
          type="submit"
          class="w-full py-3 bg-gradient-to-r from-orange-500 to-amber-400 text-white font-bold rounded-xl shadow-lg btn-gradient transition-all duration-300"
        >
          Login
        </button>
      </form>

      <!-- Links -->
      <div class="mt-6 text-center flex flex-col gap-3">
        <RouterLink
          to="/"
          class="inline-block px-6 py-2 border border-gray-300 rounded-full hover:bg-gray-100 transition"
        >
          ← Back to Home
        </RouterLink>
        <p class="text-gray-600">
          New User?
          <RouterLink to="/register" class="text-orange-600 font-semibold hover:text-orange-800 transition">
            Register Here
          </RouterLink>
          <RouterLink to="/mobile-login" class="text-orange-600 font-semibold hover:text-orange-800 transition">
            | Login with Mobile
          </RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

const email = ref('')
const password = ref('')
const showPassword = ref(false)

function togglePassword() {
  showPassword.value = !showPassword.value
}

import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

async function handleLogin() {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/login', {
      email: email.value,
      password: password.value
    })

    userStore.setUser(response.data)
    // redirect based on role
    if (userStore.role === 'admin') router.push({ name: 'admin-dashboard' })
    else router.push('/user/dashboard')
  } catch (error) {
    alert('Login failed')
  }
}


onMounted(() => {
  nextTick(() => {
    if (window.AOS) {
      window.AOS.init({ duration: 800, easing: 'ease-in-out', once: false })
      window.AOS.refreshHard()
    }
    if (window.feather) {
      window.feather.replace()
    }
  })
})
</script>

<style scoped>
@keyframes floatUp {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.animate-float { animation: floatUp 3s ease-in-out infinite; }

input:focus {
  outline: none;
  box-shadow: 0 0 12px rgba(255, 153, 0, 0.5);
  border-color: #ff9900;
}
.btn-gradient:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
}
.glow-text {
  text-shadow: 0 0 6px rgba(255, 153, 0, 0.8);
}
</style>
