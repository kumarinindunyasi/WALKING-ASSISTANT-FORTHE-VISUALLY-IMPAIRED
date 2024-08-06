import pyttsx3
import speech_recognition as sr
import webbrowser

engine = pyttsx3.init()
voice_notifications = False
toggle_btn = None

def set_toggle_btn(btn):
    global toggle_btn
    toggle_btn = btn

def toggle_voice_notifications():
    global voice_notifications, toggle_btn
    voice_notifications = not voice_notifications
    if toggle_btn:
        toggle_btn.config(text="Sesli Bildirimler: Açık" if voice_notifications else "Sesli Bildirimler: Kapalı")

def open_google_maps(destination=None):
    if destination is None:
        destination = destination_entry.get()
    if destination:
        url = f"https://www.google.com/maps/search/{destination}"
        webbrowser.open(url)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Konuşun...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='tr-TR')
            print(f"Söylenen: {command}")
            engine.say(f"Söylediğiniz: {command}")
            engine.runAndWait()
            process_command(command)
        except sr.UnknownValueError:
            print("Anlamadım, lütfen tekrar edin.")
            engine.say("Anlamadım, lütfen tekrar edin.")
            engine.runAndWait()
        except sr.RequestError as e:
            print(f"Google Ses Tanıma Servisi hatası: {e}")

def process_command(command):
    if "kamerayı aç" in command.lower():
        start_camera()
    elif "sesli bildirimleri aç" in command.lower():
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
