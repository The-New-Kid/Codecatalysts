<template>
  <div>
    
    <div class="relative w-full h-[500px] lg:h-[600px] overflow-hidden shadow-2xl">
      <div class="absolute inset-0">
        <img 
            src="/images/somnath10.jpg" 
            alt="Temple Banner" 
            class="w-full h-full object-cover object-center"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-red-900/90 via-red-900/40 to-black/30"></div>
      </div>

      <div class="relative z-10 flex flex-col items-center justify-center h-full text-center px-4" data-aos="fade-up">
        
        <div class="mb-8 animate-fade-in-up">
          <h2 class="text-4xl md:text-6xl font-serif font-bold text-white mb-2 drop-shadow-lg">
            Jai Somnath, {{ userStore.name || 'Bhakt' }}
          </h2>
          <p class="text-lg md:text-xl text-yellow-100 max-w-2xl mx-auto font-light drop-shadow-md">
            Manage your darshan bookings and parking seva with ease.
          </p>
        </div>

        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 w-full max-w-5xl">
          <RouterLink to="book-spot" class="glass-btn group bg-orange-600 border-none hover:bg-orange-700">
            <div class="icon-circle bg-white text-orange-600">
              <i data-feather="check-circle" class="w-6 h-6"></i>
            </div>
            <div class="text-left">
              <span class="block text-sm font-bold text-gray-800 group-hover:text-orange-700">Spot Booking</span>
              <span class="text-xs text-gray-500">Reserve Now</span>
            </div>
          </RouterLink>

          <RouterLink to="book_darshannew" class="glass-btn group bg-red-700 border-none hover:bg-red-800">
            <div class="icon-circle bg-white text-red-700">
              <i data-feather="calendar" class="w-6 h-6"></i>
            </div>
            <div class="text-left">
              <span class="block text-sm font-bold text-gray-800 group-hover:text-red-700">Sugam Darshan</span>
              <span class="text-xs text-gray-600">Get Ticket</span>
            </div>
          </RouterLink>
          
          <RouterLink to="book-aarti" class="glass-btn group bg-yellow-600 border-none hover:bg-yellow-700">
            <div class="icon-circle bg-white text-yellow-600">
              <i data-feather="sun" class="w-6 h-6"></i>
            </div>
            <div class="text-left">
              <span class="block text-sm font-bold text-gray-800 group-hover:text-yellow-700">Sugam Aarti</span>
              <span class="text-xs text-gray-600">Divine Experience</span>
            </div>
          </RouterLink>

          <RouterLink to="book-seva" class="glass-btn group bg-purple-600 border-none hover:bg-purple-700">
            <div class="icon-circle bg-white text-purple-600">
              <i data-feather="gift" class="w-6 h-6"></i>
            </div>
            <div class="text-left">
              <span class="block text-sm font-bold text-gray-800 group-hover:text-purple-700">Seva Daan</span>
              <span class="text-xs text-gray-600">Offerings & Rituals</span>
            </div>
          </RouterLink>
          
          <div>
            <button
              v-if="!isTatkalOpen"
              disabled
              class="glass-btn group bg-gray-400 border-none cursor-not-allowed opacity-60"
            >
              <div class="icon-circle bg-white text-gray-500">
                <i data-feather="zap" class="w-6 h-6"></i>
              </div>
              <div class="text-left">
                <span class="block text-sm font-bold text-gray-700">Darshan Tatkal</span>
                <span class="text-xs text-gray-500">{{ openMessage }}</span>
              </div>
            </button>

            <RouterLink
              v-else
              to="book_darshan_tatkal"
              class="glass-btn group bg-red-600 border-none hover:bg-red-700"
            >
              <div class="icon-circle bg-white text-red-600">
                <i data-feather="zap" class="w-6 h-6"></i>
              </div>
              <div class="text-left">
                <span class="block text-sm font-bold text-gray-800 group-hover:text-red-700">Darshan Tatkal</span>
                <span class="text-xs text-gray-600">Fast Track Entry</span>
              </div>
            </RouterLink>
          </div>

          <div>
            <button
              v-if="!isTatkalOpen"
              disabled
              class="glass-btn group bg-gray-400 border-none cursor-not-allowed opacity-60"
            >
              <div class="icon-circle bg-white text-gray-500">
                <i data-feather="sunrise" class="w-6 h-6"></i>
              </div>
              <div class="text-left">
                <span class="block text-sm font-bold text-gray-700">Aarti Tatkal</span>
                <span class="text-xs text-gray-500">{{ openMessage }}</span>
              </div>
            </button>

            <RouterLink
              v-else
              to="book_aarti_tatkal"
              class="glass-btn group bg-orange-600 border-none hover:bg-orange-700"
            >
              <div class="icon-circle bg-white text-orange-600">
                <i data-feather="sunrise" class="w-6 h-6"></i>
              </div>
              <div class="text-left">
                <span class="block text-sm font-bold text-gray-800 group-hover:text-orange-700">Aarti Tatkal</span>
                <span class="text-xs text-gray-600">Instant Booking</span>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

    <div class="w-full bg-yellow-100 border-b-2 border-yellow-300 overflow-hidden shadow-inner">
      <marquee behavior="scroll" direction="left" scrollamount="10" class="py-3 flex items-center">
        <span class="text-red-800 font-bold text-lg tracking-wide mx-4">
          🔔 Tatkal booking for Aarti and Darshan opens daily at 7:00 AM. Please plan your booking accordingly. || Jai Shri Mahakal 🙏
        </span>
      </marquee>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <h2 class="text-3xl font-serif font-extrabold text-center text-red-800 mb-12" data-aos="fade-up">
        🙏 Essential Temple Services
      </h2>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        
        <div 
          class="service-card" 
          data-aos="fade-right" 
          data-aos-delay="100"
        >
          <div class="p-6">
            <i data-feather="bell" class="w-8 h-8 text-orange-600 mb-4"></i>
            <h3 class="text-xl font-bold text-gray-900 mb-2">E-Pooja & Rituals</h3>
            <p class="text-gray-600 mb-4 text-sm">
              Perform traditional rituals and offerings remotely. Book a <em>Sankalp</em> (vow) and receive Prashad at your home.
            </p>
            <RouterLink to="#" class="text-orange-600 hover:text-orange-800 font-medium text-sm flex items-center">
              Book Your Seva <i data-feather="arrow-right" class="w-4 h-4 ml-1"></i>
            </RouterLink>
          </div>
        </div>

        <div 
          class="service-card" 
          data-aos="fade-up" 
          data-aos-delay="200"
        >
          <div class="p-6">
            <i data-feather="heart" class="w-8 h-8 text-red-700 mb-4"></i>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Temple Donations</h3>
            <p class="text-gray-600 mb-4 text-sm">
              Support the temple's maintenance, Annakshetra (food charity), and cultural activities with your generous contribution.
            </p>
            <!-- UPDATED LINK HERE -->
            <RouterLink 
              to="donation"
              class="text-red-700 hover:text-red-900 font-medium text-sm flex items-center"
            >
              Donate Now <i data-feather="arrow-right" class="w-4 h-4 ml-1"></i>
            </RouterLink>
          </div>
        </div>
        
        <div 
          class="service-card" 
          data-aos="fade-left" 
          data-aos-delay="300"
        >
          <div class="p-6">
            <i data-feather="home" class="w-8 h-8 text-purple-600 mb-4"></i>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Pilgrim Accommodation</h3>
            <p class="text-gray-600 mb-4 text-sm">
              Find comfortable and affordable <em>Dharamshala</em> (guesthouse) options near the temple for your stay.
            </p>
            <RouterLink to="/user/accomodation" class="text-purple-600 hover:text-purple-800 font-medium text-sm flex items-center">
              View Stays <i data-feather="arrow-right" class="w-4 h-4 ml-1"></i>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 pb-24" data-aos="fade-up">
      <div class="bg-red-50 border border-red-200 rounded-xl p-8 md:p-12 text-center shadow-lg">
        <h3 class="text-3xl font-serif font-bold text-red-800 mb-3">
          Need Help with Your Darshan?
        </h3>
        <p class="text-red-700 max-w-3xl mx-auto mb-6">
          Our Seva Kendra is available to assist you with all bookings, parking inquiries, and temple information. Your journey to the divine should be seamless.
        </p>
        <RouterLink 
          to="#" 
          class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-full shadow-sm text-white bg-red-700 hover:bg-red-800 transition duration-150"
        >
          <i data-feather="phone" class="w-5 h-5 mr-2"></i>
          Contact Seva Kendra
        </RouterLink>
      </div>
    </div>

    <footer class="relative w-full overflow-hidden">
      <div class="absolute inset-0">
        <img 
          src="/images/somnath10.jpg" 
          alt="Somnath Temple at Dusk" 
          class="w-full h-full object-cover object-center filter grayscale opacity-40"
        />
        <div class="absolute inset-0 bg-red-900/90 mix-blend-multiply"></div>
      </div>

      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center text-white" data-aos="zoom-in">
        <i data-feather="droplet" class="w-10 h-10 text-yellow-400 mx-auto mb-4"></i>
        
        <blockquote class="max-w-4xl mx-auto mb-10">
          <p class="text-2xl md:text-4xl font-serif font-light italic leading-relaxed">
            "The journey to the Jyotirlinga is the journey within. May the light of Mahakal illuminate your path."
          </p>
        </blockquote>

        <div class="pt-8 border-t border-red-700/50">
          <p class="text-xl font-bold mb-2">Shri Mahakal Trust</p>
          <p class="text-sm text-red-200">
            Somnath, Gujrat, India 
            <span class="mx-2">|</span> 
            E-mail: seva@mahakal.org 
            <span class="mx-2">|</span> 
            Phone: +91 0000 12345
          </p>
          <p class="text-xs mt-4 text-red-300/70">
            © 2025 Mahakal Online Seva. All Rights Reserved.
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { useUserStore } from '@/stores/user'
import feather from 'feather-icons'

