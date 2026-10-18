# PROJECT_MAP

## Project architecture

This repository is a **single-window desktop application** in one Python module.

```
texttospeech-master/
├── main.py              # GUI + speech logic (the whole program)
├── requirements.txt     # pyttsx3, comtypes, pywin32
├── README.md            # original project description
├── images/
│   ├── speak.png
│   ├── download.png
│   └── speaker logo.png
├── RUN_GUIDE.md         # how to run (added for teaching)
├── TEACHING_GUIDE.md
├── FILE_TEACHING_ORDER.md
└── PROJECT_MAP.md
```

There are no extra Python packages in the repo, no config files, no tests, and no LICENSE file in this copy.

## File relationships

```
requirements.txt  -->  pip installs pyttsx3 (+ Windows helpers)
images/*.png      -->  PhotoImage in main.py (required at startup)
main.py           -->  creates window, reads widgets, calls pyttsx3
pyttsx3           -->  Windows SAPI5 driver (on this machine)
SAPI5             -->  speakers / saved audio file
```

`main.py` does not import other project modules.

## Execution flow

```
python main.py
        ↓
import tkinter, pyttsx3, os, sys
        ↓
engine = pyttsx3.init()          # one global Engine
        ↓
define resource_path, speaknow, download
        ↓
root = Tk() ... build widgets ...
        ↓
root.mainloop()                  # wait for user events
        ↓
user closes window → process ends
```

If `import pyttsx3` fails, the process never reaches `Tk()`.
If an image path is wrong, `PhotoImage(...)` fails while building the window.

## GUI flow

```
Tk root 900x450, title "Text to Speech", bg #305065
 ├── Top_frame (white banner)
 │    ├── Label + speaker logo image
 │    └── Label "Text to Speech"
 ├── Text txt          (user types here)
 ├── Label "Voice"
 ├── Label "Speech"
 ├── Combobox gendercb (Male / Female), default Male
 ├── Combobox speedcb  (Fast / Normal / Slow), default Normal
 ├── Button Speak      command=speaknow
 └── Button Save       command=download
```

Layout manager actually used: **`place`**.  
Not used: `pack`, `grid`, `Entry`, `ScrolledText`, `Scale`, `StringVar`.

## Data flow

```
User keystrokes
        ↓
Text widget buffer (txt)
        ↓
Speak click → speaknow()
        ↓
text   = txt.get(1.0, END)          # always includes a final "\n"
gender = gendercb.get()             # "Male" or "Female"
speed  = speedcb.get()              # "Fast" / "Normal" / "Slow"
voices = engine.getProperty('voices')
        ↓
rate 250 / 150 / 50 via setProperty('rate', ...)
        ↓
voice voices[0].id or voices[1].id
        ↓
engine.say(text)
engine.runAndWait()
        ↓
audio on the default playback device
```

Save path:

```
Same text / gender / speed
        ↓
filedialog.askdirectory()
        ↓
if no folder: return
        ↓
os.chdir(path)
engine.save_to_file(text, 'text.mp3')
engine.runAndWait()
        ↓
file named text.mp3 in the chosen folder
(on this Windows test: RIFF/WAVE bytes, not MPEG)
```

## TTS flow (actual library: pyttsx3)

```
pyttsx3.init()
        ↓
Engine object (global `engine`)
        ↓
driver on this PC: pyttsx3.drivers.sapi5
        ↓
voices detected here:
  [0] Microsoft David Desktop - English (United States)
  [1] Microsoft Zira Desktop  - English (United States)
        ↓
setProperty('voice', ...)
setProperty('rate', 50 | 150 | 250)
        ↓
say(text) or save_to_file(text, 'text.mp3')
        ↓
runAndWait()  blocks until SAPI finishes
```

Not used in code: `setProperty('volume', ...)`, `engine.stop()`.

Default engine properties observed before the app changes rate: rate 200, volume 1.0.

## Dependency map (adapted to this code)

```
PROJECT (main.py)
 ↓
GUI (Tk + place widgets)
 ↓
USER INPUT (Text + Combobox)
 ↓
CALLBACK (command=speaknow or command=download)
 ↓
TEXT PROCESSING (get text, get gender, get speed, if/elif rate)
 ↓
TTS ENGINE (pyttsx3 Engine + SAPI5)
 ↓
AUDIO OUTPUT (speakers)  or  FILE (text.mp3 via save_to_file)
```

## Threading

No `threading`, no `Thread`, no `queue`, no `after()`.

`runAndWait()` runs on the Tk thread, so the window does not process clicks until speech ends. Acceptable for a first GUI lesson; mention it; do not add threads unless a later course requires it.
