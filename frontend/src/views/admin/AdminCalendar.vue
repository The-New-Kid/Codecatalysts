<template>
  <div class="max-w-6xl mx-auto mt-8 px-4">
    <h2 class="text-4xl font-extrabold text-center text-indigo-600 mb-8">
      🗓️ Festival & Crowd Density Calendar
    </h2>

    <!-- Month Navigation -->
    <div class="flex justify-between items-center mb-6">
      <button
        @click="prevMonth"
        class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
      >
        ← Prev
      </button>

      <h3 class="text-2xl font-bold text-gray-800">
        {{ monthNamesHindi[currentMonth] }} ({{ monthNamesEnglish[currentMonth] }} {{ currentYear }})
      </h3>

      <button
        @click="nextMonth"
        class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
      >
        Next →
      </button>
    </div>

    <!-- Calendar -->
    <div class="flex flex-col gap-2 bg-white shadow-lg p-6 rounded-2xl border border-gray-200">
      <!-- Day headers -->
      <div class="grid grid-cols-7 gap-3 font-semibold text-gray-700">
        <div
          v-for="d in dayNames"
          :key="d"
          class="text-center"
        >
          {{ d }}
        </div>
      </div>

      <!-- Weeks -->
      <div
        v-for="(week, wIdx) in weeks"
        :key="wIdx"
        class="grid grid-cols-7 gap-3 mb-3"
      >
        <div
          v-for="(cell, cIdx) in week"
          :key="cIdx"
        >
          <!-- empty cell -->
          <div v-if="cell.isEmpty"></div>

          <!-- day cell -->
          <div
            v-else
            class="relative p-4 text-center rounded-xl font-semibold shadow-sm border hover:shadow-md transition"
            :class="densityClass(cell.density)"
          >
            <div class="text-lg">
              {{ cell.day }}
            </div>
            <div
              v-if="cell.festivalName"
              class="text-xs mt-1 font-normal"
            >
              {{ cell.festivalName }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div class="flex justify-center mt-8 space-x-6 text-sm text-gray-700">
      <div class="flex items-center">
        <span class="w-4 h-4 bg-green-500 rounded-full mr-2"></span> Normal Days
      </div>
      <div class="flex items-center">
        <span class="w-4 h-4 bg-yellow-400 rounded-full mr-2"></span> Moderate / Weekend
      </div>
      <div class="flex items-center">
        <span class="w-4 h-4 bg-red-500 rounded-full mr-2"></span> Festivals / High Density
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const festivalsList = [
  { name: 'Lohri', date: '2025-01-13', density: 'Medium' },
  { name: 'Makar Sankranti/Pongal', date: '2025-01-14', density: 'Medium' },
  { name: 'Vasant Panchami', date: '2025-02-02', density: 'Medium' },
  { name: 'Maha Shivratri', date: '2025-02-26', density: 'Medium' },
  { name: 'Holika Dahan', date: '2025-03-13', density: 'High' },
  { name: 'Holi', date: '2025-03-14', density: 'High' },
  { name: 'Hindi New Year', date: '2025-03-20', density: 'High' },
  { name: 'Ugadi', date: '2025-03-30', density: 'High' },
  { name: 'Ram Navami', date: '2025-04-06', density: 'Medium' },
  { name: 'Hanuman Jayanti', date: '2025-04-12', density: 'Medium' },
  { name: 'Vaisakhi', date: '2025-04-14', density: 'Medium' },
  { name: 'Akshaya Tritiya', date: '2025-04-30', density: 'Medium' },
  { name: 'Buddha Purnima', date: '2025-05-12', density: 'High' },
  { name: 'Savitri Pooja', date: '2025-05-26', density: 'Medium' },
  { name: 'Puri Rath Yatra', date: '2025-06-27', density: 'Low' },
  { name: 'Guru Purnima', date: '2025-07-10', density: 'Medium' },
  { name: 'Sawan Shivratri', date: '2025-07-23', density: 'High' },
  { name: 'Hariyali Teej', date: '2025-07-27', density: 'Medium' },
  { name: 'Nag Panchami', date: '2025-07-29', density: 'Medium' },
  { name: 'Varalakshmi Vrat', date: '2025-08-08', density: 'High' },
  { name: 'Raksha Bandhan', date: '2025-08-09', density: 'High' },
  { name: 'Krishna Janmashtami', date: '2025-08-15', density: 'High' },
  { name: 'Hartalika Teej', date: '2025-08-26', density: 'High' },
  { name: 'Ganesh Chaturthi', date: '2025-08-27', density: 'High' },
  { name: 'Onam', date: '2025-09-05', density: 'Medium' },
  { name: 'Navaratri Begins', date: '2025-09-22', density: 'Medium' },
  { name: 'Navaratri Ends', date: '2025-10-01', density: 'High' },
  { name: 'Dussehra', date: '2025-10-02', density: 'High' },
  { name: 'Gandhi Jayanti', date: '2025-10-02', density: 'High' },
  { name: 'Sharad Purnima', date: '2025-10-06', density: 'High' },
  { name: 'Karwa Chauth', date: '2025-10-10', density: 'High' },
  { name: 'Dhan Teras', date: '2025-10-18', density: 'High' },
  { name: 'Diwali', date: '2025-10-20', density: 'High' },
  { name: 'Bhai Dooj', date: '2025-10-23', density: 'High' },
  { name: 'Chhath Puja', date: '2025-10-27', density: 'High' },
  { name: 'Kartik Poornima', date: '2025-11-05', density: 'Low' },
  { name: 'Geeta Jayanti', date: '2025-12-01', density: 'Low' },
  { name: 'Dhanu Sankranti', date: '2025-12-16', density: 'Low' },
  { name: 'Christmas', date: '2025-12-25', density: 'Low' }
]

const monthNamesHindi = [
  'जनवरी',
  'फ़रवरी',
  'मार्च',
  'अप्रैल',
  'मई',
  'जून',
  'जुलाई',
  'अगस्त',
  'सितंबर',
  'अक्टूबर',
  'नवंबर',
  'दिसंबर'
]
const monthNamesEnglish = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
]
const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const today = new Date()
const currentMonth = ref(today.getMonth())
const currentYear = ref(today.getFullYear())

