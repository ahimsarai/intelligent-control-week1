import cv2
import numpy as np

# Fungsi untuk menghitung akurasi berdasarkan area piksel yang terdeteksi
def calculate_accuracy(mask):
    total_pixels = mask.size
    detected_pixels = cv2.countNonZero(mask)
    accuracy = (detected_pixels / total_pixels) * 100
    return accuracy

# Inisialisasi kamera
cap = cv2.VideoCapture(1)

# Cek apakah kamera berhasil dibuka
if not cap.isOpened():
    print("Error: Kamera tidak dapat diakses")
    exit()

while True:
    # Membaca frame dari kamera
    ret, frame = cap.read()

    # Jika frame kosong, keluar dari loop
    if not ret:
        print("Error: Gagal membaca frame")
        break

    # Mengonversi frame dari BGR ke HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rentang warna untuk deteksi
    # Merah
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    # Hijau
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])
    # Biru
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])

    # Masking untuk mendeteksi warna
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Menambahkan deteksi warna dalam satu frame
    result_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    result_green = cv2.bitwise_and(frame, frame, mask=mask_green)
    result_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)

    # Menghitung akurasi deteksi untuk masing-masing warna
    accuracy_red = calculate_accuracy(mask_red)
    accuracy_green = calculate_accuracy(mask_green)
    accuracy_blue = calculate_accuracy(mask_blue)

    # Menambahkan teks dan bingkai (frame) pada objek yang terdeteksi
    def draw_bounding_box_and_label(mask, color, label, accuracy):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Hanya deteksi objek besar (untuk menghindari noise)
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, f"{label} - {accuracy:.2f}%", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Gambar bingkai dan label untuk masing-masing warna
    draw_bounding_box_and_label(mask_red, (0, 0, 255), 'Merah', accuracy_red)
    draw_bounding_box_and_label(mask_green, (0, 255, 0), 'Hijau', accuracy_green)
    draw_bounding_box_and_label(mask_blue, (255, 0, 0), 'Biru', accuracy_blue)

    # Menampilkan hasil dalam satu tampilan real-time
    cv2.imshow("Detected Colors", frame)

    # Menunggu input 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan kamera dan menutup jendela
cap.release()
cv2.destroyAllWindows()
