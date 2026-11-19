# KONSEP FINAL — DAC Data Slayer 4.0
# Paradoks Pengangguran Rendah
## Pendidikan, Kualitas Pekerjaan, dan Peta Kerentanan Pasar Kerja Indonesia

| | |
|---|---|
| **Tema** | **Tema 4** (utama, satu-satunya di formulir). Unsur Tema 3 (kelompok rentan) dan Tema 5 (capaian pendidikan) hanya pendukung |
| **Cakupan** | **Nasional penuh**: 6 jenjang pendidikan → 38 provinsi → 514 kab/kota (dipilih lewat "pilih provinsi"). Tidak ada provinsi yang diistimewakan |
| **Data** | Hanya portal BPS (FAQ 3, 14). WebAPI BPS 2015–2025, periode Agustus seragam; kemiskinan periode Maret |
| **Platform** | Tableau Public (usulan; Power BI masih opsi). 2 halaman · 1900×1100 · watermark resmi tidak diubah |
| **Analisis** | Python (`scripts/`) → CSV (`Processed_Dataset/v5`, `v6`) → paket dashboard `Processed_Dataset/tableau/` |
| **Versi** | **v6**, 19 November 2026. Menggantikan v5 (diarsipkan di `docs/KONSEP_FINAL_DAC_TEMA4_v5_arsip.md`) |

> **Label bukti:**
> - **[DATA]** = angka resmi BPS.
> - **[TERUJI]** = hasil analisis yang lolos uji ketahanan (tanpa Papua, batas/bobot berbeda, pembanding tandingan).
> - **[BERSYARAT]** = berlaku dengan catatan; tidak boleh jadi judul visual tunggal.
> - **[ESTIMASI]** = hasil olahan/interpolasi, bukan angka BPS (FAQ 15).
> - **[PAPER]** = dipakai di paper final saja, tidak di dashboard.
> - **[GUGUR]** = tidak dipakai.

### Perubahan v5 → v6 (ringkas)
1. Skala nasional penuh. Langkah Jawa Tengah diganti "pilih provinsi → kab/kota" untuk semua provinsi.
2. Dari dashboard dibuang: proyeksi 2026–2030, panel fixed effects, loading PCA, LISA/peta poligon. Semua pindah ke paper.
3. Klaim "TPT dan kerja tidak layak berkebalikan" diturunkan menjadi "TPT **tidak mencerminkan** kerja layak" (ρ = −0,30; p = 0,066).
4. Fitur "Kembaran Provinsi + target" diganti **Provinsi Pembanding** tanpa target (gagal uji tandingan, lihat §4).
5. Klaim forecast kab/kota diuji ulang pada **514 kab/kota**, bukan hanya 35 kab/kota Jateng.
6. Kab/kota "persisten tinggi" kini juga dibandingkan dengan **sesama kota / sesama kabupaten**, supaya tidak sekadar efek kota.
7. Data batas wilayah non-BPS (`Spatial/`, `Raw_Dataset/spasial_non_bps/`) **disimpan di repo** sambil menunggu jawaban panitia, tetapi tidak dipakai di dashboard dan tidak masuk ZIP kecuali diizinkan.

---

## 1. Inti Konsep

### 1.1 Satu kalimat
> **Angka pengangguran yang rendah bisa menyembunyikan pekerjaan yang tidak layak. Pasar kerja Indonesia punya dua wajah yang terpisah secara statistik, yaitu "tidak bekerja" dan "bekerja tetapi tidak layak". Pendidikan menentukan wajah mana yang dialami seseorang, sedangkan struktur ekonomi wilayah menentukan seberapa besar kerja tidak layaknya.**

### 1.2 Ilustrasi
- **Wilayah A:** hampir semua orang bekerja, tetapi serabutan. Pengangguran rendah, terlihat baik, padahal tidak layak. Polanya seperti **lulusan SD** dan **NTB/Sulbar**.
- **Wilayah B:** banyak lulusan SMK/PT yang mengantre pekerjaan formal. Pengangguran tinggi, terlihat buruk, padahal pekerjaan yang ada lebih layak. Polanya seperti **lulusan SMK** dan **DKI/Kepri**.

