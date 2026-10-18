# دليل التشغيل — Audio Extractor

هذا الدليل يصف التشغيل الذي تم التحقق منه على الجهاز الحالي. كل أمر أدناه نُفِّذ فعلًا.

البيئة التي تم القياس عليها:

- النظام: Windows 10 (10.0.19045)
- Python: 3.12.0
- pip داخل البيئة الافتراضية: 26.2.1
- Tkinter: موجود، إصدار Tcl/Tk ‏8.6
- MoviePy المثبت من `requirements.txt`: الحزمة `moviepy==2.2.1`
- النص الداخلي `moviepy.__version__` يطبع `2.1.2` رغم أن `pip show` يُظهر `2.2.1`. هذا اختلاف في ملف الإصدار داخل الحزمة، والشفرة المستخدمة هي حزمة 2.2.1
- FFmpeg على `PATH`: غير موجود
- ملف FFmpeg الذي تستخدمه MoviePy: موجود داخل الحزمة `imageio-ffmpeg` بعد تثبيت MoviePy

## 1. المتطلبات

- Windows مع Python 3.12 يتضمن Tcl/Tk
- اتصال بالإنترنت عند أول تثبيت للحزم
- ملف فيديو. للاختبار يمكن استخدام الملفات الصناعية في `test_data/videos`

لا تثبّت الحزمة `tk` عبر pip. Tkinter هنا جزء من تثبيت Python نفسه.

## 2. إصدار Python

الأمر:

```
python --version
```

النتيجة المتحققة:

```
Python 3.12.0
```

## 3. الاعتماديات

محتوى `requirements.txt` سطر واحد فقط:

```
moviepy
```

تثبيت هذا السطر سحب الحزم التالية (الإصدارات المثبتة فعليًا في `venv`):

| الحزمة | الإصدار |
| --- | --- |
| moviepy | 2.2.1 |
| imageio | 2.37.4 |
| imageio-ffmpeg | 0.6.0 |
| numpy | 2.5.3 |
| pillow | 11.3.0 |
| decorator | 5.3.1 |
| proglog | 0.1.12 |
| python-dotenv | 1.2.3 |
| tqdm | 4.70.1 |
| colorama | 0.4.6 |

`numpy` و`pillow` و`imageio` تأتي مع MoviePy. المشروع لا يستوردها في `extractor.py`.

## 4. التحقق من Tkinter

لا تستخدم `pip install tk`.

الأمر المتحقَّق منه على Python الأساسي وعلى بيئة `venv`:

```
python -c "import tkinter; print(tkinter.TkVersion)"
```

النتيجة:

```
8.6
```

إذا ظهر `ModuleNotFoundError: No module named 'tkinter'` فمثبت Python نفسه لا يتضمن Tcl/Tk، ويجب إصلاح تثبيت Python، لا تثبيت حزمة pip باسم `tk`.

## 5. إصدار MoviePy

بعد التثبيت:

```
venv\Scripts\python.exe -m pip show moviepy
```

النتيجة: `Version: 2.2.1`

والاستيراد الذي يستخدمه المشروع يعمل مع هذه الحزمة:

```
venv\Scripts\python.exe -c "import moviepy; print(moviepy.__version__); print(hasattr(moviepy, 'VideoFileClip'))"
```

النتيجة المتحققة:

```
2.1.2
True
```

`True` يعني أن `moviepy.VideoFileClip` موجود. المشروع يستدعيه بهذا الشكل في `extractor.py`، وهذا متوافق مع MoviePy 2. لا يوجد في المشروع `from moviepy.editor import ...`، ووحدة `moviepy.editor` غير موجودة في الإصدار 2.

## 6. FFmpeg

### لماذا هو مطلوب؟

`extractor.py` لا يستدعي `ffmpeg` بنفسه. MoviePy تستدعيه عند `VideoFileClip(...)` لقراءة الملف، وعند `write_audiofile(...)` لكتابة الصوت.

### أين؟

