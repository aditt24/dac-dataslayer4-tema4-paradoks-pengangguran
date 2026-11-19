# Hasil Cek Data BPS — 19 November 2026

**Kesimpulan: semua data inti tersedia, jadi tidak ada rencana B yang perlu dipakai.** Ada juga peningkatan besar: data **TPT per kabupaten/kota se-Indonesia (2017–2025)** tersedia.

Cara cek: halaman tabel BPS diambil langsung, lalu daftar tahun (`listTahun`), kategori wilayah, dan nilai tahun terbaru dibaca. Hasil nilai tahun terbaru tersimpan di `Raw_Dataset/bps_web_terbaru/` (20 file CSV + `_ringkasan_ketersediaan.csv`).

---

## 1. Ketersediaan tabel

| File | Tabel BPS | var_id | Tahun tersedia | Cakupan | Status |
|---|---|---|---|---|---|
| D05 | TPT Menurut Provinsi | 543 | 1986–2026 (Feb & Agt) | 38 prov + Indonesia | ✅ |
| D05b | TPT Menurut Provinsi (Triwulanan) | 2562 | 2025–2026 | 38 prov | ✅ (tidak dipakai, konsistensi Agustus) |
| D06 | TPAK Menurut Provinsi | 2396 | 2021–2026 | 38 prov | ✅ |
| **D03b** | **Tingkat Setengah Pengangguran Menurut Provinsi** | 1181 | **2015–2025** | 38 prov | ✅ **(sebelumnya belum pasti)** |
| D07 | Proporsi Lapangan Kerja Informal Menurut Provinsi | 2153 | **2018–2025** | 38 prov | ✅ |
| D08 | Informal Sektor Non-Pertanian Menurut Provinsi | 1162 | 2015–2024 | 38 prov | ✅ |
| D10 | Persentase Tenaga Kerja Formal Menurut Provinsi | 1168 | 2015–2025 | 38 prov | ✅ |
| D11 | Upah Rata-rata per Jam Pekerja Menurut Provinsi | 1172 | 2015–2025 | 38 prov | ✅ |
| **D15** | **NEET 15–24 Menurut Provinsi** | 1186 | **2015–2025** | 38 prov | ✅ **(sebelumnya belum pasti)** |
| D18 | RLS 15+ Menurut Provinsi | 1429 | 2015–2025 | 38 prov | ✅ |
| D01 | TPT Menurut Tingkat Pendidikan | 1179 | 2015–2025 | 6 jenjang | ✅ |
| D02 | Informal Menurut Tingkat Pendidikan | 2157 | **2018–2023 saja** | 8 jenjang | ⚠️ berhenti di 2023 |
| **D02b** | **Informal Sektor Non-Pertanian Menurut Tingkat Pendidikan** | 1166 | **2015–2025** | 6 jenjang | ✅ **solusi untuk perbandingan di tahun yang sama** |
| D03 | Setengah Pengangguran Menurut Tingkat Pendidikan | 1184 | 2015–2025 | 6 jenjang | ✅ |
| D04 | TPT Menurut Kelompok Umur | 1180 | 2015–2025 | 11 kelompok | ✅ |
| D04b | TPT Menurut Jenis Kelamin | 1177 | 2015–2025 | L/P | ✅ |
| D16 | NEET Menurut Jenis Kelamin | 2655 | 2020–2025 | L/P/Total | ✅ |
| D17 | TPT Menurut Status Disabilitas | 2652 | 2020–2025 | 3 | ✅ |
| D14 | Penduduk Bekerja menurut Lapangan Usaha × Pendidikan | 1971 | 2018–2025 | 17 sektor + total | ✅ |
| **K01** | **TPT menurut Jenis Kelamin dan Kabupaten/Kota** | 2824 | **2017–2025** | **±514 kab/kota (579 baris termasuk judul provinsi)** | ✅ **PENINGKATAN** |

Tabel lain yang ditemukan di katalog dan berguna: Pekerja Anak menurut Provinsi (2018–2024), Perkawinan Anak Perempuan 20–24 menurut Provinsi (2015–2025), Akses Internet menurut Provinsi (2014–2023), dan Penduduk Bekerja menurut Status Pekerjaan (1986–2025).

## 2. Keputusan

