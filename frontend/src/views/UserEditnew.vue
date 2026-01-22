<template>
  <div>

    <!-- ✅ RESPONSIVE BANNER -->
    <div class="relative w-full h-[200px] sm:h-[300px] md:h-[350px] overflow-hidden shadow-2xl">
      <div class="absolute inset-0">
        <img 
          src="/images/image.jpeg" 
          alt="Temple Profile Banner" 
          class="w-full h-full object-cover object-top"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-red-900/80 via-red-900/40 to-black/30"></div>
      </div>

      <div class="relative z-10 flex flex-col items-center justify-center h-full text-center px-3 sm:px-4" data-aos="fade-up">
        <h2 class="text-2xl sm:text-4xl md:text-5xl font-serif font-bold text-yellow-100 mb-2 drop-shadow-lg animate-fade-in-up">
          👤 Your Devotee Profile
        </h2>
        <p class="text-sm sm:text-lg md:text-xl text-yellow-200 max-w-2xl mx-auto font-light drop-shadow-md">
          Update your details for seamless Seva and Darshan bookings.
        </p>
      </div>
    </div>

    <!-- ✅ MAIN CONTENT -->
    <div class="min-h-screen bg-[#fffaf0] py-6 sm:py-10 px-3 sm:px-6">

      <div
        class="max-w-2xl mx-auto bg-white p-5 sm:p-10 rounded-2xl sm:rounded-3xl
               shadow-2xl border-t-8 border-red-700"
        data-aos="fade-up"
        data-aos-delay="200"
      >

        <h3
          class="text-xl sm:text-3xl font-serif font-bold text-red-800
                 text-center mb-6 sm:mb-8 border-b-2 border-red-100 pb-3 sm:pb-4"
        >
          ✨ Edit Your Profile
        </h3>

        <form @submit.prevent="updateProfile" class="space-y-5 sm:space-y-6">

          <!-- ✅ NAME -->
          <div>
            <label for="name" class="block mb-1 sm:mb-2 font-semibold text-gray-700 text-sm sm:text-base">
              Full Name
            </label>
            <input
              type="text"
              id="name"
              v-model="user.name"
              required
              class="w-full px-3 sm:px-4 py-2.5 sm:py-3
                     border-2 border-gray-300 rounded-xl
                     focus:outline-none focus:ring-2 focus:ring-red-200 focus:border-red-700
                     transition shadow-sm"
            />
          </div>

          <!-- ✅ EMAIL -->
          <div>
            <label for="email" class="block mb-1 sm:mb-2 font-semibold text-gray-700 text-sm sm:text-base">
              Email Address
            </label>
            <input
              type="email"
              id="email"
              v-model="user.email"
              required
              class="w-full px-3 sm:px-4 py-2.5 sm:py-3
                     border-2 border-gray-300 rounded-xl
                     focus:outline-none focus:ring-2 focus:ring-red-200 focus:border-red-700
                     transition shadow-sm"
            />
          </div>

          <!-- ✅ MOBILE -->
          <div>
            <label for="mobile" class="block mb-1 sm:mb-2 font-semibold text-gray-700 text-sm sm:text-base">
              Mobile Number
            </label>
            <input
              type="tel"
              id="mobile"
              maxlength="10"
              pattern="^[0-9]{10}$"
              placeholder="Enter 10-digit mobile number"
              v-model="user.mobile_no"
              required
              class="w-full px-3 sm:px-4 py-2.5 sm:py-3
                     border-2 border-gray-300 rounded-xl
                     focus:outline-none focus:ring-2 focus:ring-red-200 focus:border-red-700
                     transition shadow-sm"
            />
          </div>

          <!-- ✅ PINCODE -->
          <div>
            <label for="pincode" class="block mb-1 sm:mb-2 font-semibold text-gray-700 text-sm sm:text-base">
              Pincode
            </label>
            <input
              type="text"
              id="pincode"
              v-model="user.pincode"
              required
              class="w-full px-3 sm:px-4 py-2.5 sm:py-3
                     border-2 border-gray-300 rounded-xl
                     focus:outline-none focus:ring-2 focus:ring-red-200 focus:border-red-700
                     transition shadow-sm"
            />
          </div>

          <!-- ✅ ADDRESS -->
          <div>
            <label for="address" class="block mb-1 sm:mb-2 font-semibold text-gray-700 text-sm sm:text-base">
              Address
            </label>
            <textarea
              id="address"
              v-model="user.address"
              rows="3"
              required
              class="w-full px-3 sm:px-4 py-2.5 sm:py-3
                     border-2 border-gray-300 rounded-xl
                     focus:outline-none focus:ring-2 focus:ring-red-200 focus:border-red-700
                     transition shadow-sm"
            ></textarea>
          </div>

          <!-- ✅ BUTTON -->
          <div class="pt-3 sm:pt-4 text-center">
            <button
              type="submit"
              class="w-full sm:w-auto px-10 py-2.5 sm:py-3
                     bg-gradient-to-r from-red-700 to-red-900
                     text-white font-bold rounded-full
                     shadow-xl hover:shadow-2xl transform hover:scale-[1.01]
                     transition-all tracking-wider text-base sm:text-lg"
              data-aos="zoom-in"
              data-aos-delay="300"
            >
              Update Profile
            </button>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import AOS from 'aos'
import 'aos/dist/aos.css'

const userStore = useUserStore()
const user = ref({
  name: '',
  email: '',
  pincode: '',
  address: '',
  mobile_no: '',
})

// Load user data on mount
onMounted(async () => {
  AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
  const id = userStore.id || sessionStorage.getItem('user_id')
  if (!id) return
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/user/${id}`)
    user.value = res.data
  } catch (err) {
    console.error('Error loading profile:', err)
  }
})

// Update user profile
async function updateProfile() {
  const id = userStore.id || sessionStorage.getItem('user_id')
  try {
    await axios.put(`${import.meta.env.VITE_API_URL}/user/${id}`, user.value)
    userStore.updateProfile({ name: user.value.name })
    alert('Profile updated successfully!')
  } catch (err) {
    console.error('Error updating profile:', err)
    alert(err.response?.data?.message || 'Failed to update profile.')
  }
}
</script>

<style scoped>
/* Custom font simulation for 'font-serif' to match the design style */
.font-serif {
    font-family: Georgia, 'Times New Roman', Times, serif;
}

/* Animation utility class */
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

.animate-fade-in-up {
    animation: fadeInUp 1s ease-out both;
}
</style>