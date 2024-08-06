from ultralytics import YOLO
import cv2
import tkinter as tk
from tkinter import ttk, Label, Button, Entry, filedialog
from PIL import Image, ImageTk
import pyttsx3
import webbrowser
import speech_recognition as sr
import threading

# Constants
KNOWN_DISTANCE = 138  # centimeter
KNOWN_WIDTH = 29  # centimeter
LAMP_KNOWN_DISTANCE = 100  # centimeter
LAMP_KNOWN_WIDTH = 18  # centimeter
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX

# Load the YOLO models
sign_model = YOLO(r"C:\Users\doa\Downloads\best (8).pt")
pothole_model = YOLO(r"C:\Users\doa\Downloads\best (9).pt")  # cukur modeli

# Trafik isareti isimleri ve referans genislikleri (cm cinsinden)
class_names = [
    "donel kavsak", "dur levhasi", "durak", "duraklamak park yasak", "gidis donus",
    "girisi olmayan yol", "ileri mecburi", "ileri sag mecburi", "ileri sol mecburi",
    "lamba kirmizi", "lamba sari", "lamba yesil", "park edilebilir", "park engelli",
    "park yasak", "park yasak mavi", "sag mecburi", "saga donulmez", "sagdan gidin",
    "sola donulmez", "yaya gecidi"
]
reference_widths = {
    "donel kavsak": 50, "dur levhasi": 28, "durak": 50, "duraklamak park yasak": 50, "gidis donus": 50,
    "girisi olmayan yol": 50, "ileri mecburi": 50, "ileri sag mecburi": 50, "ileri sol mecburi": 50,
    "lamba kirmizi": 29, "lamba sari": 29, "lamba yesil": 29, "park edilebilir": 50, "park engelli": 50,
    "park yasak": 50, "park yasak mavi": 50, "sag mecburi": 50, "saga donulmez": 50, "sagdan gidin": 50,
    "sola donulmez": 50, "yaya gecidi": 50
}

# Pyttsx3 sesli bildirim motorunu baslatin
engine = pyttsx3.init()

# Ses motoru özelliklerini belirleyin
voices = engine.getProperty('voices')
for voice in voices:
    if 'tr_TR' in voice.id:  # Turkce ses varsa secin
        engine.setProperty('voice', voice.id)
        break

voice_notifications = False
last_notified = None

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
                return sign_type, sign_width
    return None, 0

def detect_potholes(img, model):
    results = model(img)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            if box.conf > 0.5:  # Confidence threshold
                x1, y1, x2, y2 = box.xyxy[0]
                x, y, w, h = int(x1), int(y1), int(x2 - x1), int(y2 - y1)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
                cv2.putText(
                    img=img,
                    text="Cukur",
                    org=(x, y + h + 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1,
                    color=(255, 0, 0),
                    thickness=2,
                    lineType=cv2.LINE_4,
                )
                if voice_notifications:
                    threading.Thread(target=speak_notification, args=("Cukur",)).start()

def speak_notification(text):
    engine.say(text)
    engine.runAndWait()

def focal_length(measured_distance, real_width, width_in_rf_img):
    focal_length_value = (width_in_rf_img * measured_distance) / real_width
    return focal_length_value

def distance_finder(focal_length, real_sign_width, sign_width_in_frame):
    distance = (real_sign_width * focal_length) / sign_width_in_frame
    return distance

# Read reference images
ref_img_sign = cv2.imread("Ref_img_stop.jpg")
ref_img_lamp = cv2.imread("Ref_img_lamp.jpg")

_, ref_img_sign_width = detect_sign(ref_img_sign, sign_model)
sign_focal_length = focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, ref_img_sign_width)

_, ref_img_lamp_width = detect_sign(ref_img_lamp, sign_model)
lamp_focal_length = focal_length(LAMP_KNOWN_DISTANCE, LAMP_KNOWN_WIDTH, ref_img_lamp_width)

print(f"Sign Focal Length: {sign_focal_length}")
print(f"Lamp Focal Length: {lamp_focal_length}")

cv2.imshow("ref_img_sign", ref_img_sign)
cv2.imshow("ref_img_lamp", ref_img_lamp)
cv2.waitKey(1)

# Initialize GUI
root = tk.Tk()
root.title("Traffic Sign and Pothole Detection")
root.geometry("1200x800")

# Tema ayarlari
style = ttk.Style()
style.theme_use('clam')

# Label to display video feed or image
video_label = Label(root)
video_label.pack(side=tk.LEFT)

