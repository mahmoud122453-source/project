# خريطة المشروع — Audio Extractor

المصدر الوحيد للمنطق: `extractor.py` (47 سطرًا). لا أصناف. دالتان: `extract_audio_from_video` و`main`. إنشاء المجلدين أثر جانبي عند الاستيراد.

نقطة الدخول:

```
python extractor.py
```

والتي تصل إلى:

```
if __name__ == "__main__":
    main()
```

## البنية

```
جذر المشروع
├── extractor.py          منطق الواجهة والاستخراج
├── requirements.txt      moviepy
├── readme.md
├── LICENSE               MIT، Bisal Kumar Sahoo 2023
├── Sample.png            لقطة شريط تقدم MoviePy في الطرفية
├── .gitignore            venv/  input/  output/
├── test_data/videos      فيديوهات اختبار صناعية
└── Audio-Extractor-master/   نسخة مكررة، ليست هي التي تم تشغيلها
```

أثناء التشغيل ينشئ الاستيراد، إن غابا:

```
input/     نسخة من الفيديو المختار
output/    ملف الصوت
```

## تدفق الواجهة

```
المستخدم يشغّل extractor.py
        │
        ▼
main()
        │
        ▼
Tk() ثم root.withdraw()          لا نافذة رئيسية
        │
        ▼
filedialog.askopenfilename
عنوان الحوار: Select the video file
        │
        ├── المسار فارغ ──► return     لا رسالة
        │
        ▼
نسخ ثنائي إلى input\<basename>
        │
        ▼
simpledialog.askstring
عنوان الحوار: Output Format
القيمة الابتدائية: mp3
        │
        ▼
extract_audio_from_video(dest_path, audio_path)
        │
        ├── True  ──► messagebox.showinfo("Success", ...)
        └── False ──► messagebox.showerror("Error", ...)
        │
        ▼
نهاية main وانتهاء العملية
```

لا `Button` ولا `mainloop` في شفرة المشروع. `askopenfilename` و`askstring` و`messagebox` نوافذ modal.

عناوين مربعات الحوار التي ظهرت في الاختبار:

| اللحظة | العنوان | النوع على Windows |
| --- | --- | --- |
| اختيار الملف | Select the video file | حوار أصلي `#32770` |
| الصيغة | Output Format | `TkTopLevel` |
| النجاح | Success | `#32770` |
| الفشل | Error | `#32770` |

مرشح الملفات في الشفرة:

```
("Video Files", "*.mp4;*.avi;*.mkv;*.flv;*.mov")
```

الاختبار أظهر عنصرًا واحدًا في قائمة النوع باسم `Video Files`. المرشح لا يمنع كتابة مسار كامل لملف آخر: فتح `not_a_video.txt` عبر المسار الكامل وصل إلى الاستخراج ثم فشل داخل MoviePy.

## تدفق الدخل

```
مسار يختاره المستخدم
        │
        ▼
video_path
        │
        ▼
os.path.basename(video_path)
        │
        ▼
dest_path = input\<الاسم>
        │
        ▼
open(..., "rb") / open(..., "wb")
        │
        ▼
نسخة كاملة من الفيديو داخل input
```

الاستخراج يقرأ `dest_path`، لا المسار الأصلي. إذا فشل الاستخراج بعد النسخ، تبقى النسخة في `input`.

## تدفق MoviePy

```
dest_path
    │
    ▼
moviepy.VideoFileClip(dest_path)
    │
    ▼
video
    │
    ▼
video.audio
    │
    ├── AudioFileClip إذا وُجد مسار صوت
    └── None إذا لم يوجد
    │
    ▼
audio.write_audiofile(audio_path)
    │
    ▼
FFmpeg عبر imageio-ffmpeg
    │
    ▼
ملف في output
```

`VideoFileClip` في MoviePy 2 يستدعي قارئ FFmpeg. إذا كان `audio_found`، ينشئ `AudioFileClip` على الملف نفسه. `write_audiofile` يختار الترميز من الامتداد: `mp3` ثم `libmp3lame`، و`wav` ثم `pcm_s16le`.

المشروع لا يضبط `FFMPEG_BINARY`. MoviePy تجد:

`venv\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe`

لا يوجد `ffmpeg` على `PATH`، والاستخراج نجح بهذا الملف.

