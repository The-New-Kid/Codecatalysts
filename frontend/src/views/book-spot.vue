<template>
  <div>
    <div class="max-w-lg mx-auto mt-12 px-4" data-aos="fade-up">
      <h2 class="text-3xl font-extrabold text-center text-indigo-700 mb-8">Book a Parking Spot</h2>

      <!-- Public / Private Toggle -->
      <div class="flex justify-center gap-4 mb-6">
        <button
          class="px-6 py-2 rounded-full font-semibold transition duration-200"
          :class="lotType !== 'private' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'"
          @click="setLotType('public')"
        >Public</button>

        <button
          class="px-6 py-2 rounded-full font-semibold transition duration-200"
          :class="lotType === 'private' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'"
          @click="setLotType('private')"
        >Private</button>
      </div>

      <div class="bg-white shadow-lg rounded-2xl p-6 hover:shadow-2xl transition duration-300">
        <div v-if="hasActiveBooking" class="bg-red-100 text-red-700 p-3 rounded-lg mb-4 font-semibold text-center">
          You already have an active parking booking. Release it before booking again.
        </div>

        <form @submit.prevent="onSubmit" class="space-y-4">
          
          <!-- Location -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">Select Location</label>
            <select v-model.number="form.lot_id" class="w-full border rounded-lg px-3 py-2" required>
              <option value="">-- Choose Location --</option>
              <option v-for="lot in lots" :key="lot.id" :value="lot.id">
                {{ lot.name }} - {{ lot.address }}, {{ lot.pin_code }}
              </option>
            </select>
          </div>

          <!-- Vehicle -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">Vehicle Number</label>
            <input v-model="form.vehicle_number" type="text" placeholder="Enter Vehicle Number" class="w-full border rounded-lg px-3 py-2" required />
          </div>

          <!-- Date -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">Select Date</label>
            <input v-model="form.parking_date" type="date" :min="minDate" :max="maxDate" class="w-full border rounded-lg px-3 py-2" required />
          </div>

          <!-- Slot selection -->
          <div>
            <label class="block text-gray-700 font-semibold mb-1">Select Time Slot</label>

            <!-- PUBLIC: Single slot -->
            <div v-if="lotType === 'public'">
              <select v-model.number="form.slot_id" class="w-full border rounded-lg px-3 py-2" required>
                <option value="">-- Choose Slot --</option>
                <option v-for="s in slots" :key="s.id" :value="s.id">
                  {{ s.start_time }} - {{ s.end_time }}
                </option>
              </select>
              <p class="text-sm text-gray-500 mt-1">Public parking — choose one slot.</p>
            </div>

            <!-- PRIVATE: Slot Range -->
            <div v-else>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-gray-700 font-medium mb-1">Start Slot</label>
                  <select v-model.number="form.start_slot" class="w-full border rounded-lg px-3 py-2" required>
                    <option value="">-- Start --</option>
                    <option v-for="s in slots" :key="s.id" :value="s.id">
                      {{ s.start_time }} - {{ s.end_time }}
                    </option>
                  </select>
                </div>

                <div>
                  <label class="block text-gray-700 font-medium mb-1">End Slot</label>
                  <select v-model.number="form.end_slot" class="w-full border rounded-lg px-3 py-2" required>
                    <option value="">-- End --</option>
                    <option v-for="s in slots" :key="s.id" :value="s.id">
                      {{ s.start_time }} - {{ s.end_time }}
                    </option>
                  </select>
                </div>
              </div>

              <p class="text-sm text-gray-500 mt-1">Private parking — choose continuous slots (any length).</p>

              <div v-if="privateValidationMessage" class="text-sm text-red-600 mt-2">
                {{ privateValidationMessage }}
              </div>
            </div>
          </div>

          <!-- Submit -->
          <div class="flex justify-end">
            <button type="submit" :disabled="submitting || !canSubmit"
              class="bg-green-500 hover:bg-green-600 disabled:opacity-50 text-white font-semibold px-6 py-2 rounded-xl">
              {{ submitting ? 'Booking…' : 'Book Spot' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL

const lotType = ref('public')
const lots = ref([])
const slots = ref([])
const submitting = ref(false)
const hasActiveBooking = ref(false)

const today = new Date()
const minDate = today.toISOString().split('T')[0]
const maxDateObj = new Date(today)
maxDateObj.setDate(today.getDate() + 14)
const maxDate = maxDateObj.toISOString().split('T')[0]

const form = ref({
  lot_id: null,
  vehicle_number: '',
  parking_date: '',
  slot_id: null,
  start_slot: null,
  end_slot: null
})

/* --- When user switches PUBLIC <-> PRIVATE --- */
const setLotType = (t) => {
  lotType.value = t
  form.value.lot_id = null
  form.value.slot_id = null
  form.value.start_slot = null
  form.value.end_slot = null
  loadLots()      // filtered reload
}

/* --- Load Lots (filtered) --- */
const loadLots = async () => {
  try {
    const res = await axios.get(`${BASE}/parking-lots`, {
      params: { type: lotType.value }
    })
    lots.value = res.data.lots || []
  } catch (e) {
    alert('Failed to load parking lots')
  }
}

/* --- Load Time Slots --- */
const loadSlots = async () => {
  try {
    const res = await axios.get(`${BASE}/parking-time-slots`)
    slots.value = (res.data.slots || []).map(s => ({
      ...s,
      start_minutes: parseMinutes(s.start_time),
      end_minutes: parseMinutes(s.end_time)
    }))
  } catch (e) {
    alert('Failed to load time slots')
  }
}

function parseMinutes(hhmm) {
  const [h, m] = hhmm.split(':').map(Number)
  return h * 60 + m
}

/* --- Active Booking Check (optional) --- */
const loadActiveStatus = async () => {
  try {
    const userId = localStorage.getItem('user_id')
    if (!userId) return
    const res = await axios.get(`${BASE}/user/active-parking`, {
      params: { user_id: userId }
    })
    hasActiveBooking.value = !!res.data.has_active
  } catch {
    hasActiveBooking.value = false
  }
}

/* --- Private Slot Validation (continuous only) --- */
const privateValidationMessage = computed(() => {
  if (lotType.value !== 'private') return ''
  if (!form.value.start_slot || !form.value.end_slot) return ''

  const start = slots.value.find(s => s.id === form.value.start_slot)
  const end = slots.value.find(s => s.id === form.value.end_slot)

  if (!start || !end) return 'Invalid slot selection'
  if (start.slot_order > end.slot_order) return 'End must be after start'

  const startIdx = slots.value.findIndex(s => s.id === start.id)
  const endIdx = slots.value.findIndex(s => s.id === end.id)
  const range = slots.value.slice(startIdx, endIdx + 1)

  for (let i = 0; i < range.length - 1; i++) {
    if (range[i + 1].start_minutes !== range[i].end_minutes) {
      return 'Slots must be continuous without gaps'
    }
  }

  return ''
})

/* --- Can Submit --- */
const canSubmit = computed(() => {
  if (!form.value.lot_id || !form.value.vehicle_number || !form.value.parking_date)
    return false

  if (lotType.value === 'public') {
    return !!form.value.slot_id
  }

  return (
    form.value.start_slot &&
    form.value.end_slot &&
    privateValidationMessage.value === ''
  )
})

/* --- Submit --- */
async function onSubmit() {
  if (!canSubmit.value) {
    alert('Please complete the form correctly')
    return
  }

  submitting.value = true
  const userId = localStorage.getItem('user_id')

  try {
    const payload = {
      user_id: Number(userId),
      lot_id: form.value.lot_id,
      vehicle_number: form.value.vehicle_number,
      parking_date: form.value.parking_date
    }

    if (lotType.value === 'public') {
      payload.slot_id = form.value.slot_id
    } else {
      payload.start_slot = form.value.start_slot
      payload.end_slot = form.value.end_slot
    }

    const res = await axios.post(`${BASE}/book-parking`, payload)
    alert(res.data.message)

    form.value.slot_id = null
    form.value.start_slot = null
    form.value.end_slot = null
    loadActiveStatus()

  } catch (err) {
    alert(err.response?.data?.message || 'Booking failed')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadLots()
  loadSlots()
  loadActiveStatus()
})
</script>
