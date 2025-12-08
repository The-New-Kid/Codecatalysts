<template>
  <div>

    <!-- ✅ RESPONSIVE HEADER -->
    <div class="relative w-full h-[220px] sm:h-[300px] md:h-[400px] overflow-hidden shadow-2xl">
      <div class="absolute inset-0">
        <img
          src="/images/Somnath4.jpeg"
          alt="Temple Darshan Banner"
          class="w-full h-full object-cover object-center"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-red-900/80 via-red-900/40 to-black/30"></div>
      </div>

      <div
        class="relative z-10 flex flex-col items-center justify-center h-full text-center px-4"
        data-aos="fade-up"
      >
        <h2 class="text-2xl sm:text-4xl md:text-5xl font-serif font-bold text-yellow-100 mb-2 drop-shadow-lg">
          🙏 Sugam Darshan Ticket
        </h2>

        <p class="text-sm sm:text-lg md:text-xl text-yellow-200 max-w-2xl mx-auto font-light drop-shadow-md">
          Secure your sacred visit to the divine abode.
        </p>
      </div>
    </div>

    <!-- ✅ BODY -->
    <div class="min-h-screen flex justify-center items-start bg-[#fffaf0] py-6 sm:py-10 px-3 sm:px-6">

      <div
        class="w-full max-w-3xl bg-white rounded-2xl sm:rounded-3xl
               shadow-2xl p-5 sm:p-10 border-t-8 border-red-700"
        data-aos="fade-up"
        data-aos-delay="200"
      >

        <!-- ✅ BOOKER INFO -->
        <h3 class="text-xl sm:text-2xl font-serif font-bold text-center mb-6 sm:mb-8 text-red-800">
          Devotee Details
        </h3>

        <div class="space-y-5 sm:space-y-6">
          <div>
            <label class="block font-semibold mb-1 text-gray-700 text-sm sm:text-base">
              Devotee Name
            </label>
            <input
              v-model="booker.name"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
            />
          </div>

          <div>
            <label class="block font-semibold mb-1 text-gray-700 text-sm sm:text-base">
              Email
            </label>
            <input
              v-model="booker.email"
              type="email"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
            />
          </div>

          <div>
            <label class="block font-semibold mb-1 text-gray-700 text-sm sm:text-base">
              Mobile Number
            </label>
            <input
              v-model="booker.mobile"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
            <div>
              <label class="block font-semibold mb-1 text-gray-700">
                Select Darshan Date
              </label>
              <input
                type="date"
                v-model="selectedDate"
                :min="minDate"
                :max="maxDate"
                class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
              />
            </div>

            <div>
              <label class="block font-semibold mb-1 text-gray-700">
                Total Number of Tickets
              </label>
              <input
                type="number"
                min="1"
                v-model.number="numMembers"
                @input="generatePassengers"
                class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
              />
            </div>
          </div>

          <!-- ✅ SPECIAL DEVOTEES COUNT -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
            <div>
              <label class="block font-semibold mb-1 text-gray-700">
                Number of Specially-Abled Devotees
                <span class="text-xs text-gray-500">(≤ Total Tickets)</span>
              </label>
              <input
                type="number"
                min="0"
                :max="numMembers"
                v-model.number="numSpecial"
                @input="onSpecialCountChange"
                class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
              />
            </div>

            <div class="flex flex-col justify-center text-sm sm:text-base text-gray-700">
              <span>♿ Specially-Abled: {{ countSpeciallyAbled }}</span>
              <span>👥 Accompanying Allowed: {{ countSpeciallyAbled }}</span>
            </div>
          </div>
        </div>

        <hr class="my-8 sm:my-10 border-red-100" />

        <!-- ✅ PASSENGERS -->
        <h3 class="text-xl sm:text-2xl font-serif font-bold text-center mb-6 sm:mb-8 text-red-800">
          Passenger Details & Verification
        </h3>

        <div
          v-for="(p, i) in passengers"
          :key="i"
          class="mt-5 p-4 sm:p-6 rounded-xl bg-red-50 border border-red-200 shadow-lg transition"
        >

          <h4 class="font-bold text-red-700 mb-3 text-base sm:text-lg flex items-center">
            <span class="mr-2" v-if="p.speciallyAbled">♿</span>
            <span class="mr-2" v-else>👤</span>

            <span v-if="p.speciallyAbled">
              Specially Abled Devotee {{ getSpecialIndex(i) }}
            </span>
            <span v-else>
              Passenger {{ getNormalIndex(i) }}
            </span>
          </h4>

          <input
            v-model="p.name"
            placeholder="Passenger Name"
            class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl mb-3"
          />

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
            <input
              v-model="p.aadhar"
              placeholder="Aadhar Number"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl"
            />

            <button
              @click="sendOtp(i)"
              :disabled="p.cooldown > 0 || p.verified"
              class="w-full bg-red-700 text-white px-4 py-2 rounded-xl shadow font-semibold disabled:bg-gray-400"
            >
              <span v-if="p.cooldown > 0">Resend in {{ p.cooldown }}s</span>
              <span v-else-if="p.verified">OTP Sent ✓</span>
              <span v-else>Send OTP</span>
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
            <input
              v-model="p.age"
              type="number"
              placeholder="Age"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl"
            />

            <select
              v-model="p.gender"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl bg-white"
            >
              <option value="">Select Gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>

          <div class="flex flex-col sm:flex-row gap-3 mb-4">
            <!-- Info badge instead of checkbox for special flag -->
            <div class="flex items-center gap-2 text-red-700 font-medium">
              <span v-if="p.speciallyAbled">♿ Specially Abled Devotee</span>
              <span v-else>👤 Normal Passenger</span>
            </div>

            <label class="flex items-center gap-2 text-blue-700 font-medium cursor-pointer">
              <input
                type="checkbox"
                v-model="p.accompanying"
                @change="onAccompanying(i)"
                :disabled="p.speciallyAbled || !canSelectAccompanying(i)"
              />
              👥 Accompanying
            </label>

            <label class="flex items-center gap-2 text-purple-700 font-medium cursor-pointer">
              <input
                type="checkbox"
                v-model="p.wheelchairNeeded"
              />
              🦽 Wheelchair Needed
            </label>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <input
              v-model="p.otp"
              placeholder="Enter OTP"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl"
            />

            <button
              @click="verifyOtp(i)"
              :disabled="p.verified || !p.otpSent"
              class="w-full bg-green-600 text-white px-4 py-2 rounded-xl shadow font-semibold disabled:bg-gray-400"
            >
              {{ p.verified ? 'Verified ✓' : 'Verify OTP' }}
            </button>
          </div>
        </div>

        <!-- ✅ SLOT -->
        <div class="mt-8">
          <label class="block font-serif font-bold mb-2 text-red-800 text-lg sm:text-xl">
            Select Darshan Slot
          </label>
          <select
            v-model="selectedSlot"
            class="w-full p-3 border-2 border-gray-300 rounded-xl bg-white"
          >
            <option value="">-- Select Slot --</option>
            <option v-for="s in slots" :key="s.id" :value="s.id">
              {{ s.slot_type }} | {{ s.start }} - {{ s.end }}
            </option>
          </select>
        </div>

        <!-- ✅ SUBMIT -->
        <button
          @click="bookTickets"
          class="w-full py-3 sm:py-4 mt-8 sm:mt-10 rounded-full
                 bg-gradient-to-r from-red-700 to-red-900 text-white
                 font-bold text-base sm:text-lg shadow-xl"
        >
          Book Darshan Tickets
        </button>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "axios"
