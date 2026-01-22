<template>
  <div class="max-w-6xl mx-auto mt-10 px-4">

    <!-- Page Title -->
    <h2 class="text-3xl font-extrabold text-center mb-8 text-indigo-700">
      👥 Registered Users
    </h2>

    <!-- Loading -->
    <div v-if="loading" class="text-center text-gray-600">
      Loading users...
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center text-red-600">
      {{ error }}
    </div>

    <!-- Users Table Card -->
    <div v-else class="bg-white rounded-3xl shadow-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-indigo-700">
            <tr>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-100 uppercase tracking-wider">ID</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-100 uppercase tracking-wider">Email ID</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-100 uppercase tracking-wider">Name</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-100 uppercase tracking-wider">Address</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-100 uppercase tracking-wider">Pincode</th>
            </tr>
          </thead>

          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="user in users"
              :key="user.id"
              class="hover:bg-indigo-50 transition duration-200"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ user.id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800">{{ user.email }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800">{{ user.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800">{{ user.address }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800">{{ user.pincode }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:5000/api'

const users = ref([])
const loading = ref(true)
const error = ref('')

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${API_BASE}/admin/users`)
    users.value = res.data
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load registered users.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
  if (window.AOS) {
    window.AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
  }
})
</script>