### 1.3 Temuan kunci
| # | Temuan | Bukti | Status |
|---|---|---|---|
| T1 | **Paradoks SMK konsisten 11 tahun**: setiap tahun 2015–2025 TPT SMK tertinggi, tetapi informal non-pertanian SMK lebih rendah dari SMA | 2025: TPT SMK 8,63% vs ≤SD 2,30%; informal SMK 35,8% vs SMA 43,8% vs ≤SD 68,4% | [DATA] |
| T2 | **Informalisasi lulusan terdidik** | Informal non-pertanian Universitas 8,2% → 16,6%; SMK 26,9% → 35,8% (2015 → 2025) | [DATA] |
| T3 | **SMK paling terpukul COVID** (+3,2 poin TPT 2019 → 2020), kini di bawah level 2019 | Analisis kejadian | [DATA] |
| T4 | **Dua wajah pasar kerja terpisah**: "tidak bekerja" (TPT, NEET) dan "kerja tidak layak/KTL" (informal, setengah pengangguran) | PCA 8 indikator, KMO 0,65, Bartlett p < 0,001 | [TERUJI] |
| T5 | **TPT tidak mencerminkan kerja layak** (bukan "berkebalikan") | ρ(TPT, KTL) = −0,30 (p = 0,066); tanpa 6 provinsi Papua −0,22 (p = 0,22) | [TERUJI] |
| T6 | **Ranking berbalik**: NTB 34 → 2, Sulbar 36 → 4, NTT 32 → 6; DKI 7 → 38, Kepri 5 → 37, Banten 4 → 33 | Ranking TPT vs ranking KTL | [TERUJI] |
| T7 | **Indeks KTL tervalidasi** | KTL ~ kemiskinan ρ = 0,66; KTL ~ pekerja formal ρ = −0,92; TPT ~ kemiskinan ns | [TERUJI] |
| T8 | **Prioritas tangguh: Aceh dan Maluku** di 100% dari 1.000 skenario bobot (juga tanpa Papua); Maluku Utara 92% | Monte Carlo 4 komponen | [TERUJI] |
| T9 | **Struktur ekonomi, bukan lama sekolah,** paling terkait besarnya KTL | Urbanisasi ~ KTL parsial −0,67; RLS ~ KTL ≈ 0 setelah kontrol | [TERUJI] |
| T10 | **Struktur persisten**: 25 dari 32 provinsi tetap di kuadran yang sama 2018 → 2025; informal naik di Jabar (+6,7) dan DKI (+6,5) | Matriks transisi | [TERUJI] |
| T11 | **Pengangguran kab/kota sangat persisten**: urutan kab/kota tahun ini hampir sama dengan tahun depan, dan model ML tidak lebih akurat dari tebakan "sama seperti tahun lalu" | 514 kab/kota, 2017–2025: Spearman t vs t+1 = 0,91; MAE naif 0,51 vs linear 0,51 vs GB 0,52 | [TERUJI] |
| T12 | **66 kab/kota "persisten ganda"**: selalu di atas TPT nasional **dan** di atas median sesama kota/kabupaten di semua tahun 2017–2025 (32 kota, 34 kabupaten) | Jejak kab/kota | [TERUJI] |
| T13 | Contoh di provinsi berstatus "Relatif Layak": Jawa Tengah tetap punya 5 kab/kota persisten tinggi (Brebes, Tegal, Cilacap, Kota Tegal, Pemalang). Rata-rata provinsi menyembunyikan kantong | Jejak kab/kota | [DATA] |

**Klaim yang gugur atau turun status:**
- "Provinsi terdidik lebih formal" → [GUGUR] (didorong Papua; hilang setelah kontrol urbanisasi).
- "Kembaran provinsi memberi target realistis" → [GUGUR] (lihat §4.1).
- Proyeksi TPT SMK 2030, panel RLS → NEET (FE p = 0,02 tetapi first-difference ns; sebagian mekanis karena NEET = tidak sekolah), LISA Jateng → [PAPER].

---

## 2. Latar Belakang, Celah, dan Tujuan

**Masalah.** TPT adalah indikator utama pasar kerja, tetapi hanya membedakan bekerja dan tidak bekerja. Orang yang bekerja serabutan atau kurang jam tetap dihitung "bekerja".

