<template>
  <div class="max-w-7xl mx-auto mt-10 px-4 space-y-8">
    <!-- Page Title -->
    <h2 class="text-3xl font-extrabold text-center text-indigo-700 mb-8">
      🔒 Private Parking Lots
    </h2>

    <!-- Loading / Error -->
    <div v-if="loading" class="text-center text-gray-600">
      Loading private parking lots...
    </div>
    <div v-else-if="error" class="text-center text-red-600">
      {{ error }}
    </div>

    <!-- Lots Grid -->
    <div
      v-else
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <div
        v-for="lot in privateLots"
        :key="lot.id"
        class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition duration-300"
      >
        <!-- Lot Header -->
        <div class="flex justify-between items-center mb-3">
          <h3 class="text-lg font-semibold text-gray-800">
            {{ lot.prime_location_name }}
          </h3>
          <div class="flex items-center space-x-3">
            <!-- Edit (same edit page as public lot) -->
            <RouterLink
              :to="`/admin/parking-lots/${lot.id}/edit`"
              class="text-green-600 font-medium hover:underline"
            >
              Edit
            </RouterLink>

            <!-- Delete -->
            <button
              type="button"
              class="text-red-600 font-medium hover:underline"
              @click="onDeleteLot(lot.id)"
            >
              Delete
            </button>
          </div>
        </div>

        <!-- Occupancy Info -->
        <p class="text-gray-500 mb-3">
          Occupied:
          <span class="font-semibold">
            {{ lot.occupied_count }}/{{ lot.max_spots }}
          </span>
        </p>

        <!-- Spot Grid -->
        <div class="grid grid-cols-5 gap-2">
          <RouterLink
            v-for="spot in lot.spots"
            :key="spot.id"
            :to="`/admin/spots/${spot.id}`"
            class="text-center py-1 rounded cursor-pointer text-sm font-medium
                   hover:bg-green-300 hover:text-green-900"
            :class="spot.status === 'A'
              ? 'bg-green-200 text-green-800 hover:bg-green-300'
              : 'bg-red-200 text-red-800 hover:bg-red-300'"
          >
            {{ spot.status }}
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Add Lot Button -->
    <div class="text-center mt-6">
      <RouterLink
        to="/admin/private-parking/add"
        class="inline-block bg-yellow-400 text-white font-semibold px-6 py-3 rounded-xl shadow hover:bg-yellow-500 transition duration-200"
      >
        + Add Lot
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:5000/api'

const privateLots = ref([])
const loading = ref(true)
const error = ref('')
const router = useRouter()

const fetchPrivateLots = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_BASE}/admin/private-parking-lots`)
    privateLots.value = res.data
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load private parking lots.'
  } finally {
    loading.value = false
  }
}

const onDeleteLot = async (lotId) => {
  if (!window.confirm('Are you sure you want to delete this private parking lot?')) return
  try {
    await axios.delete(`${API_BASE}/admin/private-parking-lots/${lotId}`)
    privateLots.value = privateLots.value.filter((lot) => lot.id !== lotId)
  } catch (err) {
    console.error(err)
    alert(err.response?.data?.message || 'Failed to delete private lot.')
  }
}

onMounted(() => {
  fetchPrivateLots()
  if (window.AOS) {
    window.AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
  }
})
</script>
