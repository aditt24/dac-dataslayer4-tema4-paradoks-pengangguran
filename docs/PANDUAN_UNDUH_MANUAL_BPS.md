# Panduan Unduh Manual Data BPS

**Tujuan:** mengambil data tahun-tahun sebelumnya. Halaman web BPS hanya menampilkan tahun terbaru, padahal kita butuh **tren 2018 → 2025** dan **tren jenjang pendidikan**. Data ini juga dipakai sebagai **raw dataset resmi** untuk ZIP pengumpulan.

**Perkiraan waktu:** ±45–60 menit untuk Prioritas 1 + 2, dan bisa dibagi ke 2 orang.

---

## Cara mengunduh (per tabel, per tahun)
1. Buka link tabel di bawah.
2. Tunggu tabel muncul, lalu pilih **tahun** di menu pilihan tahun (di atas tabel).
3. Klik **"Unduh"**, lalu pilih **JSON**.
   - JSON paling mudah dibaca skrip. Kalau JSON tidak tersedia, pilih **Excel (.xlsx)**.
4. Untuk raw dataset ZIP, unduh juga versi **Excel (.xlsx)** dari tabel yang sama.
5. **Ganti nama file** sesuai pola `KODE_TAHUN.json`, misalnya `D07_2018.json`.
6. Simpan semuanya ke folder: **`Raw_Dataset/manual/`**

> ⚠️ **Tabel TPT provinsi (D05)** punya dua periode, Februari dan Agustus. Kita pakai **Agustus**. Kalau file berisi keduanya, tidak masalah: skrip menyimpan semua periode, dan analisis hanya memakai Agustus.
> ⚠️ **Tabel kemiskinan (D25)** punya periode Maret dan September. Kita pakai **Maret**.

---

## PRIORITAS 1 (wajib): provinsi, tahun **2018** dan **2025**
Untuk panah perubahan 2018 → 2025 dan untuk menyamakan tahun semua indikator.