**Teori:** Lewis (1954): orang miskin "tidak mampu menganggur". Spence (1973): lulusan terdidik mengantre pekerjaan formal. La Porta & Shleifer (2014): informalitas turun seiring transformasi ekonomi.

**Celah:** studi Indonesia umumnya memakai TPT sebagai satu-satunya outcome (Koto dkk. 2022). Belum ada yang menunjukkan secara statistik bahwa pasar kerja punya dua dimensi terpisah, lalu menelusurinya dari jenjang, provinsi, sampai kab/kota secara nasional.

**Tujuan khusus:**
1. Mengukur paradoks per jenjang 2015–2025.
2. Membuktikan dua dimensi pasar kerja.
3. Memetakan 38 provinsi ke kuadran dan menguji kestabilannya.
4. Menunjukkan bahwa rata-rata provinsi menyembunyikan kab/kota yang persisten bermasalah.
5. Menyusun rekomendasi per tipe masalah.

---

## 3. Alur Corong: Satu Kasus, Didalami Terus

```
① JENJANG (2015–2025)                                   → Halaman 1
   Paradoks SMK 11 tahun · informalisasi lulusan terdidik · COVID memukul SMK
   → "Apakah dua wajah ini juga terlihat antarwilayah?"
        ▼
② DUA WAJAH + ③ PETA BERBALIK (38 provinsi)            → Halaman 2 atas
   PCA: tidak bekerja ⟂ kerja tidak layak · NTB 34 → 2 · DKI 7 → 38 · 4 kuadran
   Penimbang: Aceh & Maluku prioritas di 100% skenario
   → "Provinsi mana yang kondisinya mirip, dan bagaimana perubahannya?"
        ▼
④ PROVINSI PEMBANDING (2018 → 2025)                     → Halaman 2 tengah
   Bandingkan perubahan diri sendiri dengan 3 provinsi berkondisi awal mirip
   → "Rata-rata provinsi juga menyembunyikan sesuatu?"
        ▼
⑤ JEJAK KAB/KOTA (514 kab/kota, 2017–2025)             → Halaman 2 kanan
   66 kab/kota persisten ganda · posisi kab/kota hampir tidak berubah (ρ 0,91)
   → REKOMENDASI per kuadran + kab/kota persisten
```

Pesan yang berulang: **angka agregat (TPT, rata-rata provinsi) menyembunyikan masalah yang sebenarnya.**

---

## 4. Metode (dipetakan ke alur)

| Langkah | Metode | Hasil utama | Validasi | Status |
|---|---|---|---|---|
| ① | Tren 11 tahun + analisis kejadian COVID | Paradoks 11/11 tahun; SMK +3,2 | — | [DATA] |
| ② | PCA + varimax, KMO, Bartlett | F1 KTL (informal 0,95), F2 tidak bekerja (NEET 0,91; TPT 0,77) | Struktur sama tanpa Papua | [TERUJI] |
| ③ | Indeks dua dimensi (min-max) + kuadran batas median | 4 kuadran | Batas rata-rata 87% sama, persentil 45 89% sama | [TERUJI] |
| ③ | Monte Carlo 1.000 bobot Dirichlet, 4 komponen (TPT, NEET, setengah pengangguran, informal) | Aceh, Maluku = 1,00 | Diulang tanpa Papua | [TERUJI] |
| ③ | Validasi konvergen | KTL ~ miskin 0,66; ~ formal −0,92 | 3 sampel | [TERUJI] |
| ④ | kNN k = 3 pada 7 indikator 2018 (TPT, setengah pengangguran, informal, NEET, RLS, urbanisasi [ESTIMASI], kemiskinan Maret) | 3 pembanding per provinsi (32 provinsi) | Stabil 81% saat 1 indikator dibuang; lebih mirip dari acak (p = 0,001); **kalah dari regresi tingkat awal** di 3 dari 4 indikator | Deskriptif saja |
| ⑤ | Persistensi TPT kab/kota vs nasional dan vs median sejenis | 81 persisten vs nasional (47 kota); 66 persisten ganda | Tahun tanpa data dihitung "tidak ada data" | [TERUJI] |
| ⑤ | Uji mundur 2021–2025: naif vs linear vs gradient boosting | Tidak ada model yang lebih baik secara berarti dari naif | 514 kab/kota; versi Jateng + tetangga hanya di paper | [TERUJI] |

