<template>
  <!-- 👇 Only show on native (Android/iOS), not on web -->
  <div v-if="isNativeApp" class="sos-button-container">
    <!-- MAIN SOS BUTTON -->
    <button 
      @click="handleSosClick"
      :disabled="isSending"
      :class="['sos-button', { 'pulse-animation': !isConfirming, 'opacity-50': isSending }]"
    >
      <i data-feather="alert-triangle" class="w-6 h-6"></i>
      <span>Emergency SOS</span>
    </button>

    <!-- CONFIRM BUTTON -->
    <button
      v-if="isConfirming"
      @click="openTypeSelector"
      :disabled="isSending"
      class="sos-confirm-button"
    >
      {{ isSending ? 'Sending...' : 'CONFIRM - CHOOSE EMERGENCY TYPE' }}
    </button>

    <!-- EMERGENCY TYPE SELECTION POPUP -->
    <div
      v-if="isSelectingType"
      class="type-overlay"
      @click.self="closeTypeSelector"
    >
      <div class="type-card">
        <h3 class="type-title-main">Select Emergency Type</h3>
        <p class="type-subtitle">
          This helps the security & admin team respond faster.
        </p>

        <div class="type-grid">
          <button
            v-for="type in emergencyTypes"
            :key="type.id"
            class="type-chip"
            :class="{ 'type-chip-active': selectedEmergencyType === type.id }"
            :disabled="isSending"
            @click="selectTypeAndSend(type.id)"
          >
            <div class="type-chip-header">
              <span class="type-chip-label">{{ type.label }}</span>
            </div>
            <p class="type-chip-desc">{{ type.description }}</p>
          </button>
        </div>

        <button
          class="type-cancel-btn"
          @click="closeTypeSelector"
          :disabled="isSending"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import feather from 'feather-icons'
import { Capacitor } from '@capacitor/core'
import { Geolocation } from '@capacitor/geolocation'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const isConfirming = ref(false)
const isSending = ref(false)

const isSelectingType = ref(false)
const selectedEmergencyType = ref(null)

// 👇 only show SOS when app is running as Capacitor native
const isNativeApp = ref(false)

const emergencyTypes = [
  {
    id: 'medical',
    label: 'Medical Emergency',
    description: 'Injury, fainting, chest pain, breathing issues, etc.'
  },
  {
    id: 'security',
    label: 'Security / Threat',
    description: 'Suspicious activity, fight, theft, illegal entry, etc.'
  },
  {
    id: 'fire',
    label: 'Fire / Hazard',
    description: 'Fire, gas smell, electrical spark, structural risk.'
  },
  {
    id: 'crowd',
    label: 'Crowd / Stampede',
    description: 'Overcrowding, pushing, risk of stampede in any area.'
  }
]

const API_BASE = import.meta.env.VITE_API_URL
const IS_TESTING_MODE = false

// ✅ HYBRID GEOLOCATION: Capacitor (native) + browser fallback
const getGeoLocation = async () => {
  // 🔹 1) Native app → use Capacitor Geolocation
  if (Capacitor.isNativePlatform()) {
    try {
      // Check + request permissions
      const perm = await Geolocation.checkPermissions()
      if (perm.location !== 'granted' && perm.coarseLocation !== 'granted') {
        const req = await Geolocation.requestPermissions()
        if (req.location !== 'granted' && req.coarseLocation !== 'granted') {
          alert('Location permission denied. Please enable location for DevDhamPath app.')
          return { error: true, message: 'Permission denied' }
        }
      }

      // Try current GPS position (can timeout)
      try {
        const pos = await Geolocation.getCurrentPosition({
          enableHighAccuracy: true,
          timeout: 30000 // 30 seconds
        })

        const data = {
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
          accuracy: pos.coords.accuracy
        }
        console.log('📍 Native Geolocation SUCCESS:', data)
        return data
      } catch (err) {
        console.warn('⚠️ getCurrentPosition failed, trying last known:', err)

        // Fallback: last known position
        const last = await Geolocation.getLastKnownPosition()
        if (last && last.coords) {
          const data = {
            latitude: last.coords.latitude,
            longitude: last.coords.longitude,
            accuracy: last.coords.accuracy
          }
          console.log('📍 Native LastKnownPosition USED:', data)
          return data
        }

        alert('Unable to get GPS location. Please go outdoors and enable GPS, then try again.')
        return { error: true, message: 'Timeout / no position' }
      }
    } catch (error) {
      console.error('❌ Native Geolocation error:', error)
      alert('Unable to fetch location from device. Check GPS and app permissions.')
      return { error: true, message: String(error) }
    }
  }

  // 🔹 2) Web fallback → browser geolocation
  return new Promise((resolve) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const data = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy
          }
          console.log('📍 Web Geolocation SUCCESS:', data)
          resolve(data)
        },
        (error) => {
          console.warn(`Geolocation error (${error.code}): ${error.message}`)
          alert(`Location error (code ${error.code}): ${error.message}`)
          resolve({
            error: true,
            code: error.code,
            message: error.message
          })
        },
        { enableHighAccuracy: true, timeout: 30000, maximumAge: 0 }
      )
    } else {
      alert('Geolocation not supported in this browser.')
      resolve({ error: true, message: 'Geolocation not supported' })
    }
  })
}

const handleSosClick = () => {
  if (isConfirming.value || isSending.value) return
  isConfirming.value = true

  setTimeout(() => {
    if (isConfirming.value && !isSending.value && !isSelectingType.value) {
      isConfirming.value = false
    }
  }, 5000)
}

