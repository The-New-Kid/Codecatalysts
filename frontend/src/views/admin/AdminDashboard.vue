<template>
  <div class="relative w-full min-h-screen overflow-auto">
    
    <div class="fixed inset-0 w-full h-full">
      <img 
        src="/images/somnath10.jpg" 
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

      <div class="flex justify-center mb-20 px-4">
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
      
      <hr class="mb-10 mx-auto max-w-7xl border-red-200"/>

      <h3 class="text-2xl font-serif font-semibold text-yellow-100 text-center mb-6 drop-shadow">Other Tools</h3>
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
import { onMounted } from 'vue' // Removed ref, axios, fetchParkingLots, spotClasses, etc.
import { RouterLink } from 'vue-router'
import feather from 'feather-icons'
import AOS from 'aos'
import 'aos/dist/aos.css'

onMounted(() => {
  feather.replace() 
  
  if (window.AOS) {
    AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
  }
})
</script>

<style scoped>
/* Base Button Style: Smaller, More Attractive */
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

/* Shine/Gradient Effect on Hover */
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

/* Hover Effect */
.admin-link-btn:hover {
    transform: translateY(-5px); 
    box-shadow: 0 15px 25px rgba(0, 0, 0, 0.4);
}

/* --- Primary (Hero) Button Sizes --- */
.primary-btn {
    padding: 12px 18px; 
}

/* --- Secondary Button Sizes --- */
.secondary-btn {
    padding: 10px 15px; 
}

/* --- Icon Circles --- */
.icon-circle-sm {
    width: 40px; 
    height: 40px;
    background-color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); 
}

.icon-circle-xs {
    width: 35px; 
    height: 35px;
    background-color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>