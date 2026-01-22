<template>
  <div>
    <!-- ✅ RESPONSIVE BANNER -->
    <div class="relative w-full h-[200px] sm:h-[300px] lg:h-[450px] overflow-hidden shadow-2xl">
      <div class="absolute inset-0">
        <img 
          src="/images/somnath2.jpeg" 
          alt="Temple Banner" 
          class="w-full h-full object-cover object-center animate-slow-zoom"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-red-900/95 via-red-900/60 to-black/40"></div>
      </div>

      <div class="relative z-10 flex flex-col items-center justify-center h-full text-center px-3 sm:px-4">
        <h1 class="text-xl sm:text-3xl md:text-5xl font-serif font-bold text-white mb-3 sm:mb-4 drop-shadow-lg tracking-wide animate-fade-in-down">
          📅 Festival & Crowd Density Calendar
        </h1>
        <p class="text-sm sm:text-lg text-yellow-100 max-w-2xl mx-auto font-light drop-shadow-md animate-fade-in-up">
          Plan your darshan by checking daily tithis and expected crowd levels.
        </p>
      </div>
    </div>

    <!-- ✅ CONTENT WRAPPER -->
    <div class="max-w-6xl mx-auto px-2 sm:px-4 md:px-6 lg:px-8 pb-20 relative z-20 -mt-12 sm:-mt-16">
      
      <div class="bg-white rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.15)] border-t-4 border-orange-600 overflow-hidden p-3 sm:p-4 md:p-8">

        <!-- ✅ HEADER CONTROLS -->
        <div class="flex flex-col sm:flex-row justify-between items-center mb-6 sm:mb-8 bg-orange-50 p-3 sm:p-4 rounded-xl border border-orange-100 gap-3 sm:gap-0">
          
          <button 
            @click="prevMonth" 
            class="group w-full sm:w-auto px-5 py-2 bg-red-800 hover:bg-red-900 text-white font-semibold rounded-lg shadow-sm transition-all duration-200 flex items-center justify-center gap-2 active:scale-95"
          >
            <span class="group-hover:-translate-x-1 transition-transform">←</span> Prev
          </button>

          <div class="text-center">
            <h2 class="text-xl sm:text-3xl font-serif font-bold text-red-900">
              {{ monthName }} <span class="text-orange-700">{{ currentYear }}</span>
            </h2>
          </div>
          
          <button 
            @click="nextMonth" 
            class="group w-full sm:w-auto px-5 py-2 bg-red-800 hover:bg-red-900 text-white font-semibold rounded-lg shadow-sm transition-all duration-200 flex items-center justify-center gap-2 active:scale-95"
          >
            Next <span class="group-hover:translate-x-1 transition-transform">→</span>
          </button>
        </div>

        <!-- ✅ ERROR -->
        <div v-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-6 text-center text-red-700 font-bold rounded-md">
          ⚠ Failed to load calendar data. Please try again later.
        </div>

        <!-- ✅ LEGEND -->
        <div class="flex flex-wrap items-center gap-2 sm:gap-4 mb-4 text-[10px] sm:text-xs md:text-sm">
          <div class="flex items-center gap-1">
            <span class="inline-block w-3 h-3 rounded-full bg-emerald-200 border border-emerald-400"></span>
            <span>Low Crowd (&lt; 20k)</span>
          </div>
          <div class="flex items-center gap-1">
            <span class="inline-block w-3 h-3 rounded-full bg-amber-200 border border-amber-400"></span>
            <span>Moderate (20k–40k)</span>
          </div>
          <div class="flex items-center gap-1">
            <span class="inline-block w-3 h-3 rounded-full bg-red-200 border border-red-400"></span>
            <span>High (&gt; 40k)</span>
          </div>
        </div>

        <!-- ✅ DAY HEADERS -->
        <div class="grid grid-cols-7 mb-2 sm:mb-4">
          <div 
            v-for="d in days" 
            :key="d" 
            class="text-center font-bold text-red-800 uppercase tracking-wider text-[10px] sm:text-sm md:text-base py-1 sm:py-2"
          >
            {{ d }}
          </div>
        </div>

        <!-- ✅ CALENDAR GRID -->
        <div class="grid grid-cols-7 gap-1 sm:gap-2 md:gap-4">

          <!-- Blank cells before 1st -->
          <div 
            v-for="blank in startDay" 
            :key="'b'+blank" 
            class="bg-gray-50/50 rounded-xl min-h-[60px] sm:min-h-[110px]"
          ></div>

          <!-- ✅ LOADING SKELETON -->
          <template v-if="loading">
            <div 
              v-for="n in totalDays" 
              :key="n"
              class="warm-skeleton rounded-xl h-20 sm:h-28 md:h-36">
            </div>
          </template>

          <!-- ✅ DAY CELLS -->
          <template v-else>
            <div 
              v-for="(day, index) in totalDays" 
              :key="day"
              class="group relative bg-white border border-orange-100 rounded-xl p-1.5 sm:p-3 md:p-4 flex flex-col justify-between overflow-hidden min-h-[80px] sm:min-h-[110px] md:min-h-[140px] cursor-pointer transition-all duration-300 ease-out hover:z-10 hover:border-orange-400 hover:shadow-[0_10px_25px_-5px_rgba(234,88,12,0.3)] hover:-translate-y-1 sm:hover:-translate-y-2 stagger-anim"
              :style="{ animationDelay: `${index * 30}ms` }"
            >
              <div class="absolute inset-0 bg-gradient-to-br from-orange-50 via-white to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-orange-300 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

              <!-- Day number -->
              <div class="relative z-10 text-center">
                <span class="font-bold text-lg sm:text-2xl md:text-3xl text-red-900/80 block mb-0.5 sm:mb-2 group-hover:text-red-700 transition-all duration-300">
                  {{ day }}
                </span>
              </div>
              
              <!-- Tithi + Festival + Crowd -->
              <div class="relative z-10 text-center space-y-0.5 sm:space-y-1">

                <!-- Tithi badge -->
                <small 
                  class="text-[9px] sm:text-xs md:text-sm font-medium line-clamp-2 leading-tight px-1 py-0.5 rounded-lg block w-full transition-colors"
                  :class="{
                    'text-orange-800/70 bg-orange-50 group-hover:bg-orange-100 group-hover:text-orange-900': !tithiMap[day]?.fest,
                    'text-red-900 font-bold bg-red-100 group-hover:bg-red-200 group-hover:text-red-800 border border-red-400': tithiMap[day]?.fest
                  }"
                >
                  {{ tithiMap[day]?.tithi || 'No Data' }}
                </small>

                <!-- Festival line -->
                <div 
                  v-if="tithiMap[day]?.fest"
                  class="text-[9px] sm:text-[10px] md:text-xs font-semibold text-red-700"
                >
                  🛕 {{ tithiMap[day].fest }}
                </div>

                <!-- 🧮 Crowd prediction -->
                <div
                  v-if="tithiMap[day]?.crowd !== undefined"
                  class="inline-flex items-center justify-center mx-auto mt-0.5 sm:mt-1 px-1.5 py-0.5 rounded-full border text-[9px] sm:text-[10px] md:text-xs font-semibold"
                  :class="crowdClass(tithiMap[day].crowd)"
                >
                  👥 {{ formatNumber(tithiMap[day].crowd) }}
                  <span class="ml-1 uppercase tracking-wide text-[8px] sm:text-[9px]">
                    ({{ crowdLabel(tithiMap[day].crowd) }})
                  </span>
                </div>

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

