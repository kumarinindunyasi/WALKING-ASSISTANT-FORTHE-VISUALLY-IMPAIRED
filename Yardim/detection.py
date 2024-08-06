import cv2
from ultralytics import YOLO
import pyttsx3

GREEN = (0, 255, 0)
RED = (0, 0, 255)

engine = pyttsx3.init()
voice_notifications = False

def detect_sign(img, model):
    sign_width = 0
    results = model(img)
    sign_type = None
    for result in results:
        boxes = result.boxes  # Boxes object for bbox outputs
        for box in boxes:
            if box.conf > 0.5:  # Confidence threshold
                x1, y1, x2, y2 = box.xyxy[0]  # Bounding box coordinates
                x, y, w, h = int(x1), int(y1), int(x2 - x1), int(y2 - y1)
                sign_type = model.names[int(box.cls)]
                cv2.rectangle(img, (x, y), (x + w, y + h), GREEN, 3)
                cv2.putText(
                    img=img,
                    text=sign_type.capitalize(),
                    org=(x, y + h + 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1,
                    color=RED,
                    thickness=2,
                    lineType=cv2.LINE_4,
                )
                sign_width = w
                if voice_notifications:
                    engine.say(sign_type.capitalize())
                    engine.runAndWait()
                return sign_type, sign_width
    return None, 0

def detect_pothole(img, model):
    results = model(img)
    pothole_detected = False
    for result in results:
        boxes = result.boxes  # Boxes object for bbox outputs
        for box in boxes:
            if box.conf > 0.5:  # Confidence threshold
                x1, y1, x2, y2 = box.xyxy[0]  # Bounding box coordinates
                x, y, w, h = int(x1), int(y1), int(x2 - x1), int(y2 - y1)
                cv2.rectangle(img, (x, y), (x + w, y + h), RED, 3)
                cv2.putText(
                    img=img,
                    text="Pothole",
                    org=(x, y + h + 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1,
                    color=RED,
                    thickness=2,
                    lineType=cv2.LINE_4,
                )
                pothole_detected = True
                if voice_notifications:
                    engine.say("Pothole detected")
                    engine.runAndWait()
    return pothole_detected

def focal_length(measured_distance, real_width, width_in_rf_img):
    focal_length_value = (width_in_rf_img * measured_distance) / real_width
    return focal_length_value

def distance_finder(focal_length, real_sign_width, sign_width_in_frame):
    distance = (real_sign_width * focal_length) / sign_width_in_frame
    return distance