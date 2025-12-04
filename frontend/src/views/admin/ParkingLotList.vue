<template>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        
                <div class="flex flex-col sm:flex-row justify-between items-center mb-12">
                    <div class="flex flex-wrap gap-4 mb-8">

            <!-- Date picker -->
            <input
                type="date"
                v-model="selectedDate"
                @change="fetchParkingLots"
                class="px-4 py-2 border rounded-lg shadow-sm"
            />

            <!-- Time slot dropdown -->
            <select
                v-model="selectedTimeSlot"
                @change="fetchParkingLots"
                class="px-4 py-2 border rounded-lg shadow-sm"
            >
                <option value="">Select Time Slot</option>
                <option
                    v-for="slot in timeSlots"
                    :key="slot.id"
                    :value="slot.id"
                >
                    {{ slot.start_time }} - {{ slot.end_time }}
                </option>
            </select>

        </div>

            <h2
                class="text-4xl sm:text-5xl font-extrabold text-red-800 
                       mb-4 sm:mb-0 drop-shadow-md font-serif"
                data-aos="fade-right"
            >
                Mandir Parking Lots Management
            </h2>
            
            <RouterLink
                to="/admin/parking-lots/add"
                class="inline-block px-8 py-3 bg-gradient-to-r from-orange-500 to-red-500 text-white font-bold rounded-full shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 text-lg"
                data-aos="fade-left"
            >
                + Add New Parking Lot
            </RouterLink>
        </div>

        <div v-if="loading" class="text-center text-gray-600">
            Loading parking lots...
        </div>
        <div v-else-if="error" class="text-center text-red-600">
            {{ error }}
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <div
                v-for="lot in parkingLots"
                :key="lot.id"
                class="bg-white rounded-3xl shadow-lg p-6 hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 border-t-4 border-yellow-500"
                data-aos="fade-up"
            >
                <h3 class="text-2xl font-semibold mb-4 text-red-800">
                    {{ lot.prime_location_name }}
                </h3>

                <div class="flex flex-wrap gap-3 mb-4 text-sm font-medium text-gray-700">
                    <span class="inline-flex items-center gap-1">
                        <span class="w-4 h-4 bg-green-500 rounded-sm"></span>Normal
                    </span>
                    <span class="inline-flex items-center gap-1">
                        <span class="w-4 h-4 bg-gray-400 rounded-sm"></span>Extra
                    </span>
                    <span class="inline-flex items-center gap-1">
                        <span class="w-4 h-4 bg-pink-500 rounded-sm"></span>VIP
                    </span>
                    <span class="inline-flex items-center gap-1">
                        <span class="w-4 h-4 bg-red-600 rounded-sm"></span>Occupied
                    </span>
                </div>

                <div class="flex gap-4 mb-4">
                    <RouterLink
                        :to="`/admin/parking-lots/${lot.id}/edit`"
                        class="text-orange-600 font-semibold hover:text-orange-800 transition"
                    >
                        Edit
                    </RouterLink>

                    <button
                        type="button"
                        class="text-red-600 font-semibold hover:text-red-800 transition"
                        @click="onDeleteLot(lot.id)"
                    >
                        Delete
                    </button>
                </div>

                <p class="text-gray-600 mb-4 font-medium">
                    Occupied: {{ lot.occupied_count }}/{{ lot.max_spots }}
                </p>

                <div class="grid grid-cols-5 gap-3">
                    <RouterLink
                        v-for="spot in lot.colored_spots"
                        :key="spot.id"
                        :to="`/admin/spots/${spot.id}`"
                        class="flex items-center justify-center w-12 h-12 rounded-lg font-bold text-sm
                                hover:scale-110 transform transition-all duration-200 shadow-md"
                        :class="spotClasses(spot)"
                    >
                        {{ spotLabel(spot) }}
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'
import feather from 'feather-icons'
import AOS from 'aos'
import 'aos/dist/aos.css'

const selectedDate = ref('')
const selectedTimeSlot = ref('')
const timeSlots = ref([])
const parkingLots = ref([])
const loading = ref(true)
const error = ref('')

const API_BASE = 'http://127.0.0.1:5000/api' // backend base

const fetchParkingLots = async () => {
    loading.value = true
    error.value = ''

    try {
        const params = {}
        if (selectedDate.value) params.date = selectedDate.value
        if (selectedTimeSlot.value) params.timeslot_id = selectedTimeSlot.value

        const res = await axios.get(`${API_BASE}/admin/parking-lots`, { params })

        parkingLots.value = res.data
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load parking lots.'
    } finally {
        loading.value = false
    }
}


const onDeleteLot = async (id) => {
    if (!window.confirm('Are you sure you want to delete this parking lot?')) return
    try {
        await axios.delete(`${API_BASE}/admin/parking-lots/${id}`)
        parkingLots.value = parkingLots.value.filter((lot) => lot.id !== id)
    } catch (err) {
        console.error(err)
        alert('Failed to delete parking lot.')
    }
}

const spotClasses = (spot) => {
    // same as Jinja logic: first color class, then occupied override
    if (spot.status === 'O') {
        return 'bg-red-600 text-white'
    }
    if (spot.color === 'green') return 'bg-green-500 text-black'
    if (spot.color === 'grey') return 'bg-gray-400 text-white'
    if (spot.color === 'pink') return 'bg-pink-500 text-white'
    return ''
}

const spotLabel = (spot) => {
    if (spot.status !== 'A') return 'O'
    if (spot.color === 'green') return 'A'
    if (spot.color === 'grey') return 'E'
    if (spot.color === 'pink') return 'V'
    return ''
}


const fetchTimeSlots = async () => {
    try {
        const res = await axios.get(`${API_BASE}/admin/time-slots`)
        timeSlots.value = res.data
    } catch (err) {
        console.error(err)
        alert("Failed to load time slots")
    }
}

onMounted(() => {
    // Ensure Feather and AOS are initialized on the new page
    feather.replace() 
    AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
    fetchTimeSlots()
    fetchParkingLots()

    fetchParkingLots()
})
</script>