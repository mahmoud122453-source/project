# 🗣 Text‑to‑Speech App

A simple Python desktop application built with **Tkinter** and **pyttsx3** for converting typed text into speech. Features a clean GUI, adjustable voice and speech rate, and works entirely offline—perfect for learning Python GUI programming and speech synthesis.

---

##  Features
- **Text-to-Speech Conversion** — Type or paste text and listen instantly.
- **Voice & Speed Controls** — Choose Male/Female (first/second system voice) and Fast/Normal/Slow rate.
- **Save speech** — The **Save** button writes a file named `text.mp3` in a folder you choose (the Windows engine may store WAV data under that name).
- **Offline Operation** — No internet required; works with the local TTS engine.
- **User-Friendly GUI** — Beginner-friendly layout with Tkinter interface.

Arabic (and other non-English) pronunciation depends on voices installed in the operating system. This project does not bundle language voices.

---

##  Technologies Used
- **Python**
- **Tkinter** (for GUI)
- **pyttsx3** (for offline text-to-speech synthesis)

---

##  Project Structure
```
texttospeech/
│-- main.py           # Core application logic (GUI + pyttsx3)
│-- requirements.txt  # Library dependencies
│-- images/           # Required GUI icons (speak, download, logo)
│-- README.md         # Project documentation
```

On Windows, `requirements.txt` installs `pyttsx3`, `comtypes`, and `pywin32`. Tkinter ships with the official Windows Python installer (do not `pip install tkinter`).

---

##  Getting Started

### 1. Clone the repository
```
git clone https://github.com/Dinesh8778/texttospeech.git
cd texttospeech
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Run the app
```
python main.py
```

---

##  How It Works
1. Launch the app—run `main.py`.
2. Type text into the input field.
3. Adjust voice and speech rate if desired.
4. Click **Speak** to hear the speech output.
5. Click **Save** to pick a folder and export `text.mp3`.

While speech is playing, the window may freeze until `runAndWait()` finishes. That is expected in this original code (no background thread).

Teaching and run notes for this copy: `RUN_GUIDE.md`, `TEACHING_GUIDE.md`, `FILE_TEACHING_ORDER.md`, `PROJECT_MAP.md`.

---

##  Future Enhancements

- Multiple voices or language support.
- Themed or customizable GUI layouts.

---

##  Contact
- **GitHub:** [Dinesh8778](https://github.com/Dinesh8778)  
- **Email:** dineshkumarselvaraj31@gmail.com 

---

⭐ If you enjoy this project or find it helpful, feel free to **star** the repo!
