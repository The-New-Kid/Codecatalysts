<template>
  <UserLayout>
    <div class="max-w-lg mx-auto mt-12 px-4" data-aos="fade-up">
      
      <!-- Page Title -->
      <h2 class="text-3xl font-extrabold text-center text-indigo-700 mb-8">
        Book a Parking Spot
      </h2>

      <!-- Lot Type Toggle -->
      <div class="flex justify-center gap-4 mb-6">
        <button
          class="px-6 py-2 rounded-full font-semibold transition duration-200"
          :class="lotType !== 'private' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'"
          @click="setLotType('public')"
        >
          Public
        </button>
        <button
          class="px-6 py-2 rounded-full font-semibold transition duration-200"
          :class="lotType === 'private' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'"
          @click="setLotType('private')"
        >
          Private
        </button>
      </div>

      <div class="bg-white shadow-lg rounded-2xl p-6 hover:shadow-2xl transition duration-300">

        <div
          v-if="hasActiveBooking"
          class="bg-red-100 text-red-700 p-3 rounded-lg mb-4 font-semibold text-center"
        >
          You already have an active parking booking. You must release it before booking again.
        </div>

        <form @submit.prevent="submitBooking" class="space-y-4">
          <!-- Select Location -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">Select Location</label>
            <select
              v-model="form.lot_id"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              required
            >
              <option value="">-- Choose Location --</option>
              <option v-for="lot in filteredLots" :key="lot.id" :value="lot.id">
                {{ lot.name }} - {{ lot.address }}, {{ lot.pin_code }}
              </option>
            </select>
          </div>

          <!-- Vehicle Number -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">Vehicle Number</label>
            <input
              type="text"
              v-model="form.vehicle_number"
              placeholder="Enter Vehicle Number"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              required
            />
          </div>

          <!-- Select Date -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">Select Date</label>
            <input
              type="date"
              v-model="form.parking_date"
              :min="minDate"
              :max="maxDate"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              required
            />
          </div>

          <!-- Select Time Slot -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">Select Time Slot</label>
            <select
              v-model="form.slot_id"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              required
            >
              <option value="">-- Choose Slot --</option>
              <option v-for="slot in validSlots" :key="slot.id" :value="slot.id">
                {{ slot.start_time }} - {{ slot.end_time }}
              </option>
            </select>
          </div>

          <!-- Continuous Slot Count -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">Number of Continuous Slots</label>
            <input
              type="number"
              min="1"
              :max="maxContinuousSlots"
              v-model.number="form.slot_count"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              required
            />
            <p class="text-sm text-gray-500 mt-1">
              Max allowed: {{ maxContinuousSlots }} slots
            </p>
          </div>

          <!-- Submit Button -->
          <div class="flex justify-end">
            <button
              type="submit"
              :disabled="!formValid || hasActiveBooking"
              class="bg-green-500 hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold px-6 py-2 rounded-xl transition duration-200"
            >
              Book Spot
            </button>
          </div>
        </form>
      </div>
    </div>
  </UserLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import UserLayout from '@/layouts/UserLayout.vue'

const BASE = 'http://127.0.0.1:5000/api'

const lotType = ref('public')
const slots = ref([])
const lots = ref([])
const hasActiveBooking = ref(false)

const today = new Date()
const minDate = today.toISOString().split('T')[0]
const maxDateObj = new Date(today)
maxDateObj.setDate(today.getDate() + 14)
const maxDate = maxDateObj.toISOString().split('T')[0]

const form = ref({
  lot_id: '',
  vehicle_number: '',
  parking_date: '',
  slot_id: '',
  slot_count: 1
})

const setLotType = (type) => {
  lotType.value = type
}

const filteredLots = computed(() => {
  return lots.value.filter(lot => lot.is_private === (lotType.value === 'private'))
})

// Right now backend always sends available=true,
// but we keep this filter for future extension
const validSlots = computed(() => {
  return slots.value.filter(s => s.available === true)
})

const maxContinuousSlots = computed(() => {
  if (!form.value.slot_id) return 1
  const selectedSlot = slots.value.find(s => s.id === form.value.slot_id)
  if (!selectedSlot) return 1

  const startOrder = selectedSlot.slot_order
  let count = 0

  for (const slot of slots.value) {
    if (slot.slot_order >= startOrder && slot.available === true) {
      count++
    } else if (slot.slot_order > startOrder) {
      break
    }
  }
  return count || 1
})

const formValid = computed(() => {
  return (
    !!form.value.lot_id &&
    !!form.value.vehicle_number &&
    !!form.value.parking_date &&
    !!form.value.slot_id &&
    form.value.slot_count >= 1
  )
})

// Keep slot_count within allowed bound when user changes slot
watch(
  () => form.value.slot_id,
  () => {
    if (form.value.slot_count > maxContinuousSlots.value) {
      form.value.slot_count = maxContinuousSlots.value
    }
  }
)

const loadLots = async () => {
  try {
    const res = await axios.get(`${BASE}/parking-lots`)
    lots.value = res.data.lots || []
  } catch (err) {
    console.error('Error loading lots', err)
    alert('Failed to load parking lots')
  }
}

const loadSlots = async () => {
  try {
    const res = await axios.get(`${BASE}/parking-time-slots`)
    slots.value = res.data.slots || []
  } catch (err) {
    console.error('Error loading slots', err)
    alert('Failed to load time slots')
  }
}

const loadActiveStatus = async () => {
  try {
    const userId = localStorage.getItem('user_id')
    if (!userId) {
      hasActiveBooking.value = false
      return
    }

    const res = await axios.get(`${BASE}/user/active-parking`, {
      params: { user_id: userId }
    })

    hasActiveBooking.value = !!res.data.has_active
  } catch (err) {
    console.error('Error loading active status', err)
    // if backend returns 400 or error, we assume no active booking
    hasActiveBooking.value = false
  }
}

const submitBooking = async () => {
  try {
    const userId = localStorage.getItem('user_id')
    if (!userId) {
      alert('User not logged in')
      return
    }

    if (!formValid.value) {
      alert('Please fill all required fields')
      return
    }

    if (form.value.slot_count > maxContinuousSlots.value) {
      alert(`Maximum continuous slots allowed from this time is ${maxContinuousSlots.value}`)
      form.value.slot_count = maxContinuousSlots.value
      return
    }

    const payload = {
      ...form.value,
      user_id: userId
    }

    const res = await axios.post(`${BASE}/book-parking`, payload)
    alert(res.data.message || 'Parking request submitted')
    // optional: reset form
    // form.value = { lot_id: '', vehicle_number: '', parking_date: '', slot_id: '', slot_count: 1 }
    // loadActiveStatus()
  } catch (err) {
    console.error('Booking failed', err)
    const msg = err.response?.data?.message || 'Booking failed'
    alert(msg)
  }
}

onMounted(() => {
  loadLots()
  loadSlots()
  loadActiveStatus()
})
</script>
