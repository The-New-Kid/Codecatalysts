<template>
  <div>
    <div class="w-full min-h-screen bg-orange-50">
      
      <!-- Header -->
      <div class="p-4 bg-red-700 text-white shadow-md">
        <h2 class="text-2xl font-bold font-serif tracking-wide">
          🏨 Nearby Accommodation — Somnath
        </h2>
        <p class="text-sm text-orange-200">Find hotels, guest houses & dharmshalas near the temple</p>
      </div>

      <!-- Distance Filter -->
      <div class="flex gap-3 p-4 overflow-x-auto">
        <button
          v-for="d in distances"
          :key="d"
          @click="setRadius(d)"
          :class="[
            'px-4 py-2 rounded-full text-sm font-medium transition border',
            radiusKm === d
              ? 'bg-red-700 text-white border-red-800'
              : 'bg-white text-red-700 border-red-400 hover:bg-red-100'
          ]"
        >
          {{ d }} km
        </button>
      </div>

      <!-- Map -->
      <div
        ref="mapEl"
        class="w-full min-h-[350px] md:min-h-[500px]"
        style="height: 60vh; max-height: 500px;"
      ></div>

      <!-- Recenter -->
      <button
        @click="recenter"
        class="fixed bottom-24 right-4 z-[999] bg-red-600 text-white px-4 py-2 rounded-full shadow-lg hover:bg-red-700 transition"
      >
        Recenter
      </button>

      <!-- Stays List -->
      <div class="p-4 bg-white mt-4 rounded-t-xl shadow-inner">
        <h3 class="text-lg font-bold text-red-800 mb-3">
          Available stays ({{ places.length }})
        </h3>

        <!-- Sorting -->
        <div class="mb-4">
          <select
            v-model="sortCriteria"
            @change="sortPlaces"
            class="px-3 py-2 border border-red-300 rounded-lg text-sm bg-white focus:ring-2 focus:ring-red-600"
          >
            <option value="distance">Sort by: Nearest</option>
            <option value="name">Sort by: Name (A-Z)</option>
          </select>
        </div>

        <!-- Loading Skeleton -->
        <div v-if="loading" class="space-y-3 mt-4">
          <div class="h-4 bg-orange-200/40 rounded w-1/2 animate-pulse"></div>
          <div class="h-4 bg-orange-200/40 rounded w-3/4 animate-pulse"></div>
          <div class="h-4 bg-orange-200/40 rounded w-2/3 animate-pulse"></div>
        </div>

        <!-- No Results -->
        <div v-if="!loading && places.length === 0" class="text-gray-500 text-sm">
          No places found in this radius.
        </div>

        <!-- Place Cards -->
        <div
          v-for="(p, i) in places"
          :key="p.id"
          @click="focusPlace(i)"
          class="p-4 mb-3 rounded-lg border border-orange-200 bg-orange-50 hover:bg-orange-100 cursor-pointer transition"
        >
          <div class="flex items-start justify-between">
            <div>
              <h4 class="font-bold text-lg text-red-800">
                {{ i + 1 }}. {{ p.name || 'Unnamed Stay' }}
              </h4>
              <p class="text-sm text-gray-600">{{ p.address }}</p>
              <p class="text-xs text-gray-500 mt-1">
                Distance: {{ p.distance.toFixed(2) }} km
              </p>
            </div>

            <a
              :href="directionsUrl(p)"
              target="_blank"
              class="text-sm bg-red-600 text-white px-3 py-1 rounded-full hover:bg-red-700"
            >
              Directions
            </a>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const map = ref(null)
const mapEl = ref(null)
const markers = ref([])
const places = ref([])
const loading = ref(false)

const center = { lat: 20.8896, lng: 70.4012 }
const radiusKm = ref(3)
const distances = [1, 3, 5, 10]

const sortCriteria = ref("distance")

