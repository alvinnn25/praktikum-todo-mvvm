# Aplikasi Manajemen Tugas (To-Do) — Arsitektur MVVM

**Nama:** Muhamad Alfiansyah  
**NIM:** 24371005  

## Deskripsi Proyek
Aplikasi manajemen tugas (To-Do List) berbasis desktop menggunakan Python (`tkinter`) yang menerapkan:
1. **Arsitektur MVVM:** Pemisahan kode ke dalam folder `Model`, `View`, dan `ViewModel`.
2. **Pola Singleton:** Diterapkan pada `TaskRepository` agar hanya ada satu pengelola penyimpanan data lokal (`tasks_data.json`).
3. **Pola Observer:** Diterapkan antara `TaskViewModel` dan `TaskView` sehingga daftar tugas di layar diperbarui otomatis tanpa tombol *refresh* manual.

## Cara Menjalankan Aplikasi
Pastikan Python 3 sudah terinstal, lalu jalankan perintah berikut di terminal:
```bash
python main.py