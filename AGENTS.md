# AGENTS.md

## Gambaran Proyek

Repositori ini berisi modul Odoo 19 bernama **cctv_management**.

Tujuan modul adalah mengelola infrastruktur CCTV perusahaan, meliputi:

* NVR / DVR
* Kamera CCTV (phase 2)
* Switch PoE (phase 2)

Modul harus dirancang agar dapat digunakan mulai dari puluhan hingga ribuan perangkat CCTV.

---

# Peran Agent

Anda adalah seorang **Senior Odoo 19 Developer dan System Analyst**.

Saat membuat atau mengubah kode:

* Ikuti best practice Odoo 19.
* Gunakan ORM Odoo.
* Hindari duplikasi kode.
* Utamakan desain yang mudah dikembangkan.
* Pertahankan kompatibilitas data yang sudah ada.
* Sertakan migrasi jika ada perubahan struktur model.
* Selalu pertimbangkan kebutuhan monitoring dan maintenance di masa depan.

---

# Ruang Lingkup Modul

Modul digunakan untuk:

1. Inventaris NVR/DVR
2. Inventaris CCTV

Diutamakan untuk mencatat NVR terlebih dahulu, mengingat CCTV terinstall mengikat ke NVR.

---

# Struktur Lokasi

Data lokasi berupa tagging, mengingat tiap NVR bisa mengakomodir beberapa CCTV yang mempunyai lokasi berbeda.

---


# Model Utama

## cctv.nvr

Model induk seluruh perangkat.

Field umum:

* name
* asset_code
* device_type
* status
* brand
* model
* serial_number
* ip_address
* mac_address
* installation_date
* warranty_end_date
* channel_count
* storage_capacity_tb
* used_storage_tb
* firmware_version
* lokasi
* notes

Status perangkat:

* draft
* active
* maintenance
* offline
* retired

Asset code harus unik, diisi manual.

Field tambahan:

* rtsp_url
* stream_url
* resolution
* frame_rate
* codec

Relasi:

* Satu NVR memiliki banyak kamera. persiapkan untuk pengembangan berikutnya.

---

# Dashboard

Siapkan struktur agar mendukung dashboard berikut:

* Menampilkan daftar NVR/DVR, field: name, ip address, lokasi

---

# Keamanan

Setiap model wajib memiliki:

* Access Rights
* Security Group
* Record Rule jika diperlukan

Grup yang digunakan:

## CCTV User

Hak akses:

* Lihat data
* Lihat laporan

## CCTV Supervisor

Hak akses:

* Tambah data
* Edit data
* Kelola maintenance

## CCTV Administrator

Hak akses:

* Akses penuh

---

# Struktur Folder

Gunakan struktur:

cctv_management/

├── models/
├── views/
├── security/
├── data/
├── report/
├── wizard/
├── static/
└── tests/

---

# Standar Kode Python

* Gunakan ORM Odoo.
* Hindari SQL langsung.
* Tambahkan help text pada field penting.
* Gunakan compute field jika sesuai.
* Gunakan constraint untuk validasi.
* Gunakan selection field untuk nilai tetap.

---

# Standar XML

* Pisahkan tree, form, search, dan menu.
* Gunakan notebook untuk data yang banyak.
* Kelompokkan field berdasarkan fungsi.
* Gunakan smart button untuk relasi penting.

---

# Konvensi Penamaan

Model:

* cctv.nvr
* cctv.camera

View:

* cctv_nvr_form
* cctv_camera_form

Action:

* action_cctv_nvr

Menu:

* menu_cctv_nvr

---

# Fitur Masa Depan

Saat membuat desain, pertimbangkan kompatibilitas untuk:

* Integrasi ONVIF
* Integrasi RTSP
* Peta lokasi CCTV
* Floor Plan Gedung
* Monitoring otomatis
* Integrasi Telegram/WhatsApp Alert
* Integrasi Email Alert
* Monitoring Storage NVR
* Integrasi AI Analytics
* Face Recognition
* License Plate Recognition (LPR)

Jangan membuat desain yang menghambat implementasi fitur-fitur tersebut.

---

# Ekspektasi Output

Saat diminta membuat kode:

1. Berikan file lengkap.
2. Sertakan perubahan manifest jika diperlukan.
3. Jelaskan relasi model.
4. Jelaskan dampak migrasi database.
5. Ikuti konvensi Odoo 19.

Saat diminta memodifikasi kode:

1. Tunjukkan file yang berubah.
2. Jelaskan alasan perubahan.
3. Hindari refactor yang tidak diperlukan.
4. Jaga kompatibilitas data yang sudah ada.
