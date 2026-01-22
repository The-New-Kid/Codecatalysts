<template>
  <div>

    <div class="min-h-screen bg-gray-50 py-10 flex justify-center">
      <div class="w-full max-w-3xl bg-white rounded-2xl shadow-xl p-8">

        <h2 class="text-3xl font-serif font-bold text-center mb-6 text-red-800">
          Check Slot Availability
        </h2>

        <!-- SELECT TYPE -->
        <div class="mb-6">
          <label class="block font-semibold mb-2 text-gray-700">
            Select Type
          </label>

          <select 
            v-model="selectedType"
            class="w-full p-3 border rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200"
          >
            <option value="">-- Choose --</option>
            <option value="Aarti">Aarti</option>
            <option value="Darshan">Darshan</option>
          </select>
        </div>

        <!-- SELECT DATE -->
        <div class="mb-6">
          <label class="block font-semibold mb-2 text-gray-700">Select Date</label>

          <input
            type="date"
            v-model="selectedDate"
            :min="minDate"
            class="w-full p-3 border rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200"
          />
        </div>

        <!-- BUTTON -->
        <button 
          @click="fetchSlots"
          class="w-full py-3 rounded-xl bg-red-700 text-white font-semibold hover:bg-red-800 transition"
        >
          Show Slots
        </button>

        <!-- RESULT -->
        <div v-if="loading" class="text-center py-6 text-gray-500">
          Fetching slots...
        </div>

        <div v-if="slots.length > 0" class="mt-8 space-y-4">
          <h3 class="text-xl font-bold text-red-700 text-center mb-4">
            Available Slots
          </h3>

          <div 
            v-for="slot in slots" 
            :key="slot.slot_id"
            class="p-5 border rounded-xl shadow hover:shadow-md transition bg-white"
          >
            <p class="text-lg font-semibold text-red-800">
              {{ slot.slot_type }}
            </p>

            <p class="text-gray-700 mt-1">
              🕒 {{ slot.start }} to {{ slot.end }}
            </p>

            <p class="mt-1 text-gray-600">
              Capacity: {{ slot.capacity }}
            </p>

            <p class="text-gray-600">
              Booked: {{ slot.booked }}
            </p>

            <p class="font-bold mt-2"
               :class="slot.available > 0 ? 'text-green-700' : 'text-red-700'">
              Available: {{ slot.available }}
            </p>
          </div>
        </div>

        <p v-if="slots.length === 0 && !loading && tried" class="text-center text-gray-500 mt-6">
          No slots found for selected date and type.
        </p>

      </div>
    </div>

</div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"

const BASE = "http://127.0.0.1:5000/api"

const selectedType = ref("")
const selectedDate = ref("")
const slots = ref([])
const loading = ref(false)
const tried = ref(false)

const today = new Date()
const minDate = today.toISOString().split("T")[0]

async function fetchSlots() {
  tried.value = true

  if (!selectedType.value) {
    alert("Select Aarti or Darshan")
    return
  }

  if (!selectedDate.value) {
    alert("Select a date")
    return
  }

  loading.value = true
  slots.value = []

  try {
    const res = await axios.get(`${BASE}/slots`, {
      params: {
        type: selectedType.value,
        date: selectedDate.value
      }
    })

    slots.value = res.data.slots || []
  } catch (err) {
    console.error(err)
    alert("Error fetching slots")
  }

  loading.value = false
}
</script>

<style scoped>
.font-serif {
  font-family: Georgia, "Times New Roman", serif;
}
</style>
