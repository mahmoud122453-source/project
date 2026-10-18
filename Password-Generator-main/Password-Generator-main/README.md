# 🔐 Random Password Generator (Python)

A simple Python command-line program that generates random passwords using uppercase letters, lowercase letters, numbers, and symbols.

---

## Project Description

The program asks the user for a password length, checks that the length is at least 4, then builds a random password from Python’s `string` character sets and prints it.

---

## Features

- User chooses desired password length
- Uses letters (A-Z, a-z), digits (0-9), and symbols
- Checks for minimum password length (4)
- Handles non-numeric input without crashing
- Fully commented and beginner-friendly code

---

## Requirements

- Python 3.x  
  Verified with Python 3.12.0

No external libraries needed — only the built-in `random` and `string` modules.

---

## Installation

1. Download or clone the project.
2. Open the project folder that contains `main.py` (`Password-Generator-main`).
3. No `pip install` step is required.

---

## How to Run

Open a terminal in the folder that contains `main.py`, then run:

```bash
python main.py
```

On some Windows systems this also works:

```bash
py main.py
```

The program will prompt:

```text
Enter Password Length:
```

Enter an integer of 4 or more.

---

## Project Structure

```text
Password-Generator-main/
  main.py        # Program entry point
  README.md      # Project overview
  RUN_GUIDE.md   # Arabic run instructions
```

---

## Example Usage

```text
python main.py
🔐 Random Password Geberator
Enter Password Length: 12
✅ Your Password : wQ#o^1:r&;s:
```

The password text above is only an example. Each run produces a new random password of the requested length.

Arabic step-by-step run instructions are in `RUN_GUIDE.md`.
