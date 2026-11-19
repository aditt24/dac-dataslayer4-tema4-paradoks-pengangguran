# Spesifikasi Dashboard Tableau (v6)

Panduan bangun untuk tim. Data: `Processed_Dataset/tableau/` (dibuat ulang dengan `python scripts/siapkan_tableau.py`).
Ukuran dashboard: **Fixed size 1900 × 1100**. Watermark resmi versi terbaru, warna tidak diubah (FAQ 35).
Semua visual dibuat tim di Tableau (FAQ 9). Dokumen ini hanya daftar data, formula, dan tata letak.

---

## 1. Sumber data

| File | Grain | Dipakai untuk |
|---|---|---|
| `t1_jenjang_tren.csv` | indikator × jenjang × tahun (2015–2025) | Dumbbell, tren, KPI Hal. 1 |
| `t2_jenjang_sektor_2025.csv` | sektor × jenjang | Heatmap Hal. 1 |
| `t3_provinsi_2025.csv` | 38 provinsi | Peta berbalik, penimbang, kuadran, narasi |
| `t4_pembanding.csv` | provinsi × 3 pembanding (32 provinsi) | Dumbbell perubahan 2018→2025 berdampingan |
| `t4_pembanding_uji.csv` | hasil uji | Kartu metode (termasuk keterbatasan) |
| `t5_kabkota_tren.csv` | 514 kab/kota × 2017–2025 | Heatmap jejak kab/kota |
| `t5_kabkota_jejak.csv` | 514 kab/kota | Daftar persisten, KPI |
| `t6_transisi_2018_2025.csv` | 32 provinsi | Panah kuadran 2018 → 2025 (opsional) |
| `t7_uji_forecast_kabkota.csv` | tahun target 2021–2025 + RATA2 | Kartu metode sheet I |

Relasi (Data Source → Relationships):
- `t3.wilayah` = `t4_pembanding.provinsi`
- `t3.wilayah` = `t5_kabkota_jejak.nama_prov` dan `t5_kabkota_tren.nama_prov`

Catatan data yang wajib ditulis di dashboard:
- `t1` jenjang "SD" = tamat SD ke bawah.
- `t5`: Kota Pekalongan 2017 dikosongkan (anomali sumber), Lombok Utara 2018 tidak tersedia di BPS.
- `t5`: kab/kota di 4 provinsi Papua baru memakai TPT provinsi induk sebelum 2024 (`tpt_prov_induk` = TRUE) → label ESTIMASI di tooltip.
- `t3`/`t4`: urbanisasi 2018 di pembanding = interpolasi proyeksi (ESTIMASI). Kemiskinan = periode Maret (2018 dan 2025).

---

## 2. Parameter

| Nama | Tipe | Nilai | Default |
|---|---|---|---|
| `Pilih Provinsi` | String, list | `Indonesia` + 38 nama dari `t3.wilayah` | `Indonesia` |
| `Mode Peta` | String, list | `Pengangguran (TPT)`, `Kerja tidak layak` | `Pengangguran (TPT)` |
| `W TPT` | Float 0–1, langkah 0,05 | slider | 0,25 |
| `W NEET` | Float 0–1, langkah 0,05 | slider | 0,25 |
| `W Setengah` | Float 0–1, langkah 0,05 | slider | 0,25 |
| `W Informal` | Float 0–1, langkah 0,05 | slider | 0,25 |
| `Langkah Cerita` | Integer 1–4 | tombol/slider | 1 |
| `Pembanding Jejak` | String, list | `Nasional`, `Sesama kota/kabupaten` | `Sesama kota/kabupaten` |

Tambahkan **Parameter Action**: klik tile provinsi di peta mana pun → set `Pilih Provinsi` = `wilayah`.

---

## 3. Calculated field

