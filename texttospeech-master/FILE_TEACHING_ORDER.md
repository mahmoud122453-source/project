# FILE_TEACHING_ORDER

Order follows conceptual dependency, not the alphabet.

---

## 1. README.md

- **Teaching priority:** C (show briefly)
- **Teaching order:** 1
- **What to explain:** this is a desktop text-to-speech app; original author credit; run with `python main.py`.
- **What NOT to explain deeply:** marketing wording, future enhancements, clone URL during the first lab hour.
- **Required previous concepts:** none.
- **Note:** the original README under-describes Save and calls `images/` optional screenshots. The code requires those PNG files.

---

## 2. requirements.txt

- **Teaching priority:** C (show briefly)
- **Teaching order:** 2
- **What to explain:** the app needs `pyttsx3`. On Windows it also lists `comtypes` and `pywin32` because the engine talks to SAPI5.
- **What NOT to explain deeply:** COM, version pinning strategy, `pypiwin32`.
- **Required previous concepts:** “libraries are installed with pip”.

---

## 3. images/ (speak.png, download.png, speaker logo.png)

- **Teaching priority:** C (show briefly)
- **Teaching order:** 3
- **What to explain:** these are icons loaded by `PhotoImage`. If they are missing, the window may fail while starting.
- **What NOT to explain deeply:** PNG format, image editing, PyInstaller bundling.
- **Required previous concepts:** files live in folders next to `main.py`.

---

## 4. main.py — imports and engine

- **Teaching priority:** A (must teach deeply)
- **Teaching order:** 4
- **What to explain:** `tkinter`, `Combobox`, `pyttsx3`, `os`, `sys`; `engine = pyttsx3.init()` creates one shared speaker for the whole program.
- **What NOT to explain deeply:** `from tkinter import *` wildcard style wars; driver internals.
- **Required previous concepts:** `import`.

---

## 5. main.py — window construction

- **Teaching priority:** A
- **Teaching order:** 5
- **Lines:** about 85–155
- **What to explain:** `Tk()`, `title`, `geometry("900x450")`, `resizable(False, False)`, `configure(bg=...)`, `Frame`, `Label`, `Text`, two `Combobox` widgets, `place(x=..., y=...)`.
- **What NOT to explain deeply:** `resource_path` / `_MEIPASS` (mention: “helps find images”).
- **Required previous concepts:** running a script; what a window is.

---

## 6. main.py — `speaknow`

- **Teaching priority:** A (line by line)
- **Teaching order:** 6
- **Lines:** 24–49
- **What to explain:** read text, read comboboxes, get voices, set rate, nested `setvoice`, `say`, `runAndWait`.
- **What NOT to explain deeply:** why SAPI voice IDs look like registry paths.
- **Required previous concepts:** functions, `if`, lists, the Text widget existing on screen.

---

## 7. main.py — Speak / Save buttons

- **Teaching priority:** A
- **Teaching order:** 7
- **Lines:** 157–179
- **What to explain:** `command=speaknow` and `command=download` connect a click to a function. No `lambda` and no `bind` in this project.
- **What NOT to explain deeply:** `compound=LEFT` beyond “image + text on the button”.
- **Required previous concepts:** `speaknow` already understood.

---

## 8. main.py — `download`

- **Teaching priority:** B (teach partially)
- **Teaching order:** 8
- **Lines:** 52–82
- **What to explain:** same gender/speed idea, then choose a folder, `save_to_file`, `runAndWait`. Cancel path: empty folder → `return`.
- **What NOT to explain deeply:** `os.chdir` side effects; WAV payload with `.mp3` name (mention as a fact, do not rebuild saving).
- **Required previous concepts:** `speaknow`; files and folders.

---

## 9. main.py — `resource_path`

- **Teaching priority:** D for internals, C as a one-minute aside
- **Teaching order:** 9 (late)
- **Lines:** 12–21
- **What to explain:** “this function builds a full path to an image.”
- **What NOT to explain deeply:** PyInstaller, `sys._MEIPASS`, frozen apps.
- **Required previous concepts:** `os.path.join`.

---

## 10. main.py — `mainloop`

- **Teaching priority:** A conceptually, short in time
- **Teaching order:** 10 (can be previewed when the window is first shown)
- **Line:** 181
- **What to explain:** the program waits here and reacts to events until the window closes.
- **What NOT to explain deeply:** Tk event queue implementation.
- **Required previous concepts:** the window exists.

---

## 11. RUN_GUIDE.md / this teaching set

- **Teaching priority:** B for instructors, C for students
- **Teaching order:** after the app runs once
- **What to explain:** how to install and the known limitations.
- **What NOT to explain deeply:** the QA automation used to test the project.

---

## Files not to treat as curriculum source

| Path | Class | Why |
| --- | --- | --- |
| `.venv/` | D | Local environment created for running, not original project code |
| GitHub `.git` metadata | D | Not needed to understand speech or Tkinter |
