<template>
  <div>

    <!-- ✅ RESPONSIVE HEADER -->
    <div class="relative w-full h-[200px] sm:h-[300px] md:h-[400px] overflow-hidden shadow-2xl">
      <div class="absolute inset-0">
        <img 
          src="/images/Somnath4.jpeg" 
          alt="Temple Aarti Banner" 
          class="w-full h-full object-cover object-center"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-red-900/80 via-red-900/40 to-black/30"></div>
      </div>

      <div class="relative z-10 flex flex-col items-center justify-center h-full text-center px-3 sm:px-4" data-aos="fade-up">
        <h2 class="text-2xl sm:text-4xl md:text-5xl font-serif font-bold text-yellow-100 mb-2 drop-shadow-lg animate-fade-in-up">
          🪔 Aarti Ticket Booking
        </h2>
        <p class="text-sm sm:text-lg md:text-xl text-yellow-200 max-w-2xl mx-auto font-light drop-shadow-md">
          Secure your sacred visit to the divine abode.
        </p>
      </div>
    </div>

    <!-- ✅ BODY -->
    <div class="min-h-screen flex justify-center items-start bg-[#fffaf0] py-6 sm:py-10 px-3 sm:px-6">

      <div class="w-full max-w-3xl bg-white rounded-2xl sm:rounded-3xl shadow-2xl p-5 sm:p-10 border-t-8 border-red-700"
           data-aos="fade-up" data-aos-delay="200">

        <h3 class="text-xl sm:text-2xl font-serif font-bold text-center mb-6 sm:mb-8 text-red-800">
          Devotee Information
        </h3>

        <div class="space-y-5 sm:space-y-6">
          <div>
            <label class="block font-semibold mb-1 text-gray-700 text-sm sm:text-base">Booker Name</label>
            <input v-model="booker.name"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm" />
          </div>

          <div>
            <label class="block font-semibold mb-1 text-gray-700 text-sm sm:text-base">Email</label>
            <input v-model="booker.email" type="email"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm" />
          </div>

          <div>
            <label class="block font-semibold mb-1 text-gray-700 text-sm sm:text-base">Mobile Number</label>
            <input v-model="booker.mobile"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm" />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
            <div>
              <label class="block font-semibold mb-1 text-gray-700">Select Aarti Date</label>
              <input type="date" v-model="selectedDate" :min="minDate" :max="maxDate"
                class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm" />
            </div>

            <div>
              <label class="block font-semibold mb-1 text-gray-700">Number of Tickets</label>
              <input type="number" min="1" v-model.number="numMembers" @input="generatePassengers"
                class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm" />
            </div>
          </div>
        </div>

        <hr class="my-8 sm:my-10 border-red-100" />

        <h3 class="text-xl sm:text-2xl font-serif font-bold text-center mb-6 sm:mb-8 text-red-800">
          Devotee Details & Verification
        </h3>

        <div
          v-for="(p, i) in passengers"
          :key="i"
          class="mt-5 p-4 sm:p-6 rounded-xl bg-red-50 border border-red-200 shadow-lg darshan-card"
        >
          <h4 class="font-bold text-red-700 mb-3 text-base sm:text-lg flex items-center">
            <span class="mr-2">👤</span> Devotee {{ i + 1 }}
          </h4>

          <input v-model="p.name"
            class="w-full p-2.5 sm:p-3 border rounded-lg mb-3"
            placeholder="Passenger Name" />

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
            <input v-model="p.aadhar"
              class="w-full p-2.5 sm:p-3 border rounded-lg"
              placeholder="Aadhar Number" />

            <button
              class="bg-red-700 text-white rounded-lg px-4 py-2 font-semibold disabled:bg-gray-400"
              @click="sendOtp(i)"
              :disabled="p.cooldown > 0 || p.verified"
            >
              <span v-if="p.cooldown > 0">Resend in {{ p.cooldown }}s</span>
              <span v-else-if="p.verified">OTP Sent ✓</span>
              <span v-else>Send OTP</span>
            </button>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
            <input v-model="p.age" type="number" placeholder="Age"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl" />

            <select v-model="p.gender"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl bg-white">
              <option value="">Select Gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <input v-model="p.otp"
              class="w-full p-2.5 sm:p-3 border rounded-lg"
              placeholder="Enter OTP" />

            <button
              class="bg-green-600 text-white rounded-lg px-4 py-2 font-semibold disabled:bg-gray-400"
              @click="verifyOtp(i)"
              :disabled="p.verified || !p.otpSent"
            >
              {{ p.verified ? 'Verified ✓' : 'Verify OTP' }}
            </button>
          </div>

          <p class="text-sm mt-3 font-medium" :class="p.verified ? 'text-green-700' : 'text-red-700'">
            {{ p.status }}
          </p>
            <label class="flex items-center gap-2 text-purple-700 font-medium cursor-pointer">
            <input type="checkbox" v-model="p.wheelchairNeeded" />
            🦽 Wheelchair Needed
          </label>
        </div>

        <hr class="my-8 sm:my-10 border-red-100" />

        <div class="mt-6 sm:mt-8">
          <label class="block font-serif font-bold mb-2 text-red-800 text-lg sm:text-xl">
            Select Aarti Slot
          </label>
          <select v-model="selectedSlot"
            class="w-full p-3 border-2 border-gray-300 rounded-xl bg-white">
            <option value="">-- Select Slot --</option>
            <option v-for="s in slots" :key="s.id" :value="s.id">
              {{ s.slot_type }} | {{ s.start }} - {{ s.end }}
            </option>
          </select>
        </div>

        <button
          class="w-full py-3 sm:py-4 mt-8 sm:mt-10 rounded-full
                 bg-gradient-to-r from-red-700 to-red-900 text-white
                 font-bold text-base sm:text-lg shadow-xl"
          @click="bookTickets"
        >
          Book Aarti Tickets
        </button>

        <p class="text-center text-xs sm:text-sm text-gray-500 mt-4">
          By clicking Book Ticket, you agree to the temple's terms and conditions.
        </p>

      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue"
