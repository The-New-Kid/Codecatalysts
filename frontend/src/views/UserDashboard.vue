<template>
  <UserLayout>
    <div class="space-y-8">

      <!-- Welcome Card -->
      <div
        class="bg-white rounded-2xl shadow-lg p-6 text-center hover:shadow-2xl transition duration-300"
        data-aos="fade-up"
      >
        <h2 class="text-3xl font-extrabold text-indigo-700 mb-2">
          Welcome, {{ userStore.name || 'User' }}!
        </h2>
        <p class="text-gray-600">
          Here’s a quick overview of your recent parking activity.
        </p>
      </div>

      <!-- Recent Parking History -->
      <div
        class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition duration-300"
        data-aos="fade-up"
      >
        <h3 class="text-xl font-semibold mb-4 text-gray-700">
          🚗 Recent Parking History
        </h3>

        <div class="overflow-x-auto">
          <table class="min-w-full table-auto border-collapse">
            <thead class="bg-indigo-600 text-white rounded-t-xl">
              <tr>
                <th class="px-4 py-2 text-left">Prime Location</th>
                <th class="px-4 py-2 text-left">Vehicle Number</th>
                <th class="px-4 py-2 text-left">Start Time</th>
                <th class="px-4 py-2 text-left">End Time</th>
                <th class="px-4 py-2 text-left">Cost/hr</th>
                <th class="px-4 py-2 text-left">Action</th>
              </tr>
            </thead>

            <tbody class="divide-y divide-gray-200">
              <tr
                v-for="r in reservations"
                :key="r.id"
                class="hover:bg-gray-50 transition"
              >
                <td class="px-4 py-2">
                  <span class="font-semibold">{{ r.prime_location }}</span><br />
                  <small class="text-gray-500">{{ r.address }}</small>
                </td>
                <td class="px-4 py-2">{{ r.vehicle_number || 'N/A' }}</td>
                <td class="px-4 py-2">{{ r.start_time }}</td>
                <td class="px-4 py-2">
                  <span v-if="r.end_time">{{ r.end_time }}</span>
                  <span
                    v-else
                    class="inline-block px-2 py-1 bg-yellow-300 text-yellow-900 rounded-full text-sm"
                    >Ongoing</span
                  >
                </td>
                <td class="px-4 py-2">₹{{ r.cost_per_hour }}</td>
                <td class="px-4 py-2">
                  <button
                    v-if="r.end_time"
                    class="bg-green-500 text-white px-4 py-1 rounded-full cursor-not-allowed"
                    disabled
                  >
                    Done
                  </button>
                  <button
                    v-else
                    @click="releaseSpot(r.id)"
                    class="bg-yellow-400 text-gray-800 px-4 py-1 rounded-full hover:bg-yellow-500 transition"
                  >
                    Release
                  </button>
                </td>
              </tr>

              <tr v-if="reservations.length === 0">
                <td
                  colspan="6"
                  class="text-center py-6 text-gray-500 font-semibold"
                >
                  No bookings yet
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap justify-center gap-4" data-aos="fade-up">
        <RouterLink
          to="#"
          class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3 rounded-xl transition"
        >
          Check Public Availability
        </RouterLink>

        <RouterLink
          to="#"
          class="bg-purple-600 hover:bg-purple-700 text-white font-semibold px-6 py-3 rounded-xl transition"
        >
          Check Private Availability
        </RouterLink>

        <RouterLink
          to="#"
          class="bg-green-500 hover:bg-green-600 text-white font-semibold px-6 py-3 rounded-xl transition"
        >
          Book a Spot
        </RouterLink>

        <RouterLink
          to="#"
          class="bg-green-500 hover:bg-green-600 text-white font-semibold px-6 py-3 rounded-xl transition"
        >
          Book a Ticket
        </RouterLink>
      </div>
    </div>
  </UserLayout>
</template>

<script setup>
import UserLayout from '@/layouts/UserLayout.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

// Get user store (reactive global state)
const userStore = useUserStore()
const reservations = ref([])

onMounted(async () => {
  const id = userStore.id || sessionStorage.getItem('user_id')
  if (!id) {
    console.warn('No user ID found in store or sessionStorage.')
    return
  }

  try {
    const res = await axios.get(`http://127.0.0.1:5000/api/user/dashboard/${id}`)
    userStore.name = res.data.user.name
    reservations.value = res.data.reservations
    console.log('Dashboard data loaded:', res.data)
  } catch (err) {
    console.error('Error loading dashboard:', err)
  }
})

async function releaseSpot(reservationId) {
  try {
    await axios.post(`http://127.0.0.1:5000/api/release/${reservationId}`)
    reservations.value = reservations.value.filter(
      (r) => r.id !== reservationId
    )
  } catch (err) {
    console.error('Error releasing spot:', err)
  }
}
</script>
