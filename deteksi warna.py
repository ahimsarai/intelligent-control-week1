import cv2
import numpy as np

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

    # Rentang warna merah dalam HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Masking untuk mendeteksi warna merah
    mask = cv2.inRange(hsv, lower_red, upper_red)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Menampilkan hasil
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    # Menunggu input 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan kamera dan menutup jendela
cap.release()
cv2.destroyAllWindows()
