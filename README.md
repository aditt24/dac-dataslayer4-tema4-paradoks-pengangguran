# Paradoks Pengangguran Rendah
### Pendidikan, Kualitas Pekerjaan, dan Peta Kerentanan Pasar Kerja Indonesia
**DAC Data Slayer 4.0 · Tema 4: Pendidikan untuk Masa Depan Dunia Kerja**

> Angka pengangguran yang rendah bisa menyembunyikan pekerjaan yang tidak layak. Pasar kerja Indonesia punya dua wajah yang berbeda secara statistik, yaitu **"tidak bekerja"** dan **"bekerja tetapi tidak layak"**. Pendidikan menentukan wajah mana yang dialami seseorang, sedangkan struktur ekonomi wilayah menentukan seberapa besar kerja tidak layaknya.

📄 **Konsep lengkap:** [`KONSEP_FINAL_DAC_TEMA4.md`](KONSEP_FINAL_DAC_TEMA4.md)

---

## Temuan utama (data BPS 2015–2025)
- **Paradoks SMK konsisten 11 tahun.** Lulusan SMK punya pengangguran tertinggi (8,63% pada 2025), tetapi lebih formal daripada lulusan SMA. Lulusan ≤SD hampir tidak menganggur (2,30%), tetapi 68% bekerja informal.
- **Informalisasi lulusan terdidik.** Lulusan PT yang bekerja informal (non-pertanian) naik dari 8,2% (2015) menjadi 16,6% (2025).
- **Dua wajah pasar kerja (PCA):** *tidak bekerja* (pengangguran + NEET) dan *bekerja tidak layak* (informal + setengah pengangguran) terpisah secara statistik.
- **Pengangguran tidak mencerminkan kerja layak.** NTB peringkat pengangguran 34 tetapi peringkat kerja tidak layak 2; DKI dari 7 ke 38.
- **Aceh dan Maluku** menjadi prioritas di 100% dari 1.000 skenario bobot (Monte Carlo).
- **66 kab/kota persisten ganda**: selalu di atas TPT nasional dan di atas median sesama kota/kabupaten pada 2017–2025. Posisi kab/kota hampir tidak berubah antartahun (ρ = 0,91), dan model ML tidak lebih akurat dari tebakan naif.

## Struktur repositori
```
├── KONSEP_FINAL_DAC_TEMA4.md        # Konsep final (v6)
├── docs/                            # Spesifikasi dashboard, rencana v6, riset, arsip konsep v4/v5
├── Raw_Dataset/
│   ├── bps_webapi/                  # Data BPS via WebAPI 2015–2026 (CSV + JSON asli per tahun)
│   ├── bps_web_terbaru/             # Snapshot tabel BPS tahun terbaru
│   ├── bps_jateng/                  # Tabel BPS Provinsi Jawa Tengah (cek silang & paper)
│   ├── bps_static/                  # Tabel statis BPS (urbanisasi)
│   └── spasial_non_bps/             # geoBoundaries (NON-BPS; disimpan, menunggu jawaban panitia)
├── Processed_Dataset/
│   ├── tableau/                     # Paket data dashboard (t1–t7)
│   ├── v6/                          # Kab/kota nasional, provinsi pembanding, uji forecast
│   ├── v5/                          # Analisis jenjang & provinsi (PCA, kuadran, Monte Carlo)
│   └── v4/, preliminary/            # Versi sebelumnya (jejak audit)
├── Spatial/                         # SHP/GeoJSON turunan geoBoundaries (NON-BPS; tidak dipakai di dashboard)
└── scripts/                         # Seluruh skrip pengambilan & analisis data
```

## File untuk dashboard (`Processed_Dataset/tableau/`)
| File | Isi |
|---|---|
| `t1_jenjang_tren.csv` | TPT, informal non-pertanian, setengah pengangguran per jenjang 2015–2025 |
| `t2_jenjang_sektor_2025.csv` | Distribusi sektor per jenjang |
| `t3_provinsi_2025.csv` | 38 provinsi: indikator, dua dimensi, kuadran, ranking, Monte Carlo, tile map, pembanding |
| `t4_pembanding.csv`, `t4_pembanding_uji.csv` | Provinsi pembanding (kNN 2018) dan hasil ujinya |
| `t5_kabkota_tren.csv`, `t5_kabkota_jejak.csv` | TPT 514 kab/kota 2017–2025 dan persistensinya |
| `t6_transisi_2018_2025.csv` | Perpindahan kuadran 2018 → 2025 |
| `t7_uji_forecast_kabkota.csv` | Uji mundur forecast kab/kota (kartu metode) |

Spesifikasi visual: [`docs/SPEK_DASHBOARD_TABLEAU.md`](docs/SPEK_DASHBOARD_TABLEAU.md).

## Menjalankan ulang
```bash
pip install pandas numpy scipy statsmodels scikit-learn pyshp
# (opsional) ambil ulang data BPS — butuh key gratis dari https://webapi.bps.go.id/developer/
export BPS_KEY="key-anda"        # PowerShell: $env:BPS_KEY = "key-anda"
python scripts/ambil_panel_bps.py
# analisis
python scripts/analisis_lanjutan_v5.py
python scripts/olah_kabkota_nasional.py
python scripts/analisis_pembanding_v6.py
python scripts/uji_forecast_kabkota_nasional.py
python scripts/siapkan_tableau.py
```
Key WebAPI **tidak disimpan** di repositori. Isi lewat environment variable.

## Sumber data & lisensi
- **Badan Pusat Statistik (BPS)**: bps.go.id dan jateng.bps.go.id (Sakernas, Susenas, proyeksi penduduk). Semua angka statistik berasal dari BPS. Tautan tabel ada di konsep §9.
- **Batas wilayah kab/kota**: [geoBoundaries](https://www.geoboundaries.org/) IDN ADM2 (2020). Sumber asli: BPS, WFP, dan OCHA ROAP via HDX. Lisensi **CC BY 3.0 IGO**. Tidak dipakai di dashboard v6; disimpan sampai panitia menjawab apakah poligon non-BPS boleh dipakai (FAQ 3, 12).
- Literatur: lihat daftar referensi di konsep (DOI terverifikasi).

## Catatan metodologi
Semua hubungan bersifat **asosiasi**, bukan kausal. IDKK/KTL adalah konstruksi analitis tim, **bukan indikator resmi BPS**. Estimasi (urbanisasi 2018, TPT provinsi induk Papua) diberi label dan dibedakan dari data BPS (FAQ 15). Provinsi pembanding adalah alat banding deskriptif, bukan prediksi.