const BASE = import.meta.env.VITE_API_URL

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
  new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
)

const startDay = computed(() =>
  new Date(currentYear.value, currentMonth.value, 1).getDay()
)

// ---- Crowd helpers ----
function formatNumber(num) {
  if (num == null) return '—'
  return Number(num).toLocaleString('en-IN')
}

function crowdLabel(value) {
  if (value == null) return 'No Data'
  if (value < 20000) return 'Low'
  if (value < 40000) return 'Moderate'
  return 'High'
}

function crowdClass(value) {
  if (value == null) return 'text-gray-700 bg-gray-50 border border-gray-200'
  if (value < 20000) return 'text-emerald-800 bg-emerald-50 border border-emerald-300'
  if (value < 40000) return 'text-amber-800 bg-amber-50 border border-amber-300'
  return 'text-red-800 bg-red-50 border border-red-300'
}

// ---- API loader ----
async function loadTithi() {
  loading.value = true
  error.value = false
  tithiMap.value = {}

  try {
    const res = await axios.post(`${BASE}/calender/month`, {
      month: currentMonth.value + 1,
      year: currentYear.value
    })
    console.log("Calendar API:", res.data)
    tithiMap.value = res.data
  } catch (e) {
    console.error("Calendar Load Error:", e)
    error.value = true
  } finally {
    loading.value = false
  }
}

function nextMonth() {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
  loadTithi()
}

function prevMonth() {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
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

/* Staggered Entrance Animation */
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