<template>
  <UserLayout>
    <!-- HEADER -->
    <div class="relative w-full h-[300px] sm:h-[400px] overflow-hidden shadow-2xl">
      <div class="absolute inset-0">
        <img 
          src="/images/Somnath4.jpeg" 
          alt="Temple Darshan Banner" 
          class="w-full h-full object-cover object-center"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-red-900/80 via-red-900/40 to-black/30"></div>
      </div>

      <div class="relative z-10 flex flex-col items-center justify-center h-full text-center px-4" data-aos="fade-up">
        <h2 class="text-4xl md:text-5xl font-serif font-bold text-yellow-100 mb-2 drop-shadow-lg">
          🙏 Darshan Ticket Booking
        </h2>
        <p class="text-lg md:text-xl text-yellow-200 max-w-2xl mx-auto font-light drop-shadow-md">
          Secure your sacred visit to the divine abode.
        </p>
      </div>
    </div>

    <!-- BODY -->
    <div class="min-h-screen flex justify-center items-start bg-[#fffaf0] py-10">
      <div class="w-full max-w-3xl bg-white rounded-3xl shadow-2xl p-6 sm:p-10 border-t-8 border-red-700" data-aos="fade-up" data-aos-delay="200">

        <!-- BOOKER INFORMATION -->
        <h3 class="text-2xl font-serif font-bold text-center mb-8 text-red-800">
          Booker Information
        </h3>

        <div class="space-y-6">
          <div>
            <label class="block font-semibold mb-1 text-gray-700">Booker Name</label>
            <input v-model="booker.name"
                   class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 shadow-sm" />
          </div>

          <div>
            <label class="block font-semibold mb-1 text-gray-700">Email</label>
            <input v-model="booker.email" type="email"
                   class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 shadow-sm" />
          </div>

          <div>
            <label class="block font-semibold mb-1 text-gray-700">Mobile Number</label>
            <input v-model="booker.mobile"
                   class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 shadow-sm" />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block font-semibold mb-1 text-gray-700">Select Darshan Date</label>
              <input 
                type="date"
                v-model="selectedDate"
                :min="minDate"
                :max="maxDate"
                class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 shadow-sm"
              />
            </div>

            <div>
              <label class="block font-semibold mb-1 text-gray-700">Number of Tickets</label>
              <input 
                type="number"
                min="1"
                v-model.number="numMembers"
                @input="generatePassengers"
                class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 shadow-sm"
              />
            </div>
          </div>
        </div>

        <hr class="my-10 border-red-100" />

        <!-- PASSENGER DETAILS -->
        <h3 class="text-2xl font-serif font-bold text-center mb-8 text-red-800">
          Passenger Details & Verification
        </h3>

        <div 
          v-for="(p, i) in passengers" 
          :key="i"
          :data-aos="i % 2 === 0 ? 'fade-right' : 'fade-left'"
          :data-aos-delay="300 + (i * 100)"
          class="mt-6 p-5 sm:p-6 rounded-xl bg-red-50 border border-red-200 shadow-lg transition-all duration-300 hover:-translate-y-1 hover:border-red-700 hover:shadow-xl"
        >

          <h4 class="font-bold text-red-700 mb-4 text-lg border-b border-red-200 pb-2 flex items-center">
            <span class="mr-2 text-xl">👤</span> Passenger {{ i + 1 }}
          </h4>

          <input 
            v-model="p.name" 
            placeholder="Passenger Name"
            class="w-full p-3 border-2 border-gray-300 rounded-xl shadow-sm focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 mb-3"
          />

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <input 
              v-model="p.aadhar" 
              placeholder="Aadhar Number"
              class="w-full p-3 border-2 border-gray-300 rounded-xl shadow-sm focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300"
            />

            <button
              @click="sendOtp(i)"
              :disabled="p.cooldown > 0 || p.verified"
              class="w-full bg-red-700 text-white px-4 py-2 rounded-xl shadow font-semibold hover:bg-red-800 transition duration-300 disabled:bg-gray-400 disabled:opacity-60"
            >
              <span v-if="p.cooldown > 0">Resend in {{ p.cooldown }}s</span>
              <span v-else-if="p.verified">OTP Sent ✓</span>
              <span v-else>Send OTP</span>
            </button>
          </div>

          <!-- CHECKBOXES -->
          <div class="flex flex-col sm:flex-row gap-4 mb-4">
            <!-- Specially Abled -->
            <label class="flex items-center gap-2 text-red-700 font-medium cursor-pointer">
              <input 
                type="checkbox" 
                v-model="p.speciallyAbled"
                @change="onSpeciallyAbled(i)"
                class="w-5 h-5"
              />
              ♿ Specially Abled
            </label>

            <!-- Accompanying -->
            <label class="flex items-center gap-2 text-blue-700 font-medium cursor-pointer">
              <input 
                type="checkbox" 
                v-model="p.accompanying"
                @change="onAccompanying(i)"
                :disabled="!p.speciallyAbled && !canSelectAccompanying(i)"
                class="w-5 h-5 disabled:opacity-40"
              />
              👥 Accompanying
            </label>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input 
              v-model="p.otp"
              placeholder="Enter OTP"
              class="w-full p-3 border-2 border-gray-300 rounded-xl shadow-sm focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300"
            />

            <button
              @click="verifyOtp(i)"
              :disabled="p.verified || !p.otpSent"
              class="w-full bg-green-600 text-white px-4 py-2 rounded-xl shadow font-semibold hover:bg-green-700 transition duration-300 disabled:bg-gray-400 disabled:opacity-60"
            >
              {{ p.verified ? 'Verified ✓' : 'Verify OTP' }}
            </button>
          </div>

          <p :class="p.verified ? 'text-green-700' : 'text-red-700'" class="text-sm mt-3 font-medium">
            {{ p.status }}
          </p>

        </div>

        <!-- SUMMARY -->
        <div class="mt-8 p-4 bg-yellow-100 border border-yellow-300 rounded-xl text-center shadow">
          <p class="text-lg font-semibold text-yellow-800">
            ♿ {{ countSpeciallyAbled }} Specially Abled  &nbsp; | &nbsp;
            👥 {{ countAccompanying }} Accompanying
          </p>
        </div>

        <hr class="my-10 border-red-100" />

        <!-- SLOT SELECTION -->
        <div>
          <label class="block font-serif font-bold mb-2 text-red-800 text-xl">Select Darshan Slot</label>
          <select 
            v-model="selectedSlot"
            class="w-full p-3 border-2 border-gray-300 rounded-xl shadow-sm focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 bg-white"
          >
            <option value="">-- Select Slot --</option>
            <option v-for="s in slots" :key="s.id" :value="s.id">
              {{ s.slot_type }} | {{ s.start }} - {{ s.end }}
            </option>
          </select>
        </div>

        <!-- SUBMIT -->
        <button
          @click="bookTickets"
          class="w-full py-4 mt-10 rounded-full bg-gradient-to-r from-red-700 to-red-900 text-white font-bold text-lg shadow-xl hover:shadow-2xl hover:from-red-800 hover:to-red-900 transition duration-300 transform hover:scale-[1.01]"
        >
          Book Darshan Tickets (Submit)
        </button>

        <p class="text-center text-sm text-gray-500 mt-4">
          By clicking Book Ticket, you agree to the temple's terms and conditions.
        </p>

      </div>
    </div>
  </UserLayout>
