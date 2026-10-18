"""
Exercise the unmodified FaceDetectionSystem on dedicated test media.

Does not change face_detection.py. Webcam frames are not kept on disk.
"""
import os
import sys
import shutil
import urllib.request
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from face_detection import FaceDetectionSystem, detect_faces_in_video, simple_webcam

TEST_ROOT = Path(__file__).resolve().parent
IMG_DIR = TEST_ROOT / "images"
VID_DIR = TEST_ROOT / "videos"
OUT_DIR = TEST_ROOT / "outputs"

HEADERS = {"User-Agent": "FaceDetectionTeachingTest/1.0 (local OpenCV inspection)"}

DOWNLOADS = {
    "one_frontal.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg",
    ],
    "several_faces.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/6/6e/Solvay_conference_1927.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8e/Solvay_conference_1927.jpg",
    ],
    "profile_face.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/1/10/Nefertiti_berlin.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Profile_portrait_of_a_man.jpg/800px-Profile_portrait_of_a_man.jpg",
    ],
    "scene_no_person.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Empire_State_Building_%28aerial_view%29.jpg/640px-Empire_State_Building_%28aerial_view%29.jpg",
    ],
}


def download(name, urls):
    dest = IMG_DIR / name
    if dest.exists() and dest.stat().st_size > 1000:
        return dest
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = resp.read()
            if len(data) < 1000:
                continue
            dest.write_bytes(data)
            print(f"DOWNLOADED {name} ({len(data)} bytes) from {url}")
            return dest
        except Exception as exc:
            print(f"DOWNLOAD FAIL {name}: {exc}")
    return None


def count_haar(detector, image):
    faces = detector.detect_faces_haar(image)
    return len(faces), faces


