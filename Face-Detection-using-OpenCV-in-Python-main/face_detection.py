import cv2
import numpy as np
import time
from datetime import datetime

class FaceDetectionSystem:
    def __init__(self):
        # Multiple face detection methods
        self.methods = {
            'haar': self.detect_faces_haar,
            'dnn': self.detect_faces_dnn,
            'hog': self.detect_faces_hog
        }
        
        # Load Haar Cascade (Fast but less accurate)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Load alternative cascades for better detection
        self.alt_cascades = {
            'frontal': cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'),
            'profile': cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml'),
            'upper_body': cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
        }
        
        # Load DNN face detector (More accurate)
        try:
            self.face_dnn = cv2.dnn.readNetFromCaffe(
                'deploy.prototxt',
                'res10_300x300_ssd_iter_140000.caffemodel'
            )
            self.use_dnn = True
            print("✅ DNN face detector loaded!")
        except:
            self.use_dnn = False
            print("⚠️ DNN models not found, using Haar Cascade only")
        
        # Statistics
        self.total_faces_detected = 0
        self.frame_count = 0
        self.fps = 0
        self.last_time = time.time()
        
    def detect_faces_haar(self, frame, scaleFactor=1.1, minNeighbors=5):
        """Haar Cascade based face detection (Fast)"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Try multiple cascades for better detection
        faces = self.alt_cascades['frontal'].detectMultiScale(
            gray, scaleFactor, minNeighbors, minSize=(30, 30)
        )
        
        # Frontal detectMultiScale returns () when it finds nothing.
        # vstack cannot join that empty tuple to the profile rectangles.
        if len(faces) == 0:
            faces_profile = self.alt_cascades['profile'].detectMultiScale(
                gray, scaleFactor, minNeighbors, minSize=(30, 30)
            )
            if len(faces_profile) > 0:
                faces = faces_profile
        
        return faces
    
    def detect_faces_dnn(self, frame, confidence_threshold=0.5):
        """Deep Learning based face detection (Accurate)"""
        if not self.use_dnn:
            return []
        
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))
        self.face_dnn.setInput(blob)
        detections = self.face_dnn.forward()
        
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > confidence_threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                startX, startY = max(0, startX), max(0, startY)
                endX, endY = min(w, endX), min(h, endY)
                faces.append((startX, startY, endX - startX, endY - startY))
        
        return faces
    
    def detect_faces_hog(self, frame):
        """HOG based face detection (Fallback)"""
        # Using OpenCV's HOG descriptor
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        faces, _ = hog.detectMultiScale(frame)
        return faces
    
    def draw_face_info(self, frame, faces, method='haar'):
        """Draw bounding boxes and information"""
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
                  (255, 0, 255), (0, 255, 255)]
        
        for i, (x, y, w, h) in enumerate(faces):
            color = colors[i % len(colors)]
            
            # Draw rectangle with gradient effect
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
            
            # Add corner effects
            corner_len = min(20, w//4, h//4)
            cv2.line(frame, (x, y), (x+corner_len, y), color, 3)
            cv2.line(frame, (x, y), (x, y+corner_len), color, 3)
            cv2.line(frame, (x+w, y), (x+w-corner_len, y), color, 3)
            cv2.line(frame, (x+w, y), (x+w, y+corner_len), color, 3)
            cv2.line(frame, (x, y+h), (x+corner_len, y+h), color, 3)
            cv2.line(frame, (x, y+h), (x, y+h-corner_len), color, 3)
            cv2.line(frame, (x+w, y+h), (x+w-corner_len, y+h), color, 3)
            cv2.line(frame, (x+w, y+h), (x+w, y+h-corner_len), color, 3)
            
            # Background for text
            label = f"Face {i+1}"
            (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x, y-label_h-10), (x+label_w+10, y), color, -1)
            
            # Put text
            cv2.putText(frame, label, (x+5, y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
            # Add face number circle
            cv2.circle(frame, (x+15, y+15), 15, color, -1)
            cv2.putText(frame, str(i+1), (x+8, y+22), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        return frame
    
    def calculate_fps(self):
        """Calculate frames per second"""
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_time >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.last_time = current_time
        return self.fps
    
    def process_webcam(self, method='haar'):
        """Process webcam feed"""
        cap = cv2.VideoCapture(0)
        
        # Set resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("\n" + "="*60)
        print("🎯 ADVANCED FACE DETECTION SYSTEM")
        print("="*60)
        print(f"Detection Method: {method.upper()}")
        print("Controls:")
        print("  'q' - Quit")
        print("  's' - Save screenshot")
        print("  'm' - Change detection method")
        print("  'r' - Reset statistics")
        print("  '1-3' - Switch method (1:Haar, 2:DNN, 3:HOG)")
        print("-"*60)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Camera error!")
                break
            
            # Detect faces
            if method == 'haar':
                faces = self.detect_faces_haar(frame, scaleFactor=1.1, minNeighbors=5)
            elif method == 'dnn':
                faces = self.detect_faces_dnn(frame, confidence_threshold=0.5)
            else:
                faces = self.detect_faces_hog(frame)
            
            # Update statistics
            self.total_faces_detected += len(faces)
            fps = self.calculate_fps()
            
            # Draw results
            frame = self.draw_face_info(frame, faces, method)
            
            # Display information panel
            info_panel = np.zeros((120, frame.shape[1], 3), dtype=np.uint8)
            
            # Method info
            method_colors = {'haar': (100, 200, 100), 'dnn': (100, 100, 200), 'hog': (200, 100, 100)}
            cv2.putText(info_panel, f"Method: {method.upper()}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, method_colors.get(method, (255,255,255)), 2)
            
            # Statistics
            cv2.putText(info_panel, f"Faces: {len(faces)} | Total: {self.total_faces_detected}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(info_panel, f"FPS: {fps} | Frame: {self.frame_count}", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Combine panels
            display = np.vstack([info_panel, frame])
            
            cv2.imshow('Advanced Face Detection', display)
            
            # Key handling
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"face_detection_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Screenshot saved: {filename}")
            elif key == ord('m') or key == ord('1'):
                method = 'haar'
                print("🔄 Switched to HAAR Cascade method")
            elif key == ord('2'):
                if self.use_dnn:
                    method = 'dnn'
                    print("🔄 Switched to DNN method")
                else:
                    print("❌ DNN method not available")
            elif key == ord('3'):
                method = 'hog'
                print("🔄 Switched to HOG method")
            elif key == ord('r'):
                self.total_faces_detected = 0
                print("🔄 Statistics reset!")
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Final statistics
        print("\n📊 Session Summary:")
        print(f"Total faces detected: {self.total_faces_detected}")
        print(f"Average FPS: {fps}")
    
    def fit_for_display(self, image, max_width=1280, max_height=720):
        """Return a smaller copy when the photo is larger than the window."""
        height, width = image.shape[:2]
        scale = min(max_width / width, max_height / height, 1.0)
        if scale == 1.0:
            return image
        return cv2.resize(
            image,
            (max(1, int(width * scale)), max(1, int(height * scale))),
            interpolation=cv2.INTER_AREA,
        )

    def process_image(self, image_path, method='haar'):
        """Process single image"""
        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ Could not load image: {image_path}")
            return
        
        # Detect faces
        if method == 'haar':
            faces = self.detect_faces_haar(img)
        elif method == 'dnn':
            faces = self.detect_faces_dnn(img)
        else:
            faces = self.detect_faces_hog(img)
        
        # Draw results
        img = self.draw_face_info(img, faces, method)
        
        # Add info. Scale the text with the photo so it stays readable after fitting.
        font_scale = max(0.8, max(img.shape[0], img.shape[1]) / 900)
        text_y = max(30, int(28 * font_scale))
        cv2.putText(img, f"Faces Detected: {len(faces)}", (10, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), max(2, int(font_scale)))
        
        # Save the full image. Show a copy that fits the screen, otherwise a
        # large photo opens at 1:1 and only its top-left corner is visible.
        output_path = "detected_faces.jpg"
        cv2.imwrite(output_path, img)
        display = self.fit_for_display(img)
        cv2.namedWindow('Face Detection Result', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Face Detection Result', display.shape[1], display.shape[0])
        cv2.imshow('Face Detection Result', display)
        print(f"✅ Processed image saved: {output_path}")
        print(f"🎯 Total faces detected: {len(faces)}")
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Face detection in video file
def detect_faces_in_video(video_path, method='haar'):
    """Process video file"""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Could not open video: {video_path}")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Video writer
    out = cv2.VideoWriter('output_detection.mp4', 
                         cv2.VideoWriter_fourcc(*'mp4v'), 
                         fps, (width, height))
    
    face_detector = FaceDetectionSystem()
    frame_count = 0
    faces_detected = 0
    
    print(f"\n🎬 Processing video: {video_path}")
    print(f"Total frames: {total_frames}")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect faces
        if method == 'haar':
            faces = face_detector.detect_faces_haar(frame)
        else:
            faces = face_detector.detect_faces_dnn(frame)
        
        faces_detected += len(faces)
        frame = face_detector.draw_face_info(frame, faces, method)
        
        # Add frame counter
        cv2.putText(frame, f"Frame: {frame_count}/{total_frames}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        out.write(frame)
        
        # Show progress
        if frame_count % 100 == 0:
            print(f"Processing: {frame_count}/{total_frames} frames")
        
        frame_count += 1
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"\n✅ Video processing complete!")
    print(f"Total faces detected: {faces_detected}")
    print(f"Output saved: output_detection.mp4")

# Main menu
def main():
    detector = FaceDetectionSystem()
    
    while True:
        print("\n" + "="*50)
        print("🎯 FACE DETECTION SYSTEM")
        print("="*50)
        print("1. Webcam (Real-time)")
        print("2. Single Image")
        print("3. Video File")
        print("4. Compare Methods")
        print("5. Exit")
        print("-"*50)
        
        choice = input("Select option (1-5): ")
        
        if choice == '1':
            method = input("Detection method (haar/dnn/hog): ").lower()
            detector.process_webcam(method)
        
        elif choice == '2':
            path = input("Enter image path: ")
            method = input("Detection method (haar/dnn/hog): ").lower()
            detector.process_image(path, method)
        
        elif choice == '3':
            path = input("Enter video path: ")
            method = input("Detection method (haar/dnn/hog): ").lower()
            detect_faces_in_video(path, method)
        
        elif choice == '4':
            print("\n📊 Method Comparison:")
            print("1. Haar Cascade - Fast, works on CPU, less accurate")
            print("2. DNN - Accurate, needs GPU for best performance")
            print("3. HOG - Good balance of speed and accuracy")
        
        elif choice == '5':
            print("\n👋 Thank you for using Face Detection System!")
            break
        
        else:
            print("❌ Invalid choice!")

# Simple webcam version (Original enhanced)
def simple_webcam():
    """Simple webcam face detection with multiple cascades"""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    
    cap = cv2.VideoCapture(0)
    
    print("\n🎥 Simple Face Detection with Features")
    print("Press 'q' to quit | 's' for screenshot")
    
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        
        for (x, y, w, h) in faces:
            # Face rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
            
            # Face region
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            # Detect eyes
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            
            # Detect smile
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.7, 20)
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)
            
            # Text
            cv2.putText(frame, f'Face Detected', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Face count
            cv2.putText(frame, f'Faces: {len(faces)}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Face Detection', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite("face_detection.jpg", frame)
            print("📸 Screenshot saved!")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Choose mode
    print("Select Mode:")
    print("1. Advanced System (with menu)")
    print("2. Simple Webcam (original enhanced)")
    
    mode = input("Choice (1/2): ")
    
    if mode == '2':
        simple_webcam()
    else:
        main()