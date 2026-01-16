# Secure Password Studio – Python GUI Application

Secure Password Studio is a **desktop-based password generation tool** built with **Python and Tkinter**.  
It allows users to create **high-entropy, secure passwords** using modern security principles and a clean graphical interface.

This project focuses on **security awareness**, **entropy-based strength analysis**, and **GUI application development**.

---

## About the Project

Passwords are a critical part of digital security. This application generates random passwords using **cryptographically secure randomness** and evaluates their strength using **entropy (measured in bits)** rather than simple rules.

The project is suitable for students learning:
- Python GUI programming  
- Secure random generation  
- Practical cybersecurity concepts  

---

## Core Functionalities

- Generate passwords between **8 and 32 characters**
- Select character types:
  - Uppercase & lowercase letters
  - Numbers
  - Symbols
- Entropy-based password strength calculation
- Visual strength indicator with color feedback
- Copy generated password to clipboard
- Simple and distraction-free user interface

---

## Security Approach

Instead of using basic random functions, this project uses:

- `secrets` module for cryptographic randomness
- Entropy calculation based on character pool size
- Strength grading using entropy thresholds

This ensures the generated passwords are **suitable for real-world use**.

---

## Password Strength Evaluation

Password strength is calculated using **Shannon entropy**.

### Strength Levels
- **Weak** – Low entropy  
- **Moderate** – Acceptable for basic use  
- **Strong** – Good security  
- **Excellent** – High resistance to brute-force attacks  

The entropy value (in bits) is displayed along with the strength label.

---

## User Interface Design

- Built entirely with **Tkinter**
- Soft pastel color palette for reduced eye strain
- Centered layout with clear typography
- Fixed window size for layout consistency
- Beginner-friendly interaction flow

---

## Technologies Used

- **Programming Language:** Python 3  
- **GUI Framework:** Tkinter  
- **Security Module:** secrets  
- **Mathematics:** entropy calculation using `math`  

---