المشروع لا يضبط مسار FFmpeg. الإعداد الافتراضي داخل MoviePy هو `FFMPEG_BINARY = "ffmpeg-imageio"`، ثم تحصل على المسار من `imageio`.

الأمر المتحقَّق منه:

```
venv\Scripts\python.exe -c "import moviepy.config as c; print(c.FFMPEG_BINARY)"
```

النتيجة على هذا الجهاز:

```
D:\project_lv3\Audio-Extractor-master\venv\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe
```

### كيف يُثبَّت هنا؟

يأتي مع تثبيت MoviePy عبر الحزمة `imageio-ffmpeg`. لا تشغّل `pip install ffmpeg` كبديل للملف التنفيذي.

فحص `PATH`:

```
where.exe ffmpeg
```

النتيجة المتحققة: لا يوجد `ffmpeg` على `PATH`. الاستخراج نجح رغم ذلك لأن MoviePy تستخدم الملف داخل `imageio-ffmpeg`.

### كيف تتحقق؟

1. الأمر السابق يطبع مسارًا ينتهي بـ `ffmpeg-win-x86_64-v7.1.exe`
2. تشغيل استخراج حقيقي ينتج ملف صوت حجمه أكبر من صفر ويمكن فتحه

## 7. التثبيت

من مجلد المشروع `d:\project_lv3\Audio-Extractor-master`:

```
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
```

هذان الأمران تم تنفيذهما، وانتهى التثبيت بنجاح.

## 8. البيئة الافتراضية

لم تكن هناك بيئة افتراضية في المستودع. تم إنشاء `venv`، وهي مذكورة أصلًا في `.gitignore`.

لتشغيل الأوامر اللاحقة استخدم مفسر البيئة:

```
venv\Scripts\python.exe
```

إذا استخدمت `python extractor.py` من خارج البيئة وMoviePy غير مثبتة على Python العام، يتوقف التشغيل عند:

```
ModuleNotFoundError: No module named 'moviepy'
```

هذا ما حدث عند فحص Python العام قبل إنشاء `venv`.

## 9. أمر التشغيل

من مجلد المشروع:

```
venv\Scripts\python.exe extractor.py
```

هذا هو الأمر الذي فُتح به البرنامج الأصلي. لا تمرر وسائط. الملف نقطة الدخول الوحيدة، والحارس في آخره هو `if __name__ == "__main__"`.

## 10. اختيار الفيديو

عند التشغيل لا تظهر نافذة رئيسية. `main()` تنشئ `Tk()` ثم تستدعي `root.withdraw()`، فيظهر مباشرة مربع الحوار:

- العنوان: `Select the video file`
- الزر: `Open`
- الزر: `Cancel`
- مرشح النوع الظاهر في الحوار: عنصر واحد اسمه `Video Files`
- الامتدادات المكتوبة في الشفرة: `*.mp4;*.avi;*.mkv;*.flv;*.mov`

إلغاء الحوار ينهي `main()` من غير رسالة.

بعد اختيار الفيديو يظهر حوار مجلد عنوانه `Select the folder to save the video and audio`. يفتح على مجلد `output` كمكان افتراضي، ويمكن اختيار أي مجلد آخر. إلغاء هذا الحوار ينهي البرنامج من غير حفظ.

البرنامج ينسخ الفيديو نسخًا ثنائيًا إلى المجلد المختار:

```
<المجلد المختار>\<اسم الملف>
```

## 11. اختيار صيغة الصوت

بعد اختيار المجلد يظهر حوار `simpledialog.askstring`:

- العنوان: `Output Format`
- النص: `Enter desired audio format (e.g. mp3, wav):`
- القيمة الابتدائية: `mp3`
- الزران داخل الحوار: `OK` و`Cancel`

لا توجد قائمة منسدلة. الصيغة هي النص الذي يكتبه المستخدم، ويُلصَق كما هو بعد نقطة في اسم ملف الخرج.

تم التحقق من هذه النتائج على فيديو قصير فيه صوت:

