# خريطة المشروع

## هيكل المستودع

```text
Gesture-Volume-Control-using-MediaPipe-and-OpenCV-master
├── Gesture_Volume_Control.py    نقطة الدخول. سكربت بلا أصناف
├── HandTrackingModule.py        HandDetector حول MediaPipe
├── requirements.txt             إصدارات التشغيل المتحقَّق منها
├── README.md
├── LICENSE                      MIT، Pushtogithub23، 2024
├── RUN_GUIDE.md
├── TEACHING_GUIDE.md
├── FILE_TEACHING_ORDER.md
└── PROJECT_MAP.md
```

لا توجد مجلدات أصول أو لقطات أو إعداد. `.venv` بيئة محلية وليست جزءًا من مصدر المشروع.

## العلاقات بين الوحدات

```text
Gesture_Volume_Control.py
    ├── cv2            الكاميرا والرسم والعرض
    ├── numpy          المسافة و interp
    ├── comtypes       CLSCTX_ALL
    ├── pycaw          مخرج Windows
    └── HandTrackingModule.HandDetector
            └── mediapipe.solutions.hands
            └── mediapipe.solutions.drawing_utils
```

تطبيق الصوت لا يستدعي `fingersUp` ولا `release` ولا `main`.

## تدفق الكاميرا

```text
VideoCapture(0)
    → isOpened وإلا Exception
    → while cap.isOpened
        → read
        → إن فشل ret: break
        → معالجة
        → flip
        → شريط الصوت
        → imshow("Hand")
        → waitKey(1)
        → p: break
    → cap.release()
    → destroyAllWindows()
```

## تدفق MediaPipe

```text
إطار BGR
    → cvtColor إلى RGB
    → Hands.process
    → results.multi_hand_landmarks أو لا شيء
    → لكل يد، إن كان draw=True:
          draw_landmarks(frame, hand, HAND_CONNECTIONS)
```

المنشئ في التطبيق: `detectionCon=0.7` و`trackCon=0.7`. باقي القيم من افتراضي الصنف: `mode=False` و`maxHands=2` و`complexity=1`.

الرسم يستخدم اليدين المكتشفتين. حساب الصوت يستخدم اليد `handNo=0` فقط.

## تدفق المعالم

```text
hand.landmark[id]
    x, y معيارية
    z موجودة على الكائن ولا تُحفظ
        → cx = int(x * عرض الإطار)
        → cy = int(y * ارتفاع الإطار)
        → landmarks[id] = (cx, cy)
```

تطبيق الصوت يقرأ:

```text
landmarks[4] → (x1, y1) طرف الإبهام
landmarks[8] → (x2, y2) طرف السبابة
```

## تدفق المسافة

```text
(x2 - x1, y2 - y1)
    → np.linalg.norm
    → length بالبكسل
    → cv.line من (x1, y1) إلى (x2, y2)
```

## تدفق التحويل

```text
length
    → interp [20, 200] → [min_vol, max_vol]  → vol بالديسيبل
    → interp [20, 200] → [400, 150]          → vol_bar
    → interp [20, 200] → [0, 100]            → vol_per
```

خارج [20, 200] تُثبَّت النتيجة على الطرف الأقرب.

## تدفق PyCaw

```text
GetSpeakers()
    → Activate(IAudioEndpointVolume, CLSCTX_ALL)
        → QueryInterface(IAudioEndpointVolume)
            → GetVolumeRange()[:2]  → min_vol, max_vol
            → SetMasterVolumeLevel(vol, None)
                → مخرج التشغيل الافتراضي في Windows
```

على الجهاز المختبَر المدى `(-65.25, 0.0)` dB. لا يُستدعى كتم الصوت.

إذا كانت `landmarks` فارغة تُتخطى هذه الخطوة الأخيرة، ويبقى آخر مستوى ضبطه البرنامج أو المستوى الذي كان عليه النظام قبل ظهور اليد.

## تدفق العرض

```text
قلب أفقي للإطار
    → أخضر إذا vol_per <= 70 وإلا أحمر
    → rectangle إطار (50,150)-(85,400)
    → rectangle ممتلئ من (50, vol_bar) إلى (85, 400)
    → putText النسبة عند (45, 140)
    → imshow
```

القيم الابتدائية قبل أي يد: `vol=0` و`vol_bar=400` و`vol_per=0`، فيظهر شريط فارغ ونص `0 %` إلى أن تُكتشف يد.

## المسار الكامل

```text
إيماءة الإبهام والسبابة
    → إطار الكاميرا
        → MediaPipe Hands
            → المعلمان 4 و 8 بالبكسل
                → length
                    → vol بالديسيبل + vol_per للشاشة
                        → SetMasterVolumeLevel
                            → مستوى صوت Windows
                        → شريط ونص على النافذة Hand
```
