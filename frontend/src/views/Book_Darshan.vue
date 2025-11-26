<template>
  <UserLayout>
    <div class="min-h-screen flex justify-center items-start bg-[#fffaf0] py-10">
      <div class="w-full max-w-3xl bg-white rounded-3xl shadow-xl p-10">

        <h2 class="text-3xl font-bold text-center mb-10 text-purple-700">
          Book Darshan Ticket
        </h2>

        <!-- Booker Info -->
        <div class="space-y-6">
          <div>
            <label class="block font-semibold mb-1">Booker Name</label>
            <input v-model="booker.name" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-purple-400" />
          </div>

          <div>
            <label class="block font-semibold mb-1">Email</label>
            <input v-model="booker.email" type="email" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-purple-400" />
          </div>

          <div>
            <label class="block font-semibold mb-1">Mobile Number</label>
            <input v-model="booker.mobile" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-purple-400" />
          </div>

          <!-- Darshan Date -->
          <div>
            <label class="block font-semibold mb-1">Select Darshan Date</label>
            <input
              type="date"
              v-model="selectedDate"
              :min="minDate"
              :max="maxDate"
              class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-purple-400"
            />
          </div>

          <div>
            <label class="block font-semibold mb-1">Number of Tickets</label>
            <input
              type="number"
              min="1"
              v-model.number="numMembers"
              @input="generatePassengers"
              class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-purple-400"
            />
          </div>
        </div>

        <!-- Passenger Section -->
        <div v-for="(p, i) in passengers" :key="i" class="mt-8 p-5 rounded-xl bg-purple-50 border">

          <h4 class="font-semibold text-purple-700 mb-4">
            Passenger {{ i + 1 }}
          </h4>

          <input v-model="p.name" class="w-full p-3 border rounded-lg mb-3" placeholder="Passenger Name" />

          <div class="grid grid-cols-2 gap-4 mb-3">
            <input v-model="p.aadhar" class="w-full p-3 border rounded-lg" placeholder="Aadhar Number" />

            <button
              class="bg-purple-500 text-white rounded-lg px-4 py-2 hover:bg-purple-600 disabled:opacity-50"
              @click="sendOtp(i)"
              :disabled="p.cooldown > 0"
            >
              <span v-if="p.cooldown > 0">Resend in {{ p.cooldown }}s</span>
              <span v-else>Send OTP</span>
            </button>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <input v-model="p.otp" class="w-full p-3 border rounded-lg" placeholder="Enter OTP" />

            <button
              class="bg-green-500 text-white rounded-lg px-4 py-2 hover:bg-green-600 disabled:opacity-50"
              @click="verifyOtp(i)"
              :disabled="p.verified"
            >
              {{ p.verified ? 'Verified ✓' : 'Verify OTP' }}
            </button>
          </div>

          <p class="text-sm mt-2" :class="p.verified ? 'text-green-600' : 'text-red-600'">
            {{ p.status }}
          </p>
        </div>

        <!-- Slot Selection -->
        <div class="mt-8">
          <label class="block font-semibold mb-2">Select Slot</label>
          <select v-model="selectedSlot" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-purple-400">
            <option value="">-- Select Slot --</option>
            <option v-for="s in slots" :key="s.id" :value="s.id">
              {{ s.slot_type }} | {{ s.start }} - {{ s.end }}
            </option>
          </select>
        </div>

        <button
          class="w-full py-3 mt-8 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 text-white font-semibold shadow-lg hover:shadow-xl"
          @click="bookTickets"
        >
          Book Ticket
        </button>

      </div>
    </div>
  </UserLayout>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { useUserStore } from "@/stores/user"
import UserLayout from "@/layouts/UserLayout.vue"

const BASE = "http://127.0.0.1:5000/api"
const userStore = useUserStore()

const booker = ref({ name: userStore.name, email: "", mobile: "" })
const numMembers = ref(1)
const passengers = ref([])
const slots = ref([])
const selectedSlot = ref("")
const selectedDate = ref("")

// Date limits (today to next 14 days)
const today = new Date()
const minDate = today.toISOString().split('T')[0]
const maxLimit = new Date()
maxLimit.setDate(today.getDate() + 7)
const maxDate = maxLimit.toISOString().split('T')[0]

function generatePassengers() {
  passengers.value = []
  for (let i = 0; i < numMembers.value; i++) {
    passengers.value.push({
      name: "",
      aadhar: "",
      otp: "",
      otpSent: false,
      verified: false,
      status: "",
      cooldown: 0,
      timer: null
    })
  }
}

async function loadPage() {
  const res = await axios.get(`${BASE}/book-ticket/${userStore.id}`)
  slots.value = res.data.slots
}

async function sendOtp(index) {
  const p = passengers.value[index]
  if (!p.aadhar) return alert("Enter Aadhar number")

  const res = await axios.post(`${BASE}/send-otp`, { aadhar: p.aadhar })
  p.status = res.data.message
  p.otpSent = true

  p.cooldown = 60
  p.timer = setInterval(() => {
    p.cooldown--
    if (p.cooldown === 0) {
      clearInterval(p.timer)
      p.timer = null
    }
  }, 1000)
}

async function verifyOtp(index) {
  const p = passengers.value[index]
  const res = await axios.post(`${BASE}/verify-otp`, { aadhar: p.aadhar, otp: p.otp })
  p.verified = res.data.success
  p.status = p.verified ? "Verified ✓" : "OTP Invalid"
}

async function bookTickets() {
  if (!selectedDate.value) return alert("Please select Darshan date")
  if (!selectedSlot.value) return alert("Please select a slot")
  if (passengers.value.some(p => !p.verified)) return alert("Verify all OTPs first")

  const res = await axios.post(`${BASE}/book-ticket`, {
    user_id: userStore.id,
    slot_id: selectedSlot.value,
    darshan_date: selectedDate.value,
    mobile_number: booker.value.mobile,
    passengers: passengers.value
  })

  alert(res.data.success ? "Tickets Booked Successfully!" : res.data.message)
}

onMounted(() => {
  generatePassengers()
  loadPage()
})
</script>