```
// Peta berbalik: nilai yang diwarnai (1 = paling buruk)
[Rank Peta]       = IF [Mode Peta] = "Pengangguran (TPT)" THEN [rank_tpt] ELSE [rank_ktl] END

// Highlight wilayah terpilih (dipakai di semua sheet provinsi)
[Terpilih]        = [wilayah] = [Pilih Provinsi]

// Penimbang: skor & ranking dinamis (sama dengan Monte Carlo di skrip v5, 4 komponen min-max)
[Total Bobot]     = [W TPT] + [W NEET] + [W Setengah] + [W Informal]
[Skor Dinamis]    = IF [Total Bobot] = 0 THEN NULL     // semua slider 0 -> tampilkan pesan "isi minimal satu bobot"
                    ELSE 100 * ([W TPT]*[z_tpt] + [W NEET]*[z_neet] + [W Setengah]*[z_tsp] + [W Informal]*[z_informal])
                         / [Total Bobot] END
[Rank Dinamis]    = RANK(SUM([Skor Dinamis]), 'desc')          // compute using: wilayah
[Prioritas Stabil] = [prob_top10] >= 0.9
                    // STATIS dari Monte Carlo 1.000 skenario, TIDAK ikut slider. Tampilkan sebagai penanda (★) di bar
                    // dan teks tetap: "3 provinsi masuk 10 terburuk di ≥90% skenario: Aceh, Maluku, Maluku Utara".
                    // Jangan dicampur dengan [Rank Dinamis]: slider = eksplorasi juri, Monte Carlo = jawaban tim.

// Pembanding: peran tiap tile terhadap provinsi terpilih
[P1 Terpilih]     = { FIXED : MAX(IF [wilayah] = [Pilih Provinsi] THEN [pembanding_1] END) }
[P2 Terpilih]     = { FIXED : MAX(IF [wilayah] = [Pilih Provinsi] THEN [pembanding_2] END) }
[P3 Terpilih]     = { FIXED : MAX(IF [wilayah] = [Pilih Provinsi] THEN [pembanding_3] END) }
[Peran Pembanding]= IF [wilayah] = [Pilih Provinsi] THEN "Terpilih"
                    ELSEIF [wilayah] = [P1 Terpilih] OR [wilayah] = [P2 Terpilih] OR [wilayah] = [P3 Terpilih] THEN "Pembanding"
                    ELSE "Lain" END
[Pesan Pembanding]= IF [Pilih Provinsi] <> "Indonesia" AND ISNULL([P1 Terpilih])
                    THEN "Pembanding tidak tersedia: wilayah provinsi ini berubah karena pemekaran Papua 2022, data 2018 tidak sebanding." END

// Narasi dinamis (pengganti Smart Narrative)
[Narasi Provinsi] = IF ISNULL([Pilih Provinsi]) OR [Pilih Provinsi] = "Indonesia"
                    THEN "Klik provinsi di peta untuk melihat posisinya."
                    ELSE [wilayah] + ": peringkat pengangguran " + STR([rank_tpt]) + " dari 38, peringkat kerja tidak layak "
                         + STR([rank_ktl]) + ". Tipe: " + [kuadran] + "." END

// Kab/kota: hanya provinsi terpilih; default = semua kab/kota persisten tinggi
[Tampil KabKota]  = IF [Pilih Provinsi] = "Indonesia" THEN [persisten_ganda] ELSE [nama_prov] = [Pilih Provinsi] END
[Acuan Tahun]     = IF [Pembanding Jejak] = "Nasional" THEN [tpt_nasional] ELSE [tpt_median_sejenis] END
[Status Tahun]    = IF ISNULL([tpt]) THEN "Tidak ada data"
                    ELSEIF [tpt] > [Acuan Tahun] THEN "Di atas acuan" ELSE "Di bawah acuan" END
```

---

## 4. Palet warna (konsisten di semua visual)

| Makna | Warna |
|---|---|
| Rentan Ganda | `#B2182B` |
| Rentan Tersembunyi | `#EF8A62` |
| Antrean Kerja Formal | `#67A9CF` |
| Relatif Layak | `#1B7837` |
| Ranking peta (sekuensial) | 1 = `#7F0000` → 38 = `#FEE8C8` |
| Terpilih / sorotan | garis tepi `#111111`, tebal 2 px |
| Lain / konteks | `#D9D9D9` |
| Di atas nasional / di bawah | `#C0392B` / `#E8E8E8` |
| Teks utama / sekunder | `#1F1F1F` / `#6B6B6B` |

Font ≥10 pt. Judul visual = **kalimat temuan**, bukan nama grafik. Tooltip selalu memuat sumber tabel BPS.

