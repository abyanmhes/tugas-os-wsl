# Analisis Simulasi Beban Proses pada WSL

### A. Kondisi Saat Simulasi Beban (Sebelum Terminasi)
Berdasarkan pengamatan pada `htop` saat perintah `yes > /dev/null &` dijalankan, dapat diidentifikasi hal-hal berikut:
* **Identifikasi Proses:** Mencari penyebab sangat mudah dikarenakan berada pada hierarki paling atas. Proses tersebut memiliki **PID 9842** (milik *user* `barra`) dengan perintah eksekusi `yes`.
* **Penggunaan CPU 100%:** Pada kolom `%CPU`, terlihat bahwa proses `yes` memakan **100.0%** tenaga CPU.
* **Isolasi Beban oleh OS:** Jika melihat panel indikator CPU di bagian atas, terlihat bahwa beban 100% tersebut **hanya dibebankan pada Core nomor 10**. Core nomor 10 penuh (ditandai dengan indikator bar yang mentok), sementara 15 core lainnya berada di angka `0.0%`.
* **Load Average:** Angka *load average* mulai naik ke `0.52`, menandakan sistem mulai merasakan beban.

### B. Kondisi Setelah Terminasi (Setelah `killall yes`)
Setelah perintah `killall yes` dieksekusi, sistem merespons dengan cepat:
* **Proses Menghilang:** Sistem operasi mengirimkan sinyal untuk menghentikan program, sehingga proses `yes` langsung hilang dari daftar.
* **Pemulihan Resource:** Core nomor 10 yang sebelumnya bekerja 100%, kini sudah kembali normal (rata-rata di bawah 2%).
* **Normalisasi:** Urutan teratas beban CPU sekarang hanyalah aplikasi `htop` itu sendiri yang memakan sekitar `1.3%` CPU. *Load average* menit pertama juga langsung turun drastis menjadi `0.03`.

### C. Kesimpulan: Bagaimana OS Menangani Proses Intensif

1. **Multiprocessing dan Isolasi Core:** Meskipun ada satu proses yang meminta *resource* CPU 100%, sistem operasi tidak membiarkan seluruh komputer *freeze*. OS melakukan *scheduling* (penjadwalan) dengan menaruh proses beban berat tersebut ke satu *core* spesifik (Core 10).
2. **Kendali Penuh User dan Terminasi Instan:** Sistem operasi memberikan hierarki kendali yang jelas. Selama *user* memiliki hak akses, OS akan memprioritaskan dan mengeksekusi perintah (`killall`) secara instan, lalu mengembalikan *CPU cycle* seperti semula tanpa perlu melakukan *restart* pada sistem.