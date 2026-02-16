# 🌌 The Cosmic Odometer

> **"You think you are sitting still. Physics disagrees."**

---

## 📖 Introduction

**The Cosmic Odometer** is a Python CLI tool that calculates and visualizes your *actual physical velocity through the universe in real-time*. Even if you're sitting still in your office chair, you're traveling at tremendous speeds due to Earth's rotation, Earth's orbit around the Sun, and our Solar System’s orbit around the Milky Way galaxy.

This tool combines geolocation data with astrophysical constants to render a live telemetry dashboard of your journey through space.

---


---

## 🔭 How It Works (The Science)

Most people perceive speed relative to the ground. The Cosmic Odometer calculates your motion relative to three cosmic frames of reference:

### 1️⃣ Earth's Rotation (`V_rot`)

- Earth spins at approximately **1,670 km/h (0.46 km/s)** at the equator.
- Your rotational speed depends on your **latitude (ϕ)**.
- As you move closer to the poles, the effective rotational radius decreases.



- Someone in **Kenya** moves faster than someone in **Norway** due to latitude differences.

---

### 2️⃣ Earth's Orbit Around the Sun (`V_orb`)

- Earth travels around the Sun at approximately:
  - **29.78 km/s**
  - **107,200 km/h**

---

### 3️⃣ Galactic Orbit (`V_gal`)

- Our Solar System orbits the center of the Milky Way galaxy at approximately:
  - **220 km/s**
  - **792,000 km/h**

---

### 🧮 Total Velocity Calculation

The tool sums these velocity components to compute:

- Your **instantaneous cosmic velocity**
- The **total distance traveled** since starting the script

---

## 🚀 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Wasserpuncher/cosmic-odometer.git
cd cosmic-odometer
pip install rich geopy