| Kode | Tabel | Unduh tahun | Nama file | Link |
|---|---|---|---|---|
| D05 | Tingkat Pengangguran Terbuka Menurut Provinsi | 2018, 2025 | `D05_2018.json`, `D05_2025.json` | [buka](https://www.bps.go.id/id/statistics-table/2/NTQzIzI=/tingkat-pengangguran-terbuka-menurut-provinsi.html) |
| D03b | Tingkat Setengah Pengangguran Menurut Provinsi | 2018, 2025 | `D03b_2018.json`, `D03b_2025.json` | [buka](https://www.bps.go.id/id/statistics-table/2/MTE4MSMy/tingkat-setengah-pengangguran-menurut-provinsi.html) |
| D07 | Proporsi Lapangan Kerja Informal Menurut Provinsi | 2018, 2025 | `D07_2018.json`, `D07_2025.json` | [buka](https://www.bps.go.id/id/statistics-table/2/MjE1MyMy/proporsi-lapangan-kerja-informal-menurut-provinsi.html) |
| D15 | Persentase Usia Muda (15–24) NEET | 2018, 2025 | `D15_2018.json`, `D15_2025.json` | [buka](https://www.bps.go.id/id/statistics-table/2/MTE4NiMy/persentase-usia-muda-15-24-tahun-yang-sedang-tidak-sekolah-bekerja-atau-mengikuti-pelatihan.html) |
| D18 | Rata-Rata Lama Sekolah 15+ Menurut Provinsi | 2018, 2025 | `D18_2018.json`, `D18_2025.json` | [buka](https://www.bps.go.id/id/statistics-table/2/MTQyOSMy/rata-rata-lama-sekolah-penduduk-umur-15-tahun-ke-atas-menurut-provinsi.html) |
| D25 | Persentase Penduduk Miskin (P0) Menurut Provinsi dan Daerah | 2018, 2025 | `D25_2018.json`, `D25_2025.json` | [buka](https://www.bps.go.id/id/statistics-table/2/MTkyIzI=/persentase-penduduk-miskin-p0-menurut-provinsi-dan-daerah.html) |

**Total: 12 unduhan.**

> Catatan: tahun 2018 masih memakai **34 provinsi** (sebelum pemekaran Papua). Ini normal; skrip analisis akan menanganinya.

## PRIORITAS 2 (sangat dianjurkan): tren jenjang pendidikan
Untuk grafik tren SMK vs SMA (insight "apakah paradoks SMK menyempit?").

| Kode | Tabel | Unduh tahun | Link |
|---|---|---|---|
| D01 | TPT Berdasarkan Tingkat Pendidikan | **2015, 2017, 2019, 2021, 2023, 2025** | [buka](https://www.bps.go.id/id/statistics-table/2/MTE3OSMy/tingkat-pengangguran-terbuka-berdasarkan-tingkat-pendidikan.html) |
| D02b | Informal Sektor Non-Pertanian Menurut Tingkat Pendidikan | **2015, 2017, 2019, 2021, 2023, 2025** | [buka](https://www.bps.go.id/id/statistics-table/2/MTE2NiMy/proporsi-lapangan-kerja-informal-sektor-non-pertanian-menurut-tingkat-pendidikan.html) |
| D03 | Tingkat Setengah Pengangguran Menurut Tingkat Pendidikan | **2015, 2017, 2019, 2021, 2023, 2025** | [buka](https://www.bps.go.id/id/statistics-table/2/MTE4NCMy/tingkat-setengah-pengangguran-menurut-tingkat-pendidikan.html) |

**Total: 18 unduhan.** Nama file contoh: `D01_2015.json`. Jika waktunya cukup, unduh semua tahun 2015–2025 supaya garis trennya lebih halus.

## PRIORITAS 3 (opsional)
| Kode | Tabel | Tahun | Kegunaan | Link |
|---|---|---|---|---|
| D06b | Angkatan Kerja menurut Provinsi | 2025 | Ukuran titik di scatter dan bobot | [buka](https://www.bps.go.id/id/statistics-table/2/MjM5NCMy/angkatan-kerja-ak-menurut-provinsi.html) |
| J03 | TPT Kab/Kota × Tingkat Pendidikan, Jawa Tengah | 2019 | Tren paradoks Jateng 2019 → 2023 | [buka](https://jateng.bps.go.id/id/statistics-table/2/MTg2NCMy/tingkat-pengangguran-terbuka-menurut-kabupaten-kota-dan-tingkat-pendidikan-di-provinsi-jawa-tengah.html) |

---

## Setelah selesai mengunduh
Jalankan di PowerShell, dari folder proyek:

```powershell
python scripts/gabung_unduhan_manual.py
```

Skrip akan:
- Membaca semua file di `Raw_Dataset/manual/` dan menyimpan hasil rapi ke `Processed_Dataset/manual/`.
- Membuat **laporan cek** (`_laporan_cek.csv`). Laporan ini menandai file yang tahunnya tidak cocok dengan nama file, atau yang jumlah provinsinya kurang.
- Menampilkan status Prioritas 1: **LENGKAP** atau **KURANG**.

Kalau semuanya **LENGKAP**, kabari saya. Saya akan menghitung ulang semua angka (tahun yang sama), membuat tren 2018 → 2025, dan memperbarui konsep final.

## Pembagian tugas (saran)
| Orang | Tabel |
|---|---|
| Anggota 1 | Prioritas 1: D05, D03b, D07 (6 unduhan) + Prioritas 2: D01 (6 unduhan) |
| Anggota 2 | Prioritas 1: D15, D18, D25 (6 unduhan) + Prioritas 2: D02b, D03 (12 unduhan) |

## Masalah yang mungkin muncul
| Masalah | Solusi |
|---|---|
| Tabel tidak muncul atau loading terus | Muat ulang halaman, atau buka versi bahasa Inggris (ganti `/id/` menjadi `/en/` di link) |
| Tombol JSON tidak ada | Unduh Excel (.xlsx) dengan pola nama yang sama. Skrip mencoba membaca xlsx, tetapi hasilnya **dicek manual** |
| Tahun 2018 tidak tersedia di tabel D07 (informal mulai 2018) | Pakai tahun paling awal yang tersedia, lalu beri tahu saya |
| Nama file salah | Skrip akan menampilkan "Lewati". Ganti nama sesuai pola `KODE_TAHUN.json` |
