<template>
  <div class="flex min-h-screen">
    <!-- 🌺 Sidebar -->
    <aside
      class="sidebar-gradient w-64 text-white fixed h-full shadow-2xl flex flex-col justify-between"
    >
      <div>
        <!-- Logo / App Name -->
        <div
          class="flex items-center gap-3 px-6 py-5 border-b border-white/20"
        >
          <span class="text-3xl">🛕</span>
          <h1 class="text-xl font-bold leading-tight">
            DevDhamPath
            <br />
            <span class="text-sm font-medium opacity-90">
              Welcome, {{ user.name }}
            </span>
          </h1>
        </div>

        <!-- Nav Links -->
        <nav class="mt-6 space-y-2">
          <RouterLink
            to="/user/dashboard"
            class="sidebar-link flex items-center gap-3 px-6 py-3 hover:pl-8"
          >
            <i data-feather="home"></i> <span>Dashboard</span>
          </RouterLink>

          <RouterLink to="/calander" class="flex items-center px-5 py-3 hover:bg-white/20 rounded-lg">
            <i data-feather="calendar" class="mr-3"></i>
            <span>View Calendar</span>
          </RouterLink>

          <RouterLink to="/book-darshan" class="sidebar-link flex items-center gap-3 px-6 py-3 hover:pl-8">
            <i data-feather="calendar"></i> <span>Book Darshan</span>
          </RouterLink>

          <a href="#" class="sidebar-link flex items-center gap-3 px-6 py-3 hover:pl-8">
            <i data-feather="file-text"></i> <span>Summary</span>
          </a>
          
          <RouterLink
            to="/user/edit-profile"
            class="sidebar-link flex items-center gap-3 px-6 py-3 hover:pl-8">
            <i data-feather="user"></i> <span>Edit Profile</span>
          </RouterLink>


        <button
          @click="handleLogout"
          class="sidebar-link flex items-center gap-3 px-6 py-3 hover:pl-8"
        >
           <i data-feather="log-out"></i> <span>Logout</span>
        </button>

        </nav>
      </div>

      <div class="px-6 py-5 border-t border-white/20 text-sm italic opacity-90">
        <p>“May your Darshan bring peace and blessings.” 🌼</p>
      </div>
    </aside>

    <!-- 🌼 Main Content -->
    <main class="flex-1 ml-64 px-8 py-10">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import feather from 'feather-icons'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { useUserStore } from '@/stores/user'

const user = useUserStore()

onMounted(() => {
  feather.replace()
  AOS.init({ duration: 800, easing: 'ease-in-out', once: true })
})
function handleLogout() {
  user.logout()
  window.location.href = '/login'
}
</script>

<style scoped>
.sidebar-gradient {
  background: linear-gradient(180deg, #fbbf24 0%, #e879f9 100%);
}
.sidebar-link {
  transition: all 0.3s ease;
}
.sidebar-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateX(4px);
}
.active-link {
  background-color: rgba(255, 255, 255, 0.3);
  border-left: 4px solid white;
}
</style>
