# TEACHING_GUIDE — Text to Speech (Tkinter + pyttsx3)

## Project objective

Teach absolute Python beginners how a small desktop app:

1. Opens a window.
2. Lets the user type text.
3. Reads that text when a button is clicked.
4. Sends the text to a speech engine.
5. Optionally saves speech to a file.

The original GitHub project is a single-file application: `main.py`.

## Prerequisite knowledge

Students should already know:

- running `python file.py`
- variables and strings
- `if` / `elif` / `else`
- defining a function with `def`
- calling a function
- lists and indexing (`voices[0]`)
- basic imports (`import os`)

They do **not** need prior Tkinter or pyttsx3 experience.

## Learning objectives

By the end, a student can:

- explain what this app does in one sentence
- identify the window, text box, comboboxes, and buttons
- trace a click from `command=speaknow` to `engine.say`
- change speech rate values and predict Fast / Normal / Slow
- explain that Male / Female here means “first voice / second voice on this computer”
- run the app from `main.py`
- name two limitations: GUI freeze during speech, and Arabic depending on Windows voices

## Concepts actually in this project

Present:

- imports, functions, nested functions, `if` conditions
- `Tk`, `Frame`, `Label`, `Text`, `Button`, `Combobox`, `PhotoImage`
- layout with `place` (not `pack` / `grid`)
- `command=` callbacks and `mainloop()`
- `pyttsx3.init`, `say`, `runAndWait`, `getProperty`, `setProperty`, `save_to_file`
- `filedialog.askdirectory`
- `try` / `except AttributeError` only inside `resource_path`

Not present:

- classes written by the project
- `StringVar` / `Scale` / volume UI
- `threading`, `after()`, `bind()`, `lambda`
- `engine.stop()`
- language selection

## Teaching order (conceptual dependency)

1. Project idea: type text → hear speech.
2. `python main.py` and the window.
3. Imports at the top of `main.py`.
4. `engine = pyttsx3.init()` as “prepare the speaker”.
5. Create `root = Tk()`, title, size, background.
6. Top `Frame` + labels + images (visual only).
7. `Text` widget: where the user types.
8. `Combobox` for voice and speed (reading `.get()` comes later).
9. Functions: `speaknow` is a named action.
10. Button `command=speaknow`.
11. Inside `speaknow`: `txt.get(1.0, END)`.
12. `if text:` then set rate then nested `setvoice()`.
13. `engine.say` + `engine.runAndWait`.
14. `download()` and Save as a second path that uses the same settings.
15. `resource_path` as “find the image files” (do not deep-dive PyInstaller).
16. `mainloop()` as the waiting loop that listens for clicks.
17. Limitations: empty text is `"\n"`, no volume control, no stop, speech blocks the GUI, Arabic needs an OS Arabic voice.

## Code blocks (see also FILE_TEACHING_ORDER.md)

| Block | File | Lines (approx.) | Teach? |
| --- | --- | --- | --- |
| Imports + `engine` | `main.py` | 1–9 | Yes, line by line |
| `resource_path` | `main.py` | 12–21 | Concept only |
| `speaknow` | `main.py` | 24–49 | Yes, line by line |
| `download` | `main.py` | 52–82 | After Speak works |
| Window + widgets | `main.py` | 85–179 | Yes, widget by widget |
| `mainloop` | `main.py` | 181 | Yes |

## Difficulty

- **BEGINNER:** window, labels, text box, buttons, `command=`, `if` speed branches, `engine.say`
- **INTERMEDIATE:** nested `setvoice`, `Text.get(1.0, END)`, combobox `state='readonly'`, `filedialog`, `os.chdir`
- **ADVANCED / postpone:** `sys._MEIPASS`, PyInstaller, SAPI5 internals, WAV-vs-mp3, threading (not in the project)

## Common mistakes

1. Running Python from the wrong folder so images are not found.
2. Forgetting `pip install -r requirements.txt`.
3. Thinking `if text:` rejects an empty box. Tkinter `Text.get(1.0, END)` returns `"\n"`, which is True.
4. Thinking Female is “a female voice file in the project”. It is `voices[1]` on the machine.
5. Expecting Arabic to sound correct with English Windows voices.
6. Clicking Speak again while speech is running and believing the app crashed (the GUI is blocked).
7. Opening `text.mp3` and assuming it is MPEG audio. On this Windows test it was a WAV file named `.mp3`.
8. Teaching `pack`/`grid` as if this project used them. It uses `place`.

## Practical exercises

1. Change the window title and size, then run.
2. Change Fast rate from `250` to `300` and listen.
3. Add a print of `repr(text)` inside `speaknow` to see the trailing newline.
4. Type numbers and punctuation; listen how SAPI reads them.
5. Save a file, inspect the folder, note the name `text.mp3`.
6. (Optional, do not require) Count how many voices `engine.getProperty('voices')` returns.

## Final student challenge

Without rewriting the architecture:

- Explain the full path from typing to audio using the real function names.
- Predict what happens with an empty text box, and then verify.
- State one thing the README mentions and one thing the code has that the original README did not emphasize (Save / images as required icons).
- Do **not** add threading unless a later lesson asks for it.
