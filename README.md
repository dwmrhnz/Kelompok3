# 🍔 Sariawam Resto - CLI Cashier System

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![CLI](https://img.shields.io/badge/Interface-CLI-lightgrey.svg)

Proyek ini adalah aplikasi Sistem Kasir Restoran berbasis *Command Line Interface* (CLI) yang dibangun menggunakan bahasa pemrograman Python. Proyek ini disusun untuk memenuhi Tugas Proyek Akhir mata kuliah **Algoritma & Struktur Data (TPL2106)** pada program studi D4 Teknologi Rekayasa Perangkat Lunak, Sekolah Vokasi IPB University.

## 👥 Tim Pengembang (Kelompok 3)
- **Fardhan** (Fokus: Data Menu & Linked List)
- **Hirzi** (Fokus: Antrean Queue & File Handling)
- **Dawam Raihan Zufar** (Fokus: Sutradara Program, CLI UI/UX & Admin Mode)

## 💡 Konsep & Struktur Data
Aplikasi ini menerapkan dua struktur data utama untuk menyimulasikan operasional restoran yang nyata:
1. **Single Linked List:** Digunakan untuk menyimpan dan mengelola daftar menu (karena memudahkan proses penambahan dan penghapusan menu secara dinamis).
2. **Queue (FIFO - First In First Out):** Digunakan untuk mengelola antrean pelanggan (pelanggan yang datang lebih dulu akan dilayani lebih dulu).

## ✨ Fitur Utama
- **Antarmuka Modern:** Tampilan terminal yang rapi, berwarna, dan interaktif menggunakan library `rich`.
- **Manajemen Antrean:** Pelanggan dapat mengambil nomor antrean (Dine-in/Takeaway) dan dipanggil sesuai urutan.
- **Pencarian & Pengurutan:** Dilengkapi fitur *partial search* untuk mencari hidangan dan *Bubble Sort* untuk mengurutkan harga menu.
- **Mode Admin Tersembunyi (CRUD):** Admin dapat melakukan *Create, Update, dan Delete* data menu makanan & stok.
- **Penyimpanan Permanen:** Perubahan stok dan menu otomatis tersimpan di file `data/menu.txt`.
- **Cetak Struk Dinamis (PDF):** Menghasilkan bukti transaksi berformat `.pdf` secara otomatis menyesuaikan jumlah pesanan pelanggan menggunakan `reportlab`.

## 🛠️ Prasyarat & Instalasi
Sebelum menjalankan aplikasi ini, pastikan komputer Anda sudah terpasang Python 3 dan beberapa pustaka pihak ketiga.

1. Clone *repository* ini:
   ```bash
   git clone https://github.com/dwmrhnz/Kelompok3.git
   cd Kelompok3
   ```

2. Instal pustaka yang dibutuhkan:
   ```bash
   pip install rich reportlab
   ```

3. Jalankan aplikasi:
   ```bash
   python main.py
   ```

## 📂 Struktur Direktori
```text
Kelompok3/
│
├── data/
│   └── menu.txt                 # Database utama (format txt)
├── modules/
│   ├── linkedlist_menu.py       # Logika struktur data Linked List
│   └── queue_antrean.py         # Logika struktur data Queue & Transaksi
├── struk/                       # Folder auto-generated untuk file PDF struk
├── .gitignore                   # Konfigurasi pengabaian file Git
├── main.py                      # File eksekusi utama aplikasi
└── README.md                    # Dokumentasi proyek
```

## 🔒 Catatan Khusus
- **Akses Admin:** Untuk mengakses menu Admin, masukkan kode rahasia `67` pada menu layanan utama.