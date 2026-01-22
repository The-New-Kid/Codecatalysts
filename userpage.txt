<template>
  <UserLayout>
    <div class="relative w-full h-[300px] sm:h-[400px] overflow-hidden shadow-2xl">
      <div class="absolute inset-0">
        <img 
          src="/images/Somnath4.jpeg" 
          alt="Temple Darshan Banner" 
          class="w-full h-full object-cover object-center"
        />
        <div class="absolute inset-0 bg-red-900/80 via-red-900/40 to-black/30"></div>
      </div>

      <div class="relative z-10 flex flex-col items-center justify-center h-full text-center px-4" data-aos="fade-up">
        <h2 class="text-4xl md:text-5xl font-serif font-bold text-yellow-100 mb-2 drop-shadow-lg animate-fade-in-up">
          🙏 Darshan Ticket Booking
        </h2>
        <p class="text-lg md:text-xl text-yellow-200 max-w-2xl mx-auto font-light drop-shadow-md">
          Secure your sacred visit to the divine abode.
        </p>
      </div>
    </div>
    
    <div class="min-h-screen flex justify-center items-start bg-[#fffaf0] py-10">
      <div class="w-full max-w-3xl bg-white rounded-3xl shadow-2xl p-6 sm:p-10 border-t-8 border-red-700" data-aos="fade-up" data-aos-delay="200">

        <h3 class="text-2xl font-serif font-bold text-center mb-8 text-red-800">
          Booker Information
        </h3>

        <div class="space-y-6">
          <div>
            <label class="block font-semibold mb-1 text-gray-700">Booker Name</label>
            <input v-model="booker.name" class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 shadow-sm" />
          </div>

          <div>
            <label class="block font-semibold mb-1 text-gray-700">Email</label>
            <input v-model="booker.email" type="email" class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 shadow-sm" />
          </div>

          <div>
            <label class="block font-semibold mb-1 text-gray-700">Mobile Number</label>
            <input v-model="booker.mobile" class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 shadow-sm" />
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

        <h3 class="text-2xl font-serif font-bold text-center mb-8 text-red-800">
          Passenger Details & Verification
        </h3>

        <div 
          v-for="(p, i) in passengers" 
          :key="i" 
          class="mt-6 p-5 sm:p-6 rounded-xl bg-red-50 border border-red-200 shadow-lg darshan-card" 
          :data-aos="i % 2 === 0 ? 'fade-right' : 'fade-left'"
          :data-aos-delay="300 + (i * 100)"
        >

          <h4 class="font-bold text-red-700 mb-4 text-lg border-b border-red-200 pb-2 flex items-center">
            <span class="mr-2 text-xl">👤</span> Passenger {{ i + 1 }}
          </h4>

          <input v-model="p.name" class="w-full p-3 border rounded-lg mb-3 focus:border-red-600" placeholder="Passenger Name" />

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
            <input v-model="p.aadhar" class="w-full p-3 border rounded-lg focus:border-red-600" placeholder="Aadhar Number" />

            <button
              class="bg-red-700 text-white rounded-lg px-4 py-2 font-semibold hover:bg-red-800 transition duration-300 disabled:opacity-50 disabled:bg-gray-400"
              @click="sendOtp(i)"
              :disabled="p.cooldown > 0 || p.verified"
            >
              <span v-if="p.cooldown > 0">Resend in {{ p.cooldown }}s</span>
              <span v-else-if="p.verified" class="flex items-center justify-center">OTP Sent ✓</span>
              <span v-else>Send OTP</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input v-model="p.otp" class="w-full p-3 border rounded-lg focus:border-red-600" placeholder="Enter OTP" />

            <button
              class="bg-green-600 text-white rounded-lg px-4 py-2 font-semibold hover:bg-green-700 transition duration-300 disabled:opacity-50 disabled:bg-gray-400"
              @click="verifyOtp(i)"
              :disabled="p.verified || !p.otpSent"
            >
              {{ p.verified ? 'Verified ✓' : 'Verify OTP' }}
            </button>
          </div>

          <p class="text-sm mt-3 font-medium" :class="p.verified ? 'text-green-700' : 'text-red-700'">
            {{ p.status }}
          </p>
        </div>
        
        <hr class="my-10 border-red-100" />

        <div class="mt-8">
          <label class="block font-serif font-bold mb-2 text-red-800 text-xl">Select Darshan Slot</label>
          <select v-model="selectedSlot" class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition duration-300 shadow-sm bg-white">
            <option value="">-- Select Slot --</option>
            <option v-for="s in slots" :key="s.id" :value="s.id">
              {{ s.slot_type }} | {{ s.start }} - {{ s.end }}
            </option>
          </select>
        </div>

        <button
          class="w-full py-4 mt-10 rounded-full bg-gradient-to-r from-red-700 to-red-900 text-white font-bold text-lg shadow-xl hover:shadow-2xl hover:from-red-800 hover:to-red-900 transition duration-300 transform hover:scale-[1.01] tracking-wider"
          @click="bookTickets"
          data-aos="zoom-in"
          data-aos-delay="500"
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
import { ref, onMounted } from "vue"
import axios from "axios"
import { useUserStore } from "@/stores/user"
import UserLayout from "@/layouts/Userlayoutnew.vue"
import AOS from 'aos'
import 'aos/dist/aos.css'

// Initialize AOS (for animations)
onMounted(() => {
  AOS.init({ duration: 800, once: true })
})

const BASE = "http://127.0.0.1:5000/api"
const userStore = useUserStore()

// Variable names and logic remain **unchanged**
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