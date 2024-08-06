import cv2
from tkinter import filedialog
from detection import detect_sign, detect_pothole, distance_finder
from PIL import Image, ImageTk

# Global cap değişkenini kullanın
global cap

focal_length_found = None
KNOWN_WIDTH = 60  # centimeter
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX

def start_camera(sign_model, pothole_model, focal_length, video_label):
    global cap, focal_length_found
    focal_length_found = focal_length
    cap = cv2.VideoCapture(0)  # Bilgisayar kamerasını kullan
    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return
    update_frame(sign_model, pothole_model, video_label)

def start_video(sign_model, pothole_model, focal_length, video_label):
    global cap, focal_length_found
    focal_length_found = focal_length
    file_path = filedialog.askopenfilename()
    if file_path:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("Error: Video could not be opened.")
            return
        update_frame(sign_model, pothole_model, video_label)

def open_image(sign_model, pothole_model, focal_length, video_label):
    global focal_length_found
    focal_length_found = focal_length
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        if img is None:
            print("Error: Image could not be opened.")
            return

        # Detect signs and potholes in the image
        sign_type, sign_width_in_frame = detect_sign(img, sign_model)
        pothole_detected = detect_pothole(img, pothole_model)
        if sign_width_in_frame != 0:
            distance = distance_finder(focal_length_found, KNOWN_WIDTH, sign_width_in_frame)
            distance = round(distance, 2) / 10
            cv2.putText(img, f"{sign_type.capitalize()}", (50, 50), fonts, 1, WHITE, 3)
            cv2.putText(img, f"Distance = {distance:.2f} m", (50, 90), fonts, 1, WHITE, 3)
        if pothole_detected:
            cv2.putText(img, "Pothole detected", (50, 130), fonts, 1, WHITE, 3)

        # Convert the image to a format that tkinter can use
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img_pil)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

def update_frame(sign_model, pothole_model, video_label):
    global cap, focal_length_found
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Videonun sonuna geldiğinde başa dön
        return

    # Detect signs and potholes in the frame
    sign_type, sign_width_in_frame = detect_sign(frame, sign_model)
    pothole_detected = detect_pothole(frame, pothole_model)
    if sign_width_in_frame != 0:
        distance = distance_finder(focal_length_found, KNOWN_WIDTH, sign_width_in_frame)
        distance = round(distance, 2) / 10
        cv2.putText(frame, f"{sign_type.capitalize()}", (50, 50), fonts, 1, WHITE, 3)
        cv2.putText(frame, f"Distance = {distance:.2f} m", (50, 90), fonts, 1, WHITE, 3)
    if pothole_detected:
        cv2.putText(frame, "Pothole detected", (50, 130), fonts, 1, WHITE, 3)

    # Convert the frame to a format that tkinter can use
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    # Call this function again after 10ms
    video_label.after(10, update_frame, sign_model, pothole_model, video_label)