</template>



<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "axios"
import { useUserStore } from "@/stores/user"
import UserLayout from "@/layouts/Userlayoutnew.vue"
import AOS from 'aos'
import 'aos/dist/aos.css'

onMounted(() => AOS.init({ duration: 800, once: true }))

const BASE = "http://192.168.29.154:5000/api"
const userStore = useUserStore()

const booker = ref({ name: userStore.name, email: "", mobile: "" })
const numMembers = ref(1)
const passengers = ref([])
const slots = ref([])
const selectedSlot = ref("")
const selectedDate = ref("")

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
      timer: null,

      // checkboxes
      speciallyAbled: false,
      accompanying: false
    })
  }
}

async function loadPage() {
  const res = await axios.get(`${BASE}/book-ticket/${userStore.id}`,
    { params: { type: 'Darshan' } }
  )
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

function canSelectAccompanying(index) {
  return passengers.value.every((p, i) => i === index || !p.accompanying)
}

function onAccompanying(index) {
  const p = passengers.value[index]
  if (p.accompanying && !canSelectAccompanying(index)) {
    alert("Only one passenger can be marked as Accompanying.")
    p.accompanying = false
  }
}

function onSpeciallyAbled(index) {
  const p = passengers.value[index]

  // If unchecked special, also uncheck accompanying
  if (!p.speciallyAbled) p.accompanying = false
}

/* ---------------- COMPUTED SUMMARY ---------------- */

const countSpeciallyAbled = computed(() => passengers.value.filter(p => p.speciallyAbled).length)
const countAccompanying = computed(() => passengers.value.filter(p => p.accompanying).length)

/* ---------------- BOOKING ---------------- */

async function bookTickets() {
  if (!selectedDate.value) return alert("Please select Darshan date")
  if (!selectedSlot.value) return alert("Please select a slot")
  if (passengers.value.some(p => !p.verified)) return alert("Verify all OTPs first")
  if (countAccompanying.value > 1) return alert("Only one passenger can be Accompanying")

  // SEND VALUES AS is_special AND with_special
  const finalPassengers = passengers.value.map(p => ({
    ...p,
    is_special: p.speciallyAbled ? true : false,
    with_special: p.accompanying ? true : false
  }))

  const res = await axios.post(`${BASE}/book-ticket`, {
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
