<template>
  <div class="max-w-2xl mx-auto mt-10 relative z-10" data-aos="fade-up">
    <div class="bg-white shadow-xl rounded-2xl p-6">
      <h2 class="text-2xl font-bold text-indigo-700 text-center mb-6">
        🅿️ New Parking Lot
      </h2>

      <!-- Error / Success Message -->
      <div v-if="message" class="mb-4">
        <div
          :class="[
            'px-4 py-2 rounded-xl text-sm',
            success
              ? 'bg-green-100 text-green-700'
              : 'bg-red-100 text-red-700'
          ]"
        >
          {{ message }}
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Prime Location -->
        <div>
          <label class="block text-gray-700 font-medium mb-1 text-sm">
            Prime Location Name
          </label>
          <input
            type="text"
            v-model="prime_location_name"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none transition text-sm"
          />
        </div>

        <!-- Address -->
        <div>
          <label class="block text-gray-700 font-medium mb-1 text-sm">
            Address
          </label>
          <textarea
            v-model="address"
            rows="2"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none transition text-sm"
          ></textarea>
        </div>

        <!-- Row for Pin Code, Price & Max Spots -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block text-gray-700 font-medium mb-1 text-sm">
              Pin Code
            </label>
            <input
              type="number"
              v-model.number="pin_code"
              required
              class="w-full px-2 py-1 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none text-sm"
            />
          </div>
          <div>
            <label class="block text-gray-700 font-medium mb-1 text-sm">
              Price (per hr)
            </label>
            <input
              type="number"
              step="0.01"
              v-model.number="price_per_hour"
              required
              class="w-full px-2 py-1 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none text-sm"
            />
          </div>
          <div>
            <label class="block text-gray-700 font-medium mb-1 text-sm">
              Max Spots
            </label>
            <input
              type="number"
              v-model.number="max_spots"
              required
              class="w-full px-2 py-1 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none text-sm"
            />
          </div>
        </div>

        <!-- Buttons -->
        <div class="flex justify-between items-center pt-3">
          <button
            type="submit"
            :disabled="loading"
            class="bg-green-600 hover:bg-green-700 text-white font-semibold px-5 py-2 rounded-xl shadow-md transition text-sm disabled:opacity-60 disabled:cursor-not-allowed"
          >
            <span v-if="!loading">Add Lot</span>
            <span v-else>Saving...</span>
          </button>

          <RouterLink
            to="/admin/dashboard"
            class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold px-5 py-2 rounded-xl transition text-sm"
          >
            Cancel
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const API_BASE = 'http://127.0.0.1:5000/api' // adjust if needed

const prime_location_name = ref('')
const address = ref('')
const pin_code = ref(null)
const price_per_hour = ref(null)
const max_spots = ref(null)

const loading = ref(false)
const message = ref('')
const success = ref(false)

const handleSubmit = async () => {
  loading.value = true
  message.value = ''
  success.value = false

  try {
    await axios.post(`${API_BASE}/admin/parking-lots`, {
      prime_location_name: prime_location_name.value,
      address: address.value,
      pin_code: pin_code.value,
      price_per_hour: price_per_hour.value,
      max_spots: max_spots.value
    })

    success.value = true
    message.value = 'Parking lot added successfully.'

    // slight delay then go back to dashboard
    setTimeout(() => {
      router.push('/admin/dashboard')
    }, 600)
  } catch (err) {
    console.error(err)
    success.value = false
    message.value =
      err.response?.data?.message || 'Failed to add parking lot.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (window.AOS) {
    window.AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
  }
})
</script>
