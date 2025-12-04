<template>
  <div class="flex flex-col min-h-screen bg-[#fffbf2] font-sans">
    <header class="fixed top-0 w-full z-50 bg-gradient-to-r from-orange-600 via-red-700 to-red-800 shadow-lg text-white">
      <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
          
          <div class="flex items-center gap-3">
            <div class="bg-white/10 p-2 rounded-full border border-yellow-400/50 backdrop-blur-sm">
              <span class="text-3xl glow-text">🛕</span>
            </div>
            <div class="flex flex-col">
              <h1 class="text-xl font-bold font-serif tracking-wide text-yellow-50">
                Mandir Admin
              </h1>
              <span class="text-xs text-orange-200 uppercase tracking-widest">Management Portal</span>
            </div>
          </div>

          <nav class="hidden lg:flex space-x-6 overflow-x-auto items-center">
            <RouterLink 
              to="/admin/dashboard" 
              class="nav-item text-sm font-medium text-orange-100 hover:text-white transition-colors"
            >
              <span class="flex items-center gap-1"><i data-feather="home" class="w-4 h-4"></i>Home</span>
            </RouterLink>
            
            <RouterLink 
              to="/admin/users" 
              class="nav-item text-sm font-medium text-orange-100 hover:text-white transition-colors"
            >
              <span class="flex items-center gap-1"><i data-feather="users" class="w-4 h-4"></i>Users</span>
            </RouterLink>

            <RouterLink 
              to="/admin/parking-lots" 
              class="nav-item text-sm font-medium text-orange-100 hover:text-white transition-colors"
            >
              <span class="flex items-center gap-1"><i data-feather="trello" class="w-4 h-4"></i>Parking</span>
            </RouterLink>

            <RouterLink 
              to="/admin/cctv" 
              class="nav-item text-sm font-medium text-orange-100 hover:text-white transition-colors"
            >
              <span class="flex items-center gap-1"><i data-feather="video" class="w-4 h-4"></i>CCTV Live</span>
            </RouterLink>
            
            <RouterLink 
              to="/admin/analytics" 
              class="nav-item text-sm font-medium text-orange-100 hover:text-white transition-colors"
            >
              <span class="flex items-center gap-1"><i data-feather="bar-chart-2" class="w-4 h-4"></i>Analytics</span>
            </RouterLink>
            </nav>

          <div class="flex items-center gap-4">
            <div class="hidden sm:flex flex-col items-end">
              <span class="text-sm font-bold text-yellow-100">{{ username }}</span>
              <span class="text-xs text-orange-200">Administrator</span>
            </div>
            
            <button
              @click="logout"
              class="bg-red-900/50 hover:bg-red-900 border border-red-400 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 flex items-center gap-2 shadow-sm"
            >
              <span class="hidden sm:inline">Logout</span>
              <i data-feather="log-out" class="w-4 h-4"></i>
            </button>
            
            <button
              @click="isMobileMenuOpen = !isMobileMenuOpen"
              class="lg:hidden text-white p-2 rounded-lg hover:bg-white/10 transition-colors"
            >
              <i v-if="!isMobileMenuOpen" data-feather="menu" class="w-6 h-6"></i>
              <i v-else data-feather="x" class="w-6 h-6"></i>
            </button>
          </div>
        </div>
      </div>
      
      <transition 
        enter-active-class="transition ease-out duration-200"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <div v-if="isMobileMenuOpen" class="lg:hidden px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-red-800/95 shadow-inner">
            <RouterLink 
              to="/admin/dashboard" 
              class="block px-3 py-2 rounded-md text-base font-medium text-orange-100 hover:bg-white/10"
              @click="isMobileMenuOpen = false"
            >Dashboard</RouterLink>
            <RouterLink 
              to="/admin/users" 
              class="block px-3 py-2 rounded-md text-base font-medium text-orange-100 hover:bg-white/10"
              @click="isMobileMenuOpen = false"
            >Users</RouterLink>
            <RouterLink 
              to="/admin/parking-lots" 
              class="block px-3 py-2 rounded-md text-base font-medium text-orange-100 hover:bg-white/10"
              @click="isMobileMenuOpen = false"
            >Parking Lots</RouterLink>
            
            <h4 class="text-sm font-bold text-yellow-300 px-3 pt-3">— Security & Management —</h4>
            
            <RouterLink to="/admin/cctv" class="block px-3 py-2 text-sm text-yellow-300 hover:bg-white/10" @click="isMobileMenuOpen = false">CCTV Live Surveillance</RouterLink>
            <RouterLink to="/admin/analytics" class="block px-3 py-2 text-sm text-yellow-100 hover:bg-white/10" @click="isMobileMenuOpen = false">Analytics & Reports</RouterLink>
            <RouterLink to="/newcalender" class="block px-3 py-2 text-sm text-yellow-100 hover:bg-white/10" @click="isMobileMenuOpen = false">View Calendar</RouterLink>
            <RouterLink to="/admin/private-parking" class="block px-3 py-2 text-sm text-yellow-100 hover:bg-white/10" @click="isMobileMenuOpen = false">Private Parking</RouterLink>
            <RouterLink to="/admin/scan-ticket" class="block px-3 py-2 text-sm text-yellow-100 hover:bg-white/10" @click="isMobileMenuOpen = false">Scan Ticket</RouterLink>
            <RouterLink to="/admin/all-tickets" class="block px-3 py-2 text-sm text-yellow-100 hover:bg-white/10" @click="isMobileMenuOpen = false">All Tickets</RouterLink>

        </div>
      </transition>
    </header>
      <main class="flex-1 pt-20 pb-4">
        <!-- FULL WIDTH CONTENT (banners, maps, analytics, charts) -->
        <div class="w-full">
          <RouterView />
        </div>
      </main>

    <footer class="bg-red-900 text-orange-100 py-6 text-center border-t-4 border-yellow-500">
      <p class="font-serif italic">“Satyam Shivam Sundaram”</p>
      <p class="text-xs mt-2 opacity-70">&copy; 2024 Mandir Admin. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, RouterView, RouterLink } from 'vue-router'
import feather from 'feather-icons'

const router = useRouter()

const username = ref('Admin')

const isMobileMenuOpen = ref(false)

const logout = () => {
  localStorage.removeItem('devdham_user')
  router.push('/login')
}

onMounted(() => {
  if (feather) {
    feather.replace()
  }
})

</script>

<style scoped>
/* Style for active link matching the requested visual style */
.router-link-active {
  color: #fbbf24; /* Amber-400 */
  font-weight: 700;
  border-bottom: 2px solid #fbbf24;
}

/* Ensure the RouterLink itself is the target for active class */
.nav-item {
  position: relative;
  padding: 0 0 4px 0; /* Add bottom padding for the border */
}

/* Optional: Subtle glow for the icon */
.glow-text {
  text-shadow: 0 0 6px rgba(255, 153, 0, 0.8);
}
</style>