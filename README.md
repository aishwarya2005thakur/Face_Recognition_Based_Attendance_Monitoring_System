# 🧠 Face Recognition Based Attendance Monitoring System

A smart attendance system that uses **face recognition** to automatically detect and record student or employee attendance. This eliminates manual entry errors and saves time by leveraging computer vision and machine learning techniques.

---

## 🚀 Features

* 🎥 Real-time face detection and recognition
* 🧾 Automatic attendance marking with date & time
* 💾 Attendance stored in CSV / Database format
* 👥 Handles multiple users with registration & training
* 📊 Admin dashboard for attendance viewing and export

---

## 🛠️ Tech Stack

* **Python**
* **OpenCV** – for face detection
* **face_recognition** (Dlib) – for facial feature encoding and matching
* **NumPy**, **Pandas** – for data handling
* **Flask / Tkinter (optional)** – for UI or web dashboard

---

## ⚙️ How It Works

1. **Register Faces:** Capture and store images of each user.
2. **Train Model:** Encode facial features and store them for recognition.
3. **Recognize & Record:** When a face is detected in real time, the system identifies the person and marks their attendance with timestamp.
4. **View Attendance:** Admin can view or export daily logs.

---

## 🧩 Installation

```bash
# Clone the repo
git clone https://github.com/aishwarya2005thakur/face_recognition_based_attendance_monitoring_system.git
cd face_recognition_based_attendance_monitoring_system

# Install dependencies
pip install -r requirements.txt

# Run the system
python main.py
```

---

## 📁 Folder Structure

```
📦 FaceRecognitionAttendance
 ┣ 📂 dataset/           # Stored face images
 ┣ 📂 encodings/         # Trained facial encodings
 ┣ 📂 attendance/        # Attendance CSV files
 ┣ 📜 main.py            # Main script
 ┣ 📜 requirements.txt   # Dependencies
 ┗ 📜 README.md          # Documentation
```
---
## 📸 Screenshots 

<img src ="![WhatsApp Image 2025-10-09 at 11 30 00_7cda1c97](https://github.com/user-attachments/assets/fd96599b-db73-4816-bcc7-a756e4df5407)">


---

---

##  Sample Output

* Recognized faces displayed with bounding boxes
* Attendance auto-saved as:

  ```
  Name, Date, Time
  Aishwarya, 2025-10-08, 09:12:30
  ```

---

## 🧑‍💻 Future Improvements

* Cloud database integration (Firebase / MySQL)
* Mobile app or web-based dashboard
* Spoof detection for added security

---

## 🪪 License

This project is open-source and available under the [MIT License](LICENSE).