| النص المدخل | النتيجة على هذا الجهاز |
| --- | --- |
| `mp3` | ملف MP3 صالح |
| `wav` | ملف WAV صالح |
| `ogg` | ملف OGG صالح |
| `flac` | ملف FLAC صالح |
| `m4a` | MoviePy تطبع `Done` لكن الملف لا يُنشأ |
| إلغاء الحوار (`None`) | رسالة خطأ، ولا يُنشأ ملف صوت صالح |

`ogg` و`flac` و`m4a` ليست خيارات ظاهرة في الواجهة. هي امتدادات يفهم قاموس MoviePy بعضًا منها إذا كتبها المستخدم بنفسه.

## 12. أين يُحفظ الخرج؟

المجلد الذي يختاره المستخدم في حوار المجلد. الحوار يفتح أولًا على `output` بجانب `extractor.py`، وهذا هو المجلد الافتراضي.

يُحفظ داخل ذلك المجلد ملفان:

- نسخة الفيديو بالاسم الأصلي
- ملف الصوت: `<اسم الفيديو من غير الامتداد>.<الصيغة>`

مثال إذا بقي المجلد الافتراضي:

```
output\longer_with_audio.mp4
output\longer_with_audio.mp3
```

رسالة النجاح تعرض مسار ملف الصوت. مجلدا `input` و`output` ما زالا يُنشآن عند التشغيل، و`output` هو المكان الذي يفتح عليه حوار الحفظ.

## 13. أخطاء ظهرت فعلًا

إلغاء اختيار الفيديو:

- السلوك: البرنامج يغلق بهدوء
- لا رسالة

فيديو من غير مسار صوتي (`test_data/videos/silent.mp4`):

- يطبع في الطرفية: `An error occurred: 'NoneType' object has no attribute 'write_audiofile'`
- يظهر مربع بعنوان `Error` ونصه: `Failed to extract audio. Please check the video file.`
- لا يُنشأ ملف صوت

ملف نصي أو بيانات غير صالحة:

- الطرفية تطبع خطأ FFmpeg: `Invalid data found when processing input`
- مربع `Error` نفسه
- النسخة تُنسخ أولًا إلى `input` ثم يفشل الاستخراج

ملف غير موجود:

- `An error occurred: '<path>' not found`
- الدالة تُرجع `False`

إلغاء حوار الصيغة:

- الاسم يصبح مثل `name.None`
- الطرفية: `MoviePy couldn't find the codec associated with the filename`
- مربع `Error`
- النسخة داخل `input` تبقى

مجلد خرج غير موجود، أو كتابة لا ينتج عنها ملف (مثل `m4a` على بناء FFmpeg هذا):

- قد تطبع MoviePy `MoviePy - Done.`
- `extract_audio_from_video` تُرجع `True` لأن MoviePy 2.2.1 لا تفحص رمز خروج FFmpeg في `FFMPEG_AudioWriter.close()`
- الملف قد لا يكون موجودًا
- المسار العادي `output\` لا يمر بهذه الحالة لأن البرنامج ينشئ المجلد عند الاستيراد

## 14. استكشاف الأخطاء

1. تأكد أن الأمر يُشغَّل من مجلد المشروع، لأن `input` و`output` يُنشآن في مجلد العمل الحالي.
2. استخدم `venv\Scripts\python.exe` حتى تُستورد MoviePy 2.2.1.
3. إذا لم يُفتح الحوار، جرّب فحص Tkinter في القسم 4.
4. إذا نجح الحوار وفشل الاستخراج، اقرأ سطر `An error occurred:` في الطرفية. مربع الرسالة لا يعرض سبب MoviePy.
5. إذا كانت الرسالة نجاحًا والمسار داخل `output`، تأكد أن حجم الملف أكبر من صفر وأنه يُفتح. النجاح المطبوع لا يكفي إذا كان مسار الخرج غير قابل للكتابة.
6. لا تثبّت FFmpeg يدويًا على هذا الجهاز ما دام المسار في القسم 6 موجودًا والاستخراج ينتج ملفًا صالحًا.