import { useUserStore } from "@/stores/user"
import AOS from 'aos'
import 'aos/dist/aos.css'

onMounted(() => AOS.init({ duration: 800, once: true }))

const BASE = import.meta.env.VITE_API_URL
const userStore = useUserStore()

const booker = ref({ name: userStore.name, email: "", mobile: "" })

const numMembers = ref(1)
const numSpecial = ref(0)

const passengers = ref([])
const slots = ref([])
const selectedSlot = ref("")
const selectedDate = ref("")

const today = new Date()
today.setDate(today.getDate() + 1)
const minDate = today.toISOString().split("T")[0]
const maxLimit = new Date()
maxLimit.setDate(today.getDate() + 6)
const maxDate = maxLimit.toISOString().split("T")[0]

function generatePassengers() {
  // Basic safety on counts
  if (numMembers.value < 1) numMembers.value = 1
  if (numSpecial.value < 0) numSpecial.value = 0
  if (numSpecial.value > numMembers.value) numSpecial.value = numMembers.value

  const oldPassengers = passengers.value
  passengers.value = []

  for (let i = 0; i < numMembers.value; i++) {
    const old = oldPassengers[i] || {}

    passengers.value.push({
      name: old.name || "",
      aadhar: old.aadhar || "",
      otp: "",
      otpSent: false,
      verified: old.verified || false,
      status: "",
      cooldown: 0,
      timer: null,
      // first numSpecial are specially abled
      speciallyAbled: i < numSpecial.value,
      accompanying: false,
      age: old.age || "",
      gender: old.gender || "",
      wheelchairNeeded: old.wheelchairNeeded || false,
    })
  }
}