---

## 5. Halaman 1 — "Dua Wajah Masalah Kerja Lulusan" (1900 × 1100)

```
y=0    ┌──────────────────────────────────────────────────────────────────────────────┐
       │ JUDUL + 1 kalimat pesan                                          [WATERMARK]  │ h=110
y=110  ├──────────┬──────────┬──────────┬──────────┬───────────────────────────────────┤
       │ KPI TPT  │ KPI TPT  │ KPI Info-│ KPI NEET │ Mode cerita: [1][2][3][4]          │ h=130
       │ 4,85%    │ SMK 8,63%│ rmal PT  │ 19,4%    │                                   │
       │          │          │ 8%→17%   │          │                                   │
y=240  ├──────────┴──────────┴──────────┴──────────┼───────────────────────────────────┤
       │ A. DUMBBELL JENJANG 2025                   │ B. TREN TPT PER JENJANG 2015–2025  │ h=430
       │ TPT vs informal non-pertanian per jenjang  │ sorot SMK & SMA, pita COVID 2020   │
       │ w=950                                      │ w=950                              │
y=670  ├────────────────────────────────────────────┼───────────────────────────────────┤
       │ C. HEATMAP JENJANG × SEKTOR 2025           │ D. 3 kartu insight + jembatan:     │ h=380
       │ (10 sektor terbesar)                       │ "Apakah dua wajah ini juga terlihat│
       │                                            │  antarprovinsi? → Halaman 2"       │
y=1050 ├────────────────────────────────────────────┴───────────────────────────────────┤
       │ Definisi & sumber BPS                                                         │ h=50
       └──────────────────────────────────────────────────────────────────────────────┘
```

| Sheet | Isi | Judul temuan |
|---|---|---|
| A | `t1` tahun = 2025, indikator TPT & informal_nonag, jenjang di sumbu Y (urut_jenjang), dua titik + garis | "Lulusan SD hampir tidak menganggur (2,3%), tapi 68% kerja informal; SMK paling banyak menganggur, tapi lebih formal" |
| B | `t1` indikator = TPT, garis per jenjang, SMK & SMA berwarna, lainnya abu | "SMK selalu punya pengangguran tertinggi, 11 tahun berturut-turut" |
| C | `t2`, sektor × jenjang, warna = persen | "Lulusan SMK bergantung pada industri & perdagangan; sepertiga sarjana di jasa pendidikan" |
| D | Teks | 3 kalimat bacaan + pertanyaan jembatan |

---

## 6. Halaman 2 — "Pengangguran Rendah, Kerja Tidak Layak: Dari Provinsi ke Kab/Kota"

```
y=0    ┌──────────────────────────────────────────────────────────────────────────────┐
       │ JUDUL · [Pengangguran (TPT) | Kerja tidak layak] · Narasi dinamis  [WATERMARK]│ h=110
y=110  ├────────────────────────────────────────────────┬─────────────────────────────┤
       │ E. PETA BERBALIK (tile map 38 provinsi)         │ F. KUADRAN DUA WAJAH         │ h=430
       │ warna = [Rank Peta], tepi tebal = [Terpilih]    │ x = tidak_bekerja, y = ktl,   │
       │ w=1150                                          │ warna = kuadran, garis median │
y=540  ├──────────────────────┬─────────────────────────┼─────────────────────────────┤
       │ G. PENIMBANG          │ H. PROVINSI PEMBANDING   │ I. JEJAK KAB/KOTA 2017–2025  │ h=500
       │ 4 slider bobot        │ mini tile map [Peran     │ heatmap kab/kota × tahun,    │
       │ + bar ranking dinamis │ Pembanding] + dumbbell   │ warna = [Status Tahun],      │
       │ + pita p05–p95        │ informal 2018→2025       │ filter [Tampil KabKota]      │
       │ + ★ prioritas stabil  │ + kartu metode (no target)│ + KPI 66 persisten ganda    │
       │ w=560                 │ w=590                    │ w=750                        │
y=1040 ├──────────────────────┴─────────────────────────┴─────────────────────────────┤
       │ Rekomendasi per kuadran (1 baris) · Sumber BPS · Catatan metode                │ h=60
       └──────────────────────────────────────────────────────────────────────────────┘
```

