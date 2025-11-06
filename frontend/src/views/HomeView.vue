<template>
  <div class="text-gray-900 bg-gradient-to-br from-orange-50 via-yellow-50 to-orange-100">

    <!-- Navbar -->
    <nav class="bg-gradient-to-r from-orange-700 via-amber-500 to-yellow-500 shadow-lg fixed w-full z-50">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 flex justify-between items-center h-16 text-white font-medium">
        <RouterLink to="/" class="text-2xl font-extrabold glow-text tracking-wide">🛕 DevDhamPath</RouterLink>
        <div class="hidden sm:flex space-x-6">
          <a href="#features" class="hover:text-yellow-200 transition">Features</a>
          <a href="#about" class="hover:text-yellow-200 transition">About</a>
          <a href="#testimonials" class="hover:text-yellow-200 transition">Testimonials</a>
          <a href="#contact" class="hover:text-yellow-200 transition">Contact</a>
        </div>
        <div class="flex space-x-4">
          <RouterLink to="/login" class="px-4 py-2 bg-white text-orange-600 font-semibold rounded-lg shadow hover:scale-105 transition">Login</RouterLink>
          <RouterLink to="/register" class="px-4 py-2 border-2 border-white text-white rounded-lg hover:bg-white hover:text-orange-600 transition">Register</RouterLink>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative h-screen pt-32 overflow-hidden">
      <div class="absolute inset-0">
        <img class="hero-slide fade-1" src="/images/somnath10.jpg" alt="Somnath Mandir" />
        <img class="hero-slide fade-2" src="/images/image.jpeg" alt="Temple Crowd" />
        <img class="hero-slide fade-3" src="/images/Dwarka.jpeg" alt="Dwarka Mandir" />
      </div>

      <div class="absolute inset-0 bg-black bg-opacity-50"></div>

      <div class="relative z-10 flex flex-col justify-center items-center h-full text-center px-6">
        <h1 class="text-6xl md:text-7xl font-extrabold text-white glow-text animate-fade-up">
          DevDhamPath
        </h1>
        <p class="text-2xl md:text-3xl text-white mt-6 animate-fade-up delay-200">
          Manage Darshan Slots, Parking, and Crowd Flow Seamlessly.
        </p>
        <div class="mt-10 flex gap-6 animate-fade-up delay-400">
          <RouterLink to="/login" class="px-8 py-4 bg-gradient-to-r from-yellow-400 to-orange-500 text-white font-bold rounded-full shadow-lg hover:shadow-xl hover:-translate-y-1 transition">
            User Login
          </RouterLink>
          <RouterLink to="/register" class="px-8 py-4 bg-white text-orange-600 font-bold rounded-full shadow-lg hover:-translate-y-1 transition">
            Register Now
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section id="features" class="py-24">
      <div class="max-w-7xl mx-auto px-6 lg:px-8">
        <h2 class="text-4xl font-extrabold text-center mb-16 text-orange-700 glow-text" data-aos="fade">✨ Key Features</h2>
        <div class="grid md:grid-cols-3 sm:grid-cols-1 gap-10">
          <div class="bg-gradient-to-br from-orange-500 via-amber-400 to-yellow-300 text-white p-8 rounded-3xl shadow-xl hover:-translate-y-2 transition" data-aos="fade-up" data-aos-delay="100">
            <h3 class="text-2xl font-bold mb-3">📅 Smart Darshan Slots</h3>
            <p class="text-lg">Book temple darshan slots easily with automatic crowd control & instant QR generation.</p>
          </div>

          <div class="bg-gradient-to-br from-yellow-400 via-orange-400 to-amber-500 text-white p-8 rounded-3xl shadow-xl hover:-translate-y-2 transition" data-aos="fade-up" data-aos-delay="200">
            <h3 class="text-2xl font-bold mb-3">🅿️ Parking Integration</h3>
            <p class="text-lg">Reserve nearest available parking automatically. Prevent congestion during rush hours.</p>
          </div>

          <div class="bg-gradient-to-br from-orange-600 via-amber-400 to-yellow-400 text-white p-8 rounded-3xl shadow-xl hover:-translate-y-2 transition" data-aos="fade-up" data-aos-delay="300">
            <h3 class="text-2xl font-bold mb-3">📊 Admin Dashboard</h3>
            <p class="text-lg">Monitor slots, view bookings, track density, and generate reports in real-time.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- About -->
    <section id="about" class="py-24 bg-white" data-aos="fade-up">
      <div class="max-w-5xl mx-auto text-center px-6">
        <h2 class="text-4xl font-extrabold mb-6 text-orange-700 glow-text">About DevDhamPath</h2>
        <p class="text-lg text-gray-700 mb-8 leading-relaxed">
          DevDhamPath ensures a smooth temple experience through intelligent slot booking, crowd flow management, and integrated parking. Blending technology and devotion for a sacred, seamless journey.
        </p>
        <RouterLink to="/register" class="px-8 py-3 bg-gradient-to-r from-orange-500 via-amber-400 to-yellow-400 text-white rounded-full font-semibold hover:shadow-xl hover:-translate-y-1 transition">
          Get Started
        </RouterLink>
      </div>
    </section>

    <!-- Testimonials -->
    <section id="testimonials" class="py-24 bg-gradient-to-br from-orange-50 via-yellow-50 to-amber-50">
      <div class="max-w-7xl mx-auto text-center px-6">
        <h2 class="text-4xl font-extrabold mb-16 text-orange-700 glow-text" data-aos="fade-up">What Devotees Say 🙏</h2>
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-10">
          <div class="bg-white p-8 rounded-2xl shadow-lg hover:-translate-y-2 transition" data-aos="fade-up" data-aos-delay="100">
            <p class="text-gray-700 mb-4">“Slot booking and parking management made my visit completely hassle-free!”</p>
            <h4 class="font-bold text-orange-700">– Rajesh Kumar</h4>
          </div>
          <div class="bg-white p-8 rounded-2xl shadow-lg hover:-translate-y-2 transition" data-aos="fade-up" data-aos-delay="200">
            <p class="text-gray-700 mb-4">“The live dashboard helped maintain total safety during big events.”</p>
            <h4 class="font-bold text-orange-700">– Meena Sharma</h4>
          </div>
          <div class="bg-white p-8 rounded-2xl shadow-lg hover:-translate-y-2 transition" data-aos="fade-up" data-aos-delay="300">
            <p class="text-gray-700 mb-4">“A divine union of tradition and technology. Perfectly executed.”</p>
            <h4 class="font-bold text-orange-700">– Arjun Patel</h4>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gradient-to-r from-orange-700 via-amber-500 to-yellow-500 py-10 text-white text-center">
      <p class="mb-3">&copy; 2025 DevDhamPath. All Rights Reserved.</p>
      <div class="flex justify-center gap-6 text-sm">
        <a href="#" class="hover:text-yellow-200">Privacy Policy</a>
        <a href="#" class="hover:text-yellow-200">Terms of Service</a>
        <a href="#" class="hover:text-yellow-200">Contact</a>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, nextTick } from 'vue'

onMounted(() => {
  nextTick(() => {
    if (window.AOS) {
      // reset scroll so AOS can re-trigger animations
      window.scrollTo(0, 0)
      window.AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: false, // 🔥 allow animations on scroll again
        mirror: false, // do not animate out on scroll up
        offset: 120 // start a bit before element enters viewport
      })
      // force refresh in case Vue rendered late
      setTimeout(() => window.AOS.refreshHard(), 500)
    }
  })
})
</script>



