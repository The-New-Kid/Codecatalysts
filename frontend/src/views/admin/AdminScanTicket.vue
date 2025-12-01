<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-3xl shadow-lg text-center">
    <h2 class="text-3xl font-bold mb-4">Scan Ticket</h2>

    <!-- Flash / Error -->
    <div v-if="message" class="mb-4">
      <div
        :class="[
          'px-4 py-2 rounded-xl text-sm',
          success ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
        ]"
      >
        {{ message }}
      </div>
    </div>

    <!-- File Upload Form -->
    <form @submit.prevent="handleImageUpload" enctype="multipart/form-data">
      <input
        type="file"
        accept="image/*"
        class="mb-4"
        @change="onFileChange"
      />
      <button
        type="submit"
        :disabled="uploading || !selectedFile"
        class="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 disabled:opacity-60 disabled:cursor-not-allowed"
      >
        <span v-if="!uploading">Scan Image</span>
        <span v-else>Scanning...</span>
      </button>
    </form>

    <hr class="my-6" />

    <!-- Live Scan Button -->
    <button
      @click="startLiveScan"
      class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700"
    >
      Scan QR via Camera
    </button>

    <!-- Simple inline camera frame (like your original) -->
    <div
      v-if="cameraVisible"
      id="cameraFrame"
      class="mt-4 flex flex-col items-center space-y-2"
    >
      <video
        ref="videoRef"
        id="video"
        width="400"
        height="300"
        autoplay
        class="rounded-lg border"
      ></video>
      <p id="qrResult" class="text-green-600 font-semibold">
        {{ liveResultText }}
      </p>
      <button
        id="closeCamera"
        @click="stopCamera"
        class="bg-gray-300 text-gray-800 px-4 py-1 rounded-lg hover:bg-gray-400"
      >
        Close Camera
      </button>
    </div>

    <!-- Ticket info (from server) -->
    <div
      v-if="ticket"
      class="mt-6 p-4 bg-gray-100 rounded-lg text-left"
    >
      <h3 class="font-bold text-xl">Ticket #{{ ticket.id }}</h3>
      <p>Status: {{ ticket.status }}</p>
      <p>Scans: {{ ticket.scan_count }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:5000/api' // tumhara Flask API base

// state
const selectedFile = ref(null)
const uploading = ref(false)

const message = ref('')
const success = ref(false)

const ticket = ref(null)

// live scan state
const cameraVisible = ref(false)
const videoRef = ref(null)
const liveResultText = ref('')
let scanning = false
let stream = null

const onFileChange = (event) => {
  const file = event.target.files[0]
  selectedFile.value = file || null
}

const handleImageUpload = async () => {
  if (!selectedFile.value) return

  uploading.value = true
  message.value = ''
  success.value = false

  try {
    const formData = new FormData()
    formData.append('qr_image', selectedFile.value)

    // This should match your Flask endpoint logic
    const res = await axios.post(`${API_BASE}/scan-ticket/image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    success.value = res.data.success ?? true
    message.value = res.data.message || 'Ticket scanned successfully.'

    if (res.data.ticket) {
      ticket.value = res.data.ticket
    }
  } catch (err) {
    console.error(err)
    success.value = false
    message.value =
      err.response?.data?.message || 'Failed to scan ticket image.'
  } finally {
    uploading.value = false
  }
}

// live scan
const startLiveScan = async () => {
  message.value = ''
  liveResultText.value = ''
  cameraVisible.value = true
  scanning = true

  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment' }
    })

    if (videoRef.value) {
      videoRef.value.srcObject = stream
    }

    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')

    const tick = async () => {
      if (!scanning || !videoRef.value) return

      const video = videoRef.value
      if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight
        context.drawImage(video, 0, 0, canvas.width, canvas.height)
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height)

        if (window.jsQR) {
          const code = window.jsQR(imageData.data, canvas.width, canvas.height)
          if (code) {
            liveResultText.value = `QR Detected: ${code.data}`

            try {
              const res = await axios.post(`${API_BASE}/scan-ticket/live`, {
                ticket_id: code.data
              })

              success.value = res.data.success ?? true
              message.value = res.data.message || 'Ticket scanned successfully.'
              if (res.data.ticket) {
                ticket.value = res.data.ticket
              }
            } catch (err) {
              console.error(err)
              success.value = false
              message.value =
                err.response?.data?.message || 'Failed to validate scanned ticket.'
            }

            scanning = false
            stopCamera()
            return
          }
        }
      }

      requestAnimationFrame(tick)
    }

    requestAnimationFrame(tick)
  } catch (err) {
    console.error(err)
    message.value =
      'Unable to access camera. Please allow camera permission or try another device.'
    success.value = false
    scanning = false
    cameraVisible.value = false
  }
}

const stopCamera = () => {
  scanning = false
  cameraVisible.value = false
  if (stream) {
    stream.getTracks().forEach((t) => t.stop())
    stream = null
  }
}

onBeforeUnmount(() => {
  stopCamera()
})
</script>
