<template>
  <div class="relative w-full min-h-screen overflow-auto">
    <div class="fixed inset-0 w-full h-full">
      <img 
        src="/images/prem mandir.jpeg" 
        alt="Temple Background" 
        class="w-full h-full object-cover object-center"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-red-900/90 via-red-900/40 to-black/30"></div>
    </div>

    <div class="relative z-10 py-16 px-4 sm:px-6 lg:px-8 bg-transparent">
      <h2
        class="text-6xl sm:text-7xl font-serif font-extrabold text-transparent 
               bg-clip-text bg-gradient-to-r from-red-200 via-orange-100 to-yellow-100 
               text-center mb-16 leading-snug sm:leading-snug drop-shadow-2xl"
        data-aos="fade-down"
      >
        DevDhamPath Seva Administration
      </h2>

      <!-- MAIN ADMIN CARDS -->
      <div class="flex justify-center mb-10 px-4">
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-6 w-full max-w-7xl">
          <RouterLink to="/admin/parking-lots" class="admin-link-btn primary-btn group bg-orange-600 hover:bg-orange-700">
            <div class="icon-circle-sm bg-white text-orange-600">
              <i data-feather="trello" class="w-6 h-6"></i>
            </div>
            <div class="text-left">
              <span class="block text-base font-bold text-white">Parking Lots</span>
              <span class="text-xs text-orange-200">Manage Zones</span>
            </div>
          </RouterLink>

          <RouterLink to="/admin/users" class="admin-link-btn primary-btn group bg-red-700 hover:bg-red-800">
            <div class="icon-circle-sm bg-white text-red-700">
              <i data-feather="users" class="w-6 h-6"></i>
            </div>
            <div class="text-left">
              <span class="block text-base font-bold text-white">Users</span>
              <span class="text-xs text-red-200">Devotee Accounts</span>
            </div>
          </RouterLink>

          <RouterLink to="/admin/darshan-slots" class="admin-link-btn primary-btn group bg-blue-700 hover:bg-blue-800">
            <div class="icon-circle-sm bg-white text-blue-700">
              <i data-feather="clock" class="w-6 h-6"></i>
            </div>
            <div class="text-left">
              <span class="block text-base font-bold text-white">Darshan Slots</span>
              <span class="text-xs text-blue-200">Set Availability</span>
            </div>
          </RouterLink>
          
          <RouterLink to="/admin/scan-ticket" class="admin-link-btn primary-btn group bg-green-700 hover:bg-green-800">
            <div class="icon-circle-sm bg-white text-green-700">
              <i data-feather="maximize-2" class="w-6 h-6"></i>
            </div>
            <div class="text-left">
              <span class="block text-base font-bold text-white">Scan Ticket</span>
              <span class="text-xs text-green-200">Quick Entry Check</span>
            </div>
          </RouterLink>

          <RouterLink to="/admin/analytics" class="admin-link-btn primary-btn group bg-purple-700 hover:bg-purple-800">
            <div class="icon-circle-sm bg-white text-purple-700">
              <i data-feather="bar-chart-2" class="w-6 h-6"></i>
            </div>
            <div class="text-left">
              <span class="block text-base font-bold text-white">Analytics</span>
              <span class="text-xs text-purple-200">Booking Reports</span>
            </div>
          </RouterLink>
        </div>
      </div>

      <!-- ⭐ INDEPENDENT RED SEND ALERT BUTTON ⭐ -->
      <div class="flex justify-center mb-6 px-4">
        <button
          type="button"
          class="admin-link-btn primary-btn group bg-red-600 hover:bg-red-700"
          @click="toggleAlertPanel"
        >
          <div class="icon-circle-sm bg-white text-red-600">
            <i data-feather="alert-octagon" class="w-6 h-6"></i>
          </div>
          <div class="text-left">
            <span class="block text-base font-bold text-white">Send Alert</span>
            <span class="text-xs text-red-200">
              {{ showAlertPanel ? 'Choose alert type' : 'Broadcast emergency' }}
            </span>
          </div>
        </button>
      </div>

      <!-- 🧩 ALERT TYPE OPTIONS PANEL -->
      <div v-if="showAlertPanel" class="flex justify-center mb-8 px-4">
        <div class="bg-red-900/80 border border-red-300/70 rounded-2xl shadow-xl p-4 sm:p-5 max-w-xl w-full">
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-lg sm:text-xl font-semibold text-red-50 flex items-center gap-2">
              <i data-feather="bell" class="w-4 h-4"></i>
              Choose Alert Type
            </h3>
            <button
              class="text-xs px-2 py-1 rounded-full bg-red-700/70 text-red-100 hover:bg-red-700"
              @click="showAlertPanel = false"
            >
              Close
            </button>
          </div>

          <p class="text-xs sm:text-sm text-red-100 mb-4">
            Select the type of emergency. An alert will be sent to the backend for quick action.
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <!-- Medical Help -->
            <button
              type="button"
              class="alert-type-btn bg-emerald-700/70 hover:bg-emerald-700"
              @click="triggerAdminAlert('MEDICAL')"
            >
              <i data-feather="heart-pulse" class="w-4 h-4 mb-1"></i>
              <span class="text-xs font-semibold">Medical Help</span>
              <span class="text-[10px] text-emerald-100">Injury / health issue</span>
            </button>

            <!-- Fire Broke Out -->
            <button
              type="button"
              class="alert-type-btn bg-orange-700/70 hover:bg-orange-700"
              @click="triggerAdminAlert('FIRE')"
            >
              <i data-feather="flame" class="w-4 h-4 mb-1"></i>
              <span class="text-xs font-semibold">Fire Broke Out</span>
              <span class="text-[10px] text-orange-100">Smoke / fire hazard</span>
            </button>

            <!-- Stampede -->
            <button
              type="button"
              class="alert-type-btn bg-yellow-700/70 hover:bg-yellow-700"
              @click="triggerAdminAlert('CROWD')"
            >
              <i data-feather="users" class="w-4 h-4 mb-1"></i>
              <span class="text-xs font-semibold">Stampede</span>
              <span class="text-[10px] text-yellow-100">Crowd / rush</span>
            </button>
          </div>
        </div>
      </div>

      <!-- 🚨 EMERGENCY SOS PANEL -->
      <div class="max-w-7xl mx-auto mb-16 px-4" data-aos="fade-up">
        <div class="bg-red-900/70 border border-red-300/60 rounded-2xl shadow-xl p-6 sm:p-8 text-red-50">
          <div class="flex items-center justify-between mb-4 flex-wrap gap-3">
            <div class="flex items-center gap-3">
              <div class="flex items-center justify-center w-10 h-10 rounded-full bg-red-500 shadow-lg">
                <i data-feather="alert-triangle" class="w-5 h-5"></i>
              </div>
              <div>
                <h3 class="text-xl font-semibold">Live Emergency SOS Alerts</h3>
                <p class="text-xs sm:text-sm text-red-100">
                  Auto-refreshing every 5 seconds. Latest alerts shown first.
                </p>
              </div>
            </div>

            <div class="flex items-center gap-4">
              <button @click="clearAlerts" class="clear-btn">Clear All Alerts</button>
              <div class="text-right text-sm">
                <div class="font-semibold">
                  Total Alerts: <span class="text-yellow-200">{{ alerts.length }}</span>
                </div>
                <div v-if="loading" class="text-xs text-red-100">Refreshing...</div>
                <div v-if="error" class="text-xs text-red-200">{{ error }}</div>
              </div>
            </div>
          </div>

          <div class="bg-black/20 rounded-xl overflow-hidden border border-red-500/30 max-h-72 sm:max-h-80 overflow-y-auto">
            <table class="min-w-full text-xs sm:text-sm">
              <thead class="bg-red-700/80 text-red-50 sticky top-0">
                <tr>
                  <th class="px-3 py-2 text-left">Time (IST)</th>
                  <th class="px-3 py-2 text-left">Devotee</th>
                  <th class="px-3 py-2 text-left">Emergency Type</th>
                  <th class="px-3 py-2 text-left">Location</th>
                  <th class="px-3 py-2 text-left">Status</th>
                  <th class="px-3 py-2 text-left">Action</th>
                </tr>
              </thead>

              <tbody class="divide-y divide-red-800/60">
                <tr
                  v-for="alert in alerts"
                  :key="alert.id"
                  class="hover:bg-red-800/60 transition"
                >
                  <td class="px-3 py-2 align-top">
                    {{ formatDate(alert.timestamp_utc) }}
                  </td>

                  <td class="px-3 py-2 align-top">
                    <div class="font-semibold text-red-50">
                      {{ alert.user_name || 'Unknown' }}
                    </div>
                    <div class="text-[10px] text-red-200">
                      ID: {{ alert.user_id || 'N/A' }}
                    </div>
                  </td>

                  <td class="px-3 py-2 align-top">
                    <div class="text-[11px] font-semibold">
                      {{ formatEmergencyType(alert.emergency_type) }}
                    </div>
                  </td>

                  <td class="px-3 py-2 align-top">
                    <div v-if="alert.latitude && alert.longitude" class="text-[11px]">
                      Lat: {{ Number(alert.latitude).toFixed(5) }}<br />
                      Lng: {{ Number(alert.longitude).toFixed(5) }}
                    </div>
                    <div v-else class="text-[11px] text-red-200">
                      Location unavailable
                    </div>
                  </td>

                  <td class="px-3 py-2 align-top">
                    <span
                      :class="[
                        'px-2 py-1 rounded-full text-[11px] font-semibold',
                        alert.status === 'PENDING'
                          ? 'bg-red-500/40 text-red-50'
                          : alert.status === 'IN_PROGRESS'
                          ? 'bg-yellow-500/30 text-yellow-100'
                          : 'bg-green-500/30 text-green-100'
                      ]"
                    >
                      {{ alert.status }}
                    </span>
                  </td>

                  <td class="px-3 py-2 align-top">
                    <button class="security-btn" @click="sendToSecurity(alert)">
                      Send to Security Officer
                    </button>
                  </td>
                </tr>

                <tr v-if="alerts.length === 0 && !loading">
                  <td colspan="6" class="px-3 py-4 text-center text-xs text-red-100">
                    No emergency alerts yet.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>
      </div>

      <hr class="mb-10 mx-auto max-w-7xl border-red-200"/>

      <h3 class="text-2xl font-serif font-semibold text-yellow-100 text-center mb-6 drop-shadow">
        Other Tools
      </h3>

      <div class="flex justify-center mb-16 px-4">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-4xl"> 
          <RouterLink to="/admin/calender" class="admin-link-btn secondary-btn group bg-indigo-600 hover:bg-indigo-700">
            <div class="icon-circle-xs bg-white text-indigo-600">
              <i data-feather="calendar" class="w-4 h-4"></i>
            </div>
            <div class="text-left">
              <span class="block text-sm font-bold text-white">View Calendar</span>
              <span class="text-xs text-indigo-200">All Events</span>
            </div>
          </RouterLink>

          <RouterLink to="/admin/all-tickets" class="admin-link-btn secondary-btn group bg-pink-600 hover:bg-pink-700">
            <div class="icon-circle-xs bg-white text-pink-600">
              <i data-feather="file-text" class="w-4 h-4"></i>
            </div>
            <div class="text-left">
              <span class="block text-sm font-bold text-white">All Tickets</span>
              <span class="text-xs text-pink-200">Darshan & Aarti</span>
            </div>
          </RouterLink>
          
          <RouterLink to="/admin/private-parking" class="admin-link-btn secondary-btn group bg-teal-600 hover:bg-teal-700">
            <div class="icon-circle-xs bg-white text-teal-600">
              <i data-feather="shield" class="w-4 h-4"></i>
            </div>
            <div class="text-left">
              <span class="block text-sm font-bold text-white">Private Parking</span>
              <span class="text-xs text-teal-200">Reserved Management</span>
            </div>
          </RouterLink>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { RouterLink } from 'vue-router'
