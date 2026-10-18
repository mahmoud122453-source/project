# خريطة المشروع

المستودع المحلي ليس مستودع Git. نقطة الدخول الوحيدة: `python weather_app.py`. لا يوجد `if __name__ == "__main__"`، فاستيراد الملف يفتح النافذة.

```text
config.py          ثوابت: مفتاح، رابط، ألوان، صور، مدينة افتراضية
weather_app.py     الواجهة + الطلب + قراءة JSON + تحديث الملصقات
requirements.txt   requests و Pillow
assets/            background.png, search_icon.png, weather.ico, screenshot.png
```

## البنية

البرنامج سكربت واحد. الواجهة تُبنى عند تشغيل الملف، لا داخل دالة `main()`. الدوال:

| الدالة | الأسطر | من يستدعيها | تلمس API؟ | تلمس الواجهة؟ |
| --- | --- | --- | --- | --- |
| `get_weather(city_name=config.DEFAULT_CITY)` | 11–61 | الخيط، و `show_default_info` | نعم | نعم |
| `search_city()` | 64–71 | زر Search | لا، تبدأ الخيط | تقرأ Entry وتعطل الزر |
| `on_enter_press(event)` | 74–75 | `<Return>` | غير مباشر | تستدعي `search_city` |
| `resize_bg(event)` | 78–82 | لا أحد | لا | كانت ستغير الخلفية |
| `set_background(image_path)` | 85–93 | تشغيل الملف | لا | `bg_label` أو messagebox |
| `show_default_info()` | 96–97 | قبل `mainloop` | عبر `get_weather` | عبر `get_weather` |

لا توجد فئات. الطلب والتحليل والعرض غير مفصولة في الكود. في الشرح تُفصل إلى ثلاث خطوات حتى لو بقيت الدالة واحدة.

## تدفق الإعداد

```text
نظام التشغيل
  OPENWEATHER_API_KEY
        ↓
config.API_KEY = os.environ.get(...)
        ↓
إن غاب المتغير: النص YOUR_OPENWEATHERMAP_API_KEY
        ↓
weather_app يقرأ BASE_URL و DEFAULT_CITY والألوان ومسارات الصور
```

الألوان والمدينة الافتراضية ما زالت في `config.py` كما في المشروع الأصلي. التغيير الوحيد في الإعداد هو مصدر المفتاح.

## تدفق API

```text
city_name
  ↓
complete_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units=metric"
  ↓
requests.get(complete_url)     بلا headers وبلا timeout وبلا params
  ↓
response.json()
```

الرابط الفعلي بعد إخفاء المفتاح:

`http://api.openweathermap.org/data/2.5/weather?q=London&appid=REDACTED&units=metric`

الدمج يدوي. مدينة فيها `#` تجعل ما بعد `#` جزءًا لا يُرسل إلى الخادم. في الاختبار رجع HTTP 401.

## تدفق JSON

استجابة ناجحة، كما قيست:

```text
data["cod"]                         int 200
data["name"]                        اسم المدينة كما يعيده الخادم
data["main"]["temp"]                Celsius
data["main"]["pressure"]
data["main"]["humidity"]
data["wind"]["speed"]               m/s
data["weather"][0]["description"]
data["sys"]["country"]
data["sys"]["sunrise"]              Unix timestamp
data["sys"]["sunset"]
```

ثم التنسيق:

```text
description.capitalize()
datetime.fromtimestamp(sunrise).strftime("%H:%M:%S")   توقيت الجهاز
النص النهائي داخل info_label مع °C و hPa و % و m/s
```

عند النجاح يُمسح `city_entry` ويُكتب `data["name"]`. لذلك `paris` تصبح `Paris` و `ToKyO` تصبح `Tokyo`.

استجابة مدينة غير موجودة:

```text
HTTP 404
{"cod": "404", "message": "city not found"}
```

`cod` هنا `str`. المقارنة مع العدد `404` لا تختار فرع «Not Found».

## تدفق الواجهة

```text
Tk()
  ↓
iconbitmap("assets/weather.ico")          بلا try
  ↓
Label خلفية + set_background(...)
  ↓
Label العنوان، Entry، Button، Label النتيجة، Label التذييل
  ↓
show_default_info()
  ↓
mainloop()
```

عناصر الإدخال: `city_entry` وزر Search ومفتاح Enter. المخرجات: `info_label` ونص الزر ومحتوى صندوق المدينة.

## تدفق الخيط

البحث:

```text
search_city
  ↓
إذا كان النص غير فارغ
  ↓
الزر: disabled / Searching     على الخيط الرئيسي
  ↓
Thread(target=get_weather, args=(city_name,), daemon=False)
  ↓
Loading ثم sleep(3) ثم GET     على خيط العامل
  ↓
تعديل Label و Entry و Button   من خيط العامل أيضًا
```

البداية:

```text
show_default_info
  ↓
get_weather على الخيط الرئيسي
  ↓
sleep(3) + GET قبل mainloop
  ↓
حوالي 4 ثوانٍ قبل أن تصبح النافذة تفاعلية
```

## تدفق الخطأ

```text
نص فارغ
  → رسالة Enter city name...
  → لا HTTP

طلب أو JSON أو شبكة أو مفتاح
  → except Exception
  → Provide a valid city name to get info
  → الزر يعود normal / Search

صورة خلفية مفقودة
  → messagebox: Background image not found!

أيقونة أو مجلد عمل خاطئ
  → TclError ويتوقف البرنامج
```

الحالات التي قيست على الشبكة:

| الحالة | HTTP | cod | ما رأته الواجهة |
| --- | --- | --- | --- |
| London / New Delhi / Paris / Tokyo / Cairo / San Francisco | 200 | int 200 | بيانات الطقس |
| NotARealCityXYZ و Londn | 404 | str "404" | Provide a valid city name to get info |
| مفتاح غير صالح أو قيمة placeholder | 401 | int 401 | الرسالة العامة نفسها |
| استعلام مدينة فارغة مباشرة على API | 400 | str "400" | الواجهة لا ترسل هذا إذا كان الصندوق فارغًا |
| ثلاثة فراغات | 200 | int 200 | مدينة Xankandi, AZ |
| city@#$ | 401 | int 401 | الرسالة العامة، لأن المفتاح لا يصل مع الرابط |
| قطع اتصال مُحاكى بـ ConnectionError | لا استجابة | — | الرسالة العامة بعد sleep |

لم يظهر HTTP 429 أثناء الاختبار. المشروع نفسه لا يوثّق حدًا للاستدعاءات.

## تدفق البيانات الكامل

```text
المستخدم يكتب المدينة
  ↓
search_city أو on_enter_press أو show_default_info
  ↓
خيط للبحث فقط
  ↓
رابط OpenWeather
  ↓
HTTP response
  ↓
قاموس JSON
  ↓
قراءة المفاتيح المتداخلة
  ↓
تنسيق النص والوقت المحلي
  ↓
info_label و city_entry
  ↓
المستخدم
```