### 4.1 Kenapa Provinsi Pembanding, bukan Kembaran + target
Uji tandingan (`Processed_Dataset/v6/pembanding_uji.csv`), MAE perubahan 2018 → 2025:

| Indikator | Rata-rata 3 pembanding | Regresi pada tingkat awal (LOO) | Rata-rata semua | Korelasi awal vs perubahan |
|---|---|---|---|---|
| TPT | 0,52 | **0,38** | 0,57 | −0,76 |
| Setengah pengangguran | 1,52 | **1,30** | 1,46 | −0,47 |
| Informal | 2,23 | **1,93** | 2,84 | −0,72 |
| NEET | **1,97** | 2,17 | 2,10 | −0,03 |

Provinsi yang awalnya tinggi cenderung turun dengan sendirinya (regresi ke rata-rata). Pembanding hanya mengalahkan provinsi acak, tidak memberi informasi tambahan. Memilih "pembanding dengan penurunan terbesar" sebagai target juga bias (memilih nilai ekstrem dari 3). **Keputusan:** tampilkan pembanding sebagai konteks ("provinsi berkondisi awal mirip dan perubahannya"), tanpa target dan tanpa kata "bisa belajar dari".

### 4.2 Forecast kab/kota
`Processed_Dataset/v6/uji_forecast_kabkota_nasional.csv`: target = selisih TPT kab/kota dengan provinsinya tahun depan. Rata-rata 2021–2025: MAE naif 0,511, linear 0,505, GB 0,521; akurasi "di atas provinsi" naif 88,6% vs linear 87,7%. **Bacaan:** posisi kab/kota sangat stabil, sehingga tebakan sederhana sudah hampir maksimal; ini dibaca sebagai tanda masalah struktural, bukan alasan memakai ML.

### 4.3 Metode yang sengaja tidak dipakai
- Forecast provinsi / deep learning: seri tahunan pendek + guncangan COVID.
- ML untuk penjelasan (XGBoost, SHAP): 38 baris, mudah overfit.
- Analisis spasial (LISA, SAR): butuh batas wilayah; sumber BPS yang bisa diunduh belum ada (menunggu panitia).
- Kausal: tidak ada pembanding valid.

---

## 5. Hasil Rinci

### 5.1 Jenjang 2015–2025 [DATA]
| Jenjang | TPT 2015 | TPT 2025 | Informal non-pertanian 2015 | 2025 |
|---|---|---|---|---|
| ≤SD | 2,71 | **2,30** | 67,7 | **68,4** |
| SMP | 6,24 | 3,80 | 53,0 | 60,1 |
| SMA | 10,27 | 6,88 | 34,2 | 43,8 |
| **SMK** | **13,02** | **8,63** | 26,9 | **35,8** |
| Diploma | 7,22 | 4,31 | 14,8 | 25,6 |
| Universitas | 5,98 | 5,39 | **8,2** | **16,6** |

TPT turun di semua jenjang menengah–tinggi, **tetapi informal naik di semua jenjang**. Penurunan TPT tidak sepenuhnya kabar baik.

Ke mana lulusan bekerja (Agustus 2025): ≤SD 44,8% di pertanian; SMK 25,7% perdagangan dan 22,3% industri; Universitas 34,1% jasa pendidikan.

### 5.2 Dua wajah dan kuadran [TERUJI]
| Kuadran (batas median) | Anggota |
|---|---|
| **Rentan Ganda** | **Aceh, Maluku**, Maluku Utara, Sumbar, Sumut, Papua Barat, Jambi*, Papua Selatan* |
| **Rentan Tersembunyi** | **NTB, Sulbar, NTT**, Bengkulu, Lampung, Sulteng, Sultra, Sumsel, Sulsel*, Papua Tengah†, Papua Pegunungan† |
| **Antrean Kerja Formal** | **DKI, Kepri, Banten**, Kaltim, Jabar*, Sulut, Papua, Papua Barat Daya, Kalbar*, Kalteng*, Gorontalo* |
| **Relatif Layak** | **Bali, DIY, Jawa Tengah**, Jatim, Kalsel, Kaltara, Riau*, Babel* |