| Sheet | Isi | Judul temuan | Interaksi |
|---|---|---|---|
| E | `t3`, Columns = `tile_x`, Rows = `tile_y` (reversed), mark Square, label singkatan, warna `[Rank Peta]` | "Peta pengangguran dan peta kerja tidak layak hampir berkebalikan: NTB peringkat 34 → 2, DKI 7 → 38" | Tombol `Mode Peta`; klik = set `Pilih Provinsi` |
| F | `t3` scatter + reference line median | "Empat tipe masalah: rendahnya pengangguran tidak berarti kerjanya layak" | Klik = set `Pilih Provinsi` |
| G | `t3` bar `[Rank Dinamis]`, Gantt `rank_p05`–`rank_p95`, ★ = `[Prioritas Stabil]` | "Geser bobotnya: Aceh dan Maluku tetap prioritas di 100% dari 1.000 skenario" | 4 slider; pesan jika total bobot 0 |
| H | `t3` tile mini warna `[Peran Pembanding]`; `t4_pembanding` filter `provinsi = [Pilih Provinsi]`, dumbbell `awal_informal` → `akhir_informal` untuk provinsi + 3 pembanding | "[Provinsi] dibandingkan 3 provinsi yang kondisinya mirip pada 2018" (tanpa angka target) | Ikut `Pilih Provinsi`; `[Pesan Pembanding]` bila kosong |
| I | `t5_kabkota_tren`, Rows = nama (urut `rata_tpt`), Columns = tahun, warna `[Status Tahun]`, filter `[Tampil KabKota]` | "66 kab/kota selalu di atas TPT nasional dan di atas sesamanya selama 9 tahun" | Ikut `Pilih Provinsi`; tombol `Pembanding Jejak` |

Kartu metode di H (wajib, dari `t4_pembanding_uji.csv`):
> "Pembanding = 3 provinsi paling mirip pada 2018 (kNN, 7 indikator BPS). Stabil 81% saat satu indikator dibuang. Ini alat banding, bukan ramalan: perubahan pembanding tidak lebih akurat daripada tren umum 'yang tinggi cenderung turun', jadi kami tidak memasang target."

Kartu metode di I (dari `t7_uji_forecast_kabkota.csv`, baris RATA2):
> "Kami menguji regresi linear dan gradient boosting untuk menebak posisi TPT 514 kab/kota tahun depan (2021–2025). Keduanya tidak lebih baik dari tebakan 'sama seperti tahun lalu' (galat 0,51 vs 0,51 poin), karena urutan kab/kota hampir tidak berubah (ρ = 0,91). Pengangguran kab/kota bersifat struktural."

Mode cerita (bookmark pengganti di Tableau = **Dynamic Zone Visibility**): buat field boolean per langkah (`[Langkah Cerita] = 1`, dst.) untuk menampilkan kotak teks sorotan di atas visual. Tetap 1 halaman (FAQ 36).

---

## 7. Status PDF default (yang dilihat juri di PDF)
- `Pilih Provinsi` = `Indonesia` → sheet I menampilkan 66 kab/kota persisten ganda, narasi berisi ajakan klik.
- `Mode Peta` = `Kerja tidak layak` (paradoks langsung terlihat), bobot semua 0,25.
- Sheet H butuh satu provinsi: di PDF tampilkan contoh statis NTB (filter khusus sheet H saat ekspor) **dengan judul "Contoh: NTB"**, supaya tidak bertentangan dengan narasi yang masih "Indonesia".

## 8. Checklist sebelum ekspor
- [ ] Semua angka di judul cocok dengan CSV
- [ ] Estimasi diberi tanda (urbanisasi 2018 di pembanding = interpolasi proyeksi; TPT provinsi induk untuk Papua baru sebelum 2024)
- [ ] Sumber BPS di tooltip setiap sheet
- [ ] Watermark terbaru, tidak diubah
- [ ] Publish ke Tableau Public, link "Anyone with the link" dimasukkan ke PDF (FAQ 37)
- [ ] `.twbx` + PDF + Raw_Dataset + Processed_Dataset + surat bermeterai dalam ZIP ≤100 MB
