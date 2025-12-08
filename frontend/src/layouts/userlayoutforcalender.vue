<template>
  <div class="flex flex-col min-h-screen bg-[#fffbf2] font-sans overflow-x-hidden">

    <!-- ✅ HEADER -->
    <header class="fixed top-0 w-full z-50 bg-gradient-to-r from-orange-600 via-red-700 to-red-800 shadow-lg text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-20 min-w-0">

          <!-- ✅ BACK BUTTON + LOGO -->
          <div class="flex items-center gap-3 min-w-0">

            <!-- ✅ BACK BUTTON -->
            <button 
              v-if="showBackButton"
              @click="goBack"
              class="flex items-center justify-center w-9 h-9 rounded-full bg-white/10 border border-yellow-400/50 hover:bg-white/20 transition md:hidden"
              aria-label="Go Back"
            >

              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-100" fill="none"
                viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round"
                  stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
            </button>

            <!-- ✅ TEMPLE LOGO -->
            <div class="bg-white/10 p-2 rounded-full border border-yellow-400/50 backdrop-blur-sm flex-shrink-0">
              <span class="text-3xl">🛕</span>
            </div>

            <!-- ✅ DEV DHAMPATH TEXT -->
            <div class="flex flex-col min-w-0">
              <h1 class="text-xl font-bold font-serif tracking-wide text-yellow-50 truncate">
                DevDhamPath
              </h1>
              <span class="text-xs text-yellow-200 uppercase tracking-widest">
                Darshan & Seva
              </span>
            </div>

          </div>


          <!-- ✅ DESKTOP NAV -->
          <nav class="hidden md:flex space-x-8">
            <RouterLink to="/user/dashboard" class="nav-item">Dashboard</RouterLink>
            <RouterLink to="/user/newcalender" class="nav-item">Calendar</RouterLink>
            <RouterLink to="/user/editnew" class="nav-item">Profile</RouterLink>
          </nav>

          <!-- ✅ DESKTOP USER -->
          <div class="hidden md:flex items-center gap-4">
            <div class="flex flex-col items-end">
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

          <!-- ✅ MOBILE MENU BUTTON -->
          <button class="md:hidden flex-shrink-0 ml-2" @click="mobileOpen = !mobileOpen">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none"
              viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round"
                stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>

        </div>

        <!-- ✅ MOBILE MENU -->
        <transition name="slide">
          <div v-if="mobileOpen" class="md:hidden pb-4 space-y-3">

            <RouterLink @click="closeMobile" to="/user/dashboard" class="mobile-link">
              Dashboard
            </RouterLink>

            <RouterLink @click="closeMobile" to="/user/newcalender" class="mobile-link">
              Calendar
            </RouterLink>

            <RouterLink @click="closeMobile" to="/user/editnew" class="mobile-link">
              Profile
            </RouterLink>

            <div class="border-t border-orange-400/30 pt-3 flex items-center justify-between">
              <div>
                <p class="text-sm font-bold text-yellow-100">{{ user.name }}</p>
                <p class="text-xs text-orange-200">Devotee</p>
              </div>
              <button
                @click="handleLogout"
                class="bg-red-900/60 px-3 py-1 rounded-lg text-sm"
              >
                Logout
              </button>
            </div>

          </div>
        </transition>
      </div>
    </header>

    <!-- ✅ PAGE CONTENT -->
    <main class="flex-1 pt-20">
      <router-view />
    </main>

    <!-- ✅ FOOTER -->
    <footer class="bg-red-900 text-orange-100 py-6 text-center border-t-4 border-yellow-500">
      <p class="font-serif italic">“Satyam Shivam Sundaram”</p>
      <p class="text-xs mt-2 opacity-70">
        &copy; 2024 DevDhamPath. All rights reserved.
      </p>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted,computed } from 'vue'
import feather from 'feather-icons'
import { useUserStore } from '@/stores/user'
import { useRouter, useRoute } from 'vue-router'

const user = useUserStore()
const router = useRouter()
const route = useRoute()

function goBack() {
  router.back()
}

const showBackButton = computed(() => {
  return route.path !== '/user/dashboard'
})


const mobileOpen = ref(false)

onMounted(() => {
  feather.replace()
})

function closeMobile() {
  mobileOpen.value = false
}

function handleLogout() {
  user.logout()
  mobileOpen.value = false
  router.push('/login')
}
</script>


<style scoped>
.router-link-active {
  color: #fbbf24;
  font-weight: 700;
  border-bottom: 2px solid #fbbf24;
}

/* ✅ NAV ITEMS */
.nav-item {
  font-size: 0.9rem;
  font-weight: 500;
  color: rgb(255 237 213);
  transition: color 0.3s ease;
}

.nav-item:hover {
  color: white;
}

/* ✅ MOBILE LINKS */
.mobile-link {
  display: block;
  padding: 0.6rem 0;
  font-size: 0.95rem;
  border-bottom: 1px solid rgba(251, 191, 36, 0.2);
}

/* ✅ MOBILE SLIDE */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

</style>