import feather from 'feather-icons'
import AOS from 'aos'
import 'aos/dist/aos.css'
import axios from 'axios'

const API_BASE = `${import.meta.env.VITE_API_URL}` || 'http://127.0.0.1:5000/api'

const alerts = ref([])
const loading = ref(false)
const error = ref('')
const showAlertPanel = ref(false)
let intervalId = null

const toggleAlertPanel = () => {
  showAlertPanel.value = !showAlertPanel.value
  setTimeout(() => feather.replace(), 0)
}

const fetchAlerts = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_BASE}/emergency/admin/alerts`)
    alerts.value = res.data || []
  } catch (err) {
    console.error('Failed to load alerts:', err)
    error.value = 'Failed to load alerts'
  } finally {
    loading.value = false
  }
}

const formatDate = (iso) => {
  if (!iso) return 'N/A'
  return new Date(iso).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })
}

const formatEmergencyType = (type) => {
  if (!type) return 'N/A'
  const t = String(type).toLowerCase()
  switch (t) {
    case 'medical':
      return 'Medical Emergency'
    case 'security':
      return 'Security / Threat'
    case 'fire':
      return 'Fire / Hazard'
    case 'crowd':
      return 'Crowd / Stampede'
    default:
      return String(type).charAt(0).toUpperCase() + String(type).slice(1)
  }
}

// 🔔 Admin manual alert trigger – send POST with alert type
// 🔔 Admin manual alert trigger – send POST with alert type to backend
const triggerAdminAlert = async (type) => {
  // Frontend passes: 'MEDICAL' | 'FIRE' | 'CROWD'
  const emergencyType = String(type).toLowerCase() // => 'medical' | 'fire' | 'crowd'

  const payload = {
    // These fields match what your /api/emergency/trigger expects/uses
    user_id: 'ADMIN_PANEL',                // you can replace with real admin id if you have auth
    user_name: 'Admin Panel',              // or logged-in admin name
    current_page: 'ADMIN_EMERGENCY_PANEL', // just a marker for you
    emergency_type: emergencyType,         // 🔴 important for backend & UI
    status: 'PENDING',
    // optional: explicit timestamp if you want, backend can also generate it
    timestamp_utc: new Date().toISOString(),
    // location is optional; backend already handles missing lat/lng
    // latitude: null,
    // longitude: null,
    // accuracy: null,
  }

  try {
    const res = await axios.post(`${API_BASE}/emergency/triggerforces`, payload)
    console.log('Admin alert sent:', res.data)

    // refresh alerts table so this new alert appears instantly
    await fetchAlerts()

    showAlertPanel.value = false
    alert(`Alert "${formatEmergencyType(emergencyType)}" sent successfully.`)
  } catch (err) {
    console.error('Failed to send admin alert:', err)
    alert('Failed to send alert. Check backend logs.')
  }
}


const clearAlerts = async () => {
  try {
    await axios.post(`${API_BASE}/emergency/clear`)
    await fetchAlerts()
    alert('All SOS alerts cleared.')
  } catch (err) {
    console.error('Failed to clear alerts:', err)
    alert('Failed to clear alerts. Check backend logs.')
  }
}

const sendToSecurity = async (alertItem) => {
  try {
    await axios.post(`${API_BASE}/emergency/send-to-security`, {
      alert_id: alertItem.id,
    })
    alerts.value = alerts.value.map(a =>
      a.id === alertItem.id ? { ...a, status: 'IN_PROGRESS' } : a
    )
    alert('Alert sent to Security Officer.')
  } catch (err) {
    console.error('Failed to send to security:', err)
    alert('Failed to send to Security Officer. Check backend logs.')
  }
}

onMounted(() => {
  feather.replace()
  AOS.init({ duration: 800, easing: 'ease-in-out', once: true })

  fetchAlerts()
  intervalId = setInterval(fetchAlerts, 5000)
})

onBeforeUnmount(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>

<style scoped>
.admin-link-btn {
  display: flex;
  align-items: center;
  gap: 12px; 
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); 
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  text-decoration: none;
  cursor: pointer;
  position: relative;
  overflow: hidden; 
}
.admin-link-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(120deg, rgba(255, 255, 255, 0) 30%, rgba(255, 255, 255, 0.3) 50%, rgba(255, 255, 255, 0) 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}
.admin-link-btn:hover::before {
  opacity: 1;
}
.admin-link-btn:hover {
  transform: translateY(-5px); 
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.4);
}
.primary-btn { padding: 12px 18px; }
.secondary-btn { padding: 10px 15px; }

.icon-circle-sm,
.icon-circle-xs {
  background-color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); 
}
.icon-circle-sm {
  width: 40px; 
  height: 40px;
}
.icon-circle-xs {
  width: 35px; 
  height: 35px;
}

.security-btn {
  padding: 6px 10px;
  font-size: 11px;
  border-radius: 999px;
  border: 1px solid rgba(252, 165, 165, 0.9);
  background: rgba(248, 113, 113, 0.2);
  color: #fee2e2;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.security-btn:hover {
  background: rgba(248, 113, 113, 0.4);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
}

/* Alert type buttons */
.alert-type-btn {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(254, 226, 226, 0.4);
  color: #fef2f2;
  cursor: pointer;
  transition: all 0.2s ease;
}
.alert-type-btn i {
  margin-bottom: 2px;
}
.alert-type-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.35);
}
</style>