| Isu sebelumnya | Hasil | Keputusan |
|---|---|---|
| Setengah pengangguran per provinsi | ✅ Ada (2015–2025) | IDKK lengkap 5 komponen |
| NEET per provinsi | ✅ Ada (2015–2025) | IDKK lengkap 5 komponen |
| Panjang panel provinsi | Informal mulai 2018 | **Panel M3/M7 = 2018–2025 (8 tahun)**, 34 provinsi harmonisasi atau 38 provinsi mulai 2022 |
| Informal per jenjang berhenti 2023 | Ada alternatif D02b hingga 2025 | Dumbbell paradoks 2025 memakai **informal non-pertanian** (D02b). Label wajib "sektor non-pertanian". Versi 2023 dengan D02 jadi tooltip |
| TPT kab/kota (sebelumnya hanya Jateng) | ✅ Nasional ±514 kab/kota | **Modul M5 spasial naik kelas:** Moran's I + **LISA hotspot** di level kab/kota (n besar, valid). M8 Jateng tetap sebagai zoom |

## 3. Temuan awal (PRELIMINARY)

> ⚠️ Dihitung dari nilai default halaman BPS: **TPT = Agustus 2026**, komponen lain = **2025**. Tahunnya belum sama, jadi **jangan dikutip di dashboard** sebelum diulang dengan TPT Agustus 2025 (via skrip WebAPI). Polanya sudah cukup jelas untuk menguatkan arah konsep.

**a. Paradoks di level jenjang 2025 (tahun yang sama, data BPS):**

| Jenjang | TPT 2025 | Informal non-pertanian 2025 | Setengah pengangguran 2025 |
|---|---|---|---|
| ≤SD | 2,30 | 68,43 | 8,81 |
| SMP | 3,80 | 60,10 | 8,58 |
| SMA umum | 6,88 | 43,75 | 8,34 |
| **SMK** | **8,63** | **35,84** | **6,81** |
| Diploma | 4,31 | 25,63 | 4,58 |
| Universitas | 5,39 | 16,63 | 5,29 |

→ SMK: TPT tertinggi, tetapi informal dan setengah pengangguran lebih rendah dari semua jenjang di bawahnya. **H1 terdukung.**

**b. Level provinsi (38 provinsi, korelasi Spearman):**
- TPT vs informal = **−0,42**; TPT vs RLS = **+0,51**; RLS vs informal = **−0,50**. Provinsi yang lebih terdidik punya TPT lebih tinggi tetapi informalitas lebih rendah. Ini paradoks yang sama di level wilayah (**H3 terdukung secara awal**).
- TPT vs IDKK tanpa TPT: **ρ = −0,10 (p = 0,57)**. TPT praktis **tidak berhubungan** dengan defisit kualitas kerja (**H2 terdukung**).
- Pergeseran ranking terbesar (ranking TPT → ranking IDKK, 1 = terburuk):
  - Naik ke zona buruk: **NTB 34 → 7**, **Sulawesi Barat 36 → 11**, Papua Tengah 25 → 6, NTT 31 → 13, Lampung 24 → 8.
  - Turun ke zona baik: **Kep. Riau 5 → 35**, **DKI Jakarta 8 → 37**, Kalimantan Timur 11 → 32, Banten 3 → 21.
- Monte Carlo 1.000 bobot: Aceh (100%), Maluku (98%), dan Sumatera Barat (89%) hampir selalu masuk 10 terburuk ("prioritas tangguh").

## 4. Langkah berikutnya

1. **Ambil data semua tahun.** Halaman web BPS hanya menampilkan tahun terbaru. Untuk 2015–2025, salah satu anggota tim perlu:
   - Mendaftar **gratis** di https://webapi.bps.go.id/developer/ untuk mendapatkan *key*.
   - Lalu menjalankan di PowerShell:
     ```powershell
     $env:BPS_KEY = "isi-key-di-sini"; python scripts/ambil_panel_bps.py
     ```
   - Hasilnya masuk ke `Raw_Dataset/bps_webapi/` (CSV + JSON asli sebagai bukti sumber). Key tidak disimpan di file.
   - *Alternatif manual:* buka setiap tabel di bps.go.id, pilih tahun, klik Unduh (±18 tabel × 8–11 tahun).
2. Unduh juga **file resmi (xlsx) tahun terbaru** dari tombol Unduh setiap tabel untuk dimasukkan ke ZIP sebagai raw dataset resmi.
3. Data pendukung yang belum diambil: PDRB menurut lapangan usaha per provinsi (publikasi D20), RLS dan kemiskinan kab/kota (untuk LISA kab/kota), dan centroid lat/long provinsi/kab-kota.