def update_frame():
    global cap, last_notified
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Videonun sonuna geldiginde basa don
        return

    # Detect potholes in the frame
    detect_potholes(frame, pothole_model)

    # Detect signs in the frame
    sign_type, sign_width_in_frame = detect_sign(frame, sign_model)
    if sign_width_in_frame != 0:
        if sign_type in ["lamba_kirmizi", "lamba_sari", "lamba_yesil"]:
            distance = distance_finder(lamp_focal_length, LAMP_KNOWN_WIDTH, sign_width_in_frame)
        else:
            distance = distance_finder(sign_focal_length, KNOWN_WIDTH, sign_width_in_frame)
        distance = round(distance, 2) / 200
        cv2.putText(frame, f"{sign_type.capitalize()}", (50, 50), fonts, 1, WHITE, 3)
        cv2.putText(frame, f"Uzaklik = {distance:.2f} m", (50, 90), fonts, 0.5, WHITE, 1)
        if voice_notifications:
            notification_text = f"{sign_type.capitalize()}, Uzaklik: {distance:.2f} metre"
            threading.Thread(target=speak_notification, args=(notification_text,)).start()

    # Convert the frame to a format that tkinter can use
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    # Call this function again after 10ms
    video_label.after(10, update_frame)

def start_camera():
    global cap
    cap = cv2.VideoCapture(0)  # Bilgisayar kamerasini kullan
    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return
    update_frame()

def start_video():
    global cap
    file_path = filedialog.askopenfilename()
    if file_path:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("Error: Video could not be opened.")
            return
        update_frame()

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        if img is None:
            print("Error: Image could not be opened.")
            return

        # Detect potholes in the image
        detect_potholes(img, pothole_model)

        # Detect signs in the image
        sign_type, sign_width_in_frame = detect_sign(img, sign_model)
        if sign_width_in_frame != 0:
            if sign_type in ["lamba kirmizi", "lamba sari", "lamba yesil"]:
                distance = distance_finder(lamp_focal_length, LAMP_KNOWN_WIDTH, sign_width_in_frame)
            else:
                distance = distance_finder(sign_focal_length, KNOWN_WIDTH, sign_width_in_frame)
            distance = round(distance, 2) / 200
            cv2.putText(img, f"{sign_type.capitalize()}", (50, 50), fonts, 1, WHITE, 3)
            cv2.putText(img, f"Uzaklik = {distance:.2f} m", (50, 90), fonts, 0.5, WHITE, 1)
            if voice_notifications:
                notification_text = f"{sign_type.capitalize()}, Uzaklik: {distance:.2f} metre"
                threading.Thread(target=speak_notification, args=(notification_text,)).start()

        # Convert the image to a format that tkinter can use
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img_pil)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

def toggle_voice_notifications():
    global voice_notifications
    voice_notifications = not voice_notifications
    toggle_btn.config(text="Sesli Bildirimler: Acik" if voice_notifications else "Sesli Bildirimler: Kapali")

def open_google_maps(destination=None):
    if destination is None:
        destination = destination_entry.get()
    if destination:
        url = f"https://www.google.com/maps/search/{destination}"
        webbrowser.open(url)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Konusun...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='tr-TR')
            print(f"Söylenen: {command}")
            engine.say(f"Söylediginiz: {command}")
            engine.runAndWait()
            process_command(command)
        except sr.UnknownValueError:
            print("Anlamadim, lutfen tekrar edin.")
            engine.say("Anlamadim, lutfen tekrar edin.")
            engine.runAndWait()
        except sr.RequestError as e:
            print(f"Google Ses Tanima Servisi hatasi: {e}")

def process_command(command):
    if "kamerayi ac" in command.lower():
        start_camera()
    elif "sesli bildirimleri ac" in command.lower():
        if not voice_notifications:
            toggle_voice_notifications()
    elif "sesli bildirimleri kapat" in command.lower():
        if voice_notifications:
            toggle_voice_notifications()
    elif command.lower().endswith("ara"):
        destination = command.lower().replace(" ara", "")
        open_google_maps(destination)
    else:
        destination_entry.delete(0, tk.END)
        destination_entry.insert(0, command)
        engine.say(f"Girilen konum: {command}")
        engine.runAndWait()

# Buttons to control the GUI
camera_btn = ttk.Button(root, text="Kamerayi Ac", command=start_camera)
camera_btn.pack(pady=10)

start_btn = ttk.Button(root, text="Videoyu Baslat", command=start_video)
start_btn.pack(pady=10)

open_img_btn = ttk.Button(root, text="Resim Yukle", command=open_image)
open_img_btn.pack(pady=10)

toggle_btn = ttk.Button(root, text="Sesli Bildirimler: Kapali", command=toggle_voice_notifications)
toggle_btn.pack(pady=10)

# Entry and Button for Google Maps
destination_entry = ttk.Entry(root, width=50, font=('Helvetica', 16))
destination_entry.pack(pady=10)
destination_btn = ttk.Button(root, text="Google Haritalar'da Ara", command=lambda: open_google_maps())
destination_btn.pack(pady=10)

# Button for Speech Recognition
voice_command_btn = ttk.Button(root, text="Sesli Komut Ver", command=recognize_speech)
voice_command_btn.pack(pady=10)

# Start the GUI event loop
root.mainloop()

# Release the video capture and close windows when done
if cap is not None:
    cap.release()
cv2.destroyAllWindows()