\* Dekat batas (berubah jika batas diganti). † Flag ekonomi subsisten (informal > 80%, RLS < 7).
Catatan [BERSYARAT]: kuadran versi lama (TPT × indeks 3 komponen) hanya 61% sama, jadi kuadran sensitif definisi. Kuadran jangan jadi headline tunggal; headline utamanya ranking berbalik.

### 5.3 Prioritas (Monte Carlo) [TERUJI]
| Provinsi | P(10 terburuk) | Tanpa Papua | Rentang ranking p05–p95 |
|---|---|---|---|
| Aceh | **1,00** | **1,00** | 2–7 |
| Maluku | **1,00** | **1,00** | 1–4 |
| Maluku Utara | 0,92 | 0,99 | 4–12 |
| Jawa Barat | 0,76 | 0,76 | 3–18 |

### 5.4 Jejak kab/kota [TERUJI]
- 81 kab/kota selalu di atas TPT nasional 2017–2025, **47 di antaranya kota**. Karena TPT kota memang lebih tinggi, dashboard memakai pembanding sejenis.
- **66 persisten ganda** (di atas nasional dan di atas median sesama jenis setiap tahun): tertinggi Kota Ambon (rata-rata 12,0%), Kota Makassar, Kota Padang, Kab. Serang, Kota Sorong.
- 135 kab/kota persisten di atas median sejenis (103 kabupaten). Kabupaten bermasalah lebih banyak daripada yang terlihat dari perbandingan dengan angka nasional.
- Catatan data: Kota Pekalongan 2017 dikosongkan (10,44 di tabel nasional vs 5,05 di BPS Jateng); Lombok Utara 2018 tidak tersedia; 4 provinsi Papua baru memakai TPT provinsi induk sebelum 2024 [ESTIMASI].

---

## 6. Insight Final (judul visual)
| # | Insight | Status |
|---|---|---|
| H1 | "SMK: pengangguran tertinggi 11 tahun berturut-turut, tetapi lebih formal daripada SMA" | [DATA] |
| H2 | "TPT turun, tetapi kerja informal lulusan PT naik 2× lipat sejak 2015" | [DATA] |
| H3 | "COVID paling memukul lulusan SMK" | [DATA] |
| H4 | "Pengangguran rendah tidak berarti kerja layak: NTB peringkat 34 → 2, DKI 7 → 38" | [TERUJI] |
| H5 | "Geser bobotnya sesukamu: Aceh dan Maluku tetap prioritas di 1.000 dari 1.000 skenario" | [TERUJI] |
| H6 | "Struktur ekonomi, bukan lama sekolah, yang membedakan besarnya kerja tidak layak" | [TERUJI] |
| H7 | "66 kab/kota selalu di atas rata-rata nasional dan sesamanya selama 9 tahun" | [TERUJI] |
| H8 | "Posisi pengangguran kab/kota hampir tidak berubah dari tahun ke tahun: masalahnya struktural" | [TERUJI] |

---

## 7. Rekomendasi
| Sasaran | Dasar | Rekomendasi | Indikator pemantau (BPS) |
|---|---|---|---|
| Lulusan SMK | H1, H3 | Evaluasi SMK berbasis kerja layak lulusan (tracer study), bukan TPT saja; diversifikasi jurusan; bantalan saat guncangan | TPT & informal SMK |
| Lulusan PT & menengah | H2 | Perluasan kerja formal, jaminan sosial pekerja informal terdidik | Informal per jenjang |
| Rentan Ganda: Aceh, Maluku, Malut | H5 | Padat karya formal, job matching, program NEET *second chance* | NEET, informal, TPT |
| Rentan Tersembunyi: NTB, Sulbar, NTT | H4, H6 | Hilirisasi pertanian, formalisasi usaha mikro | Informal, setengah pengangguran |
| Antrean Kerja Formal: DKI, Kepri, Banten | H4, T10 | Percepat penyerapan; cegah informalisasi metropolitan | TPT, informal |
| 66 kab/kota persisten ganda | H7, H8 | Program jangka panjang (bukan respons tahunan), karena posisinya tidak berubah sendiri | TPT kab/kota |
| Flag subsisten: Papua Pegunungan, Papua Tengah | † | Pendidikan afirmatif; indikator kerentanan khusus | RLS, informal |

