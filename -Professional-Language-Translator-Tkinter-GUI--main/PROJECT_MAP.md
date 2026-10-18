# خريطة المشروع

## الملفات

```text
-Professional-Language-Translator-Tkinter-GUI-
├── translator.py          البرنامج
├── README.md              وصف المؤلف والتشغيل
├── RUN_GUIDE.md           تشغيل تم التحقق منه
├── TEACHING_GUIDE.md      تسلسل التدريس
├── FILE_TEACHING_ORDER.md ترتيب الملفات والكتل
└── PROJECT_MAP.md         هذه الخريطة
```

لا يوجد `LICENSE`. لا توجد حزمة ولا قاعدة بيانات ولا ملف لغات منفصل.

المجلد `.venv` بيئة محلية أُنشئت للتحقق. ليس من مصدر المشروع.

## مسار الترجمة

```text
USER TEXT
    self.input_text.get("1.0", tk.END).strip()
        ↓
SOURCE LANGUAGE
    غير مختارة في الواجهة
    translate(..., dest=target_lang) يترك src='auto'
        ↓
TARGET LANGUAGE
    self.lang_combobox.get()
    مثال: "ar - Arabic"
    target_lang = "ar"
        ↓
TRANSLATOR
    self.translator = Translator()
    يُنشأ مرة واحدة في __init__
    المضيف الافتراضي داخل المكتبة: translate.google.com
        ↓
TRANSLATE
    self.translator.translate(text, dest=target_lang)
        ↓
RESULT
    كائن googletrans.models.Translated
    المشروع يقرأ translated.text فقط
        ↓
GUI OUTPUT
    self.output_text.delete("1.0", tk.END)
    self.output_text.insert(tk.END, translated.text)
```

## مسار الحدث

```text
GUI
    زر Translate أو زر Clear
        ↓
EVENT
    command=self.translate_text
    command=self.clear_text
        ↓
METHOD
    translate_text أو clear_text
        ↓
TRANSLATION
    في translate_text فقط، وبعد رفض النص الفارغ
    clear_text لا يستدعي المترجم
        ↓
DISPLAY
    مربع الناتج، أو messagebox عند التحذير أو الخطأ
```

## الصنف

```text
if __name__ == "__main__"
    root = tk.Tk()
    app = ProfessionalTranslatorApp(root)
        __init__
            self.root
            self.translator = Translator()
            create_styles()
            create_widgets()
                self.input_text
                self.lang_combobox
                self.output_text
                Translate → translate_text
                Clear → clear_text
    root.mainloop()
```

## خريطة اللغات الفعلية

القائمة مكتوبة داخل `create_widgets`. ليست قاموسًا ولا ملفًا خارجيًا.

```text
"en - English"  → en
"fa - Persian"  → fa
"ar - Arabic"   → ar
"fr - French"   → fr
"de - German"   → de
"tr - Turkish"  → tr
"ur - Urdu"     → ur
```

الفصل يتم بـ `lang_selection.split(" - ")[0]`.

## ما لا يوجد على الخريطة

- Combobox للغة المصدر
- قراءة `result.src` أو `result.dest`
- تخزين سجل ترجمات
- تشغيل دون شبكة
- محرك ترجمة بديل
