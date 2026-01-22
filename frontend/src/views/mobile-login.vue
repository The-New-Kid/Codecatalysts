<template>
  <div class="h-screen flex items-center justify-center bg-gradient-to-br from-orange-400 via-amber-300 to-yellow-100 relative overflow-hidden">
    <div class="absolute w-72 h-72 bg-orange-500 rounded-full opacity-20 -top-20 -left-20 animate-float"></div>
    <div class="absolute w-96 h-96 bg-amber-400 rounded-full opacity-20 -bottom-32 -right-32 animate-float"></div>

    <div class="w-full max-w-md p-10 bg-white/95 rounded-3xl shadow-2xl border border-orange-200 backdrop-blur-sm" data-aos="fade-up">
      <h1 class="text-3xl font-extrabold text-center mb-8 text-orange-700 glow-text">📱 Mobile OTP Login</h1>

      <form v-if="step === 1" @submit.prevent="sendOtp" class="space-y-6">
        <div>
          <label class="block mb-2 text-gray-700 font-medium">Mobile Number</label>
          <input
            type="tel"
            v-model="mobile"
            pattern="^[0-9]{10}$"
            placeholder="Enter 10-digit mobile"
            required
            class="w-full px-5 py-3 rounded-xl border border-gray-300 shadow-inner focus:ring-2 focus:ring-orange-300 transition"
          />
        </div>

        <button
          type="submit"
          class="w-full py-3 bg-gradient-to-r from-orange-500 to-amber-400 text-white font-bold rounded-xl shadow-lg btn-gradient transition-all duration-300"
        >
          Send OTP
        </button>
      </form>

      <form v-else @submit.prevent="verifyOtp" class="space-y-6">
        <div>
          <label class="block mb-2 text-gray-700 font-medium">Enter OTP</label>
          <input
            type="text"
            v-model="otp"
            placeholder="Enter received OTP"
            required
            class="w-full px-5 py-3 rounded-xl border border-gray-300 shadow-inner focus:ring-2 focus:ring-orange-300 transition"
          />
        </div>

        <button
          type="submit"
          class="w-full py-3 bg-gradient-to-r from-orange-500 to-amber-400 text-white font-bold rounded-xl shadow-lg btn-gradient transition-all duration-300"
        >
          Verify OTP
        </button>
      </form>

      <p v-if="message" class="mt-4 text-center text-sm text-gray-700">{{ message }}</p>

      <div class="mt-6 text-center flex flex-col gap-3">
        <RouterLink to="/" class="inline-block px-6 py-2 border border-gray-300 rounded-full hover:bg-gray-100 transition">
          ← Back to Home
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const mobile = ref('')
const otp = ref('')
const step = ref(1)
const message = ref('')

async function sendOtp() {
  if (mobile.value.length !== 10) {
    message.value = 'Enter valid 10-digit mobile number'
    return
  }

  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/mobile-login`, {
      mobile_number: mobile.value
    })

    message.value = response.data.message
    step.value = 2
  } catch (error) {
    message.value = error.response?.data?.message || 'User not found'
  }
}

async function verifyOtp() {
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/login-verify-otp`, {
      mobile_number: mobile.value,
      otp: otp.value
    })

    const data = response.data
    userStore.setUser(data)
    message.value = data.message

    if (data.role === 'admin') router.push('/admin/dashboard')
    else router.push('/user/dashboard')

  } catch (error) {
    message.value = error.response?.data?.message || 'Wrong OTP'
  }
}

onMounted(() => {
  nextTick(() => {
    if (window.AOS) {
      window.AOS.init({ duration: 800, easing: 'ease-in-out', once: false })
      window.AOS.refreshHard()
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
