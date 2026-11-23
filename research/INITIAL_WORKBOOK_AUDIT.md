# Audit Awal Workbook — 22 Nov 2026

Metode: .twbx di-unzip ke folder sementara (read-only), XML .twb dibaca. Workbook belum dibuka di Tableau Desktop pada titik audit ini.

## File
| File | Ukuran | Waktu | Catatan |
|---|---|---|---|
| DAC_Dashboard_Tema4_new.twbx | 1.342.433 B | 22 Nov 19:07 | Identik byte-per-byte dengan BACKUP |
| DAC_Dashboard_Tema4_BACKUP.twbx | 1.342.433 B | 22 Nov 19:07 | Salinan `new`, JANGAN diubah |
| DAC_Dashboard_Tema4_WORKING.twbx | 1.339.731 B | 22 Nov 20:14 | Salinan kerja, lebih baru; 25 worksheet, 3 dashboard (sama dengan new) |
Tableau versi file 18.1 (Windows). Watermark: `Image/New_Watermark.png` (dipakai sebagai latar bitmap tiap dashboard).

## Dashboard (semua Fixed 1900×1100)
1. **Hal 1 - Dua Wajah**: 4 KPI (TPT nasional, TPT SMK, informal PT, NEET), A Dumbbell, B Tren TPT, C Heatmap sektor, D COVID bar, E Donut SMK sektor, F Informal 2015 vs 2025.
2. **Hal 2 - Provinsi ke KabKota**: E Peta Geo (poligon provinsi) + Peta Berbalik (tile) + Teks Cerita + Narasi, F Kuadran, G Penimbang + Pesan Bobot, H Mini Tile + Dumbbell Pembanding + Pesan, I KPI + Jejak KabKota.
3. **Hal 3 - Bukti Tambahan**: H2-J Kab vs Kota (pie), H2-K Struktur Scatter, H2-L Forecast Bar.

## Data source (6) 
t7_forecast_long, "Provinsi & KabKota" (gabungan t3/t4/t5), Jenjang Tren (t1), NEET Nasional, Jenjang Sektor (t2), IDN_provinsi_38+ (geometri provinsi).

## Parameter (8) dan nilai tersimpan
Pilih Provinsi = **"MALUKU"** (spec: Indonesia), Mode Peta = "Kerja tidak layak" (sesuai spec PDF), Pembanding Jejak = "Sesama kota/kabupaten", Langkah Cerita = **2** (spec: 1), W TPT/NEET/Setengah/Informal = 0,25.

## Aksi
Hanya 1: parameter action "Klik provinsi" (set Pilih Provinsi). Tidak ada highlight/filter action/navigasi.

## Calculated field (ada & sesuai spec)
Rank Peta, Terpilih, Skor Dinamis (slider bobot), Rank Dinamis, Lebar Pita, Tanda Stabil (★), Pesan Bobot, Provinsi H, P1–P3 Terpilih, Peran Pembanding, Judul H, Pesan Pembanding, Tampil KabKota, Status Tahun, Catatan Data (label ESTIMASI/anomali), Urut Jejak, Batas Baris (top 20 bila Indonesia), Teks Cerita (CASE 4 langkah), KPI Jenjang, dsb.

## Temuan / risiko (urut prioritas)
1. **Hal 3 melanggar batas 2 halaman** (guidebook, FAQ 35–36). Harus dihapus dari berkas kumpul, atau isinya dilipat ke Hal 2 (bukan tab terpisah).
2. Default parameter bukan sesuai spec PDF: `Pilih Provinsi` MALUKU (spec Indonesia → 66 persisten ganda & ajakan klik), `Langkah Cerita` 2 (spec 1). Perlu keputusan: panel H memakai "Contoh: NTB" saat Indonesia.
3. **Donut/pie** (H1-E, H2-J) dan bar COVID (H1-D) = visual yang kemungkinan redundan; periksa apakah punya pesan unik sebelum dipertahankan.
4. Hanya satu aksi interaktif; belum ada tombol reset eksplisit, tidak ada penanda sedang di halaman mana (navigasi).
5. Banyak zona duplikat di XML dashboard (layout ganda tercatat) — periksa di GUI apakah ada elemen bertumpuk.
6. Judul sheet H2-H Dumbbell memakai field dinamis `<...>`; cek tampil benar.
7. Data sumber ada ekstrak .hyper di `Data/TableauTemp*` (aman dalam twbx; ukuran 1,3 MB, jauh di bawah 100 MB).

## Pertahankan
Seluruh calculated field & parameter action; struktur dua halaman; tile map; kuadran; penimbang; jejak kab/kota; label ESTIMASI; kartu metode.

## Didesain ulang / diperiksa
Layout visual (hirarki, spasi), tooltip, navigasi, default parameter, konsolidasi Hal 3, pemakaian donut/pie.
