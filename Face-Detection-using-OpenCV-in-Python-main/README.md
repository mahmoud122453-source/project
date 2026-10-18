

# 👤 Face Detection using OpenCV in Python

Detect and locate faces in images and real-time video using OpenCV’s powerful **Haar Cascade Classifiers**.

---


## 🚀 Features

* 👥 Detects multiple faces in a single image
* 🎥 Real-time webcam face detection
* 👤 Supports frontal and profile face detection
* 📦 Draws bounding boxes around detected faces
* 💾 Saves detected faces as separate images
* ⚡ Lightweight and fast (no heavy deep learning required)

---

## 🧠 How It Works

1. Load Haar Cascade classifier (pre-trained XML file)
2. Convert image/video frame to grayscale
3. Detect faces using `detectMultiScale()`
4. Draw rectangles around detected faces
5. Optionally crop and save detected faces

---

## 📦 Installation

### 1️⃣ Install required libraries

```bash
pip install opencv-python numpy
```

---

## 📁 Requirements

* Python 3.x
* OpenCV (`cv2`)
* NumPy

---

## 📂 Project Structure (Recommended)

```
Face-Detection-OpenCV/
│── haarcascades/
│     ├── haarcascade_frontalface_default.xml
│     ├── haarcascade_profileface.xml
│
│── images/
│── outputs/
│── face_detection.py
│── README.md
```

---

## ▶️ Usage

### 🔹 1. Image Detection

```bash
python face_detection.py --image path/to/image.jpg
```

---

### 🔹 2. Real-Time Webcam Detection

```bash
python face_detection.py
```

---

## 💻 Example Code (Basic)

```python
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

cv2.imshow('Face Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## 📸 Output Example

* Faces highlighted with rectangles
* Multiple faces detected in group images
* Live webcam detection with bounding boxes

---

## 🔧 Parameters Explanation

* `scaleFactor (1.1)` → How much image size is reduced at each scale
* `minNeighbors (4)` → Higher value reduces false detections
* `minSize` → Minimum possible face size

---

## 📊 Applications

* Security systems 🔐
* Attendance systems 🏫
* AI-based surveillance 🎥
* Photo tagging systems 📸

---

## 🚀 Future Improvements

* 🔥 Replace Haar Cascade with DNN (higher accuracy)
* 😄 Add emotion detection on faces
* 📱 Mobile app integration
* 🌐 Web app using Flask/Streamlit

---

## 🤝 Contribution

1. Fork the repository
2. Create a new branch
3. Make improvements
4. Submit a pull request

---

## 📜 License

This project is licensed under the MIT License.

---


