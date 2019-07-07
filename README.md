# absensi-face-recognition
Aplikasi pendataan mahasiswa dengan menggunakan metode Face Recognition menggunakan module  computer vision yang telah disediakan oleh OpenCV.
Menggunakan Haar Cascade Classifier sebagai pendeteksi wajah dan  Local Binary Pattern Histogram sebagai pengenal wajah. Lalu data nama dan ID disimpan pada dataframe lalu di-write ke dalam file .csv
# dependencies
Module OpenCV\
Module tkinter untuk membuat GUI\
Module numpy untuk memproses array\
Module pandas untuk memproses dataframe\
Module csv untuk menyimpan dataframe kedalam file .csv
# algoritma
Aplikasi akan mendeteksi muka menggunakan algoritma Cascade Classfier dari fitur Haar lalu membuat bounding box diantara muka saat didisplay. Aplikasi akan otomatis menangkap 100 foto tiap 100 milisecond untuk digunakan sebagai baham training. Label gambar akan diambil dari NPM dan Nama dari mahasiswa yang sudah di-input sebelumnnya\
\
Selanjutnya, aplikasi akan mentraining data gambar dan label menggunakan algoritma gabungan LBP dan HOG yaitu LBPH. Data gambar dikonversi kedalam bentuk histogram lalu dicek jika ada kontras antar pixel yang menunjukan kontur muka. Data histogram kemudian di-konversi kembali menjadi data vektor dalam format .yaml agar bisa diproses saat pengenalan Wajah\
\
Terakhir, pada pengenalan wajah aplikasi akan mengambil Haar Cascade Classifier untuk mendeteksi wajah, dan hasil data training untuk pengenalan wajah. Aplikasi akan mendeteksi wajah yang terdeteksi pada kamera lalu mengubahnya kedalam bentuk histogram dan membandingkannya dengan histogram dari data vektor hasil training sebelumnya. Jika ditemukan kecocokan, aplikasi akan mengambil label dari data yang cocok dan mendisplaynya di layar kamera lalu disimpan kedalam database yang berformat .csv
# instalasi dan penggunaan
Download file repository lalu extract\
Buka command prompt lalu set ke direktori file (command cd)\
Ketik python absensi_facial_recognition.py 
