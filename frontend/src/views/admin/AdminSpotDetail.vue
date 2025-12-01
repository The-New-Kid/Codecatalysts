<template>
  <div class="flex justify-center mt-12 px-4">
    <div
      class="bg-white rounded-3xl shadow-xl p-8 w-full max-w-md"
      data-aos="fade-up"
    >
      <!-- Heading -->
      <h2
        class="text-3xl font-extrabold text-center text-gray-800 mb-8"
        data-aos="fade-down"
      >
        Spot Details
      </h2>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center text-gray-600 mb-4">
        Loading spot details...
      </div>
      <div v-else-if="error" class="text-center text-red-600 mb-4">
        {{ error }}
      </div>

      <!-- Content -->
      <div v-else>
        <!-- Status -->
        <div class="mb-6 text-center">
          <label class="block text-gray-700 font-medium mb-2">
            Status:
          </label>

          <!-- Occupied -->
          <RouterLink
            v-if="spot.status === 'O'"
            :to="`/admin/spots/${spot.id}/occupied`"
            class="inline-block px-6 py-2 bg-red-600 text-white font-semibold rounded-2xl shadow hover:bg-red-700 transition"
          >
            Occupied
          </RouterLink>

          <!-- Available / Extra / VIP -->
          <template v-else>
            <span
              v-if="spot.color === 'green'"
              class="inline-block px-6 py-2 bg-green-500 text-black font-semibold rounded-2xl shadow"
            >
              Available
            </span>
            <span
              v-else-if="spot.color === 'grey'"
              class="inline-block px-6 py-2 bg-gray-400 text-black font-semibold rounded-2xl shadow"
            >
              Extra Availability
            </span>
            <span
              v-else-if="spot.color === 'pink'"
              class="inline-block px-6 py-2 bg-pink-500 text-white font-semibold rounded-2xl shadow"
            >
              VIP Availability
            </span>
          </template>
        </div>

        <!-- Parking Lot ID -->
        <div class="mb-6">
          <label class="block text-gray-700 font-medium mb-2">
            Parking Lot ID:
          </label>
          <div
            class="w-full px-4 py-3 border rounded-2xl bg-gray-50 text-gray-800 shadow-inner"
          >
            {{ lot.id }}
          </div>
        </div>

        <!-- Buttons -->
        <!-- Buttons -->
<div class="flex flex-col sm:flex-row justify-center gap-4 mt-6">
  <!-- Delete only if NOT occupied -->
  <button
    v-if="spot.status !== 'O'"
    type="button"
    class="flex-1 w-full bg-red-600 text-white font-semibold py-3 rounded-2xl shadow hover:bg-red-700 transition"
    @click="onDeleteSpot"
  >
    Delete Spot
  </button>

  <!-- If occupied, show non-deletable info -->
  <button
    v-else
    type="button"
    disabled
    class="flex-1 w-full bg-gray-300 text-gray-600 font-semibold py-3 rounded-2xl shadow cursor-not-allowed"
  >
    Cannot delete occupied spot
  </button>

  <RouterLink
    to="/admin/dashboard"
    class="flex-1 w-full text-center bg-gray-300 text-gray-800 font-semibold py-3 rounded-2xl shadow hover:bg-gray-400 transition"
  >
    Back to Dashboard
  </RouterLink>
</div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const spot = ref(null)
const lot = ref({ id: '' })
const loading = ref(true)
const error = ref('')

const API_BASE = 'http://127.0.0.1:5000/api'

const fetchSpotDetails = async () => {
  loading.value = true
  error.value = ''
  const spotId = route.params.id

  try {
    const res = await axios.get(`${API_BASE}/admin/spots/${spotId}`)
    // Expecting { spot: {...}, lot: {...} }
    spot.value = res.data.spot
    lot.value = res.data.lot
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load spot details.'
  } finally {
    loading.value = false
  }
}
//updated
const onDeleteSpot = async () => {
  // ❌ Guard: occupied spot delete nahi karna
  if (spot.value && spot.value.status === 'O') {
    alert('Occupied spot cannot be deleted.')
    return
  }

  if (!window.confirm('Are you sure you want to delete this spot?')) return
  const spotId = route.params.id

  try {
    await axios.delete(`${API_BASE}/admin/spots/${spotId}`)
    router.push('/admin/dashboard')
  } catch (err) {
    console.error(err)
    alert('Failed to delete spot.')
  }
}

onMounted(() => {
  if (window.AOS) {
    window.AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
  }
  fetchSpotDetails()
})
</script>
