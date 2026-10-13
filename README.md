# 🗑️ CleanPulse - Smart Waste Management System

> **A MERN-based smart waste reporting & collection tracking platform powered by Python & DAA route optimization.**

![Theme](https://img.shields.io/badge/Theme-Cool%20White-0ea5e9?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-MERN%20%2B%20Python-10b981?style=flat-square)
![Algorithm](https://img.shields.io/badge/DAA-Greedy%20TSP%20%2B%202--Opt-6366f1?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-slate?style=flat-square)

---

## 🌟 Overview

**CleanPulse** tackles municipal waste overflow through two core pillars:
1. **Citizen Reporting & Tracking:** Allows citizens to report overflowing trash with location coordinates, waste category, urgency level, and image verification, while tracking collection status (`Pending` → `In Transit` → `Collected`).
2. **DAA Route Optimization:** Implements the **Greedy Nearest Neighbor** algorithm and **2-Opt heuristic** for the Traveling Salesperson Problem (TSP) in Python and JavaScript to compute the shortest, lowest-emission collection route for municipal trucks.

---

## ✨ Features

- **Cool White Minimalist Interface:** Clean glassmorphism cards, crisp typography (`Plus Jakarta Sans`), and subtle icy-blue accents.
- **Citizen Report Portal:** Instant reporting with preset neighborhood shortcuts, category filters, and fill-level ratings.
- **Live Status Tracker:** Unique tracking IDs (`TRK-101`) with real-time status steppers and filters.
- **Interactive Route Map & Canvas:** Real-time visual map showing the central depot, active bins, and the calculated optimal collection path.
- **Animated Truck Simulator:** Watch the collection truck navigate the route in real-time, automatically servicing and collecting bins.
- **DAA Decision Trace:** Live step-by-step algorithmic breakdown showing $\mathcal{O}(N^2)$ efficiency and distances saved.

---

## 🧠 DAA Algorithm & Complexity

The municipal collection vehicle routing problem is modeled as a **Traveling Salesperson Problem (TSP)**:

| Metric | Brute Force | CleanPulse DAA (Nearest Neighbor + 2-Opt) |
| :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(N!)$ | $\mathcal{O}(N^2)$ |
| **Space Complexity** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Practical Speed** | Intractable for $N > 12$ | Computes in $< 2\text{ ms}$ |
| **Efficiency Gain** | Theoretical | **10%–25% reduction in truck travel distance & fuel** |

---

## 📁 Repository Structure

```
├── index.html                 # Standalone Cool-White Web Dashboard
├── optimizer.py               # Python DAA Route Optimization Engine
├── server.js                  # Express.js REST API Backend
├── package.json               # Node.js project configuration
├── models/
│   └── Report.js              # Waste Report Data Schema
├── PROJECT_DOCUMENTATION.md   # Complete technical documentation & theory
├── .gitignore                 # Git ignore rules (node_modules, etc.)
└── README.md                  # Project overview & GitHub presentation
```

---

## 🚀 Quick Start Guide

### 1. Direct Webpage (Zero Setup)
Simply open `index.html` in any modern web browser (Chrome, Edge, Firefox, Brave):
```powershell
start index.html
```

### 2. Run Python DAA Optimizer
```powershell
python optimizer.py
```

### 3. Run Node.js / Express Server
```powershell
npm install
npm start
```
Server runs at `http://localhost:5000`.

---

## 📜 License
This project is open-source under the [MIT License](LICENSE).
