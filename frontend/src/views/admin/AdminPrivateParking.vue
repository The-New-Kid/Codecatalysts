<template>
  <div class="max-w-7xl mx-auto mt-10 px-4 space-y-10">

    <!-- PAGE TITLE -->
    <h2 class="text-4xl font-bold text-center text-indigo-700 tracking-tight">
      🔒 Private Parking Lots
    </h2>

    <!-- FILTERS -->
    <div class="bg-white shadow-md rounded-2xl p-6 flex flex-col md:flex-row gap-4 items-center">
      <div class="flex flex-col w-full">
        <label class="text-sm text-gray-600 font-medium mb-1">Select Date</label>
        <input 
          type="date" 
          v-model="selectedDate"
          class="border rounded-xl px-3 py-2 focus:ring-2 focus:ring-indigo-400 outline-none"
        >
      </div>

      <div class="flex flex-col w-full">
        <label class="text-sm text-gray-600 font-medium mb-1">Select Time Slot</label>
<select
  v-model="selectedTimeslot"
  class="border rounded-xl px-3 py-2 focus:ring-2 focus:ring-indigo-400 outline-none"
>
  <option disabled value="">-- Choose Timeslot --</option>
  <option
    v-for="ts in timeslots"
    :key="ts.id"
    :value="ts.id"
  >
    {{ ts.start_time }} - {{ ts.end_time }}
  </option>
</select>
      </div>

      <button
        @click="fetchPrivateLots"
        class="bg-indigo-600 text-white px-6 py-3 rounded-xl shadow hover:bg-indigo-700 transition font-medium"
      >
        Apply
      </button>
    </div>

    <!-- LOADING -->
    <div v-if="loading" class="text-center text-gray-500 text-lg animate-pulse">
      Loading private parking lots...
    </div>

    <!-- ERROR -->
    <div v-else-if="error" class="text-center text-red-600 text-lg">
      {{ error }}
    </div>

    <!-- LOTS GRID -->
    <div
      v-else
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8"
    >
      <div
        v-for="lot in privateLots"
        :key="lot.id"
        class="bg-white border rounded-2xl shadow hover:shadow-xl transition p-6 space-y-4"
      >
        <!-- HEADER -->
        <div class="flex justify-between items-center">
          <h3 class="text-xl font-semibold text-gray-800">
            {{ lot.prime_location_name }}
          </h3>

          <div class="flex items-center gap-3">
            <RouterLink
              :to="`/admin/parking-lots/${lot.id}/edit`"
              class="text-indigo-600 hover:underline"
            >
              Edit
            </RouterLink>

            <button
              @click="onDeleteLot(lot.id)"
              class="text-red-500 hover:text-red-700 font-medium"
            >
              Delete
            </button>
          </div>
        </div>

        <!-- OCCUPANCY -->
        <p class="text-gray-500 text-sm">
          Occupied:
          <span class="font-semibold text-gray-800">
            {{ lot.occupied_count }}/{{ lot.max_spots }}
          </span>
        </p>

        <!-- SPOT GRID -->
        <div class="grid grid-cols-5 gap-2">
          <RouterLink
            v-for="spot in lot.spots"
            :key="spot.id"
            :to="`/admin/spots/${spot.id}?date=${selectedDate}&timeslot=${selectedTimeslot}`"
            class="text-center py-1 text-sm rounded-lg font-medium transition cursor-pointer"
            :class="spot.status === 'A'
              ? 'bg-green-100 text-green-700 hover:bg-green-200'
              : 'bg-red-100 text-red-700 hover:bg-red-200'"
          >
            {{ spot.status }}
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- ADD LOT BUTTON -->
    <div class="text-center mt-4">
      <RouterLink
        to="/admin/private-parking/add"
        class="bg-yellow-500 text-white px-8 py-3 rounded-xl shadow hover:bg-yellow-600 transition font-semibold"
      >
        + Add Private Lot
      </RouterLink>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink, useRouter } from 'vue-router'

const API_BASE = 'http://127.0.0.1:5000/api'

const privateLots = ref([])
const loading = ref(true)
const error = ref('')

const selectedDate = ref('')
const selectedTimeslot = ref('')

const onDeleteLot = async (id) => {
  if (!window.confirm('Delete this private parking lot?')) return

  try {
    await axios.delete(`${API_BASE}/admin/private-parking-lots/${id}`)
    privateLots.value = privateLots.value.filter(lot => lot.id !== id)
  } catch (err) {
    alert(err.response?.data?.message || "Deletion failed.")
  }
}
const timeslots = ref([]);

const fetchTimeslots = async () => {
  try {
    const res = await axios.get(`${API_BASE}/admin/time-slots`);
    timeslots.value = res.data;
  } catch {
    console.log("Failed to load timeslots");
  }
};

const fetchPrivateLots = async () => {
  loading.value = true;
  error.value = "";

  try {
    const res = await axios.get(`${API_BASE}/admin/private-parking-lots`, {
      params: {
        date: selectedDate.value,
        timeslot_id: selectedTimeslot.value
      }
    });

    privateLots.value = res.data;
  } catch (err) {
    error.value = "Failed to load private parking lots.";
  } finally {
    loading.value = false;
  }
};


onMounted(() => {
  fetchTimeslots();
  fetchPrivateLots();
});

</script>
