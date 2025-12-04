<template>
  <div>
    <div class="relative w-full h-[350px] lg:h-[450px] overflow-hidden shadow-2xl">
      <div class="absolute inset-0">
        <img 
            src="/images/somnath2.jpeg" 
            alt="Temple Banner" 
            class="w-full h-full object-cover object-center animate-slow-zoom"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-red-900/95 via-red-900/60 to-black/40"></div>
      </div>

      <div class="relative z-10 flex flex-col items-center justify-center h-full text-center px-4">
        <h1 class="text-3xl md:text-5xl font-serif font-bold text-white mb-4 drop-shadow-lg tracking-wide animate-fade-in-down">
          📅 Festival & Crowd Density Calendar
        </h1>
        <p class="text-lg text-yellow-100 max-w-2xl mx-auto font-light drop-shadow-md animate-fade-in-up">
          Plan your darshan by checking daily tithis and expected crowd levels.
        </p>
      </div>
    </div>

    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-20 relative z-20 -mt-16">
      
      <div class="bg-white rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.15)] border-t-4 border-orange-600 overflow-hidden p-4 md:p-8">

        <div class="flex flex-col md:flex-row justify-between items-center mb-8 bg-orange-50 p-4 rounded-xl border border-orange-100">
          <button 
            @click="prevMonth" 
            class="group px-6 py-2.5 bg-red-800 hover:bg-red-900 text-white font-semibold rounded-lg shadow-sm transition-all duration-200 flex items-center gap-2 mb-4 md:mb-0 active:scale-95"
          >
            <span class="group-hover:-translate-x-1 transition-transform">←</span> Prev
          </button>

          <div class="text-center">
            <h2 class="text-3xl font-serif font-bold text-red-900">
              {{ monthName }} <span class="text-orange-700">{{ currentYear }}</span>
            </h2>
          </div>
          
          <button 
            @click="nextMonth" 
            class="group px-6 py-2.5 bg-red-800 hover:bg-red-900 text-white font-semibold rounded-lg shadow-sm transition-all duration-200 flex items-center gap-2 mt-4 md:mt-0 active:scale-95"
          >
            Next <span class="group-hover:translate-x-1 transition-transform">→</span>
          </button>
        </div>

        <div v-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-6 text-center text-red-700 font-bold rounded-md">
          ⚠️ Failed to load calendar data. Please try again later.
        </div>

        <div class="grid grid-cols-7 mb-4">
          <div v-for="d in days" :key="d" class="text-center font-bold text-red-800 uppercase tracking-wider text-sm md:text-base py-2">
            {{ d }}
          </div>
        </div>

        <div class="grid grid-cols-7 gap-2 md:gap-4">

          <div v-for="blank in startDay" :key="'b'+blank" class="bg-gray-50/50 rounded-xl"></div>

          <template v-if="loading">
            <div v-for="n in totalDays" :key="n"
                 class="warm-skeleton rounded-xl h-28 md:h-36">
            </div>
          </template>

          <template v-else>
            <div v-for="(day, index) in totalDays" :key="day"
                 class="group relative bg-white border border-orange-100 rounded-xl p-2 md:p-4 flex flex-col justify-between overflow-hidden min-h-[110px] md:min-h-[140px] cursor-pointer transition-all duration-300 ease-out hover:z-10 hover:border-orange-400 hover:shadow-[0_10px_25px_-5px_rgba(234,88,12,0.3)] hover:-translate-y-2 stagger-anim"
                 :style="{ animationDelay: `${index * 30}ms` }"
            >
              
              <div class="absolute inset-0 bg-gradient-to-br from-orange-50 via-white to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

              <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-orange-300 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

              <div class="relative z-10 text-center">
                <span class="font-bold text-2xl md:text-3xl text-red-900/80 block mb-1 md:mb-2 group-hover:text-red-700 group-hover:scale-110 transition-all duration-300">{{ day }}</span>
              </div>
              
              <div class="relative z-10 text-center">
                <small class="text-xs md:text-sm font-medium text-orange-800/70 line-clamp-2 leading-tight px-1 py-1 rounded-lg bg-orange-50 group-hover:bg-orange-100 group-hover:text-orange-900 transition-colors block w-full">
                  {{ tithiMap[day] || 'No Data' }}
                </small>
              </div>
            </div>
          </template>

        </div>
      </div>
    </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const BASE = "http://127.0.0.1:5000/api"

const currentDate = ref(new Date())
const tithiMap = ref({})
const loading = ref(false)
const error = ref(false)

const days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

const currentMonth = computed(() => currentDate.value.getMonth())
const currentYear = computed(() => currentDate.value.getFullYear())

const monthName = computed(() =>
  currentDate.value.toLocaleString('default',{month:'long'})
)

const totalDays = computed(() =>
  new Date(currentYear.value, currentMonth.value+1,0).getDate()
)

const startDay = computed(() =>
  new Date(currentYear.value, currentMonth.value,1).getDay()
)

async function loadTithi() {
  loading.value = true
  error.value = false
  tithiMap.value = {}

  try {
    const res = await axios.post(`${BASE}/calender/month`, {
      month: currentMonth.value + 1,
      year: currentYear.value
    })

    tithiMap.value = res.data
  } catch (e) {
    console.error("Calendar Load Error:", e)
    error.value = true
  } finally {
    loading.value = false
  }
}

function nextMonth() {
  currentDate.value = new Date(currentYear.value,currentMonth.value+1,1)
  loadTithi()
}

function prevMonth() {
  currentDate.value = new Date(currentYear.value,currentMonth.value-1,1)
  loadTithi()
}

onMounted(loadTithi)
</script>

<style scoped>
/* Loading Skeleton Pulse */
.warm-skeleton {
    animation: warmPulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes warmPulse {
    0%, 100% { background-color: #fff7ed; }
    50% { background-color: #fed7aa; }
}

/* Staggered Entrance Animation 
   This makes the cards slide up one by one
*/
.stagger-anim {
    animation: fadeInUp 0.5s ease-out backwards;
}

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

/* Slow Zoom for Banner Image */
.animate-slow-zoom {
    animation: slowZoom 20s linear infinite alternate;
}

@keyframes slowZoom {
    from { transform: scale(1); }
    to { transform: scale(1.1); }
}

/* Simple Fade In for Text */
.animate-fade-in-down {
    animation: fadeInDown 1s ease-out;
}
.animate-fade-in-up {
    animation: fadeInUpText 1s ease-out 0.3s backwards;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUpText {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>