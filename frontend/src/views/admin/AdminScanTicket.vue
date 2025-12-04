<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-3xl shadow-lg text-center">
    <h2 class="text-3xl font-bold mb-4">Scan Ticket</h2>

    <!-- File Upload Form (kept minimal; you can hook it to your existing image-endpoint) -->
    <form @submit.prevent="noop" enctype="multipart/form-data" class="mb-4">
      <input type="file" accept="image/*" class="mb-4" @change="onFileChange" />
      <button type="button" @click="uploadImage" class="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700">
        Scan Image
      </button>
    </form>

    <hr class="my-6" />

    <!-- Live Scan Button -->
    <button id="liveScanBtn" @click="openCamera" class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">
      Scan QR via Camera
    </button>

    <!-- Inline camera frame -->
    <div id="cameraFrame" v-show="cameraVisible" class="mt-4">
      <video ref="video" id="video" width="400" height="300" autoplay playsinline class="rounded-lg border"></video>
      <p id="qrResult" class="text-green-600 font-semibold mt-2">{{ qrResultText }}</p>
      <button id="closeCamera" @click="closeCamera" class="bg-gray-300 text-gray-800 px-4 py-1 rounded-lg hover:bg-gray-400 mt-2">
        Close Camera
      </button>
    </div>

    <!-- Modal (kept but not opened by default) -->
    <div id="camera-modal" v-if="modalVisible" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-3xl relative w-96">
        <span id="close-modal" @click="modalVisible = false" class="absolute top-2 right-4 cursor-pointer text-xl font-bold">&times;</span>
        <h3 class="text-xl font-bold mb-4">Place QR in camera frame</h3>
        <div id="qr-reader" style="width:100%; height:300px;"></div>
        <div id="qr-result" class="mt-4 font-bold text-green-600">{{ qrResultText }}</div>
      </div>
    </div>

    <!-- Ticket info (server-provided after scan) -->
    <div v-if="ticket" class="mt-6 p-4 bg-gray-100 rounded-lg">
      <h3 class="font-bold text-xl">Ticket #{{ ticket.id }}</h3>
      <p>Status: {{ qrResultText || 'N/A' }}</p>
      <p>Scans: {{ ticket.scan_count }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import axios from 'axios'

// Adjust if your Flask API is namespaced differently
const API_BASE = 'http://127.0.0.1:5000/api' // change if needed

// reactive state
const cameraVisible = ref(false)
const modalVisible = ref(false)
const qrResultText = ref('')
const ticket = ref(null)

const selectedFile = ref(null)
const uploading = ref(false)

let stream = null
let scanning = false
const video = ref(null)

const onFileChange = (e) => {
  selectedFile.value = e.target.files[0] || null
}

// optional image upload handler (uses your existing image endpoint)
const uploadImage = async () => {
  if (!selectedFile.value) {
    alert('Select an image first.')
    return
  }
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('qr_image', selectedFile.value)
    const res = await axios.post(`${API_BASE}/scan-ticket/image`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    qrResultText.value = res.data.message || 'Image scanned'
    ticket.value = res.data.ticket || null
  } catch (err) {
    console.error(err)
    qrResultText.value = err?.response?.data?.message || 'Failed to scan image.'
  } finally {
    uploading.value = false
  }
}

const openCamera = async () => {
  qrResultText.value = ''
  cameraVisible.value = true
  scanning = true

  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    if (video.value == null) {
      // assign video ref from DOM
      video.value = document.querySelector('#video')
    }
    video.value.srcObject = stream
    // try to play (mobile may require user gesture; this is initiated by button click)
    try { await video.value.play() } catch (e) { /* ignore */ }

    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')

    const tick = async () => {
      if (!scanning) return
      if (!video.value) return

      if (video.value.readyState === video.value.HAVE_ENOUGH_DATA) {
        canvas.width = video.value.videoWidth || 400
        canvas.height = video.value.videoHeight || 300
        ctx.drawImage(video.value, 0, 0, canvas.width, canvas.height)
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
        // use jsQR (make sure jsQR script is loaded in index.html or this page)
        if (window.jsQR) {
          const code = window.jsQR(imageData.data, canvas.width, canvas.height)
          if (code) {
            // show plain result
            qrResultText.value = `QR Detected: ${code.data}`

            // send the decoded QR payload to backend
            try {
              const res = await fetch(`${API_BASE}/scan-ticket/live`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ qr_text: code.data })
              })
              const data = await res.json()
              // display server message and ticket
              qrResultText.value = data.message || qrResultText.value
              ticket.value = data.ticket || ticket.value
            } catch (err) {
              console.error('Error validating ticket:', err)
              qrResultText.value = 'Server validation failed'
            }

            // stop scanning and camera
            scanning = false
            stopCamera()
            return
          }
        } else {
          // fallback: jsQR not available
          qrResultText.value = 'jsQR library not loaded'
        }
      }
      requestAnimationFrame(tick)
    }

    requestAnimationFrame(tick)
  } catch (err) {
    console.error('camera error', err)
    qrResultText.value = 'Unable to access camera. Allow camera permission.'
    cameraVisible.value = false
    scanning = false
  }
}

const stopCamera = () => {
  scanning = false
  cameraVisible.value = false
  if (stream) {
    stream.getTracks().forEach(t => t.stop())
    stream = null
  }
  // clear video element srcObject
  if (video.value) {
    try { video.value.srcObject = null } catch (e) {}
  }
}

const closeCamera = () => stopCamera()

onBeforeUnmount(() => {
  stopCamera()
})
</script>

<style scoped>
#cameraFrame {
  display: flex;
  flex-direction: column;
  align-items: center;
}
#video {
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}
</style>