const userStore = useUserStore()

onMounted(async () => {
  feather.replace()
  AOS.init({ duration: 800, once: true })

  const id = userStore.id || sessionStorage.getItem('user_id')
  if (!id) return

  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/user/dashboard/${id}`)
    userStore.name = res.data.user.name
  } catch (err) {
    console.error('Error loading dashboard:', err)
  }
})

const isTatkalOpen = ref(false)
const openMessage = ref("")

function checkTatkalWindow() {
  const now = new Date()
  const hour = now.getHours()
  const minute = now.getMinutes()

  const current = hour * 60 + minute      // convert time to minutes
  const start = 7 * 60                    // 7 AM
  const end = 21 * 60                     // 9 PM

  if (current >= start && current <= end) {
    isTatkalOpen.value = true
    openMessage.value = "Open Now"
  } else {
    isTatkalOpen.value = false
    openMessage.value = "Opens at 7:00 AM"
  }
}

checkTatkalWindow()
setInterval(checkTatkalWindow, 60000) // update every minute
</script>

<style scoped>
.glass-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.95); 
  padding: 12px 20px;
  border-radius: 12px;
  backdrop-filter: blur(2px); 
  -webkit-backdrop-filter: blur(2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  text-decoration: none;
  cursor: pointer;
}

.glass-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -1px rgba(0, 0, 0, 0.2);
}

.icon-circle {
  width: 40px;
  height: 40px;
  background-color: #fff7ed;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.service-card {
  background-color: white;
  border-radius: 1rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease-in-out;
  border: 1px solid #f3f4f6;
}

.service-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.2);
  border-color: #f97316;
}
</style>
