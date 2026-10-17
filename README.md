# 📸 Photo Widget for Omalauncher

Widget foto dinamis dan responsif untuk [Omalauncher](https://github.com/SimonSchubert/omarchy-widgets) Android. Menampilkan foto favorit Anda di home screen dengan penyesuaian ukuran otomatis, slideshow album dengan transisi fade halus, dukungan URL online, pencarian galeri penyimpanan lokal perangkat, kemampuan menambah hingga 10 widget foto independen, dan adaptasi tema dinamis Omarchy.

![Photo Widget Preview](preview.png)

---

## ✨ Fitur Unggulan

- **🎞️ Mode Slideshow Album & Transisi Fade Halus**:
  - Dukungan multiple foto dalam 1 widget (hingga 10 foto per album).
  - Transisi fade halus (*crossfade tween 800ms*) antar foto.
  - Pilihan kecepatan rotasi foto yang dapat disesuaikan (5 detik, 8 detik, 15 detik, 30 detik, hingga 1 menit).
  - Dapat dimatikan kapan saja untuk kembali ke mode foto tunggal (*single photo*).

- **🎨 Adaptasi Tema Dinamis Omarchy (Dark & Light Mode)**:
  - Otomatis mendeteksi tema Omarchy aktif (`vantablack`, `white`, `catppuccin`, dll.).
  - Kartu, teks, tombol, dan border menyesuaikan kontras dan palet warna tema aktif secara cerdas.

- **➕ Dukungan Hingga 10 Widget Foto di Home Screen**:
  - Tambahkan widget foto baru langsung dari layar pengaturan (Widget #1 hingga #10).
  - Setiap widget beroperasi secara mandiri dengan foto/slideshow dan pengaturan masing-masing.
  - Hapus widget sekunder kapan saja dengan satu ketukan.

- **🖼️ Layout Dinamis & Responsif**:
  - Foto otomatis memenuhi kotak (*edge-to-edge*) pada berbagai ukuran grid (2x2, 3x3, 4x3, 3x6, dll.) tanpa bilah hitam (*letterbox*).
  - Pilihan mode tampilan foto: **Cover** (penuh rapi) atau **Contain** (asli proporsional).

- **🌐 Dukungan Multi-Sumber Foto**:
  - **URL Web Langsung**: Mendukung link gambar HTTP/HTTPS (`.jpg`, `.png`, `.webp`).
  - **Link Cloud Hosting**: Otomatis mengenali link share Google Drive, Dropbox, dan Imgur.
  - **Penyimpanan Lokal HP**: Mendukung file path Android (contoh: `/storage/emulated/0/Pictures/...`) dan direktori Linux (`~/Pictures`).

- **⚡ Default Foto Offline**:
  - Memiliki asset foto bawaan tersemat (*embedded base64*), sehingga widget langsung tampil cantik saat pertama kali dipasang tanpa perlu koneksi internet.

- **📑 Layar Pengaturan Interaktif**:
  - Ketuk widget untuk membuka layar konfigurasi penuh (*full-screen sheet*).
  - Preview gambar resolusi tinggi.
  - Status koneksi dan unduhan foto secara *real-time*.
  - Tombol cepat untuk membuka direktori foto di File Manager.

---

## 🚀 Panduan Instalasi

### 1. Salin File ke Direktori Widget Omalauncher
Salin file `widget.owl` ke folder widget Omalauncher Anda:

```bash
mkdir -p ~/.config/omalauncher/widgets
cp widget.owl ~/.config/omalauncher/widgets/market-zyanmd-photo.owl
```

### 2. Cek & Verifikasi Widget
Jalankan `owl-check` untuk memeriksa widget:

```bash
owl-check ~/.config/omalauncher/widgets/market-zyanmd-photo.owl
```

Widget akan langsung muncul di home screen ponsel Anda dalam beberapa detik!

---

## 🛠️ Persyaratan Sistem

- **Omalauncher**: OWL 8
- **Paket Pacman**: `python`, `python-pillow`, `curl` (otomatis diminta via deklarasi `requires`)

---

## 👨‍💻 Pembuat & Lisensi

Dibuat dengan ❤️ oleh [zyanmd](https://github.com/zyanmd).

Didistribusikan di bawah lisensi [MIT](LICENSE).
