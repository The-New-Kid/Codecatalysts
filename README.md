# 🛕 DevDhamPath – Smart Temple & Pilgrimage Management System

## 🧠 Overview
**DevDhamPath** is an **IoT and AI-based integrated system** designed to manage crowds, parking, and pilgrim experiences at large temples and pilgrimage sites efficiently and safely.  
The system enables **intelligent time-slot allocation, QR-based entry/exit, Aadhaar verification**, and **real-time monitoring** using IoT sensors, camera feeds, and aerial drones.

Developed for **Smart India Hackathon 2025** under the theme *Heritage & Culture*, this project aims to prevent overcrowding, enhance safety, and deliver a seamless pilgrim journey — from booking to darshan to exit.

---

## ⚙️ Key Features

### 👨‍💼 Admin Module
- Create and manage parking/darshan slots.
- Monitor live entry and exit using QR-based access.
- View real-time crowd heatmaps generated from camera and drone feeds.
- Access environmental and occupancy data from IoT sensors.
- Approve and verify pilgrims and staff.
- Generate analytics reports on visitor flow and slot usage.

### 🧑‍💻 User (Pilgrim) Module
- Register and log in securely.
- Book **darshan or parking slots** (up to 6 per user).
- Aadhaar verification for each accompanying devotee.
- OTP verification via **Twilio API**.
- Generate QR codes for **entry and exit gates**.
- Receive live updates on crowd density, slot timings, and environmental alerts.
- Access temple maps, navigation aids, and SOS emergency support.

---

## 🔐 Verification Flow
1. The user enters **Aadhaar number(s)** for verification.  
2. The system verifies details using artificial Aadhaar data stored in the database.  
3. An OTP is sent to the user’s registered mobile number via **Twilio API**.  
4. On successful verification, the booking is confirmed, and a **QR code** is generated for entry/exit.  
5. On-site QR scans control access:  
   - **1st Scan:** Entry Granted ✅  
   - **2nd Scan:** Exit Granted 🚪  
   - **Further Scans:** QR Expired ❌  

---

## 🧩 System Workflow
1. **Admin** defines available darshan and parking slots.  
2. **User** registers → Aadhaar verified → books slot.  
3. **QR code** generated for each valid booking.  
4. IoT sensors and cameras continuously capture cro

## Future scope
The DevDhamPath platform aims to become a comprehensive smart pilgrimage ecosystem by integrating advanced AI, IoT, and real-time analytics.
Planned developments include:

### 🧠 Artificial Intelligence & Machine Learning
Crowd surge prediction using Gradient Boosting, XGBoost, and LSTM.
Abnormal behavior detection in dense crowds using YOLOv8 + Soft-NMS.
Predictive analytics dashboard for temple authorities to prevent congestion.
Automated emergency detection using CCTV and drone feeds.

### 📡 IoT & Smart Infrastructure
Real-time monitoring through IR, RFID, and DHT sensors for crowd, temperature, and air quality.
Integration with existing CCTV systems and police control rooms.
Deployment of smart barricades and SOS alert systems for emergency handling.
IoT gateways to unify temple and parking monitoring data.

### 🌐 Computer Vision & Heatmaps
Camera-based heatmaps for crowd density estimation.
Drone surveillance integration for large temple grounds.
Use of computer vision models for real-time crowd counting and visual analytics.
Heatmap visualization dashboard for admins to track crowd distribution dynamically.

### 💻 Software & Experience
Full migration to a Vue.js frontend with REST APIs.
Development of a Flutter mobile app for pilgrims with QR, maps, and booking.
Admin dashboard with live analytics, charts, and AI alerts.
Offline-first mode for low-connectivity areas.

### 🕹️ Smart Features
AR-guided temple tours for interactive navigation.
UPI-based smart donations and transparent transaction logs.
Multilingual support (Hindi, Gujarati, English).
Priority lanes for elderly and differently-abled devotees.
Emergency SOS integration with GPS tracking and notifications.

### 🧭 Integrations & Expansion
Partnership with Gujarat Tourism and Temple Boards for unified bookings.
Multi-location support for Somnath, Dwarka, Ambaji, and Pavagadh.
Expansion into smart parking and mobility systems (auto slot assignment, EV charging).
Cloud-based hosting and scalability for festival surges.
Integration with Google Maps and weather APIs for crowd-aware routing.
