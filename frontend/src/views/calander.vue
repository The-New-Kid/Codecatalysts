<template>
  <UserLayout>
    <div style="min-height:100vh;background:#fffaf0;padding:30px;">
      <h1 style="text-align:center;font-size:32px;color:#4f46e5;margin-bottom:15px;">
        📅 Festival & Crowd Density Calendar
      </h1>

      <div style="text-align:center;font-size:22px;font-weight:bold;margin-bottom:20px;">
        {{ monthName }} {{ currentYear }}
      </div>

      <div style="display:flex;justify-content:space-between;max-width:900px;margin:0 auto 15px;">
        <button @click="prevMonth" style="padding:10px 20px;border:none;border-radius:8px;background:#4f46e5;color:#fff;">← Prev</button>
        <button @click="nextMonth" style="padding:10px 20px;border:none;border-radius:8px;background:#4f46e5;color:#fff;">Next →</button>
      </div>

      <div style="max-width:900px;margin:auto;background:#fff;border-radius:16px;padding:20px;box-shadow:0 6px 15px rgba(0,0,0,0.1);">

        <!-- Error State -->
        <div v-if="error" style="text-align:center;color:red;font-weight:bold;">
          ⚠️ Failed to load calendar. Please try again.
        </div>

        <!-- Week Header -->
        <div style="display:grid;grid-template-columns:repeat(7,1fr);font-weight:bold;text-align:center;margin-bottom:10px;">
          <div v-for="d in days" :key="d">{{ d }}</div>
        </div>

        <!-- Calendar Grid -->
        <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:10px;">

          <div v-for="blank in startDay" :key="'b'+blank"></div>

          <!-- Skeleton Loading -->
          <template v-if="loading">
            <div v-for="n in totalDays" :key="n"
              style="background:#f3f4f6;border-radius:12px;padding:20px;height:70px;animation:pulse 1.5s infinite;">
            </div>
          </template>

          <!-- Actual Days -->
          <template v-else>
            <div v-for="day in totalDays" :key="day"
              style="background:#ecfdf5;border-radius:12px;padding:12px;text-align:center;border:1px solid #86efac;">

              <div style="font-weight:bold;font-size:18px;color:#065f46;">{{ day }}</div>
              <small style="font-size:13px;color:#047857;">
                {{ tithiMap[day] || 'N/A' }}
              </small>
            </div>
          </template>

        </div>
      </div>
    </div>
  </UserLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import UserLayout from "@/layouts/UserLayout.vue"

const BASE = "http://127.0.0.1:5000/api"

const currentDate = ref(new Date())
const tithiMap = ref({})
const loading = ref(false)
const error = ref(false)

const days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

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

    tithiMap.value = res.data   // ✅ THIS IS THE FIX
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

<style>
@keyframes pulse {
  0% { background:#f3f4f6; }
  50% { background:#e5e7eb; }
  100% { background:#f3f4f6; }
}
</style>
