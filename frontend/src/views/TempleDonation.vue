<template>
    <div>
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
            
            <header class="text-center mb-10" data-aos="fade-down">
                <i data-feather="droplet" class="w-12 h-12 text-yellow-600 mx-auto mb-3"></i>
                <h1 class="text-4xl font-serif font-extrabold text-red-800">
                    Sacred Contribution (Dakshina)
                </h1>
                <p class="text-lg text-gray-600 mt-2">
                    Offer your generous donation and receive the blessings of Mahakal.
                </p>
            </header>
            
            <div class="bg-white rounded-xl shadow-2xl overflow-hidden border-t-8 border-red-700" data-aos="fade-up">
                <div class="p-6 md:p-10">
                    
                    <section class="mb-8">
                        <h3 class="text-xl font-bold text-red-700 mb-4 flex items-center">
                            <i data-feather="tag" class="w-5 h-5 mr-2"></i> Choose Seva Category
                        </h3>
                        <div class="grid grid-cols-2 gap-4">
                            <div 
                                v-for="cat in categories" 
                                :key="cat.value"
                                :class="[
                                    'p-4 rounded-xl text-center cursor-pointer transition duration-200 border-2 flex flex-col items-center justify-center', 
                                    donationCategory === cat.value 
                                        ? 'border-red-700 bg-red-100 text-red-800 shadow-md' // category-card-active
                                        : 'border-gray-200 bg-gray-50 text-gray-600 hover:border-red-400 hover:bg-red-50' // category-card
                                ]"
                                @click="donationCategory = cat.value"
                            >
                                <i :data-feather="cat.icon" class="w-6 h-6 mb-1" :class="{'text-red-800': donationCategory === cat.value}"></i>
                                <span class="text-sm font-semibold">{{ cat.name }}</span>
                            </div>
                        </div>
                    </section>

                    <hr class="my-8 border-gray-200">

                    <section class="mb-8">
                        <h3 class="text-xl font-bold text-red-700 mb-4 flex items-center">
                            <i data-feather="dollar-sign" class="w-5 h-5 mr-2"></i> Select Amount
                        </h3>
                        <div class="flex flex-wrap gap-3 mb-4">
                            <button
                                v-for="amount in suggestedAmounts"
                                :key="amount"
                                :class="[
                                    'px-4 py-2 font-semibold rounded-full border-2 transition duration-150',
                                    donationAmount === amount 
                                        ? 'border-red-700 bg-red-700 text-white shadow-lg' // amount-btn-active
                                        : 'border-orange-300 bg-orange-500 text-white hover:bg-orange-600' // amount-btn
                                ]"
                                @click="selectAmount(amount)"
                            >
                                ₹{{ amount }}
                            </button>
                        </div>

                        <div class="mt-4 flex items-center">
                            <span class="text-2xl font-bold text-gray-700 mr-2">₹</span>
                            <input
                                type="number"
                                v-model.number="donationAmount"
                                placeholder="Enter Custom Amount"
                                class="w-full p-3 border-2 border-orange-200 rounded-lg focus:border-orange-500 focus:ring-0 text-xl font-bold text-gray-900"
                                min="1"
                                @input="validateAmount"
                            />
                        </div>
                        <p v-if="donationAmountError" class="text-red-500 text-sm mt-2">{{ donationAmountError }}</p>

                    </section>

                    <hr class="my-8 border-gray-200">
                    
                    <section class="mb-10">
                        <h3 class="text-xl font-bold text-red-700 mb-4 flex items-center">
                            <i data-feather="user" class="w-5 h-5 mr-2"></i> Devotee Details (For Receipt & Sankalp)
                        </h3>
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Name</label>
                                <input type="text" v-model="devoteeDetails.name" 
                                    class="w-full p-3 border border-gray-300 rounded-lg focus:border-red-500 focus:ring-red-500 transition duration-150" disabled/>
                                <p class="text-xs text-gray-500 mt-1">Pre-filled from your profile.</p>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Email</label>
                                <input type="email" v-model="devoteeDetails.email" 
                                    class="w-full p-3 border border-gray-300 rounded-lg focus:border-red-500 focus:ring-red-500 transition duration-150"/>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Mobile Number</label>
                                <input type="tel" v-model="devoteeDetails.mobile" 
                                    class="w-full p-3 border border-gray-300 rounded-lg focus:border-red-500 focus:ring-red-500 transition duration-150"/>
                            </div>
                            <div class="pt-2">
                                <label class="flex items-center text-sm font-medium text-gray-700">
                                    <input type="checkbox" v-model="addSankalp" class="form-checkbox text-red-700 border-red-300 rounded mr-2 focus:ring-red-500">
                                    Include a **Sankalp** (Divine Vow/Prayer)
                                </label>
                                <textarea v-if="addSankalp" v-model="sankalpText" placeholder="Write your specific Sankalp or prayer intention..." 
                                    class="w-full p-3 border border-gray-300 rounded-lg focus:border-red-500 focus:ring-red-500 transition duration-150 mt-2 h-20"></textarea>
                                <p v-if="addSankalp" class="text-xs text-red-500 mt-1">
                                    *The temple priests will include this Sankalp during a relevant ritual.
                                </p>
                            </div>
                        </div>
                    </section>
                    
                    <button 
                        @click="processDonation"
                        :disabled="!isFormValid"
                        :class="{'w-full py-4 text-white font-bold rounded-xl text-xl shadow-lg transition duration-200': true, 'bg-red-700 hover:bg-red-800': isFormValid, 'bg-gray-400 cursor-not-allowed': !isFormValid}"
                    >
                        Offer Dakshina of ₹{{ donationAmount.toLocaleString('en-IN') }}
                    </button>
                    
                    <p class="text-center text-xs text-gray-500 mt-4">
                        All donations are tax-exemptible under **Section 80G** as per temple trust rules (Please verify with your receipt).
                    </p>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import AOS from 'aos'
