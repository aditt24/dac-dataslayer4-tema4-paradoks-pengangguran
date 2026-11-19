# Rencana Perubahan Repo Adit (v5 → v6)

Repo: github.com/aditt24/dac-dataslayer4-tema4-paradoks-pengangguran
Disusun 19 Nov 2026. Dasar: guidebook DAC, rekap FAQ 1–39, dan uji ulang data.

## A. Keputusan tim yang berubah
1. Skala **nasional penuh**. Jawa Tengah tidak diistimewakan. Wilayah yang diklik di-highlight.
2. Forecasting ML **dibuang** dari dashboard (uji mundur 514 kab/kota: linear & GB tidak lebih baik secara berarti dari tebakan naif; MAE 0,505/0,521 vs 0,511).
3. Fokus pada 4 fitur unggulan (FAQ 20: sedikit faktor tapi dalam).
4. Platform: Power BI atau Tableau Public, **belum diputuskan**.

## B. File yang dikeluarkan dari dashboard/ZIP
Data non-BPS **tetap disimpan di repo** sampai panitia menjawab soal poligon. Jika dilarang, cukup tidak dimasukkan ke ZIP.

| File/folder | Alasan |
|---|---|
| `Raw_Dataset/spasial_non_bps/` | geoBoundaries bukan portal BPS (FAQ 3). Risiko diskualifikasi |
| `Spatial/` (SHP/GeoJSON geoBoundaries) | Sama. Ukuran ZIP juga membengkak (FAQ 31) |
| `Processed_Dataset/v5/F_jateng_matriks_ketetanggaan.csv` | Diturunkan dari geoBoundaries; Kota Magelang & Salatiga salah tercatat "tanpa tetangga" |
| `Processed_Dataset/v5/A_proyeksi_2026_2030.csv` (dari dashboard) | OLS 11 titik + dummy COVID, lemah. Boleh tinggal di paper |
| `E_panel_fe.csv`, `C_loading_faktor.csv` (dari dashboard) | Terlalu teknis untuk 2 halaman. Pindah ke paper |

## C. Data yang ditambah
| File baru | Isi | Status |
|---|---|---|
| `Processed_Dataset/v6/kabkota_tpt_2017_2025.csv` + `kabkota_jejak_2017_2025.csv` (skrip `scripts/olah_kabkota_nasional.py`) | TPT 514 kab/kota 2017–2025 dari JSON WebAPI K01 yang sudah ada (var 2824, kolom Jumlah), kode BPS, TPT provinsi & nasional, persistensi | Sudah. 26 kab Papua dobel (kode lama 91/94) dibuang. 2018–2025 identik dengan BPS Jateng; 2017 beda ±0,1 (revisi) dan **Kota Pekalongan 2017 = 10,44 vs 5,05 di BPS Jateng** (anomali → dikosongkan). Lombok Utara 2018 kosong. 4 provinsi Papua baru: TPT provinsi < 2024 diisi dari induk (ditandai) |
| `Raw_Dataset/bps_jateng/J01_tpt_kabkota.csv` (diperluas) | TPT 35 kab Jateng 2007–2025 (tanpa 2016), format sama dengan J01 lama | Sudah. Nilai 2025 identik dengan J01 lama |
| Batas wilayah dari sig.bps.go.id | Untuk peta & tetangga | Sudah dicek: hanya WMS gambar, tidak ada unduhan SHP. Tidak di-scrape. Dashboard pakai tile map |
| Lat/long kab/kota | Hanya visual peta (FAQ 12) | Belum ditentukan sumbernya |

## D. Analisis yang ditambah (nama file sesuai repo)
| Skrip → output (`Processed_Dataset/v6/`) | Isi |
|---|---|
| `scripts/analisis_pembanding_v6.py` → `pembanding_provinsi.csv`, `pembanding_uji.csv` | kNN k=3 pada kondisi 2018 (7 indikator, kemiskinan **Maret**), perubahan 2018→2025 berdampingan. Uji stabilitas, uji vs acak, **uji vs regresi ke rata-rata**. Tanpa target (gagal uji tandingan) |
| `scripts/olah_kabkota_nasional.py` → `kabkota_tpt_2017_2025.csv`, `kabkota_jejak_2017_2025.csv` | Per kab/kota: tahun di atas provinsi / nasional / **median sejenis**, status `persisten_tinggi`, `persisten_sejenis`, `persisten_ganda` |
| `scripts/uji_forecast_kabkota_nasional.py` → `uji_forecast_kabkota_nasional.csv` | Uji mundur 514 kab/kota: naif vs linear vs GB (untuk kartu metode) |
| `scripts/uji_forecast_kabkota_jateng.py` → `uji_forecast_kabkota_jateng.csv` | Versi 35 kab Jateng + fitur tetangga (butuh matriks non-BPS) → paper saja |
| `scripts/siapkan_tableau.py` → `Processed_Dataset/tableau/t1…t7` | Paket data dashboard |