const openTypeSelector = () => {
  if (isSending.value) return
  isSelectingType.value = true
}

const closeTypeSelector = () => {
  if (isSending.value) return
  isSelectingType.value = false
  selectedEmergencyType.value = null
  isConfirming.value = false
}

const selectTypeAndSend = async (typeId) => {
  selectedEmergencyType.value = typeId
  await sendSOS()
}

const sendSOS = async () => {
  if (isSending.value) return

  if (!selectedEmergencyType.value) {
    alert('Please select an emergency type.')
    return
  }

  isSending.value = true
  isConfirming.value = false

  const locationData = await getGeoLocation()
  console.log('📍 GeoLocation result:', locationData)
  const now = new Date()

  const istOptions = {
    timeZone: 'Asia/Kolkata',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }
  const istTimestamp = now.toLocaleString('en-IN', istOptions)

  const payload = {
    user_id: userStore.id || sessionStorage.getItem('user_id'),
    user_name: userStore.name || 'Bhakt',
    timestamp_utc: now.toISOString(),
    location: locationData,
    current_page: window.location.href,
    emergency_type: selectedEmergencyType.value
  }

  console.log('🚨 SOS payload being sent:', payload)

  if (IS_TESTING_MODE) {
    const output =
      `🚨 SOS TEST MODE SUCCESS 🚨\n\n` +
      `User: ${payload.user_name} (${payload.user_id})\n` +
      `Type: ${payload.emergency_type}\n` +
      `Location Status: ${payload.location.error ? 'FAILED' : 'SUCCESS'}\n` +
      `Latitude: ${payload.location.latitude || 'N/A'}\n` +
      `Longitude: ${payload.location.longitude || 'N/A'}\n` +
      `Accuracy: ${payload.location.accuracy || 'N/A'}\n` +
      `Timestamp (IST): ${istTimestamp}\n\n`

    console.log('SOS Payload for Testing:', payload)
    alert(output)
  } else {
    try {
      await axios.post(`${API_BASE}/emergency/trigger`, payload)
      alert('🚨 Emergency Alert Sent! Help is on the way. Please remain calm.')
    } catch (error) {
      console.error('SOS API failed:', error)
      alert('⚠️ Failed to send alert. Please call helpline directly.')
    }
  }

  isSending.value = false
  isSelectingType.value = false
  selectedEmergencyType.value = null
}

onMounted(() => {
  feather.replace()
  isNativeApp.value = Capacitor.isNativePlatform()
  console.log('Is native app?', isNativeApp.value)
})
</script>

<style scoped>
.sos-button-container {
  position: fixed;
  bottom: 40px;
  right: 40px;
  z-index: 9999;
  width: 200px;
}
@media (max-width: 640px) {
  .sos-button-container {
    right: 16px;
    bottom: 16px;
    width: 160px;
  }
}
.sos-button,
.sos-confirm-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 15px 20px;
  font-weight: 700;
  border-radius: 9999px;
  box-shadow: 0 4px 15px rgba(255, 0, 0, 0.4);
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  width: 100%;
}
.sos-button {
  position: relative;
  background-color: #dc2626;
  color: white;
  gap: 10px;
  font-size: 1.1em;
  z-index: 10;
}
.sos-button:hover {
  background-color: #b91c1c;
  transform: scale(1.03);
}
.sos-confirm-button {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #b91c1c;
  color: #fee2e2;
  animation: confirm-pulse 0.5s infinite alternate;
  font-size: 0.95em;
  z-index: 20;
}
@keyframes confirm-pulse {
  from { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
  to { box-shadow: 0 0 0 20px rgba(255, 0, 0, 0); }
}
.pulse-animation {
  animation: subtle-pulse 2s infinite;
}
@keyframes subtle-pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.02); }
  100% { transform: scale(1); }
}

/* Type Popup */
.type-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 16px;
}
.type-card {
  background: #ffffff;
  border-radius: 18px;
  padding: 16px 16px 12px;
  max-width: 360px;
  width: 100%;
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.25);
  animation: type-card-in 0.18s ease-out;
}
@keyframes type-card-in {
  from { opacity: 0; transform: translateY(18px) scale(0.96); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
.type-title-main {
  font-size: 1.05rem;
  font-weight: 700;
  color: #991b1b;
  margin-bottom: 2px;
}
.type-subtitle {
  font-size: 0.8rem;
  color: #4b5563;
  margin-bottom: 10px;
}
.type-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
  margin-bottom: 10px;
}
.type-chip {
  text-align: left;
  border-radius: 12px;
  padding: 8px 10px;
  border: 1px solid #fee2e2;
  background: #fef2f2;
  cursor: pointer;
  transition: all 0.18s ease;
}
.type-chip:hover {
  border-color: #ef4444;
  background: #fee2e2;
  transform: translateY(-1px);
}
.type-chip-active {
  border-color: #b91c1c;
  background: #fee2e2;
  box-shadow: 0 0 0 1px rgba(185, 28, 28, 0.4);
}
.type-chip-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.type-chip-label {
  font-size: 0.9rem;
  font-weight: 700;
  color: #991b1b;
}
.type-chip-desc {
  font-size: 0.75rem;
  color: #4b5563;
  margin-top: 2px;
}
.type-cancel-btn {
  width: 100%;
  margin-top: 2px;
  padding: 6px 10px;
  border-radius: 9999px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  font-size: 0.8rem;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.18s ease;
}
.type-cancel-btn:hover {
  background: #f3f4f6;
}
</style>