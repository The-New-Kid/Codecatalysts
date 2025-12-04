<template>
  <div class="max-w-7xl mx-auto mt-8 px-4 space-y-10">
    <h2 class="text-4xl font-extrabold text-center mb-8 text-indigo-600">
      🚗 Parking & Analytics Dashboard
    </h2>

    <div v-if="loading" class="text-center text-gray-600">
      Loading analytics...
    </div>

    <div v-else-if="error" class="text-center text-red-600">
      {{ error }}
    </div>

    <div
      v-else
      class="grid grid-cols-1 lg:grid-cols-2 gap-10"
    >
      <!-- Occupancy Donut -->
      <div class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition">
        <h3 class="text-xl font-semibold mb-4 text-center text-gray-700">
          Occupied vs Vacant
        </h3>
        <div class="w-full h-72">
          <canvas ref="occupancyCanvas"></canvas>
        </div>
        <p class="text-center mt-4 text-gray-600 font-medium">
          Total Spots:
          <strong>{{ totalSpots }}</strong>
        </p>
      </div>

      <!-- Revenue Bar -->
      <div class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition">
        <h3 class="text-xl font-semibold mb-4 text-center text-gray-700">
          Revenue by Lot
        </h3>
        <div class="w-full h-72">
          <canvas ref="revenueCanvas"></canvas>
        </div>
        <p class="text-center text-lg font-semibold mt-4 text-indigo-700">
          💰 Total Revenue: ₹{{ totalRevenue }}
        </p>
      </div>

      <!-- Heatmap -->
      <div
        class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition col-span-1 lg:col-span-2"
      >
        <h3 class="text-xl font-semibold mb-4 text-center text-gray-700">
          Crowd Density Heatmap
        </h3>
        <div class="w-full h-96">
          <canvas ref="heatmapCanvas"></canvas>
        </div>
        <p class="text-center mt-3 text-gray-500 italic text-sm">
          *Simulated density visualization
        </p>
      </div>

      <!-- Hourly Traffic -->
      <div class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition">
        <h3 class="text-xl font-semibold mb-4 text-center text-gray-700">
          Hourly Entry Flow
        </h3>
        <div class="w-full h-72">
          <canvas ref="trafficCanvas"></canvas>
        </div>
      </div>

      <!-- 7-Day Trend -->
      <div class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition">
        <h3 class="text-xl font-semibold mb-4 text-center text-gray-700">
          7-Day Occupancy Trend
        </h3>
        <div class="w-full h-72">
          <canvas ref="trendCanvas"></canvas>
        </div>
      </div>

      <!-- Darshan Slot Popularity -->
      <div
        class="bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition col-span-1 lg:col-span-2 flex flex-col items-center"
      >
        <h3 class="text-xl font-semibold mb-4 text-center text-gray-700">
          🌙 Darshan Slot Popularity
        </h3>
        <div class="w-full sm:w-3/4 h-96">
          <canvas ref="slotCanvas"></canvas>
        </div>
        <p class="text-center mt-3 text-gray-500 italic text-sm">
          Peak darshan times across all mandirs
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

const API_BASE = 'http://127.0.0.1:5000/api'

const loading = ref(true)
const error = ref('')

// backend values
const lotNames = ref([])
const revenues = ref([])
const occupiedSpots = ref(0)
const vacantSpots = ref(0)
const totalSpots = ref(0)
const totalRevenue = ref(0)

// canvas refs
const occupancyCanvas = ref(null)
const revenueCanvas = ref(null)
const heatmapCanvas = ref(null)
const trafficCanvas = ref(null)
const trendCanvas = ref(null)
const slotCanvas = ref(null)

// chart instances
let occupancyChart = null
let revenueChart = null
let heatmapChart = null
let trafficChart = null
let trendChart = null
let slotChart = null

