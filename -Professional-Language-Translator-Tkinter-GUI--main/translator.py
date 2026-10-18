import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator

# ==============================
# Create Main Application Class
# ==============================

class ProfessionalTranslatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Professional Translator - Jaweid Moraadi")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f9")

        self.translator = Translator()

        self.create_styles()
        self.create_widgets()

    # ==============================
    # Styling
    # ==============================

    def create_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel",
                        background="#f4f6f9",
                        font=("Segoe UI", 11))

        style.configure("TButton",
                        font=("Segoe UI", 11),
                        padding=6)

        style.configure("Header.TLabel",
                        font=("Segoe UI", 16, "bold"),
                        foreground="#2c3e50")

    # ==============================
    # Widgets
    # ==============================

    def create_widgets(self):

        # Header
        header = ttk.Label(self.root,
                           text="🌍 Professional Language Translator",
                           style="Header.TLabel")
        header.pack(pady=15)

        # Input Frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(input_frame, text="Enter Text:").pack(anchor="w")

        self.input_text = tk.Text(input_frame,
                                  height=6,
                                  font=("Segoe UI", 11),
                                  bd=2,
                                  relief="groove")
        self.input_text.pack(fill="x", pady=5)

        # Language Selection
        ttk.Label(self.root, text="Select Target Language:").pack(anchor="w", padx=20)

        self.lang_combobox = ttk.Combobox(
            self.root,
            values=[
                "en - English",
                "fa - Persian",
                "ar - Arabic",
                "fr - French",
                "de - German",
                "tr - Turkish",
                "ur - Urdu"
            ],
            state="readonly"
        )
        self.lang_combobox.pack(padx=20, fill="x", pady=5)
        self.lang_combobox.current(0)

        # Buttons Frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=15)

        translate_btn = ttk.Button(btn_frame,
                                   text="Translate",
                                   command=self.translate_text)
        translate_btn.grid(row=0, column=0, padx=10)

        clear_btn = ttk.Button(btn_frame,
                               text="Clear",
                               command=self.clear_text)
        clear_btn.grid(row=0, column=1, padx=10)

        # Output Frame
        output_frame = ttk.Frame(self.root)
        output_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(output_frame, text="Translated Text:").pack(anchor="w")

        self.output_text = tk.Text(output_frame,
                                   height=6,
                                   font=("Segoe UI", 11),
                                   bd=2,
                                   relief="groove",
                                   fg="#2c3e50")
        self.output_text.pack(fill="x", pady=5)

    # ==============================
    # Functions
    # ==============================

    def translate_text(self):
        try:
            text = self.input_text.get("1.0", tk.END).strip()
            lang_selection = self.lang_combobox.get()

            if not text:
                messagebox.showwarning("Warning", "Please enter text to translate.")
                return

            target_lang = lang_selection.split(" - ")[0]

            translated = self.translator.translate(text, dest=target_lang)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated.text)

        except Exception as e:
            messagebox.showerror("Error", f"Translation failed:\n{str(e)}")

    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)


# ==============================
# Run Application
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalTranslatorApp(root)
    root.mainloop()