Tidak ada angka target karangan. Pembanding provinsi hanya untuk konteks (§4.1).

---

## 8. Dashboard (detail teknis: `docs/SPEK_DASHBOARD_TABLEAU.md`)

**Halaman 1 — "Dua Wajah Masalah Kerja Lulusan"**: KPI (TPT 4,85%, TPT SMK 8,63%, informal PT 8% → 17%, NEET 19,4%) · dumbbell jenjang 2025 · tren TPT 2015–2025 (tanpa pita proyeksi) · heatmap jenjang × sektor · jembatan ke Halaman 2.

**Halaman 2 — "Pengangguran Rendah, Kerja Tidak Layak: Dari Provinsi ke Kab/Kota"**, 4 fitur:
1. **Peta Berbalik**: tile map 38 provinsi, tombol TPT ↔ kerja tidak layak, mode cerita (Dynamic Zone Visibility, tetap 1 halaman).
2. **Kamu Jadi Penimbang**: 4 slider bobot → ranking dinamis; pita p05–p95 dan "prioritas stabil" dari Monte Carlo ditampilkan terpisah (tidak berubah oleh slider).
3. **Provinsi Pembanding**: klik provinsi → 3 provinsi berkondisi awal mirip + perubahan 2018 → 2025 berdampingan. Tanpa target.
4. **Jejak Kab/Kota**: pilih provinsi → heatmap kab/kota × 2017–2025; default = 66 kab/kota persisten ganda.

**Dilarang:** Smart Narrative, Q&A, Key Influencers, drillthrough (FAQ 9, 36).

---

## 9. Dataset
**Nasional (`Raw_Dataset/bps_webapi/`):** D01 TPT × pendidikan · D02/D02b informal × pendidikan · D03/D03b setengah pengangguran · D05 TPT provinsi · D07/D08/D10 informal/formal provinsi · D11 upah · D14 sektor × pendidikan · D15/D16 NEET · D18 RLS · D25 kemiskinan (Maret) · **K01 TPT kab/kota 2017–2025 (var 2824)**.
**BPS Jawa Tengah (`Raw_Dataset/bps_jateng/`):** J01 TPT kab/kota 2007–2025 (cek silang K01), J02–J10 → [PAPER].
**Statis BPS:** urbanisasi provinsi (proyeksi SP2010; 2018 = interpolasi [ESTIMASI]).
**Non-BPS (disimpan, belum dipakai):** `Raw_Dataset/spasial_non_bps/`, `Spatial/`, `Processed_Dataset/v5/F_jateng_matriks_ketetanggaan.csv`. Menunggu jawaban panitia; jika dilarang, dikeluarkan dari ZIP.

**Output untuk dashboard (`Processed_Dataset/tableau/`):** t1 jenjang tren · t2 jenjang × sektor · t3 provinsi 2025 · t4 pembanding + uji · t5 kab/kota tren + jejak · t6 transisi · t7 uji forecast kab/kota.

---

## 10. Validasi, Bias, dan Kelemahan
| Risiko | Penanganan | Status |
|---|---|---|
| Label jenjang tertukar (urutan alfabet tabel) | Pemetaan eksplisit, dicek ke rilis BPS | ✅ |
| NEET tumpang tindih dengan pengangguran | PCA: NEET di dimensi "tidak bekerja" | ✅ |
| Bobot indeks subjektif | Monte Carlo + slider | ✅ |
| Kuadran sensitif definisi | Provinsi dekat batas ditandai; bukan headline tunggal | ⚠️ |
| Pengaruh Papua | Semua uji diulang tanpa Papua | ✅ |
| Pemekaran Papua 2022 | Pembanding 2018 → 2025 hanya 32 provinsi; kab/kota Papua baru pakai TPT provinsi induk sebelum 2024 (ditandai) | ✅ |
| Pembanding = regresi ke rata-rata | Diuji; diturunkan jadi alat banding deskriptif | ✅ |
| "Persisten tinggi" = efek kota | Ditambah pembanding median sejenis | ✅ |
| Galat sampling kab/kota | Pakai persistensi 9 tahun, bukan ranking satu tahun | ✅ |
| Periode kemiskinan | Seragam Maret (2018 dan 2025) | ✅ |
| Urbanisasi = proyeksi | Label [ESTIMASI]; uji tanpa 5 provinsi berdata induk | ⚠️ |
| Ecological fallacy | Klaim individu dari jenjang; klaim wilayah dari provinsi/kab-kota | ✅ |

