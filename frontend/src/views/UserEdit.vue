<template>
  <UserLayout>
    <div
      class="max-w-2xl mx-auto mt-12 bg-white p-10 rounded-3xl shadow-lg border border-purple-200"
      data-aos="fade-up"
    >
      <h2
        class="text-3xl font-extrabold text-purple-700 text-center mb-8"
        data-aos="fade-down"
      >
        ✨ Edit Your Profile
      </h2>

      <form @submit.prevent="updateProfile" class="space-y-6">
        <!-- Full Name -->
        <div>
          <label for="name" class="block mb-2 font-semibold text-gray-700">
            Full Name
          </label>
          <input
            type="text"
            id="name"
            v-model="user.name"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
        </div>

        <!-- Email -->
        <div>
          <label for="email" class="block mb-2 font-semibold text-gray-700">
            Email Address
          </label>
          <input
            type="email"
            id="email"
            v-model="user.email"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
        </div>

        <!-- Pincode -->
        <div>
          <label for="pincode" class="block mb-2 font-semibold text-gray-700">
            Pincode
          </label>
          <input
            type="text"
            id="pincode"
            v-model="user.pincode"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
        </div>

        <!-- Address -->
        <div>
          <label for="address" class="block mb-2 font-semibold text-gray-700">
            Address
          </label>
          <textarea
            id="address"
            v-model="user.address"
            rows="4"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400"
          ></textarea>
        </div>

        <!-- Submit Button -->
        <div class="text-center">
          <button
            type="submit"
            class="w-full sm:w-auto px-8 py-3 bg-gradient-to-r from-purple-500 to-blue-500 text-white font-bold rounded-full shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300"
          >
            Update Profile
          </button>
        </div>
      </form>
    </div>
  </UserLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import UserLayout from '@/layouts/UserLayout.vue'
import { useUserStore } from '@/stores/user'
import AOS from 'aos'
import 'aos/dist/aos.css'

const userStore = useUserStore()
const user = ref({
  name: '',
  email: '',
  pincode: '',
  address: ''
})

// Load user data on mount
onMounted(async () => {
  AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
  const id = userStore.id || sessionStorage.getItem('user_id')
  if (!id) return
  try {
    const res = await axios.get(`http://127.0.0.1:5000/api/user/${id}`)
    user.value = res.data
  } catch (err) {
    console.error('Error loading profile:', err)
  }
})

// Update user profile
async function updateProfile() {
  const id = userStore.id || sessionStorage.getItem('user_id')
  try {
    await axios.put(`http://127.0.0.1:5000/api/user/${id}`, user.value)
    userStore.updateProfile({ name: user.value.name })
    alert('Profile updated successfully!')
  } catch (err) {
    console.error('Error updating profile:', err)
    alert('Failed to update profile.')
  }
}
</script>
