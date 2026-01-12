# Advanced BMI Tracking System

A desktop-based **BMI Tracking System** developed in **Python** using **Tkinter**, **SQLite**, and **Matplotlib**.  
The application is designed to calculate Body Mass Index, store records permanently, and analyze BMI changes over time using graphical insights.

---

## ✨ Application Highlights

### 🧮 BMI Calculation
- Computes BMI using user-provided height and weight
- Automatically classifies health status
- Displays clear health guidance for each category

### 👥 Multi-User Support
- Supports multiple users in a **single shared database**
- Each entry is timestamped for accurate tracking
- Historical records remain available across sessions

### 🗂 Persistent Storage
- Local **SQLite file-based storage**
- No external server required
- Data is preserved even after closing the application

### 📊 Visual Analytics
- Interactive BMI trend graph for individual users
- Time-based visualization using Matplotlib
- Reference lines indicate standard BMI ranges

### 🛠 History Management
- View complete BMI history of all users
- Remove selected records
- Option to clear all stored data with confirmation

### 🧯 Validation & Safety
- Validates numerical input ranges
- Prevents invalid or unrealistic entries
- Graceful error handling with alerts

---

## 🧰 Tech Stack

| Tool | Usage |
|----|------|
| Python | Application logic |
| Tkinter | GUI design |
| SQLite | Local database |
| Matplotlib | Graph plotting |
| datetime | Record timestamps |

---