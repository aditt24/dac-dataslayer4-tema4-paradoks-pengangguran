# Rencana Perubahan Repo Adit (v5 → v6)

Repo: github.com/aditt24/dac-dataslayer4-tema4-paradoks-pengangguran
Disusun 19 Nov 2026. Dasar: guidebook DAC, rekap FAQ 1–39, dan uji ulang data.

## A. Keputusan tim yang berubah
1. Skala **nasional penuh**. Jawa Tengah tidak diistimewakan. Wilayah yang diklik di-highlight.
2. Forecasting ML **dibuang** dari dashboard (uji mundur: 4 model kalah dari tebakan naif).
3. Fokus pada 4 fitur unggulan (FAQ 20: sedikit faktor tapi dalam).
4. Platform: Power BI atau Tableau Public, **belum diputuskan**.

## B. File yang dihapus atau dikeluarkan dari ZIP
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
| `Raw_Dataset/bps_web_terbaru/K01_tpt_kabkota_2017_2025.csv` | TPT 514 kab/kota 2017–2025 (tabel `MjgyNCMy` atau tabel total kab/kota) | Belum diambil. Cek apakah ada kolom total |
| `Raw_Dataset/bps_jateng/J01_tpt_kabkota.csv` (diperluas) | TPT 35 kab Jateng 2007–2025 (tanpa 2016), format sama dengan J01 lama | Sudah. Nilai 2025 identik dengan J01 lama |
| Batas wilayah dari sig.bps.go.id (jika bisa diunduh) | Untuk peta & tetangga | Belum dicek |
| Lat/long kab/kota | Hanya visual peta (FAQ 12) | Belum ditentukan sumbernya |

## D. Analisis yang ditambah (`scripts/analisis_v6.py`)
| Output | Isi |
|---|---|
| `G_kembaran_provinsi.csv` | kNN k=3 pada kondisi 2018 (urban, RLS, informal, setengah pengangguran, NEET, TPT, miskin), perubahan 2018→2025, target dari kembaran terbaik. Wajib uji stabilitas (buang 1 fitur) + uji vs 3 provinsi acak |
| `H_jejak_kabkota.csv` | Per kab/kota: jumlah tahun TPT > rata-rata provinsinya dan > nasional (2017–2025), rata-rata selisih, status persisten |
| `H_uji_forecast.csv` | Hasil uji mundur 4 model vs naif (untuk kartu kejujuran metode) |

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
3. Kembaran Provinsi: klik provinsi → 3 kembaran di-highlight + dumbbell 2018→2025 + kartu target.
4. Jejak Kab/Kota: pilih provinsi → heatmap kab/kota × 2017–2025 + titik lat/long. Default PDF: 15–20 kab/kota paling persisten nasional. Kartu: "4 model ML tidak mengalahkan tebakan naif → pengangguran kab/kota bersifat struktural".
- Rekomendasi per kuadran + narasi dinamis.

## G. Urutan kerja
1. Tim setujui A–F. Pilih platform.
2. Ambil K01 2017–2025 (WebAPI, key Adit). Cek sig.bps.go.id.
3. Jalankan `analisis_v6.py` (kembaran + jejak). Kalau kembaran gagal uji, turunkan jadi "provinsi pembanding".
4. Revisi konsep → v6.
5. Bangun dashboard (Hal. 1 lalu Hal. 2).
6. Cek silang angka, PDF, ZIP ≤100 MB, surat bermeterai, kirim sebelum 23 Nov 18.00.
