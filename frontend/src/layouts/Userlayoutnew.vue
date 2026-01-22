<template>
  <div class="flex flex-col min-h-screen bg-[#fffbf2] font-sans">
    <header class="fixed top-0 w-full z-50 bg-gradient-to-r from-orange-600 via-red-700 to-red-800 shadow-lg text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
          
          <div class="flex items-center gap-3">
             <div class="bg-white/10 p-2 rounded-full border border-yellow-400/50 backdrop-blur-sm">
                <span class="text-3xl">🛕</span>
             </div>
             <div class="flex flex-col">
                <h1 class="text-xl font-bold font-serif tracking-wide text-yellow-50">
                  DevDhamPath
                </h1>
                <span class="text-xs text-yellow-200 uppercase tracking-widest">Darshan & Seva</span>
             </div>
          </div>

          <nav class="hidden md:flex space-x-8">
            <RouterLink 
              to="/user/dashboard" 
              class="nav-item text-sm font-medium text-orange-100 hover:text-white transition-colors"
            >
              <span>Dashboard</span>
              <span class="block max-w-0 group-hover:max-w-full transition-all duration-500 h-0.5 bg-yellow-400"></span>
            </RouterLink>

            <RouterLink 
              to="/user/newcalender" 
              class="nav-item text-sm font-medium text-orange-100 hover:text-white transition-colors"
            >
              Calendar
            </RouterLink>
            
            <RouterLink 
              to="/user/editnew" 
              class="nav-item text-sm font-medium text-orange-100 hover:text-white transition-colors"
            >
              Profile
            </RouterLink>
          </nav>

          <div class="flex items-center gap-4">
            <div class="hidden md:flex flex-col items-end">
              <span class="text-sm font-bold text-yellow-100">{{ user.name }}</span>
              <span class="text-xs text-orange-200">Devotee</span>
            </div>
            <button
              @click="handleLogout"
              class="bg-red-900/50 hover:bg-red-900 border border-red-400 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 flex items-center gap-2 shadow-sm"
            >
              <span>Logout</span>
              <i data-feather="log-out" class="w-4 h-4"></i>
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="flex-1 pt-20">
      <slot />
    </main>

    <footer class="bg-red-900 text-orange-100 py-6 text-center border-t-4 border-yellow-500">
        <p class="font-serif italic">“Satyam Shivam Sundaram”</p>
        <p class="text-xs mt-2 opacity-70">&copy; 2024 DevDhamPath. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import feather from 'feather-icons'
import { useUserStore } from '@/stores/user'

const user = useUserStore()

onMounted(() => {
  feather.replace()
})

function handleLogout() {
  user.logout()
  window.location.href = '/login'
}
</script>

<style scoped>
.router-link-active {
  color: #fbbf24; /* Amber-400 */
  font-weight: 700;
  border-bottom: 2px solid #fbbf24;
}
</style>