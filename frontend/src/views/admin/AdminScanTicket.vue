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

const API_BASE = `${import.meta.env.VITE_API_URL}`

// reactive state
const cameraVisible = ref(false)
const modalVisible = ref(false)
const qrResultText = ref('')
const ticket = ref(null)

const selectedFile = ref(null)
const uploading = ref(false)

let stream = null
let scanning = false
let alreadyDetected = false

const video = ref(null)

const onFileChange = (e) => {
  selectedFile.value = e.target.files[0] || null
}

// ---------- IMAGE SCAN ----------
const uploadImage = async () => {
  if (!selectedFile.value) {
    alert('Select an image first.')
    return
  }

  qrResultText.value = 'Scanning image…'
  ticket.value = null

  try {
    const fd = new FormData()
    fd.append('qr_image', selectedFile.value)

    const res = await axios.post(`${API_BASE}/scan-ticket/image`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    qrResultText.value = res.data.message || 'Scan complete'
    ticket.value = res.data.ticket || null

  } catch (err) {
    qrResultText.value = err?.response?.data?.message || 'Image scan failed'
  }
}

// ---------- LIVE CAMERA SCAN ----------
const openCamera = async () => {
  qrResultText.value = 'Opening camera…'
  ticket.value = null
  cameraVisible.value = true
  scanning = true
  alreadyDetected = false

  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment' }
    })

    if (!video.value) {
      video.value = document.querySelector('#video')
    }

    video.value.srcObject = stream
    await video.value.play()

    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')

    const tick = async () => {
      if (!scanning || alreadyDetected) return

      if (video.value.readyState === video.value.HAVE_ENOUGH_DATA) {
        canvas.width = video.value.videoWidth
        canvas.height = video.value.videoHeight
        ctx.drawImage(video.value, 0, 0, canvas.width, canvas.height)

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)

        if (window.jsQR) {
          const code = window.jsQR(imageData.data, canvas.width, canvas.height)

          if (code) {
            alreadyDetected = true
            qrResultText.value = 'QR detected. Verifying…'

            try {
              const res = await fetch(`${API_BASE}/scan-ticket/live`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ qr_text: code.data })
              })

              const data = await res.json()
              qrResultText.value = data.message || 'Verification complete'
              ticket.value = data.ticket || null

            } catch (err) {
              qrResultText.value = 'Server validation failed'
            }

            stopCamera()
            return
          }
        }
      }

      requestAnimationFrame(tick)
    }

    requestAnimationFrame(tick)

  } catch (err) {
    qrResultText.value = 'Camera access denied'
    stopCamera()
  }
}

// ---------- CAMERA CLEANUP ----------
const stopCamera = () => {
  scanning = false
  cameraVisible.value = false

  if (stream) {
    stream.getTracks().forEach(t => t.stop())
    stream = null
  }

  if (video.value) {
    try { video.value.srcObject = null } catch {}
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
