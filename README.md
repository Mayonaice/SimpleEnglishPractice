# Aplikasi Latihan Pengucapan Bahasa Inggris

Aplikasi ini dirancang untuk membantu pengguna melatih pengucapan Bahasa Inggris dengan cara yang interaktif dan menghibur. Aplikasi ini memiliki beberapa fitur utama:

1. Menampilkan kalimat latihan bahasa Inggris
2. Merekam pengucapan pengguna melalui mikrofon
3. Membandingkan teks yang diucapkan dengan kalimat contoh
4. Memberikan skor kemiripan dan saran perbaikan ejaan
5. Antarmuka pengguna yang modern dan mudah digunakan

## Versi yang Tersedia

Proyek ini menyediakan beberapa versi aplikasi untuk mengakomodasi berbagai konfigurasi:

1. **Versi Lengkap** (`english_practice_app.py`): Menggunakan SpeechRecognition, PyAudio, dan customtkinter untuk UI modern. Optimal untuk Python 3.7-3.10.

2. **Versi Sederhana** (`simple_english_practice.py`): Menggunakan tkinter standar tanpa library tambahan. Pengguna mengetik teks alih-alih merekam suara.

3. **Versi Python 3.13** (`english_practice_app_py3_13.py`): Versi yang dioptimalkan untuk Python 3.13 yang tidak merekam suara tetapi menggunakan UI modern dengan tkinter.

4. **Versi Python 3.13 dengan Mikrofon** (`english_practice_mic_py3_13.py`): Versi yang menggunakan PyAudio langsung (tanpa SpeechRecognition) dan mensimulasikan API transkripsi untuk Python 3.13.

5. **Versi Simulator Mikrofon** (`english_practice_mic_simulator.py`): Versi baru yang mensimulasikan rekaman mikrofon tanpa memerlukan modul PyAudio. Ini adalah alternatif terbaik untuk Python 3.13 jika Anda mengalami masalah saat menginstal PyAudio.

## Persyaratan Sistem

- Python 3.7 atau lebih baru
- Mikrofon yang berfungsi (untuk versi yang menggunakan rekaman suara nyata)
- Koneksi internet (untuk API transkripsi pada versi lengkap)

## Instalasi

### 1. Clone repository ini

```bash
git clone https://github.com/username/english-practice-app.git
cd english-practice-app
```

### 2. Buat virtual environment

```bash
# Untuk Python 3.7-3.10
python -m venv venv
source venv/bin/activate  # Untuk Linux/Mac
venv\Scripts\activate     # Untuk Windows
```

### 3. Instal paket yang diperlukan

```bash
pip install -r requirements.txt
```

### Instalasi PyAudio pada Windows

Jika Anda mengalami masalah saat menginstal PyAudio di Windows, coba salah satu metode berikut:

**Metode 1**: Gunakan wheel yang sudah dikompilasi
```bash
pip install pipwin
pipwin install pyaudio
```

**Metode 2**: Unduh file wheel PyAudio yang sesuai dari [situs ini](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) dan instal secara lokal:
```bash
pip install [path-to-downloaded-wheel-file]
```

**ALTERNATIF**: Jika tetap tidak bisa menginstal PyAudio, gunakan versi simulator mikrofon (`english_practice_mic_simulator.py`) yang tidak memerlukan PyAudio.

## Menjalankan Aplikasi

Pilih versi yang sesuai dengan konfigurasi sistem Anda:

### Versi Lengkap (dengan SpeechRecognition):
```bash
python english_practice_app.py
```

### Versi Sederhana (tanpa rekaman suara):
```bash
python simple_english_practice.py
```

### Versi Python 3.13 (tanpa rekaman suara):
```bash
python english_practice_app_py3_13.py
```

### Versi Python 3.13 dengan Mikrofon (memerlukan PyAudio):
```bash
python english_practice_mic_py3_13.py
```

### Versi Simulator Mikrofon (tidak memerlukan PyAudio):
```bash
python english_practice_mic_simulator.py
```

## Cara Penggunaan

1. Jalankan aplikasi yang sesuai dengan konfigurasi Anda
2. Baca kalimat yang ditampilkan
3. Klik tombol "Rekam Suara" dan ucapkan kalimat tersebut (untuk versi dengan mikrofon)
4. Lihat hasil pengucapan dan skor kemiripan
5. Gunakan tombol "Selanjutnya" dan "Sebelumnya" untuk berpindah antar kalimat latihan

## Cara Kerja Simulator Mikrofon

Versi simulator mikrofon (`english_practice_mic_simulator.py`) memberikan pengalaman serupa dengan versi mikrofon nyata tetapi tanpa perlu merekam suara yang sebenarnya:

1. Saat tombol "Mulai Rekaman" ditekan, aplikasi akan mensimulasikan proses perekaman.
2. Setelah beberapa detik, aplikasi akan "mengenali" ucapan dengan membuat variasi dari kalimat yang ditampilkan.
3. Variasi ini secara acak akan memiliki beberapa kesalahan minor untuk mensimulasikan pengenalan suara nyata.
4. Skor kemiripan dan saran perbaikan ejaan dihitung sama seperti versi nyata.

Ini adalah solusi terbaik untuk pengguna Python 3.13 yang kesulitan menginstal PyAudio.

## Catatan Implementasi

- Versi Python 3.13 dengan mikrofon menggunakan implementasi simulasi untuk transkripsi suara karena keterbatasan kompatibilitas.
- Untuk implementasi produksi nyata, Anda perlu mengganti fungsi `simulate_transcript()` dengan integrasi API transkripsi yang sebenarnya.
- Versi simulator mikrofon tidak memerlukan modul tambahan selain tkinter yang sudah termasuk dalam instalasi Python standar.

## Kontribusi

Kontribusi, saran dan permintaan fitur sangat diterima. Silakan buat issue atau pull request. 