import axios from "axios"
import { useUserStore } from "@/stores/user"
import AOS from 'aos'
import 'aos/dist/aos.css'

onMounted(() => {
  AOS.init({ duration: 800, once: true })
})

const BASE = `${import.meta.env.VITE_API_URL}`
const userStore = useUserStore()

const booker = ref({ 
  name: userStore.name || "", 
  email: userStore.email || "", 
  mobile: userStore.mobile || "" 
})

const numMembers = ref(1)
const passengers = ref([])
const slots = ref([])
const selectedSlot = ref("")
const selectedDate = ref("")

// Date Limits
const today = new Date()
const minDate = today.toISOString().split('T')[0]
const maxLimit = new Date()
maxLimit.setDate(today.getDate() + 7)
const maxDate = maxLimit.toISOString().split('T')[0]

function generatePassengers() {
  passengers.value = Array.from({ length: numMembers.value }, () => ({
    name: "",
    aadhar: "",
    otp: "",
    otpSent: false,
    verified: false,
    status: "",
    cooldown: 0,
    timer: null,
    age: "",
    gender: "",
    wheelchairNeeded: false,
    age: "",
    gender: ""
  }))
}

// Load Slots
async function loadPage() {
  const res = await axios.get(`${BASE}/book-ticket/${userStore.id}`, {
    params: { type: 'Aarti' }
  })
  slots.value = res.data.slots
}

// Send OTP
async function sendOtp(index) {
  const p = passengers.value[index]
  if (!p.aadhar || p.aadhar.length !== 12) {
    return alert("Enter a valid Aadhar number")
  }

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

// Verify OTP
async function verifyOtp(index) {
  const p = passengers.value[index]
  if (!p.otp) return alert("Enter OTP")

  const res = await axios.post(`${BASE}/verify-otp`, {
    aadhar: p.aadhar,
    otp: p.otp
  })

  p.verified = res.data.success
  p.status = p.verified ? "Verified ✓" : "OTP Invalid"
}

// Book Tickets
async function bookTickets() {
  if (!selectedDate.value) return alert("Please select Aarti date")
  if (!selectedSlot.value) return alert("Please select a slot")

  for (const p of passengers.value) {
    if (!p.verified) return alert("Verify all OTPs")
    if (!p.name || !p.age || !p.gender) {
      return alert("Fill all devotee details")
    }
  }

  const payload = {
    user_id: userStore.id,
    slot_id: selectedSlot.value,
    darshan_date: selectedDate.value,
    booker_name: booker.value.name,
    booker_mobile: booker.value.mobile,
    booker_email: booker.value.email,
    passengers: passengers.value.map(p => ({
    name: p.name,
    aadhar: p.aadhar,
    age: p.age,
    gender: p.gender,
    wheelchair_needed: p.wheelchairNeeded 
    }))
  }

  const res = await axios.post(`${BASE}/book-ticket`, payload)
  alert(res.data.success ? "Tickets Booked Successfully!" : res.data.message)
}

onMounted(() => {
  generatePassengers()
  loadPage()
})

onBeforeUnmount(() => {
  passengers.value.forEach(p => {
    if (p.timer) clearInterval(p.timer)
  })
})
</script>


<style scoped>
/* Custom style for the passenger cards for the effect */
.darshan-card {
    transition: all 0.3s ease-in-out;
}
.darshan-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 25px -5px rgba(127, 29, 29, 0.2); /* Deep red shadow on hover */
    border-color: #991b1b; /* Darker red border on hover */
}

/* Custom font simulation for 'font-serif' to match the design style */
.font-serif {
    font-family: Georgia, 'Times New Roman', Times, serif;
}

/* Animation utility class */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in-up {
    animation: fadeInUp 1s ease-out both;
}
</style>