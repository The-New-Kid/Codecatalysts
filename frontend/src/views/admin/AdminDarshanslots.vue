<template>
  <div>

    <!-- Banner -->
    <div class="banner-container">
      <img src="/images/somnath2.jpeg" class="banner-image" />
      <div class="banner-overlay"></div>

      <div class="banner-text">
        <h1>🔱 Darshan Slot Management</h1>
        <p>Manage time slots for smooth and organized darshan.</p>
      </div>
    </div>

    <!-- Main Container -->
    <div class="main-wrapper">

      <!-- Add Slot Card -->
      <div class="card">

        <h2 class="card-title">Add New Slot</h2>

        <div class="form-row">
          <label>Start Time</label>
          <input v-model="form.start_time" type="time" class="input">
        </div>

        <div class="form-row">
          <label>End Time</label>
          <input v-model="form.end_time" type="time" class="input">
        </div>

        <div class="form-row">
          <label>Max Visitors</label>
          <input v-model="form.max_visitors" type="number" class="input">
        </div>

        <button class="btn-primary" @click="addSlot">Add Slot</button>
      </div>

      <!-- Slots List -->
      <div class="card">

        <h2 class="card-title">Existing Slots</h2>

        <table class="slot-table">
          <thead>
            <tr>
              <th>Start</th>
              <th>End</th>
              <th>Visitors</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="slot in slots" :key="slot.id">
              <td>
                <input type="time" v-model="slot.start_time" class="input small">
              </td>

              <td>
                <input type="time" v-model="slot.end_time" class="input small">
              </td>

              <td>
                <input type="number" v-model="slot.max_visitors" class="input small">
              </td>

              <td class="action-col">
                <button class="btn-green" @click="updateSlot(slot)">Update</button>
                <button class="btn-red" @click="deleteSlot(slot.id)">Delete</button>
              </td>
            </tr>
          </tbody>

        </table>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const BASE = "http://127.0.0.1:5000/api"
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
      const res = await axios.get(`${BASE}/admin/darshan-slots?type=Darshan`);
      this.slots = res.data;
    },

    async addSlot() {
      if (!this.form.start_time || !this.form.end_time || !this.form.max_visitors) {
        alert("All fields required");
        return;
      }

      await axios.post("/admin/darshan-slots", this.form);
      this.fetchSlots();

      this.form.start_time = "";
      this.form.end_time = "";
      this.form.max_visitors = "";
    },

    async updateSlot(slot) {
      await axios.put("/admin/darshan-slots", {
        id: slot.id,
        start_time: slot.start_time,
        end_time: slot.end_time,
        max_visitors: slot.max_visitors
      });

      this.fetchSlots();
    },

    async deleteSlot(id) {
      if (!confirm("Delete this slot?")) return;

      await axios.delete(`/admin/darshan-slots?id=${id}`);
      this.fetchSlots();
    }
  }
};
</script>

<style scoped>
/* Banner Section */
.banner-container {
  position: relative;
  height: 330px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  animation: slowZoom 20s linear infinite alternate;
}

.banner-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(127,0,0,0.9), rgba(127,0,0,0.6), rgba(0,0,0,0.4));
}

.banner-text {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  color: white;
  z-index: 3;
}

.banner-text h1 {
  font-size: 36px;
  font-family: serif;
  font-weight: bold;
  margin-bottom: 10px;
  text-shadow: 0 5px 10px rgba(0,0,0,0.4);
}

.banner-text p {
  font-size: 18px;
  color: #ffebc7;
}

/* Main Wrapper */
.main-wrapper {
  max-width: 900px;
  margin: -60px auto 60px;
  padding: 20px;
}

/* Cards */
.card {
  background: white;
  border-radius: 18px;
  padding: 25px;
  margin-bottom: 40px;
  border-top: 4px solid #e65a00;
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.card-title {
  font-size: 26px;
  font-weight: bold;
  color: #7f1d1d;
  margin-bottom: 20px;
  font-family: serif;
}

/* Form Rows */
.form-row {
  margin-bottom: 15px;
}

.form-row label {
  font-weight: 600;
  color: #7f1d1d;
}

.input {
  width: 100%;
  padding: 10px;
  border: 1px solid #f0a46a;
  border-radius: 8px;
  background: #fff8f0;
  font-size: 15px;
  outline: none;
  transition: 0.2s;
}

.input:focus {
  border-color: #e65a00;
  background: #fff3e6;
}

.input.small {
  width: 110px;
}

/* Buttons (theme-matched) */
.btn-primary {
  background: #7f1d1d;
  color: white;
  padding: 10px 22px;
  border-radius: 10px;
  font-weight: bold;
  font-size: 15px;
  border: none;
  cursor: pointer;
  transition: .2s;
}

.btn-primary:hover {
  background: #5f1111;
  transform: translateY(-2px);
}

.btn-green,
.btn-red {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px;
  color: white;
  transition: .2s;
}

.btn-green { background: #166534; }
.btn-red { background: #991b1b; }

.btn-green:hover { background: #0f3d20; transform: translateY(-2px); }
.btn-red:hover { background: #7a1111; transform: translateY(-2px); }

/* Table */
.slot-table {
  width: 100%;
  border-collapse: collapse;
}

.slot-table th {
  background: #fff4e6;
  padding: 12px;
  text-align: left;
  color: #7f1d1d;
  border-bottom: 2px solid #e0a56b;
  font-weight: bold;
  font-size: 15px;
}

.slot-table td {
  padding: 10px;
  border-bottom: 1px solid #f6e2c0;
}

.action-col {
  display: flex;
  gap: 10px;
}

/* Banner Zoom Animation */
@keyframes slowZoom {
  from { transform: scale(1); }
  to { transform: scale(1.1); }
}
</style>
