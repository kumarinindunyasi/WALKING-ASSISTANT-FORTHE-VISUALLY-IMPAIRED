### Türkçe
# Yol Güvenliği ve Nesne Tespit Sistemi

Bu proje, kamera görüntüleri üzerinde trafik işaretleri ve yol bozulmalarını (çukur vb.) tespit eden ve mesafe hesaplayan bir görüntü işleme sistemidir. Bilgisayar kamerası veya önceden kaydedilmiş video dosyaları kullanılarak gerçek zamanlı olarak trafik işaretlerinin ve yol bozulmalarının tespiti yapılır. Sistem, tespit edilen nesnelerin mesafesini hesaplar ve sesli bildirimler sağlar. Ayrıca, tespit edilen trafik işaretlerinin türünü ve mesafesini ekranda gösterir. Bu proje, bitirme projesi olarak geliştirilmiştir.

## Proje Özellikleri
- Gerçek zamanlı kamera veya video analizi
- Trafik işareti ve yol bozulması (çukur) tespiti
- Nesnelerin mesafesini hesaplama
- Ekran üzerinde işaret türü ve mesafenin gösterimi
- Sesli bildirim sistemi

## Kullanılan Teknolojiler
- **OpenCV**: Görüntü işleme ve kamera görüntülerinin yakalanması için kullanıldı.
- **YOLOv8**: Nesne tespiti modeli olarak kullanıldı. Trafik işaretleri ve yol bozulmaları gibi nesneleri yüksek doğrulukla tanır.
- **Tkinter**: Kullanıcı arayüzü oluşturmak için kullanıldı. Video veya görüntü dosyalarının seçimi ve görüntülenmesi Tkinter ile sağlandı.
- **PIL (Python Imaging Library)**: Görüntüleri işleyip kullanıcı arayüzünde görüntülemek için kullanıldı.
- **pyttsx3**: Sesli bildirim sistemi için kullanıldı. Tespit edilen nesneler hakkında kullanıcıya sesli bildirim yapılır.
- **SpeechRecognition**: Sesli komutları algılayarak interaktif bir kullanım deneyimi sağlar.
- **Python**: Projenin temel programlama dili olarak Python kullanıldı.

## YOLOv8 Modelleri
Proje kapsamında iki farklı model kullanılmıştır:
1. **Trafik İşareti Tespit Modeli**: Trafik işaretlerini tanır ve işaretlerin mesafesini hesaplar.
2. **Yol Bozulması (Çukur) Tespit Modeli**: Yollardaki bozulmaları ve çukurları tespit eder.

---


### English
# Road Safety and Object Detection System

This project is an image processing system that detects traffic signs and road defects (potholes, etc.) on camera images and calculates distances. It operates in real-time using computer cameras or pre-recorded video files to detect traffic signs and road defects. The system calculates the distance of detected objects and provides auditory notifications. Additionally, it displays the type and distance of detected traffic signs on the screen. This project was developed as a graduation project.

## Project Features
- Real-time camera or video analysis
- Detection of traffic signs and road defects (potholes)
- Calculation of object distances
- Display of sign type and distance on screen
- Auditory notification system

## Technologies Used
- **OpenCV**: Used for image processing and capturing camera images.
- **YOLOv8**: Used as the object detection model. It accurately identifies objects such as traffic signs and road defects.
- **Tkinter**: Used to create the user interface. Tkinter facilitates the selection and display of video or image files.
- **PIL (Python Imaging Library)**: Used to process images and display them in the user interface.
- **pyttsx3**: Used for auditory notifications. It provides spoken notifications about detected objects.
- **SpeechRecognition**: Enhances interactivity by detecting voice commands.
- **Python**: The primary programming language used for the project.

## YOLOv8 Models
Two different models were used in the project:
1. **Traffic Sign Detection Model**: Recognizes traffic signs and calculates their distances.
2. **Road Defect (Pothole) Detection Model**: Detects road defects and potholes.
