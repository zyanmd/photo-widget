# 📸 Photo Widget for Omalauncher

Widget foto dinamis dan responsif untuk [Omalauncher](https://github.com/SimonSchubert/omarchy-widgets) Android. Menampilkan foto favorit Anda di home screen dengan penyesuaian ukuran otomatis, dukungan URL online, pencarian file lokal perangkat, dan kemampuan duplikasi widget.

![Photo Widget Preview](preview.png)

---

## ✨ Fitur Unggulan

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

- **➕ Manajer Duplikasi Widget**:
  - Gandakan widget foto dengan satu ketukan untuk memasang beberapa foto berbeda di home screen.
  - Tombol bersih untuk menghapus semua duplikat sekaligus.

---

## 🚀 Panduan Instalasi

### 1. Salin File ke Direktori Widget Omalauncher
Salin file `widget.owl` dan folder `scripts/` ke folder widget Omalauncher Anda:

```bash
# Buat folder scripts jika belum ada
mkdir -p ~/.config/omalauncher/widgets/scripts

# Salin file widget dan script pembantu
cp widget.owl ~/.config/omalauncher/widgets/photo.owl
cp scripts/*.py ~/.config/omalauncher/widgets/scripts/
chmod +x ~/.config/omalauncher/widgets/scripts/*.py
```

### 2. Cek & Verifikasi Widget
Jalankan `owl-check` untuk memeriksa widget:

```bash
owl-check ~/.config/omalauncher/widgets/photo.owl
```

Widget akan langsung muncul di home screen ponsel Anda dalam beberapa detik!

---

## 🛠️ Persyaratan Sistem

- **Omalauncher**: OWL 8
- **Paket Pacman**: `python`, `curl` (otomatis diminta via deklarasi `requires`)

---

## 👨‍💻 Pembuat & Lisensi

Dibuat dengan ❤️ oleh [zyanmd](https://github.com/zyanmd).

Didistribusikan di bawah lisensi [MIT](LICENSE).
