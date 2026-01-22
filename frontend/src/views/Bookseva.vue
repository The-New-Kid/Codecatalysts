<template>
  <div>

    <!-- ✅ RESPONSIVE BANNER -->
    <div class="relative w-full h-[200px] sm:h-[300px] md:h-[400px] overflow-hidden shadow-2xl">
      <div class="absolute inset-0">
        <img 
          src="/images/Somnath4.jpeg" 
          alt="Seva Banner" 
          class="w-full h-full object-cover object-center"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-red-900/80 via-red-900/40 to-black/30"></div>
      </div>

      <div class="relative z-10 flex flex-col items-center justify-center h-full text-center px-3 sm:px-4" data-aos="fade-up">
        <h2 class="text-2xl sm:text-4xl md:text-5xl font-serif font-bold text-yellow-100 mb-2 drop-shadow-lg animate-fade-in-up">
          🛕 Book Seva
        </h2>
        <p class="text-sm sm:text-lg md:text-xl text-yellow-200 max-w-2xl mx-auto font-light drop-shadow-md">
          Reserve Seva offerings for divine blessings.
        </p>
      </div>
    </div>

    <!-- ✅ MAIN FORM -->
    <div class="min-h-screen flex justify-center items-start bg-[#fffaf0] py-6 sm:py-10 px-3 sm:px-6">
      <div
        class="w-full max-w-3xl bg-white rounded-2xl sm:rounded-3xl
               shadow-2xl p-5 sm:p-10 border-t-8 border-red-700"
        data-aos="fade-up"
        data-aos-delay="200"
      >

        <h3 class="text-xl sm:text-2xl font-serif font-bold text-center mb-6 sm:mb-8 text-red-800">
          Devotee Information
        </h3>

        <div class="space-y-5 sm:space-y-6">

          <div>
            <label class="block font-semibold mb-1 text-gray-700 text-sm sm:text-base">
              Devotee Name
            </label>
            <input 
              v-model="booker.name" 
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl
                     focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm" 
            />
          </div>

          <div>
            <label class="block font-semibold mb-1 text-gray-700 text-sm sm:text-base">
              Email
            </label>
            <input 
              v-model="booker.email" 
              type="email"
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl
                     focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm" 
            />
          </div>

          <div>
            <label class="block font-semibold mb-1 text-gray-700 text-sm sm:text-base">
              Mobile Number
            </label>
            <input 
              v-model="booker.mobile_no" 
              class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl
                     focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm" 
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
            <div>
              <label class="block font-semibold mb-1 text-gray-700">
                Select Seva Date
              </label>
              <input
                type="date"
                v-model="selectedDate"
                :min="minDate"
                :max="maxDate"
                class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl
                       focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
              />
            </div>

            <div>
              <label class="block font-semibold mb-1 text-gray-700">
                No. of People
              </label>
              <input
                type="number"
                min="1"
                v-model.number="numPeople"
                class="w-full p-2.5 sm:p-3 border-2 border-gray-300 rounded-xl
                       focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
              />
            </div>
          </div>

        </div>

        <hr class="my-8 sm:my-10 border-red-100" />

        <!-- ✅ SEVA SELECTION -->
        <div class="mt-6 sm:mt-8">
          <label class="block font-serif font-bold mb-2 text-red-800 text-lg sm:text-xl">
            Select Seva
          </label>
          <select 
            v-model="selectedSeva" 
            class="w-full p-3 border-2 border-gray-300 rounded-xl
                   focus:border-red-700 focus:ring-2 focus:ring-red-200
                   transition shadow-sm bg-white"
          >
            <option value="">-- Select Seva --</option>
            <option value="Aarti">Aarti</option>
            <option value="Aarti and Bhoj">Aarti and Bhoj</option>
          </select>
        </div>

        <!-- ✅ SUBMIT BUTTON -->
        <button
          class="w-full py-3 sm:py-4 mt-8 sm:mt-10 rounded-full
                 bg-gradient-to-r from-red-700 to-red-900 text-white
                 font-bold text-base sm:text-lg shadow-xl"
          @click="bookSeva"
        >
          Book Seva
        </button>

        <p class="text-center text-xs sm:text-sm text-gray-500 mt-4">
          By clicking Book Seva, you agree to the temple’s terms and conditions.
        </p>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { useUserStore } from "@/stores/user"
import AOS from "aos"
import "aos/dist/aos.css"

onMounted(() => {
  AOS.init({ duration: 800, once: true })
})

const BASE = import.meta.env.VITE_API_URL
const userStore = useUserStore()

const booker = ref({ name: "", email: "", mobile_no: "" })
const numPeople = ref(1)
const sevas = ref([])
const selectedSeva = ref("")
const selectedDate = ref("")

// Date limits (today → next 7 days)
const today = new Date()
const minDate = today.toISOString().split("T")[0]
const maxLimit = new Date()
maxLimit.setDate(today.getDate() + 7)
const maxDate = maxLimit.toISOString().split("T")[0]

async function loadPage() {
  const res = await axios.get(`${BASE}/book-seva/${userStore.id}`)
  booker.value = res.data
}

async function bookSeva() {
  if (!selectedDate.value) return alert("Please select Seva date")
  if (!selectedSeva.value) return alert("Please select a Seva")

  const res = await axios.post(`${BASE}/book-seva/${userStore.id}`, {
    user_id: userStore.id,
    seva_name: selectedSeva.value,
    seva_date: selectedDate.value,
    num_people: numPeople.value,
  })

  alert(res.data.success ? "Seva Booked Successfully!" : res.data.message)
}

onMounted(() => {
  loadPage()
})
</script>

<style scoped>
.font-serif {
  font-family: Georgia, "Times New Roman", Times, serif;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in-up {
  animation: fadeInUp 1s ease-out both;
}
</style>