---

## 11. Simulasi Pertanyaan Juri
| Pertanyaan | Jawaban |
|---|---|
| "Kenapa dua dimensi?" | PCA menunjukkan pengangguran dan kerja tidak layak terpisah (KMO 0,65, Bartlett p < 0,001) |
| "Indeksnya valid?" | KTL ~ kemiskinan 0,66 dan ~ formal −0,92; keduanya tidak dipakai dalam indeks |
| "TPT dan KTL berkebalikan?" | Tidak kami klaim. Korelasinya lemah dan tidak signifikan; artinya TPT **tidak bisa** dipakai untuk menilai kerja layak |
| "Kenapa tidak ML/forecast?" | Sudah diuji pada 514 kab/kota: model tidak lebih baik dari tebakan naif. Itu temuan: masalahnya persisten |
| "Kenapa pembanding, bukan target?" | Diuji: pembanding kalah dari regresi ke rata-rata. Kami tidak mau memberi target yang tidak didukung data |
| "Bukankah kab/kota persisten itu cuma kota?" | Kami bandingkan juga dengan sesama kota/kabupaten: 66 tetap persisten, 34 di antaranya kabupaten |
| "Kausal?" | Tidak. Semua asosiasi, konsisten dengan Lewis, Spence, La Porta & Shleifer |

---

## 12. Rencana Kerja Tersisa
| Hari | Tugas |
|---|---|
| Kam 19 Nov | Tim setujui v6; putuskan platform |
| Jum 20 Nov | Halaman 1 |
| Sab 21 Nov | Halaman 2 (4 fitur) |
| Min 22 Nov | Narasi, poles desain, cek silang angka vs CSV |
| Sen 23 Nov | PDF + workbook + ZIP + surat bermeterai → kirim sebelum 18.00 |

**Checklist:**
- [ ] 2 halaman, 1900×1100, watermark versi terbaru tidak diubah (FAQ 35)
- [ ] Headline hanya [DATA]/[TERUJI]; estimasi berlabel (FAQ 15)
- [ ] Sumber BPS di tooltip
- [ ] Link publik dashboard di PDF (FAQ 37)
- [ ] ZIP ≤100 MB: PDF, workbook, Raw_Dataset (BPS saja kecuali diizinkan), Processed_Dataset, surat orisinalitas bermeterai
- [ ] Nama tim ≤20 karakter
- [ ] Jawaban panitia soal poligon non-BPS
- [ ] Buat ulang key WebAPI setelah lomba

---

## 13. Referensi
- Chen (2009) https://doi.org/10.1596/1813-9450-4814
- Koto dkk. (2022) https://doi.org/10.22202/economica.2022.v11.i1.6270
- La Porta & Shleifer (2014) https://doi.org/10.1257/jep.28.3.109
- Lewis (1954) https://doi.org/10.1111/j.1467-9957.1954.tb00021.x
- Maloney (2004) https://doi.org/10.1016/j.worlddev.2004.01.008
- Newhouse & Suryadarma (2011) https://doi.org/10.1093/wber/lhr010
- Pattinasarany (2019) https://doi.org/10.7454/mjs.v24i1.10308
- Psacharopoulos & Patrinos (2018) https://doi.org/10.1080/09645292.2018.1484426
- Purnastuti dkk. (2013) https://doi.org/10.1080/00074918.2013.809842
- Cameron dkk. (2019) https://doi.org/10.1080/00074918.2018.1530727
- Spence (1973) https://doi.org/10.2307/1882010
- Barnett dkk. (2005, regresi ke rata-rata) https://doi.org/10.1093/ije/dyh299
- Segel & Heer (2010) https://doi.org/10.1109/TVCG.2010.179
- Kale dkk. (2019) https://doi.org/10.1109/TVCG.2018.2864909
- Referensi spasial/panel (Anselin 1995, Elhorst 2003) dipindah ke paper.