// helper: get festival for given date
const getFestivalForDay = (year, month, day) => {
  return (
    festivalsList.find((f) => {
      const d = new Date(f.date)
      return (
        d.getFullYear() === year &&
        d.getMonth() === month &&
        d.getDate() === day
      )
    }) || null
  )
}

// computed weeks structure like original renderCalendar
const weeks = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value

  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()

  const weeksArr = []
  let week = []

  // empty cells before first day
  for (let i = 0; i < firstDay; i++) {
    week.push({ isEmpty: true })
  }

  // actual days
  for (let day = 1; day <= daysInMonth; day++) {
    const fest = getFestivalForDay(year, month, day)
    let density = 'normal'
    let festivalName = ''

    if (fest) {
      density = fest.density.toLowerCase()
      festivalName = fest.name
    }

    week.push({
      isEmpty: false,
      day,
      festivalName,
      density
    })

    if (week.length === 7 || day === daysInMonth) {
      weeksArr.push(week)
      week = []
    }
  }

  // just in case leftover cells (shouldn't usually happen)
  if (week.length > 0) {
    while (week.length < 7) {
      week.push({ isEmpty: true })
    }
    weeksArr.push(week)
  }

  return weeksArr
})

const densityClass = (density) => {
  if (density === 'high') {
    return ['bg-red-100', 'text-red-700', 'border-red-300']
  } else if (density === 'medium') {
    return ['bg-yellow-100', 'text-yellow-700', 'border-yellow-300']
  } else {
    return ['bg-green-100', 'text-green-700', 'border-green-300']
  }
}

const prevMonth = () => {
  currentMonth.value--
  if (currentMonth.value < 0) {
    currentMonth.value = 11
    currentYear.value--
  }
}

const nextMonth = () => {
  currentMonth.value++
  if (currentMonth.value > 11) {
    currentMonth.value = 0
    currentYear.value++
  }
}

onMounted(() => {
  if (window.AOS) {
    window.AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
  }
})
</script>
