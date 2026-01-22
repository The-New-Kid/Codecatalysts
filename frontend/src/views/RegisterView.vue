<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-400 via-amber-300 to-yellow-100 relative overflow-hidden px-4"
  >
    <!-- Decorative saffron aura -->
    <div
      class="absolute w-60 sm:w-72 h-60 sm:h-72 bg-orange-500 rounded-full opacity-20 -top-20 -left-20 animate-float"
    ></div>
    <div
      class="absolute w-80 sm:w-96 h-80 sm:h-96 bg-amber-400 rounded-full opacity-20 -bottom-32 -right-32 animate-float"
    ></div>

    <div
      class="w-full max-w-md sm:max-w-lg p-6 sm:p-10 bg-white/95 rounded-3xl shadow-2xl border border-orange-200 backdrop-blur-sm"
      data-aos="fade-up"
    >
      <h1 class="text-3xl font-extrabold text-center mb-8 text-orange-700 glow-text">
        🛕 Create New Account
      </h1>

      <!-- Signup Form -->
      <form @submit.prevent="handleRegister" class="space-y-5 sm:space-y-6">
        <input
          v-model="form.name"
          type="text"
          pattern="^[A-Za-z]+(?: [A-Za-z]+)*$"
          placeholder="Full Name"
          required
          class="w-full px-5 py-3 rounded-xl border border-gray-300 shadow-inner focus:ring-2 focus:ring-orange-300 transition"
        />

        <input
          v-model="form.email"
          type="email"
          placeholder="Email Address"
          required
          class="w-full px-5 py-3 rounded-xl border border-gray-300 shadow-inner focus:ring-2 focus:ring-orange-300 transition"
        />
        <input
          v-model="form.mobile_no"
          type="tel"
          placeholder="Mobile Number"
          required
          maxlength="10"
          pattern="^[0-9]{10}$"
          class="w-full px-5 py-3 rounded-xl border border-gray-300 shadow-inner focus:ring-2 focus:ring-orange-300 transition"
        />

      <div class="relative">
        <input
          v-model="form.password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Enter Password"
          required
          minlength="6"
          pattern="^(?=.*[0-9]).{6,}$"
          @invalid="($event.target.setCustomValidity('Password must be at least 6 characters and include 1 number.'))"
          @input="($event.target.setCustomValidity(''))"
          class="w-full px-5 py-3 pr-10 rounded-xl border border-gray-300 shadow-inner focus:ring-2 focus:ring-orange-300 transition"
        />

        <button
          type="button"
          class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-orange-600"
          @click="togglePassword"
        >
          <i data-feather="eye"></i>
        </button>
      </div>

        <input
          v-model="form.pincode"
          type="number"
          placeholder="Pincode"
          pattern="^[0-9]{6}$"
          required
          class="w-full px-5 py-3 rounded-xl border border-gray-300 shadow-inner focus:ring-2 focus:ring-orange-300 transition"
        />

        <textarea
          v-model="form.address"
          rows="2"
          placeholder="Address"
          required
          class="w-full px-5 py-3 rounded-xl border border-gray-300 shadow-inner focus:ring-2 focus:ring-orange-300 transition"
        ></textarea>

        <button
          type="submit"
          class="w-full py-3 bg-gradient-to-r from-orange-500 to-amber-400 text-white font-bold rounded-xl shadow-lg btn-gradient transition-all duration-300"
        >
          Sign Up
        </button>
      </form>

      <div class="mt-6 text-center flex flex-col gap-3">
        <router-link
          to="/"
          class="inline-block px-6 py-2 border border-gray-300 rounded-full hover:bg-gray-100 transition"
          >← Back to Home</router-link
        >
        <p class="text-gray-600">
          Already have an account?
          <router-link
            to="/login"
            class="text-orange-600 font-semibold hover:text-orange-800 transition"
            >Login Here</router-link
          >
        </p>
      </div>
    </div>
    <!-- Toast Notification -->
    <div
      v-if="showToast"
      class="fixed top-6 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-6 py-3 rounded-full shadow-lg animate-fade"
    >
      {{ toastMessage }} 

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import AOS from "aos";
import "aos/dist/aos.css";
import feather from "feather-icons";
const showToast = ref(false);
const toastMessage = ref("");
import { useRouter } from 'vue-router'

const router = useRouter();


const form = ref({
  name: "",
  email: "",
  password: "",
  pincode: "",
  address: "",
  mobile_no: "",
});

const showPassword = ref(false);
const togglePassword = () => {
  showPassword.value = !showPassword.value;
  feather.replace();
};

onMounted(() => {
  AOS.init({ duration: 800, easing: "ease-in-out", once: true });
  feather.replace();
});

const handleRegister = async () => {
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/register`, form.value);

    toastMessage.value = response.data.message || "Registration successful!";
    showToast.value = true;

    // Hide toast after 2 seconds and redirect
    setTimeout(() => {
      showToast.value = false;
      // Redirect to login page
      // Or, if using Vue Router:
      router.push("/login");
    }, 1500);

  } catch (error) {
    alert(error.response?.data?.message || "Registration failed");
  }
};

</script>

<style scoped>
@keyframes floatUp {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
.animate-float {
  animation: floatUp 3s ease-in-out infinite;
}
.btn-gradient:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
}
.glow-text {
  text-shadow: 0 0 6px rgba(255, 153, 0, 0.8);
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(10px); }
  10% { opacity: 1; transform: translateY(0); }
  90% { opacity: 1; }
  100% { opacity: 0; transform: translateY(10px); }
}

.animate-fade {
  animation: fadeInOut 2s ease-in-out forwards;
}


</style>