function onSpecialCountChange() {
  if (numSpecial.value < 0) numSpecial.value = 0
  if (numSpecial.value > numMembers.value) numSpecial.value = numMembers.value
  generatePassengers()
}

async function loadPage() {
  const res = await axios.get(`${BASE}/book-ticket/${userStore.id}`, {
    params: { type: 'Darshan' }
  })
  slots.value = res.data.slots
}

/* ---------------- OTP ---------------- */

async function sendOtp(i) {
  const p = passengers.value[i]
  if (!p.aadhar) return alert("Enter Aadhar number")

  const res = await axios.post(`${BASE}/send-otp`, { aadhar: p.aadhar })
  p.status = res.data.message
  p.otpSent = true
  p.cooldown = 60

  if (p.timer) {
    clearInterval(p.timer)
  }

  p.timer = setInterval(() => {
    p.cooldown--
    if (p.cooldown === 0) {
      clearInterval(p.timer)
      p.timer = null
    }
  }, 1000)
}

async function verifyOtp(i) {
  const p = passengers.value[i]
  const res = await axios.post(`${BASE}/verify-otp`, { aadhar: p.aadhar, otp: p.otp })
  p.verified = res.data.success
  p.status = p.verified ? "Verified ✓" : "OTP Invalid"
}

/* ---------------- ACCOMPANYING RULE ---------------- */

const countSpeciallyAbled = computed(() =>
  passengers.value.filter(p => p.speciallyAbled).length
)

const countAccompanying = computed(() =>
  passengers.value.filter(p => p.accompanying).length
)

function canSelectAccompanying(index) {
  const specialCount = countSpeciallyAbled.value
  if (specialCount === 0) return false

  const currentAccompanying = passengers.value.filter(p => p.accompanying).length
  const p = passengers.value[index]

  // If trying to turn ON accompanying and already at limit, block
  if (!p.accompanying && currentAccompanying >= specialCount) {
    return false
  }
  return true
}

function onAccompanying(index) {
  const p = passengers.value[index]

  // Only normal passengers can be accompanying
  if (p.speciallyAbled) {
    p.accompanying = false
    return
  }

  // If user just turned it ON, enforce max = #special
  if (p.accompanying) {
    const specialCount = countSpeciallyAbled.value
    const currentAccompanying = passengers.value.filter(pp => pp.accompanying).length
    if (currentAccompanying > specialCount) {
      alert("Accompanying passengers cannot be more than specially-abled devotees.")
      p.accompanying = false
    }
  }
}

/* ---------------- LABEL HELPERS ---------------- */

function getSpecialIndex(index) {
  let count = 0
  for (let i = 0; i <= index; i++) {
    if (passengers.value[i].speciallyAbled) count++
  }
  return count
}

function getNormalIndex(index) {
  let count = 0
  for (let i = 0; i <= index; i++) {
    if (!passengers.value[i].speciallyAbled) count++
  }
  return count
}

/* ---------------- BOOKING ---------------- */

async function bookTickets() {
  if (!selectedDate.value) return alert("Please select Darshan date")
  if (!selectedSlot.value) return alert("Please select a slot")
  if (passengers.value.some(p => !p.verified)) return alert("Verify all OTPs first")

  if (countAccompanying.value > countSpeciallyAbled.value) {
    return alert("Accompanying passengers cannot be more than specially-abled devotees.")
  }

  const finalPassengers = passengers.value.map(p => ({
    ...p,
    age: p.age,
    gender: p.gender,
    is_special: p.speciallyAbled ? true : false,
    with_special: p.accompanying ? true : false,
    wheelchair_needed: p.wheelchairNeeded ? true : false,
  }))

  const res = await axios.post(`${BASE}/api/book-ticket`, {
    user_id: userStore.id,
    slot_id: selectedSlot.value,
    darshan_date: selectedDate.value,
    mobile_number: booker.value.mobile,
    passengers: finalPassengers
  })

  alert(res.data.success ? "Tickets Booked Successfully!" : res.data.message)
}

onMounted(() => {
  generatePassengers()
  loadPage()
})
</script>