const fetchSummary = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_BASE}/admin/summary`)
    const data = res.data

    lotNames.value = data.lot_names || []
    revenues.value = data.revenues || []
    occupiedSpots.value = data.occupied_spots || 0
    vacantSpots.value = data.vacant_spots || 0
    totalSpots.value = data.total_spots || 0
    totalRevenue.value = data.total_revenue || 0
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load analytics summary.'
  } finally {
    loading.value = false
  }
}

const initCharts = () => {
  if (!occupancyCanvas.value) return

  // ===== Occupancy Donut =====
  occupancyChart && occupancyChart.destroy()
  occupancyChart = new Chart(occupancyCanvas.value, {
    type: 'doughnut',
    data: {
      labels: ['Occupied', 'Vacant'],
      datasets: [
        {
          data: [occupiedSpots.value, vacantSpots.value],
          backgroundColor: ['#ef4444', '#10b981'],
          borderWidth: 3
        }
      ]
    },
    options: {
      plugins: { legend: { position: 'bottom' } },
      cutout: '70%'
    }
  })

  // ===== Revenue Bar =====
  revenueChart && revenueChart.destroy()
  revenueChart = new Chart(revenueCanvas.value, {
    type: 'bar',
    data: {
      labels: lotNames.value,
      datasets: [
        {
          label: 'Revenue (₹)',
          data: revenues.value,
          backgroundColor: '#6366f1',
          borderRadius: 8
        }
      ]
    },
    options: {
      scales: { y: { beginAtZero: true } },
      plugins: { legend: { display: false } }
    }
  })

  // ===== Heatmap (simulated) =====
  const gridSize = 5
  const heatData = []
  const colors = []

  for (let x = 0; x < gridSize; x++) {
    for (let y = 0; y < gridSize; y++) {
      const density = Math.floor(Math.random() * 100)
      heatData.push({ x: x + 1, y: y + 1, r: 25 })
      const red = Math.floor((density / 100) * 255)
      const green = 200 - Math.floor((density / 100) * 200)
      colors.push(`rgba(${red}, ${green}, 50, 0.7)`)
    }
  }

  heatmapChart && heatmapChart.destroy()
  heatmapChart = new Chart(heatmapCanvas.value.getContext('2d'), {
    type: 'bubble',
    data: {
      datasets: [
        {
          label: 'Crowd Density',
          data: heatData,
          backgroundColor: colors,
          borderColor: 'rgba(0,0,0,0.1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (context) => {
              const density = Math.floor(Math.random() * 100)
              return `Zone (${context.raw.x}, ${context.raw.y}): ${density} visitors`
            }
          }
        }
      },
      scales: {
        x: {
          ticks: { stepSize: 1 },
          min: 0.5,
          max: gridSize + 0.5,
          title: { display: true, text: 'X Zone' }
        },
        y: {
          ticks: { stepSize: 1 },
          min: 0.5,
          max: gridSize + 0.5,
          title: { display: true, text: 'Y Zone' }
        }
      }
    }
  })

  // ===== Hourly Traffic (static) =====
  trafficChart && trafficChart.destroy()
  trafficChart = new Chart(trafficCanvas.value, {
    type: 'line',
    data: {
      labels: ['6 AM', '8 AM', '10 AM', '12 PM', '2 PM', '4 PM', '6 PM', '8 PM'],
      datasets: [
        {
          label: 'Entries',
          data: [10, 25, 40, 70, 55, 80, 65, 30],
          fill: true,
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59,130,246,0.2)',
          tension: 0.4
        }
      ]
    },
    options: { plugins: { legend: { display: false } } }
  })

  // ===== 7-Day Occupancy Trend (static) =====
  trendChart && trendChart.destroy()
  trendChart = new Chart(trendCanvas.value, {
    type: 'line',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [
        {
          label: 'Occupancy (%)',
          data: [60, 72, 68, 75, 85, 90, 70],
          fill: true,
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245,158,11,0.3)',
          tension: 0.4
        }
      ]
    },
    options: { plugins: { legend: { display: false } } }
  })

  // ===== Darshan Slot Popularity (static) =====
  slotChart && slotChart.destroy()
  slotChart = new Chart(slotCanvas.value, {
    type: 'bar',
    data: {
      labels: [
        'Morning (6-9 AM)',
        'Late Morning (9-12)',
        'Afternoon (12-3)',
        'Evening (3-6)',
        'Night (6-9)'
      ],
      datasets: [
        {
          label: 'Visitors',
          data: [120, 180, 90, 200, 150],
          backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6366f1'],
          borderRadius: 10
        }
      ]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  })
}

onMounted(async () => {
  await fetchSummary()
  if (!error.value) {
    await nextTick()
    initCharts()
  }
  if (window.AOS) {
    window.AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
  }
})

onBeforeUnmount(() => {
  occupancyChart && occupancyChart.destroy()
  revenueChart && revenueChart.destroy()
  heatmapChart && heatmapChart.destroy()
  trafficChart && trafficChart.destroy()
  trendChart && trendChart.destroy()
  slotChart && slotChart.destroy()
})
</script>