import 'aos/dist/aos.css'
import { useUserStore } from '@/stores/user'
import feather from 'feather-icons'
import { useRouter } from 'vue-router'
import axios from 'axios'; // Import axios for API calls (e.g., payment order creation)

const userStore = useUserStore()
const router = useRouter()

// --- State ---
const donationCategory = ref('general');
const donationAmount = ref(501);
const donationAmountError = ref('');
const addSankalp = ref(false);
const sankalpText = ref('');

const suggestedAmounts = [101, 501, 1100, 2500, 5100];

const devoteeDetails = reactive({
    name: userStore.name || 'Bhakt',
    // Assume user store holds email, initialize to user's stored value
    email: userStore.email || '', 
    mobile: '',
});

const categories = [
    { name: 'Annakshetra', value: 'food', icon: 'coffee' },
    { name: 'Temple Maintenance', value: 'maintenance', icon: 'tool' },
    { name: 'Vastra Seva', value: 'clothes', icon: 'feather' },
    { name: 'General Fund', value: 'general', icon: 'globe' },
];

// --- Computed Properties ---
const isFormValid = computed(() => {
    // Basic validation
    if (donationAmount.value === 0 || donationAmount.value < 1 || donationAmountError.value) {
        return false;
    }
    // Basic presence validation for required fields
    // You might want to add better email/mobile validation here
    if (!devoteeDetails.name || !devoteeDetails.email || !devoteeDetails.mobile) {
        return false;
    }
    return true;
});

// --- Methods ---
const selectAmount = (amount) => {
    donationAmount.value = amount;
    donationAmountError.value = '';
};

const validateAmount = () => {
    if (donationAmount.value === null || donationAmount.value < 1) {
        donationAmountError.value = 'Minimum donation amount is ₹1.';
    } else {
        donationAmountError.value = '';
    }
};

const processDonation = async () => {
    if (!isFormValid.value) {
        alert("Please ensure all required fields are filled and the amount is valid.");
        return;
    }

    const donationData = {
        user_id: userStore.id,
        amount: donationAmount.value,
        category: donationCategory.value,
        details: devoteeDetails,
        sankalp: addSankalp.value ? sankalpText.value : null,
        timestamp: new Date().toISOString(),
    };

    // 🚨 IMPLEMENTATION STEP: RAZORPAY/PAYMENT GATEWAY INTEGRATION
    
    // --- TEMPORARY SIMULATION ---
    console.log('Donation Data Sent to Backend (Simulated):', donationData);
    
    // Simulate API call success
    alert(`Thank you for your generous Dakshina of ₹${donationAmount.value.toLocaleString('en-IN')}! Your offering for ${donationCategory.value} is logged. Redirecting...`);
    
    // Redirect to a success page or back to the dashboard
    router.push('/'); 
};

// --- Lifecycle Hook ---
onMounted(() => {
    feather.replace();
    AOS.init({ duration: 800, once: true });
});
</script>

<style scoped>
/*
    NOTE: All @apply directives were removed from the <style> block
    and applied directly to the HTML template using standard Tailwind utility classes.
    This ensures compatibility and avoids the PostCSS processing error in scoped styles.
*/

.category-card-active i {
    color: #b91c1c; /* Deep red for active icon */
}
</style>