## E. Isi konsep (`KONSEP_FINAL_DAC_TEMA4.md`) yang diubah
| Bagian | Perubahan |
|---|---|
| T6 / KPI "ρ = −0,30" | p = 0,066 (tanpa Papua p = 0,18), tidak signifikan. Label [BERSYARAT]. Klaim cukup "TPT tidak mencerminkan kerja layak", bukan "terbalik" |
| T11 / H8 (RLS → NEET) | Sebut sebagian mekanis (NEET = tidak sekolah). Pindah ke paper |
| T13–T15, H10–H12, langkah ⑤–⑥ | Ganti dari khusus Jateng menjadi "pilih provinsi → kab/kota" (nasional) |
| Judul Halaman 2 | Jangan "ke Jawa Tengah". Usul: "Dari Provinsi ke Kab/Kota" |
| §9 Dataset, §10 Validasi | Hapus geoBoundaries. Tambah K01 2017–2025 |
| Rekomendasi Jawa Tengah | Ganti: kab/kota persisten tinggi secara nasional |
| Kuadran | Tandai provinsi dekat batas. Sebut v4 vs v5 hanya cocok 61% (sensitif definisi), jangan jadi headline tunggal |
| Checklist | Surat orisinalitas bermeterai (FAQ 37). Watermark versi terbaru, warna tidak diubah (FAQ 35). PDF berisi link publik bila ada (FAQ 37). Nama tim ≤20 karakter |

## F. Rancangan dashboard v6
**Halaman 1 — Dua Wajah Masalah Kerja (jenjang, nasional)**
- KPI, dumbbell jenjang, tren 2015–2025 (tanpa pita proyeksi), dampak COVID, heatmap jenjang × sektor.

**Halaman 2 — Pengangguran Rendah, Kerja Tidak Layak (provinsi → kab/kota)**
1. Peta Berbalik 38 provinsi + mode cerita (bookmark, tetap 1 halaman).
2. Kamu Jadi Penimbang: slider bobot + pita ketidakpastian + "stabil x/10".
3. Provinsi Pembanding: klik provinsi → 3 pembanding di-highlight + dumbbell 2018→2025 (tanpa kartu target).
4. Jejak Kab/Kota: pilih provinsi → heatmap kab/kota × 2017–2025 + titik lat/long. Default PDF: 15–20 kab/kota paling persisten nasional. Kartu: "4 model ML tidak mengalahkan tebakan naif → pengangguran kab/kota bersifat struktural".
- Rekomendasi per kuadran + narasi dinamis.

## G. Urutan kerja
1. Tim setujui A–F. Pilih platform.
2. Ambil K01 2017–2025 (WebAPI, key Adit). Cek sig.bps.go.id.
3. Jalankan `analisis_pembanding_v6.py` + `olah_kabkota_nasional.py`. ✅ Kembaran gagal uji vs regresi ke rata-rata → sudah diturunkan jadi "provinsi pembanding".
4. Revisi konsep → v6.
5. Bangun dashboard (Hal. 1 lalu Hal. 2).
6. Cek silang angka, PDF, ZIP ≤100 MB, surat bermeterai, kirim sebelum 23 Nov 18.00.

## H. Status per 19 Nov 2026 (malam)
- ✅ Konsep v6 ditulis (`KONSEP_FINAL_DAC_TEMA4.md`); v5 diarsipkan di `docs/KONSEP_FINAL_DAC_TEMA4_v5_arsip.md`.
- ✅ Kembaran → Provinsi Pembanding (tanpa target). Kemiskinan diseragamkan ke Maret.
- ✅ Uji forecast nasional 514 kab/kota + hasil disimpan ke CSV; versi Jateng juga disimpan ke CSV.
- ✅ Jejak kab/kota: pembanding median sejenis + perbaikan hitung NaN + TPT provinsi induk Papua.
- ✅ Spesifikasi Tableau: penjaga bobot 0, prioritas stabil dipisah dari slider, pesan pembanding kosong, label contoh NTB di PDF.
- ⏳ Jawaban panitia soal poligon non-BPS. ⏳ Keputusan platform.