## تدفق استخراج الصوت

```
extract_audio_from_video(video_path, audio_path)
        │
        try
        │
        ├── VideoFileClip
        ├── video.audio
        ├── write_audiofile
        └── return True
        │
        except Exception as e
        │
        ├── print("An error occurred: {e}")
        └── return False
```

لا `finally` ولا `close()`.

## تدفق المسار والاسم

مثال متحقق: اختيار `longer_with_audio.mp4` وترك الصيغة `mp3`.

```
D:\...\test_data\videos\longer_with_audio.mp4
        │ basename
        ▼
longer_with_audio.mp4
        │ join("input", ...)
        ▼
input\longer_with_audio.mp4          النسخة، 155457 بايت
        │ splitext ثم ".mp3"
        ▼
longer_with_audio.mp3
        │ join("output", ...)
        ▼
output\longer_with_audio.mp3         192931 بايت، فك الترميز نجح، المدة 12.04 ثانية
```

عمليات `os` المستخدمة وسببها:

| العملية | السبب في هذه الشفرة |
| --- | --- |
| `os.path.exists` / `os.makedirs` | إنشاء `input` و`output` مرة عند الاستيراد |
| `os.path.basename` | رمي مجلدات المسار الأصلي والإبقاء على الاسم |
| `os.path.join` | بناء مسار بنظام Windows من غير لصق يدوي للشرطة |
| `os.path.splitext` | فصل `name` عن `.mp4` حتى لا يصبح الاسم `name.mp4.mp3` |

إذا ألغى المستخدم حوار الصيغة، `askstring` تُرجع `None`، والشفرة لا تفحص ذلك، فيصبح الامتداد النص `None` والاسم مثل `short_with_audio.None`.

## تدفق الخطأ

```
لا فيديو مختار
    return من main
    لا مربع رسالة

استثناء داخل extract_audio_from_video
    طباعة An error occurred
    return False
    messagebox.showerror
    النص ثابت: Failed to extract audio. Please check the video file.
```

حالات تم تشغيلها:

| الحالة | ما حدث |
| --- | --- |
| فيديو بلا صوت | `'NoneType' object has no attribute 'write_audiofile'` ثم مربع Error |
| ملف نصي | `Invalid data found when processing input` ثم مربع Error |
| مسار ناقص | `'...missing.mp4' not found` ثم `False` |
| إلغاء الصيغة | خطأ الترميز لأن الامتداد `.None` ثم مربع Error |
| مجلد خرج غير موجود | MoviePy قد تطبع Done وترجع الدالة True والملف غير موجود |
| `m4a` على FFmpeg المرفق | السلوك نفسه: Done من غير ملف |
| إغلاق حوار الملف | خروج برمز 0 |

المسار العادي إلى `output\` لا يقع في حالة المجلد الناقص، لأن الاستيراد ينشئ `output`.

## تدفق الخرج

```
audio_path
    │
    ▼
write_audiofile
    │
    ├── ملف صوته قابل للفتح ──► showinfo بالمسار النسبي
    └── استثناء ──► showerror
```

الصيغ التي أُنتج لها ملف صالح على فيديو الاختبار القصير:

- `mp3` حجم 48735، المدة 3.03، أعلى سعة مقاسة 0.083، فك الترميز 0
- `wav` حجم 529278، المدة 3.0، أعلى سعة 0.132، فك الترميز 0
- `ogg` حجم 12419، فك الترميز 0
- `flac` حجم 45295، فك الترميز 0

`m4a` لم يُنشأ.

مدد مصادر الاختبار التي قرأها `VideoFileClip`:

| الملف | مدة الفيديو | مدة الصوت |
| --- | --- | --- |
| short_with_audio.mp4 | 3.0 | 3.0 |
| longer_with_audio.mp4 | 12.0 | 12.0 |
| silent.mp4 | 2.0 | لا يوجد |
| short_with_audio.avi | 3.07 | 3.07 |
| short_with_audio.mkv | 3.04 | 3.04 |
| short_with_audio.mov | 3.02 | 3.02 |
| short_with_audio.flv | 3.04 | 3.04 |

استخراج هذه الصيغ إلى `mp3` أو `wav` أنتج ملفات مدتها ضمن نحو 0.1 ثانية من المصدر، وفك ترميزها نجح.
