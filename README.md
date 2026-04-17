# Sleep & Distraction Detection System

A real-time computer vision system that detects user attention, sleep, and distraction using facial landmarks.

---

## 🚀 Overview
This project monitors user alertness by analyzing:
- Eye closure (sleep detection)
- Head movement (distraction detection)
- Face presence (no-face alert)

It is designed for applications like:
- Driver monitoring systems
- Workplace productivity tracking
- Safety-critical environments

---

## 🧠 How It Works
- Uses MediaPipe for facial landmark detection
- Computes Eye Aspect Ratio (EAR) for sleep detection
- Uses head pose estimation (solvePnP) for distraction detection
- Triggers alerts when thresholds are exceeded
- Uses threaded audio system for continuous alerts

---

## ⚙️ Technologies Used
- Python
- OpenCV
- MediaPipe
- NumPy
- Pydub

---

## 📁 Project Structure
main.py              
# Main detection system requirements.txt     
# Dependencies alert.wav            
# Alert sound (optional)

---

## 📌 Current Status
⚠️ Actively under development and optimization

---

## 🎥 Demo
(Add your demo video link here)

---

## 📈 Future Improvements
- Improve detection accuracy under varying lighting conditions
- Optimize for embedded systems (ESP32 / Jetson)
- Add deep learning-based detection (YOLO / CNN)
- Enhance multi-user tracking

---

## 👨‍💻 Author
Elewa Chizi Prince