function initMap() {
  map.value = L.map(mapEl.value).setView([center.lat, center.lng], 14)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map.value)

  L.circleMarker([center.lat, center.lng], {
    radius: 7,
    fillColor: "#c2410c",
    color: "#fff",
    weight: 2,
    fillOpacity: 1,
  })
    .addTo(map.value)
    .bindPopup("Somnath Mandir (Center)")
}

function clearMarkers() {
  markers.value.forEach(m => m.remove())
  markers.value = []
}

function calcDistance(lat1, lon1, lat2, lon2) {
  const R = 6371
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1 * Math.PI / 180) *
      Math.cos(lat2 * Math.PI / 180) *
      Math.sin(dLon / 2) ** 2

  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

function formatAddress(tags = {}) {
  const parts = []
  if (tags["addr:street"]) parts.push(tags["addr:street"])
  if (tags["addr:city"]) parts.push(tags["addr:city"])
  if (tags.operator) parts.push(tags.operator)
  return parts.length ? parts.join(", ") : "No address available"
}

async function fetchStays() {
  loading.value = true
  places.value = []
  clearMarkers()

  const radiusMeters = radiusKm.value * 1000

  const query = `
[out:json][timeout:30];
(
  node["tourism"~"hotel|hostel|guest_house|motel"](around:${radiusMeters},${center.lat},${center.lng});
  way["tourism"~"hotel|hostel|guest_house|motel"](around:${radiusMeters},${center.lat},${center.lng});
);
out center;`

  try {
    const data = await fetch("https://overpass-api.de/api/interpreter", {
      method: "POST",
      body: new URLSearchParams({ data: query }),
    }).then(r => r.json())

    const results = (data.elements || [])
      .map(el => {
        const lat = el.lat || el.center?.lat
        const lon = el.lon || el.center?.lon
        if (!lat || !lon) return null

        return {
          id: el.id,
          lat,
          lon,
          name: el.tags?.name,
          address: formatAddress(el.tags),
          distance: calcDistance(center.lat, center.lng, lat, lon),
        }
      })
      .filter(Boolean)

    places.value = results
    sortPlaces()
    renderMarkers()
  } catch (e) {
    console.error(e)
    alert("Error fetching nearby stays.")
  }

  loading.value = false
}

function renderMarkers() {
  clearMarkers()

  places.value.forEach((p, i) => {
    const marker = L.marker([p.lat, p.lon]).addTo(map.value)
    marker.bindPopup(
      `<b>${i + 1}. ${p.name || "Stay"}</b><br>${p.address}`
    )
    markers.value.push(marker)
  })

  if (places.value.length > 0) {
    const bounds = places.value.map(p => [p.lat, p.lon])
    bounds.push([center.lat, center.lng])
    map.value.fitBounds(bounds, { padding: [30, 30] })
  }
}

function focusPlace(i) {
  const p = places.value[i]
  map.value.panTo([p.lat, p.lon])
  markers.value[i].openPopup()
}

function directionsUrl(p) {
  return `https://google.com/maps/dir/?api=1&destination=${p.lat},${p.lon}`
}

function setRadius(d) {
  radiusKm.value = d
  fetchStays()
}

function sortPlaces() {
  if (sortCriteria.value === "distance") {
    places.value.sort((a, b) => a.distance - b.distance)
  } else if (sortCriteria.value === "name") {
    places.value.sort((a, b) => (a.name || "").localeCompare(b.name || ""))
  }
}

function recenter() {
  map.value.setView([center.lat, center.lng], 14)
}

onMounted(() => {
  initMap()
  fetchStays()
})
</script>

<style scoped>
.custom-marker .marker-pin {
  background: #c2410c;
  color: #fff;
  font-weight: 700;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 8px rgba(0,0,0,0.28);
  border: 2px solid rgba(255,255,255,0.12);
  font-size: 13px;
  line-height: 1;
}

.custom-marker {
  background: transparent !important;
  width: 28px;
  height: 28px;
}

@media (max-width: 640px) {
  .custom-marker .marker-pin {
    width: 22px;
    height: 22px;
    font-size: 11px;
  }
}
</style>