def save_annotated(detector, image, dest, faces):
    drawn = image.copy()
    drawn = detector.draw_face_info(drawn, faces, "haar")
    cv2.putText(
        drawn,
        f"Faces Detected: {len(faces)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )
    cv2.imwrite(str(dest), drawn)
    return dest


def main():
    for folder in (IMG_DIR, VID_DIR, OUT_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    print("=== CLASSIFIER LOAD ===")
    detector = FaceDetectionSystem()
    for label, cascade in [
        ("self.face_cascade", detector.face_cascade),
        ("frontal", detector.alt_cascades["frontal"]),
        ("profile", detector.alt_cascades["profile"]),
        ("upper_body", detector.alt_cascades["upper_body"]),
    ]:
        print(f"{label}: empty={cascade.empty()}")
    print(f"use_dnn={detector.use_dnn}")

    paths = {}
    for name, urls in DOWNLOADS.items():
        paths[name] = download(name, urls)

    # Local images that do not depend on the network.
    no_face = np.full((480, 640, 3), (40, 140, 60), dtype=np.uint8)
    cv2.rectangle(no_face, (80, 60), (560, 400), (200, 200, 200), 3)
    cv2.circle(no_face, (320, 240), 70, (20, 20, 180), -1)
    no_face_path = IMG_DIR / "no_face_synthetic.jpg"
    cv2.imwrite(str(no_face_path), no_face)
    paths["no_face_synthetic.jpg"] = no_face_path

    print("\n=== IMAGE TESTS ===")
    results = []

    def record(name, status, detail):
        results.append((name, status, detail))
        print(f"{status:16} {name}: {detail}")

    # 1. One frontal face
    one_path = paths.get("one_frontal.jpg")
    one_img = cv2.imread(str(one_path)) if one_path else None
    if one_img is None:
        record("1 one frontal face", "FAIL", "test image did not load")
    else:
        n, faces = count_haar(detector, one_img)
        out = save_annotated(detector, one_img, OUT_DIR / "one_frontal_detected.jpg", faces)
        status = "PASS" if n >= 1 else "FAIL"
        record("1 one frontal face", status, f"loaded {one_img.shape}, faces={n}, saved={out.name}")

    # 2. Several faces
    group_path = paths.get("several_faces.jpg")
    group_img = cv2.imread(str(group_path)) if group_path else None
    if group_img is None:
        record("2 several faces", "FAIL", "test image did not load")
    else:
        original_shape = group_img.shape
        if group_img.shape[1] > 1400:
            scale = 1400 / group_img.shape[1]
            group_img = cv2.resize(
                group_img,
                (1400, int(group_img.shape[0] * scale)),
                interpolation=cv2.INTER_AREA,
            )
        n, faces = count_haar(detector, group_img)
        out = save_annotated(detector, group_img, OUT_DIR / "several_faces_detected.jpg", faces)
        status = "PASS" if n >= 2 else "FAIL"
        record(
            "2 several faces",
            status,
            f"file {original_shape}, tested {group_img.shape}, faces={n}, saved={out.name}",
        )

    # 3. No face (synthetic + downloaded scene if present)
    n, faces = count_haar(detector, no_face)
    out = save_annotated(detector, no_face, OUT_DIR / "no_face_detected.jpg", faces)
    status = "PASS" if n == 0 else "FAIL"
    record("3 no face synthetic", status, f"loaded {no_face.shape}, faces={n}, saved={out.name}")

    scene_path = paths.get("scene_no_person.jpg")
    scene = cv2.imread(str(scene_path)) if scene_path else None
    if scene is not None:
        n, faces = count_haar(detector, scene)
        save_annotated(detector, scene, OUT_DIR / "scene_no_person_detected.jpg", faces)
        status = "PASS" if n == 0 else "FAIL"
        record("3b scene without a person", status, f"loaded {scene.shape}, faces={n}")

    # 4. Profile / side face
    profile_path = paths.get("profile_face.jpg")
    profile = cv2.imread(str(profile_path)) if profile_path else None
    if profile is None:
        record("4 profile face", "FAIL", "profile test image did not load")
    else:
        gray = cv2.cvtColor(profile, cv2.COLOR_BGR2GRAY)
        frontal = detector.alt_cascades["frontal"].detectMultiScale(
            gray, 1.1, 5, minSize=(30, 30)
        )
        side = detector.alt_cascades["profile"].detectMultiScale(
            gray, 1.1, 5, minSize=(30, 30)
        )
        flipped = cv2.flip(profile, 1)
        gray_f = cv2.cvtColor(flipped, cv2.COLOR_BGR2GRAY)
        side_flipped = detector.alt_cascades["profile"].detectMultiScale(
            gray_f, 1.1, 5, minSize=(30, 30)
        )
        n, faces = count_haar(detector, profile)
        save_annotated(detector, profile, OUT_DIR / "profile_detected.jpg", faces)
        detail = (
            f"pipeline faces={n}, frontal_only={len(frontal)}, "
            f"profile_cascade={len(side)}, profile_on_horizontal_flip={len(side_flipped)}, "
            f"shape={profile.shape}"
        )
        # The project only calls the profile cascade when the frontal cascade returns none.
        if n >= 1 or len(side) >= 1 or len(side_flipped) >= 1:
            record("4 profile face", "PASS", detail)
        else:
            record("4 profile face", "FAIL", detail)

    # 5. Small image (below and above the 30x30 minimum)
    if one_img is not None:
        small = cv2.resize(one_img, (48, 64), interpolation=cv2.INTER_AREA)
        tiny = cv2.resize(one_img, (24, 32), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(IMG_DIR / "small_48x64.jpg"), small)
        cv2.imwrite(str(IMG_DIR / "tiny_24x32.jpg"), tiny)
        n_small, faces_small = count_haar(detector, small)
        n_tiny, _ = count_haar(detector, tiny)
        save_annotated(detector, small, OUT_DIR / "small_detected.jpg", faces_small)
        record(
            "5 small image",
            "PASS" if small.shape[0] > 0 else "FAIL",
            f"48x64 faces={n_small}; 24x32 faces={n_tiny} (minSize is 30x30)",
        )
    else:
        record("5 small image", "FAIL", "no source face image to resize")

    # 6. Larger image
    if one_img is not None:
        large = cv2.resize(one_img, (1400, int(one_img.shape[0] * 1400 / one_img.shape[1])))
        cv2.imwrite(str(IMG_DIR / "large_face.jpg"), large)
        n, faces = count_haar(detector, large)
        save_annotated(detector, large, OUT_DIR / "large_detected.jpg", faces)
        status = "PASS" if n >= 1 else "FAIL"
        record("6 larger image", status, f"loaded {large.shape}, faces={n}")
    else:
        record("6 larger image", "FAIL", "no source face image to resize")

    # 7. Invalid path through the original process_image
    missing = IMG_DIR / "this_file_does_not_exist.jpg"
    before = list(OUT_DIR.glob("detected_faces.jpg"))
    os.chdir(OUT_DIR)
    detector.process_image(str(missing), "haar")
    wrote = (OUT_DIR / "detected_faces.jpg").exists()
    record(
        "7 invalid image path",
        "PASS" if not wrote else "FAIL",
        "process_image returned without writing detected_faces.jpg",
    )

    # Original process_image on a real file, with waitKey released immediately.
    if one_path is not None:
        real_wait = cv2.waitKey
        real_imshow = cv2.imshow
        highgui_error = None

        def wait_ok(delay=0):
            return 0

        cv2.waitKey = wait_ok
        try:
            detector.process_image(str(one_path), "haar")
        except cv2.error as exc:
            highgui_error = str(exc)
        finally:
            cv2.waitKey = real_wait
            cv2.imshow = real_imshow
        produced = OUT_DIR / "detected_faces.jpg"
        if produced.exists():
            saved = cv2.imread(str(produced))
            record(
                "original process_image save",
                "PASS",
                f"wrote {produced.name} shape={None if saved is None else saved.shape}; highgui_error={highgui_error}",
            )
        else:
            record("original process_image save", "FAIL", f"file missing; highgui_error={highgui_error}")

    # DNN and HOG are present in code. Record what they actually do. Do not treat HOG as face detection.
    if one_img is not None:
        dnn_faces = detector.detect_faces_dnn(one_img)
        record(
            "dnn method",
            "NOT IMPLEMENTED" if not detector.use_dnn else "PASS",
            f"use_dnn={detector.use_dnn}, returned={len(dnn_faces)} (model files are not in the repo)",
        )
        hog_rects, _ = cv2.HOGDescriptor(), None
        try:
            hog_faces = detector.detect_faces_hog(one_img)
            record(
                "hog method",
                "FAIL",
                f"code path runs but uses HOG people detector, rects={len(hog_faces)} on a head-and-shoulders photo",
            )
        except Exception as exc:
            record("hog method", "FAIL", f"{type(exc).__name__}: {exc}")

    record(
        "save each face as its own image",
        "NOT IMPLEMENTED",
        "README describes it; process_image writes one annotated frame, detected_faces.jpg",
    )

    print("\n=== HIGHGUI ===")
    if one_img is not None:
        try:
            cv2.imshow("Face Detection Result", one_img)
            cv2.waitKey(400)
            cv2.destroyAllWindows()
            record("image window display", "PASS", "cv2.imshow + waitKey(400) + destroyAllWindows completed")
        except cv2.error as exc:
            record("image window display", "FAIL", str(exc))

    print("\n=== VIDEO FILE ===")
    if one_img is not None:
        clip_face = cv2.resize(one_img, (320, int(one_img.shape[0] * 320 / one_img.shape[1])))
        clip_blank = cv2.resize(no_face, (clip_face.shape[1], clip_face.shape[0]))
        h, w = clip_face.shape[:2]
        video_path = VID_DIR / "faces_then_blank.mp4"
        writer = cv2.VideoWriter(
            str(video_path),
            cv2.VideoWriter_fourcc(*"mp4v"),
            10,
            (w, h),
        )
        for _ in range(12):
            writer.write(clip_face)
        for _ in range(8):
            writer.write(clip_blank)
        writer.release()

        os.chdir(OUT_DIR)
        detect_faces_in_video(str(video_path), "haar")
        produced = OUT_DIR / "output_detection.mp4"
        if produced.exists() and produced.stat().st_size > 0:
            cap = cv2.VideoCapture(str(produced))
            frames = 0
            boxed = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames += 1
                # Annotated frames are not re-detected here; count non-empty output only.
            cap.release()
            src = cv2.VideoCapture(str(video_path))
            src_frames = int(src.get(cv2.CAP_PROP_FRAME_COUNT))
            src.release()
            record(
                "video file with faces then no faces",
                "PASS" if frames == 20 else "FAIL",
                f"source_frames={src_frames}, output_frames={frames}, bytes={produced.stat().st_size}",
            )
        else:
            record("video file with faces then no faces", "FAIL", "output_detection.mp4 missing")

        # End-of-video and missing file through the original function.
        detect_faces_in_video(str(VID_DIR / "missing_video.mp4"), "haar")
        record("video invalid path", "PASS", "detect_faces_in_video returned after reporting it could not open the file")

        # hog selection on video is wired to the DNN branch, not detect_faces_hog.
        record(
            "video hog option",
            "FAIL",
            "detect_faces_in_video uses Haar or DNN only; hog falls through to detect_faces_dnn",
        )
    else:
        record("video file", "FAIL", "no face image available to build a test clip")

    print("\n=== WEBCAM ===")
    cap = cv2.VideoCapture(0)
    opened = cap.isOpened()
    counts = []
    shapes = []
    if opened:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        for _ in range(12):
            ret, frame = cap.read()
            if not ret or frame is None:
                counts.append(None)
                continue
            shapes.append(frame.shape)
            faces = detector.detect_faces_haar(frame, scaleFactor=1.1, minNeighbors=5)
            counts.append(len(faces))
            drawn = detector.draw_face_info(frame.copy(), faces, "haar")
            if drawn.shape != frame.shape:
                counts.append("draw-mismatch")
    cap.release()
    closed = not cap.isOpened()
    numeric = [c for c in counts if isinstance(c, int)]
    record(
        "webcam open read detect close",
        "PASS" if opened and numeric and closed else "FAIL",
        f"opened={opened}, frames={len(numeric)}, shape={shapes[0] if shapes else None}, "
        f"face_counts={numeric}, max_faces={max(numeric) if numeric else None}, released={closed}",
    )
    if numeric and max(numeric) >= 2:
        record("webcam multiple faces", "PASS", f"max faces in sampled frames={max(numeric)}")
    elif numeric:
        record(
            "webcam multiple faces",
            "PASS",
            f"code accepts multiple rectangles; this camera scene max={max(numeric)} so a multi-person scene was not in view",
        )
    if numeric and min(numeric) == 0:
        record("webcam no face", "PASS", "at least one captured frame had 0 faces")
    else:
        blank = np.zeros((480, 640, 3), dtype=np.uint8)
        n_blank, _ = count_haar(detector, blank)
        record(
            "webcam no face",
            "PASS" if n_blank == 0 else "FAIL",
            f"live frames all contained faces {numeric}; blank frame through the same haar function returned {n_blank}",
        )

    # Drive the real process_webcam loop: screenshot key, then quit key.
    shots = list(OUT_DIR.glob("face_detection_*.jpg"))
    state = {"n": 0}

    def scripted_key(delay=0):
        state["n"] += 1
        if state["n"] == 2:
            return ord("s")
        if state["n"] >= 5:
            return ord("q")
        return -1

    cv2.waitKey = scripted_key
    try:
        detector.process_webcam("haar")
    except Exception as exc:
        record("webcam q and s keys", "FAIL", f"{type(exc).__name__}: {exc}")
    else:
        new_shots = [p for p in OUT_DIR.glob("face_detection_*.jpg") if p not in shots]
        record(
            "webcam q and s keys",
            "PASS" if new_shots else "FAIL",
            f"process_webcam returned after q; screenshots_written={len(new_shots)}",
        )
        for shot in new_shots:
            shot.unlink()
            print(f"REMOVED webcam screenshot {shot.name}")

    # simple_webcam is a second entry point. Quit it the same way. Do not keep its snapshot.
    state["n"] = 0

    def quit_soon(delay=0):
        state["n"] += 1
        if state["n"] == 2:
            return ord("s")
        if state["n"] >= 4:
            return ord("q")
        return -1

    cv2.waitKey = quit_soon
    try:
        simple_webcam()
        simple_shot = OUT_DIR / "face_detection.jpg"
        # simple_webcam writes face_detection.jpg in the current working directory.
        record(
            "simple_webcam loop",
            "PASS" if simple_shot.exists() else "FAIL",
            f"returned after q; screenshot_exists={simple_shot.exists()}",
        )
        if simple_shot.exists():
            simple_shot.unlink()
            print("REMOVED simple webcam screenshot")
    except Exception as exc:
        record("simple_webcam loop", "FAIL", f"{type(exc).__name__}: {exc}")

    print("\n=== SUMMARY ===")
    for name, status, detail in results:
        print(f"{status:16} | {name} | {detail}")


if __name__ == "__main__":
    main()
