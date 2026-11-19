# Paradoks Pengangguran Rendah
### Pendidikan, Kualitas Pekerjaan, dan Peta Kerentanan Pasar Kerja Indonesia
**DAC Data Slayer 4.0 · Tema 4: Pendidikan untuk Masa Depan Dunia Kerja**

> Angka pengangguran yang rendah bisa menyembunyikan pekerjaan yang tidak layak. Pasar kerja Indonesia punya dua wajah yang berbeda secara statistik, yaitu **"tidak bekerja"** dan **"bekerja tetapi tidak layak"**. Pendidikan menentukan wajah mana yang dialami seseorang, sedangkan struktur ekonomi wilayah menentukan seberapa besar kerja tidak layaknya.

📄 **Konsep lengkap:** [`KONSEP_FINAL_DAC_TEMA4.md`](KONSEP_FINAL_DAC_TEMA4.md)

---

## Temuan utama (data BPS 2015–2025)
- **Paradoks SMK konsisten 11 tahun berturut-turut.** Lulusan SMK punya pengangguran tertinggi (8,63% pada 2025), tetapi lebih formal daripada lulusan SMA. Lulusan ≤SD hampir tidak menganggur (2,30%), tetapi 68% bekerja informal.
- **Informalisasi lulusan terdidik.** Lulusan PT yang bekerja informal (non-pertanian) naik dari 8,2% (2015) menjadi 16,6% (2025).
- **Analisis faktor (PCA)** membuktikan dua dimensi terpisah: *tidak bekerja* (pengangguran + NEET) dan *bekerja tidak layak* (informal + setengah pengangguran).
- **Pengangguran tidak mencerminkan kerja layak.** Contoh: NTB berada di peringkat pengangguran 34 tetapi peringkat kerja tidak layak 2; DKI Jakarta dari 7 ke 38.
- **Aceh dan Maluku** menjadi prioritas di 100% dari 1.000 skenario bobot (Monte Carlo).
- **Jawa Tengah**: paradoks berlaku di 35/35 kab/kota. Hotspot pengangguran signifikan di Cilacap–Banyumas–Purbalingga–Tegal–Brebes (Moran's I = 0,62; p = 0,001).

## Struktur repositori
```
├── KONSEP_FINAL_DAC_TEMA4.md        # Konsep final (v5)
├── docs/                            # Riset pendukung, audit data, panduan, arsip konsep
├── Raw_Dataset/
│   ├── bps_webapi/                  # Data BPS via WebAPI 2015–2026 (CSV + JSON asli per tahun)
│   ├── bps_web_terbaru/             # Snapshot tabel BPS tahun terbaru
│   ├── bps_jateng/                  # Tabel BPS Provinsi Jawa Tengah (kab/kota)
│   ├── bps_static/                  # Tabel statis BPS (urbanisasi)
│   └── spasial_non_bps/             # geoBoundaries IDN ADM2 (GeoJSON asli)
├── Processed_Dataset/
│   ├── v5/                          # Hasil analisis final (siap impor ke Power BI)
│   ├── v4/, preliminary/            # Versi analisis sebelumnya (jejak audit)
├── Spatial/                         # Shapefile (SHP) & GeoJSON siap pakai
│   ├── IDN_kabkota_2020/            # 519 kab/kota Indonesia
│   ├── JATENG_kabkota_analisis/     # 35 kab/kota Jateng + atribut hasil analisis (TPT, LISA)
│   └── JATENG_kabkota.geojson
└── scripts/                         # Seluruh skrip pengambilan & analisis data
```

## File utama untuk dashboard (`Processed_Dataset/v5/`)
| File | Isi |
|---|---|
| `A_edu_trend_long.csv` | TPT, informal non-pertanian, setengah pengangguran per jenjang 2015–2025 |
| `A_kejadian_covid_jenjang.csv` | Guncangan & pemulihan COVID per jenjang |
| `A_proyeksi_2026_2030.csv` | Proyeksi TPT SMK/SMA & gap (**berlabel PROYEKSI**, interval 80%) |
| `B_prov_master_2025.csv` | 38 provinsi: indikator, indeks dua dimensi, kuadran, ranking, Monte Carlo |
| `B_uji_ketahanan.csv` | Seluruh uji ketahanan (tanpa Papua, kontrol urbanisasi) |
| `C_loading_faktor.csv` | Loading analisis faktor (PCA + varimax) |
| `D_transisi_2018_2025.csv`, `D_matriks_transisi.csv` | Perpindahan kuadran 2018 → 2025 |
| `E_panel_fe.csv`, `E_panel_2018_2025.csv` | Panel fixed effects 32 provinsi |
| `F_jateng_*.csv` | Jawa Tengah: TPT × pendidikan 2019–2023, LISA, matriks ketetanggaan |

## Menjalankan ulang
```bash
pip install pandas numpy scipy statsmodels scikit-learn pyshp
# (opsional) ambil ulang data BPS — butuh key gratis dari https://webapi.bps.go.id/developer/
export BPS_KEY="key-anda"        # PowerShell: $env:BPS_KEY = "key-anda"
python scripts/ambil_panel_bps.py
# analisis
python scripts/analisis_lanjutan_v5.py
python scripts/buat_shp.py
```
Key WebAPI **tidak disimpan** di repositori. Isi lewat environment variable.

## Sumber data & lisensi
- **Badan Pusat Statistik (BPS)**: bps.go.id dan jateng.bps.go.id (Sakernas, Susenas, proyeksi penduduk). Semua angka statistik berasal dari BPS. Tautan tabel ada di konsep §9.
- **Batas wilayah kab/kota**: [geoBoundaries](https://www.geoboundaries.org/) IDN ADM2 (2020). Sumber asli: BPS, WFP, dan OCHA ROAP via HDX. Lisensi **CC BY 3.0 IGO**. Hanya dipakai untuk visual peta dan matriks ketetanggaan, bukan sebagai data statistik.
- Literatur: lihat daftar referensi di konsep (DOI terverifikasi).

## Catatan metodologi
Semua hubungan bersifat **asosiasi**, bukan kausal. IDKK/KTL adalah konstruksi analitis tim, **bukan indikator resmi BPS**. Proyeksi diberi label jelas dan dibedakan dari data BPS (sesuai FAQ 15 DAC).
