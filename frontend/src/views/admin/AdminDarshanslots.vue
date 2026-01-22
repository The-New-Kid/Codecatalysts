<template>
  <AdminLayout>

<!-- HEADER -->
<div class="relative w-screen left-1/2 right-1/2 -mx-[50vw] h-[300px] sm:h-[380px] overflow-hidden shadow-2xl">
  <div class="absolute inset-0">
    <img 
      src="/images/Somnath4.jpeg"
      alt="Admin Slot Banner"
      class="w-full h-full object-cover object-center"
    />
    <div class="absolute inset-0 bg-gradient-to-t from-red-900/80 via-red-900/40 to-black/30"></div>
  </div>

  <div class="relative z-10 flex flex-col items-center justify-center h-full text-center px-4">
    <h2 class="text-4xl md:text-5xl font-serif font-bold text-yellow-100 drop-shadow-lg">
      🕉️ Manage Darshan Slots
    </h2>
    <p class="text-lg md:text-xl text-yellow-200 font-light drop-shadow-md mt-2">
      Create, update, and organize divine darshan timings.
    </p>
  </div>
</div>


    <!-- BODY SECTION -->
    <div class="min-h-screen flex justify-center items-start bg-[#fffaf0] py-12">
      <div class="w-full max-w-4xl bg-white rounded-3xl shadow-2xl p-6 sm:p-10 border-t-8 border-red-700">

        <!-- TITLE -->
        <h3 class="text-3xl font-serif font-bold text-center mb-10 text-red-800">
          Slot Management
        </h3>

        <!-- ADD SLOT FORM -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">

          <!-- Start -->
          <div>
            <label class="block font-semibold mb-1 text-gray-700">Start Time</label>
            <input
              type="time"
              v-model="form.start_time"
              class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
            />
          </div>

          <!-- End -->
          <div>
            <label class="block font-semibold mb-1 text-gray-700">End Time</label>
            <input
              type="time"
              v-model="form.end_time"
              class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
            />
          </div>

          <!-- Max Visitors -->
          <div>
            <label class="block font-semibold mb-1 text-gray-700">Max Visitors</label>
            <input
              type="number"
              v-model="form.max_visitors"
              class="w-full p-3 border-2 border-gray-300 rounded-xl focus:border-red-700 focus:ring-2 focus:ring-red-200 transition shadow-sm"
            />
          </div>
        </div>

        <!-- ADD BUTTON -->
        <button
          @click="addSlot"
          class="w-full py-3 rounded-xl bg-gradient-to-r from-red-700 to-red-900 text-white font-bold text-lg shadow-xl hover:shadow-2xl hover:from-red-800 hover:to-red-900 transition transform hover:scale-[1.02] mb-10"
        >
          ➕ Add Slot
        </button>

        <!-- SLOT LIST TABLE -->
        <h3 class="text-2xl font-serif font-bold mb-6 text-red-800 text-center">
          Existing Slots
        </h3>

        <div class="overflow-x-auto">
          <table class="w-full border border-red-200 rounded-xl overflow-hidden shadow-md">
            <thead class="bg-red-700 text-white">
              <tr>
                <th class="p-3 text-left">Start</th>
                <th class="p-3 text-left">End</th>
                <th class="p-3 text-left">Max Visitors</th>
                <th class="p-3 text-center">Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="slot in slots"
                :key="slot.id"
                class="border-b hover:bg-red-50 transition"
              >
                <td class="p-3">
                  <input 
                    v-model="slot.start_time"
                    class="border border-gray-300 p-2 rounded-lg w-full"
                    type="time"
                  />
                </td>

                <td class="p-3">
                  <input 
                    v-model="slot.end_time"
                    class="border border-gray-300 p-2 rounded-lg w-full"
                    type="time"
                  />
                </td>

                <td class="p-3">
                  <input 
                    v-model="slot.max_visitors"
                    type="number"
                    class="border border-gray-300 p-2 rounded-lg w-full"
                  />
                </td>

                <td class="p-3 flex gap-3 justify-center">

                  <!-- Update -->
                  <button
                    @click="updateSlot(slot)"
                    class="bg-green-600 text-white px-4 py-2 rounded-xl shadow hover:bg-green-700 transition"
                  >
                    ✔ Update
                  </button>

                  <!-- Delete -->
                  <button
                    @click="deleteSlot(slot.id)"
                    class="bg-red-700 text-white px-4 py-2 rounded-xl shadow hover:bg-red-800 transition"
                  >
                    ✖ Delete
                  </button>

                </td>
              </tr>
            </tbody>

          </table>
        </div>

      </div>
    </div>

  </AdminLayout>
</template>



<script>
import axios from "axios";

const BASE = "http://127.0.0.1:5000/api";

export default {
  data() {
    return {
      slots: [],
      form: {
        start_time: "",
        end_time: "",
        max_visitors: "",
        slot_type: "Darshan"
      }
    };
  },

  mounted() {
    this.fetchSlots();
  },

  methods: {
    async fetchSlots() {
      try {
        const res = await axios.get(`${BASE}/admin/darshan-slots`, {
          params: { type: "Darshan" }
        });
        this.slots = res.data;
      } catch (err) {
        console.error("Fetch slots failed:", err);
      }
    },

    async addSlot() {
      if (!this.form.start_time || !this.form.end_time || !this.form.max_visitors) {
        alert("All fields required");
        return;
      }

      try {
        await axios.post(`${BASE}/admin/darshan-slots`, this.form);
        this.fetchSlots();
        this.form.start_time = "";
        this.form.end_time = "";
        this.form.max_visitors = "";
      } catch (err) {
        console.error("Add slot failed:", err);
      }
    },

    async updateSlot(slot) {
      try {
        await axios.put(`${BASE}/admin/darshan-slots`, {
          id: slot.id,
          start_time: slot.start_time,
          end_time: slot.end_time,
          max_visitors: slot.max_visitors
        });
        this.fetchSlots();
      } catch (err) {
        console.error("Update slot failed:", err);
      }
    },

    async deleteSlot(id) {
      if (!confirm("Delete this slot?")) return;
      try {
        await axios.delete(`${BASE}/admin/darshan-slots`, {
          params: { id }
        });
        this.fetchSlots();
      } catch (err) {
        console.error("Delete slot failed:", err);
      }
    }
  }
};
</script>
