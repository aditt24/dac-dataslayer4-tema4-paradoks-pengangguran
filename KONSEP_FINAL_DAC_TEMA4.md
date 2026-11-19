# KONSEP FINAL — DAC Data Slayer 4.0
# Paradoks Pengangguran Rendah
## Pendidikan, Kualitas Pekerjaan, dan Peta Kerentanan Pasar Kerja Indonesia

| | |
|---|---|
| **Tema** | **Tema 4** (utama, satu-satunya di formulir). Unsur Tema 3 (kelompok rentan) dan Tema 5 (capaian pendidikan) hanya sebagai pendukung |
| **Cakupan** | Nasional: 6 jenjang pendidikan + 38 provinsi → studi kasus **Jawa Tengah** (35 kab/kota) |
| **Data** | BPS WebAPI, seluruh tahun 2015–2025 (tahun dan periode Agustus seragam). 21 tabel nasional + 10 tabel BPS Jawa Tengah |
| **Platform** | Power BI · 2 halaman · 1900×1100 · watermark resmi |
| **Analisis** | Python (`scripts/analisis_lanjutan_v5.py`) → CSV (`Processed_Dataset/v5/`) → Power BI |
| **Versi** | v5, 19 November 2026. Menggantikan seluruh versi sebelumnya (v4 diarsipkan di `docs/KONSEP_FINAL_DAC_TEMA4_v4_arsip.md`) |

> **Label bukti:**
> - **[DATA]** = angka resmi BPS.
> - **[TERUJI]** = hasil analisis yang lolos uji ketahanan: tanpa provinsi Papua, kontrol urbanisasi, dan variasi batas/bobot.
> - **[BERSYARAT]** = berlaku dengan catatan.
> - **[PROYEKSI]** = hasil model, bukan data BPS (FAQ 15).
> - **[GUGUR]** = tidak dipakai.

---

## 1. Inti Konsep

### 1.1 Satu kalimat
> **Angka pengangguran yang rendah bisa menyembunyikan pekerjaan yang tidak layak. Pasar kerja Indonesia punya dua wajah yang berbeda secara statistik, yaitu "tidak bekerja" dan "bekerja tetapi tidak layak". Pendidikan menentukan wajah mana yang dialami seseorang, sedangkan struktur ekonomi wilayah menentukan seberapa besar kerja tidak layaknya.**

### 1.2 Ilustrasi
- **Desa A:** hampir semua orang bekerja, tetapi serabutan dan tanpa kontrak. Pengangguran rendah, sehingga terlihat baik, padahal tidak layak. Polanya seperti **lulusan SD** dan **NTB/Sulbar**.
- **Desa B:** banyak lulusan SMK/PT yang mengantre pekerjaan layak. Pengangguran tinggi, sehingga terlihat buruk, padahal pekerjaannya lebih layak. Polanya seperti **lulusan SMK** dan **DKI/Kepri**.

### 1.3 Temuan kunci (data BPS 2015–2025)
| # | Temuan | Bukti | Status |
|---|---|---|---|
| T1 | **Paradoks SMK konsisten 11 tahun berturut-turut**: setiap tahun 2015–2025, lulusan SMK punya pengangguran tertinggi, tetapi lebih formal daripada lulusan SMA umum | 2025: TPT SMK 8,63% vs SD 2,30%; informal non-pertanian SMK 35,8% vs SMA 43,8% vs SD 68,4% | [DATA] |
| T2 | **Kerja tidak layak meningkat pada lulusan terdidik**: informal non-pertanian lulusan PT naik dua kali lipat, dan lulusan SMK naik 9 poin | Universitas 8,2% → 16,6%; SMK 26,9% → 35,8% (2015 → 2025) | [DATA] |
| T3 | **Antrean SMK memendek**: gap pengangguran SMK–SMA menyempit dari 3,3 poin (2018) menjadi 1,75 poin (2025) | Tren −0,19 poin/tahun (p = 0,02) | [DATA] + [PROYEKSI] |
| T4 | **SMK paling terpukul COVID-19** (+3,2 poin), tetapi pulih penuh dan kini 1,7 poin di bawah level 2019 | Analisis kejadian 2019 → 2020 → 2025 | [DATA] |
| T5 | **Analisis faktor membuktikan dua wajah pasar kerja**: "tidak bekerja" (pengangguran + NEET) dan "bekerja tidak layak" (informal + setengah pengangguran), yang secara statistik terpisah | PCA 8 indikator, KMO 0,65, Bartlett p < 0,001, 84% varians | [TERUJI] |
| T6 | **Pengangguran tidak mencerminkan kerja layak**; arahnya justru cenderung terbalik | ρ(TPT, Kerja Tidak Layak) = −0,30 (2025), −0,45 (2018, p = 0,009) | [TERUJI] |
| T7 | **Ranking berbalik**: NTB 34 → 2, Sulbar 36 → 4, NTT 32 → 6; DKI 7 → 38, Kepri 5 → 37, Banten 4 → 33 | Ranking pengangguran vs ranking kerja tidak layak | [TERUJI] |
| T8 | **Indeks kerja tidak layak tervalidasi**: berkorelasi dengan kemiskinan dan berlawanan dengan pekerjaan formal; pengangguran tidak | KTL ~ miskin ρ = 0,66 (tanpa Papua 0,75); KTL ~ formal ρ = −0,92; TPT ~ miskin −0,23 (ns) | [TERUJI] |
| T9 | **Prioritas tangguh: Aceh dan Maluku** (100% skenario), lalu Maluku Utara dan Sumbar | Monte Carlo 1.000 bobot, dengan atau tanpa Papua | [TERUJI] |
| T10 | **Struktur ekonomi, bukan rata-rata lama sekolah, yang paling terkait dengan besarnya kerja tidak layak** | Urbanisasi ~ KTL parsial −0,67 (tanpa Papua −0,72); RLS ~ KTL setelah kontrol urbanisasi ≈ 0 | [TERUJI] |
| T11 | **Kenaikan pendidikan di suatu provinsi berkaitan dengan turunnya NEET, tetapi belum dengan turunnya kerja tidak layak** | Panel fixed effects 32 provinsi × 2018–2025: RLS → NEET −4,4 (p = 0,02); RLS → informal tidak signifikan | [TERUJI] |
| T12 | **Struktur masalah persisten**: 25 dari 32 provinsi tetap di kuadran yang sama 2018 → 2025. Informalitas **naik** di Jawa Barat (+6,7) dan DKI (+6,5), dan **turun** di NTT (−7,2), Kalsel (−6,6), Lampung (−6,1) | Matriks transisi | [TERUJI] |
| T13 | **Jawa Tengah**: secara provinsi tergolong "Relatif Layak" (stabil di semua batas), tetapi **paradoksnya berlaku di 35/35 kab/kota** (2019, 2020, 2023) | TPT pendidikan menengah > dasar di semua kab/kota | [DATA] |
| T14 | **Hotspot pengangguran Jateng terbukti secara spasial**: kluster barat daya–pantura barat (Cilacap, Banyumas, Purbalingga, Tegal, Brebes, Kota Tegal) | Moran's I = 0,62 (p = 0,001); LISA | [TERUJI] |
| T15 | **Antrean lulusan menengah Jateng memburuk** di Banjarnegara (+6,5) dan Brebes (+5,8) pada 2019 → 2023. Brebes mencapai **20,8%** | Data kab/kota × pendidikan | [DATA] |

---

## 2. Latar Belakang, Celah, dan Tujuan

**Masalah.** TPT adalah indikator utama keberhasilan pasar kerja, tetapi TPT hanya membedakan bekerja dan tidak bekerja. Orang yang bekerja serabutan atau kurang jam tetap dihitung "bekerja".

**Teori:**
- Lewis (1954): orang miskin dan berpendidikan rendah "tidak mampu menganggur", sehingga masuk sektor tradisional.
- Spence (1973): lulusan terdidik mengantre pekerjaan formal.
- La Porta & Shleifer (2014): informalitas turun seiring transformasi ekonomi.

**Celah penelitian:** studi Indonesia umumnya memakai TPT sebagai satu-satunya outcome (Koto dkk. 2022). Perdebatan keunggulan SMK berbasis data individu belum tuntas (Newhouse & Suryadarma 2011; Chen 2009). **Belum ada yang membuktikan secara statistik bahwa pasar kerja punya dua dimensi terpisah, lalu menelusurinya dari jenjang pendidikan, provinsi, sampai kab/kota.**

**Tujuan umum:** membuktikan bahwa keberhasilan pendidikan di dunia kerja harus dinilai dari dua wajah, yaitu tidak bekerja dan bekerja tidak layak, dan menentukan jenjang serta wilayah yang perlu ditekankan.

**Tujuan khusus:**
1. Mengukur paradoks per jenjang dan trennya (2015–2025).
2. Membuktikan dua dimensi pasar kerja (analisis faktor).
3. Memetakan 38 provinsi ke dalam kuadran dan menguji kestabilannya.
4. Menjelaskan peran pendidikan dan struktur ekonomi (korelasi parsial, panel).
5. Menerapkan lensa yang sama di Jawa Tengah, termasuk analisis spasial.
6. Menyusun rekomendasi per tipe masalah.

---

## 3. Alur Corong: Satu Kasus, Didalami Terus

```
① JENJANG (2015–2025)                         [Tema 4 + Tema 5]
   Paradoks SMK konsisten 11 tahun · informalisasi lulusan terdidik · COVID paling memukul SMK · antrean SMK memendek
   → "Apakah dua wajah ini juga terlihat antarwilayah?"
        ▼
② DUA WAJAH PASAR KERJA (analisis faktor, 38 provinsi)
   PCA: "tidak bekerja" (TPT, NEET) ⟂ "bekerja tidak layak" (informal, setengah pengangguran)
   → "Kalau keduanya berbeda, apakah TPT menyesatkan?"
        ▼
③ TPT MENYESATKAN + KUADRAN
   ρ(TPT, kerja tidak layak) = −0,30 · NTB 34 → 2 · DKI 7 → 38 · 4 kuadran stabil 87–89%
   Prioritas tangguh: Aceh, Maluku (100% skenario)
   → "Mengapa besarnya kerja tidak layak berbeda-beda?"
        ▼
④ PENJELASAN + WAKTU
   Struktur ekonomi (urbanisasi) > rata-rata lama sekolah · panel: pendidikan naik → NEET turun, kerja tidak layak belum
   Transisi 2018→2025: struktur persisten; informalisasi Jabar & DKI
   → "Bagaimana dengan daerah kita, Jawa Tengah?"            [Tema 3: pemuda, gender]
        ▼
⑤ JAWA TENGAH
   Provinsi "Relatif Layak", tetapi paradoks berlaku di 35/35 kab/kota
   → "Di mana kantongnya?"
        ▼
⑥ KAB/KOTA JATENG (spasial)
   Hotspot LISA: Cilacap–Banyumas–Purbalingga–Tegal–Brebes · Brebes TPT lulusan menengah 20,8%
   → REKOMENDASI per tipe + kab/kota prioritas
```

Pesan yang terulang di setiap langkah: **angka rata-rata atau agregat (TPT, rata-rata provinsi) menyembunyikan masalah yang sebenarnya.** Itu sebabnya alur ini tidak melompat.

---

## 4. Metode Lanjutan (dipetakan ke alur)

| Langkah | Metode | Pertanyaan | Hasil utama | Validasi |
|---|---|---|---|---|
| ① | Tren 11 tahun | Apakah paradoks konsisten? | Ya, 11/11 tahun | — |
| ① | **Analisis kejadian COVID** (guncangan 2019 → 2020, pemulihan 2020 → 2025) | Jenjang mana paling rentan guncangan? | SMK +3,2 poin (terbesar); pulih 154% | — |
| ① | **Proyeksi 2026–2030** (OLS tren + dummy COVID, interval prediksi 80%) | Ke mana arah antrean SMK? | Gap SMK–SMA 2030: 0,4 poin [−1,0; 1,7]; TPT SMK 2030: 6,5% [5,2; 7,7] | Diberi label **PROYEKSI**; interval lebar dilaporkan |
| ② | **Analisis faktor** (PCA + rotasi varimax; KMO, Bartlett) | Apakah masalah kerja satu atau dua dimensi? | Dua dimensi: F1 kerja tidak layak (informal 0,95; kemiskinan 0,83; urbanisasi −0,80; RLS −0,77); F2 tidak bekerja (NEET 0,91; TPT 0,77) | Struktur yang sama muncul tanpa Papua |
| ③ | Indeks dua dimensi + kuadran | Provinsi mana yang tersembunyi atau rentan? | 4 kuadran | Batas median vs rata-rata vs persentil 45: 87–89% sama |
| ③ | **Monte Carlo** 1.000 bobot (4 komponen) | Prioritas mana yang pasti? | Aceh, Maluku = 1,00 | Diulang tanpa Papua |
| ③ | **Validasi konvergen** | Apakah indeks mengukur hal yang nyata? | KTL ~ miskin 0,66; ~ formal −0,92 | Tiga sampel |
| ④ | Korelasi parsial | Pendidikan atau struktur ekonomi? | Urbanisasi −0,67; RLS ≈ 0 | Tanpa Papua, tanpa provinsi berdata induk |
| ④ | **Panel two-way fixed effects** (32 provinsi × 8 tahun, SE klaster) | Jika pendidikan suatu provinsi naik, apa yang berubah? | NEET turun (β = −4,4; p = 0,02); informal, TPT, setengah pengangguran tidak signifikan | Pembanding first-difference 2018 → 2025 (arah sama, tidak signifikan) |
| ④ | **Matriks transisi kuadran** 2018 → 2025 | Apakah strukturnya berubah? | 25/32 tetap; 7 pindah | — |
| ⑤ | Paradoks per kab/kota per tahun | Apakah berlaku lokal? | 35/35 kab/kota (2019, 2020, 2023) | 5 tahun data |
| ⑥ | **Moran's I + LISA** (ketetanggaan antar-kab/kota, 999 permutasi) | Apakah pengangguran mengelompok? | TPT: I = 0,62 (p = 0,001); TPT lulusan menengah: I = 0,37 (p = 0,001) | Ketetanggaan dari batas wilayah (hanya untuk bobot; bukan data statistik) |

**Metode yang sengaja tidak dipakai (alasan untuk juri):**
- **Forecasting provinsi** (ARIMA atau deep learning): seri tahunan pendek dan ada guncangan COVID, jadi tidak meyakinkan.
- **Machine learning (XGBoost, SHAP)**: hanya 38–256 baris data, sehingga mudah *overfit*.
- **Model spasial lanjutan (SAR, GWR)**: jumlah wilayah terlalu sedikit.
- **Analisis kausal**: tidak ada kelompok pembanding yang valid.

---

## 5. Hasil Rinci

### 5.1 Langkah ①: Jenjang pendidikan 2015–2025 [DATA]
**TPT (%)**

| Jenjang | 2015 | 2018 | 2019 | 2020 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| ≤SD | 2,71 | 2,40 | 2,39 | 3,61 | 3,59 | **2,30** |
| SMP | 6,24 | 4,77 | 4,72 | 6,46 | 5,95 | 3,80 |
| SMA | 10,27 | 7,90 | 7,87 | 9,86 | 8,57 | 6,88 |
| **SMK** | **13,02** | **11,18** | **10,36** | **13,55** | **9,42** | **8,63** |
| Diploma | 7,22 | 6,00 | 5,95 | 8,08 | 4,59 | 4,31 |
| Universitas | 5,98 | 5,88 | 5,64 | 7,35 | 4,80 | 5,39 |

**Informal non-pertanian (%)**

| Jenjang | 2015 | 2018 | 2020 | 2025 | Perubahan 2015 → 2025 |
|---|---|---|---|---|---|
| ≤SD | 67,7 | 66,4 | 69,2 | **68,4** | +0,7 |
| SMP | 53,0 | 53,7 | 59,3 | 60,1 | +7,2 |
| SMA | 34,2 | 37,7 | 45,2 | 43,8 | +9,6 |
| **SMK** | 26,9 | 31,2 | 34,7 | **35,8** | +9,0 |
| Diploma | 14,8 | 18,8 | 23,7 | 25,6 | +10,8 |
| **Universitas** | **8,2** | 11,5 | 16,2 | **16,6** | **+8,4 (2× lipat)** |

**Bacaan:**
- Paradoks SMK konsisten setiap tahun.
- Antrean SMK memendek (TPT SMK turun dari 13,0 ke 8,6).
- **Tetapi kerja tidak layak naik di semua jenjang menengah–tinggi.** Sebagian lulusan yang "berhasil bekerja" ternyata masuk pekerjaan informal. Penurunan TPT **tidak sepenuhnya kabar baik**.

**Kejadian COVID (TPT):** guncangan 2019 → 2020 terbesar terjadi pada SMK (+3,19), lalu Diploma (+2,13). SMK pulih 154% dan kini 1,73 poin di bawah level 2019. ≤SD berguncang paling kecil (+1,22), karena kelompok ini "tidak mampu menganggur".

**Ke mana lulusan bekerja (Agustus 2025):**
- ≤SD: 44,8% di pertanian.
- SMK: 25,7% di perdagangan dan 22,3% di industri pengolahan (paling bergantung pada industri).
- Universitas: 34,1% di jasa pendidikan (daya serap sempit).

**[PROYEKSI] Jika tren 2015–2025 berlanjut:**
- Gap TPT SMK–SMA menjadi sekitar 0,4 poin pada 2030 (PI 80%: −1,0 sampai 1,7). Antrean SMK bisa hampir setara dengan SMA.
- TPT SMK sekitar 6,5% (5,2–7,7).
- Ini proyeksi berbasis tren, **bukan prediksi pasti**.

### 5.2 Langkah ②: Dua wajah pasar kerja [TERUJI]
| Variabel | F1 "Bekerja tidak layak" | F2 "Tidak bekerja" | F3 |
|---|---|---|---|
| Informal | **0,95** | −0,12 | 0,07 |
| Kemiskinan | **0,83** | 0,05 | −0,44 |
| Urbanisasi | **−0,80** | −0,24 | −0,27 |
| RLS | **−0,77** | 0,42 | 0,09 |
| Setengah pengangguran | **0,64** | 0,48 | 0,34 |
| NEET | 0,17 | **0,91** | −0,01 |
| TPT | −0,45 | **0,77** | −0,26 |
| Upah per jam | 0,00 | 0,09 | **−0,95** |

KMO = 0,65 (cukup) · Bartlett χ² = 187,5 (p < 0,001) · 3 faktor menjelaskan 84% varians. **Tanpa Papua, struktur dua dimensinya tetap.**

**Konsekuensi desain:** indeks dipecah menjadi dua dimensi:
- **Kerja Tidak Layak (KTL)** = rata-rata ternormalisasi informal + setengah pengangguran.
- **Tidak Bekerja** = rata-rata ternormalisasi TPT + NEET.

NEET dipindah ke dimensi "tidak bekerja" karena data menunjukkan NEET menempel pada pengangguran, bukan pada informalitas. Ini sekaligus menyelesaikan masalah tumpang tindih komponen di versi sebelumnya.

### 5.3 Langkah ③: TPT menyesatkan + kuadran [TERUJI]
| Uji | 38 provinsi | Tanpa Papua | Tanpa 5 prov. urbanisasi-induk |
|---|---|---|---|
| ρ(TPT, KTL) | −0,30 (p = 0,07) | −0,25 (ns) | −0,28 (ns) |
| ρ(Tidak bekerja, KTL) | −0,17 (ns) | −0,12 (ns) | −0,14 (ns) |
| ρ(KTL, kemiskinan) | **0,66** | **0,75** | **0,67** |
| ρ(KTL, tenaga kerja formal) | **−0,92** | **−0,95** | **−0,95** |
| ρ(TPT, kemiskinan) | −0,23 (ns) | −0,36 (p = 0,05) | −0,22 (ns) |

**Kuadran 2025** (x = Tidak Bekerja, y = Kerja Tidak Layak; batas = median):

| Kuadran | Anggota |
|---|---|
| **Rentan Ganda** (tidak bekerja tinggi + kerja tidak layak tinggi) | **Aceh, Maluku**, Maluku Utara, Sumatera Barat, Sumatera Utara, Papua Barat, Jambi*, Papua Selatan* |
| **Rentan Tersembunyi** (tidak bekerja rendah + kerja tidak layak tinggi) | **NTB, Sulawesi Barat, NTT**, Bengkulu, Lampung, Sulteng, Sultra, Sumsel, Sulsel*, Papua Tengah†, Papua Pegunungan† |
| **Antrean Kerja Formal** (tidak bekerja tinggi + kerja tidak layak rendah) | **DKI Jakarta, Kep. Riau, Banten**, Kaltim, Jabar*, Sulut, Papua, Papua Barat Daya, Kalbar*, Kalteng*, Gorontalo* |
| **Relatif Layak** (keduanya rendah) | **Bali, DIY, Jawa Tengah**, Jatim, Kalsel, Kaltara, Riau*, Babel* |

\* Dekat batas (berubah jika garis batas diganti). † Flag **Ekonomi Subsisten** (informal >80%, RLS <7).

Kuadran sama di **87%** provinsi dengan batas rata-rata, dan **89%** dengan batas persentil 45.

**Ranking berbalik (pengangguran → kerja tidak layak; 1 = terburuk):** NTB 34 → 2 · Sulbar 36 → 4 · Papua Pegunungan 37 → 5 · NTT 32 → 6 · Sulteng 35 → 14 | Kepri 5 → 37 · DKI 7 → 38 · Banten 4 → 33 · Kaltim 12 → 35.

**Prioritas (Monte Carlo 1.000 bobot dari 4 komponen):**

| Provinsi | P(10 terburuk) | Tanpa Papua | Rentang ranking |
|---|---|---|---|
| Aceh | **1,00** | **1,00** | 2–7 |
| Maluku | **1,00** | **1,00** | 1–4 |
| Maluku Utara | 0,92 | 0,99 | 4–12 |
| Sumatera Barat | 0,71 | 0,96 | 5–15 |
| Jawa Barat | 0,76 | 0,76 | 3–18 |

**Terdidik tetapi tanpa kerja layak** (RLS ≥ median dan KTL ≥ median): Aceh, Maluku, Maluku Utara, Sumbar, Sumut, Papua Barat, Bengkulu, Sultra.

### 5.4 Langkah ④: Penjelasan dan waktu [TERUJI]
| Hubungan | 38 provinsi | Tanpa Papua |
|---|---|---|
| Urbanisasi ~ KTL (kontrol RLS) | **−0,67** | **−0,72** |
| RLS ~ KTL (kontrol urbanisasi) | −0,14 (ns) | 0,01 (ns) |
| RLS ~ TPT (kontrol urbanisasi) | **+0,46** | +0,30 (p = 0,09) |

**Panel fixed effects 2018–2025 (32 provinsi, efek provinsi + tahun):**

| Outcome | β per +1 tahun RLS | p |
|---|---|---|
| **NEET** | **−4,41** | **0,02** |
| Informal | −3,49 | 0,23 |
| TPT | +0,10 | 0,85 |
| Setengah pengangguran | −0,10 | 0,94 |

**Transisi kuadran 2018 → 2025 (32 provinsi):** 25 tetap.
- Yang pindah: Sumut (Rentan Tersembunyi → Rentan Ganda), Jambi (Relatif Layak → Rentan Ganda), Sumsel dan Sulsel (Rentan Ganda → Rentan Tersembunyi), Gorontalo (Rentan Ganda → Antrean), Kalteng (Relatif Layak → Antrean), Kalsel (Antrean → Relatif Layak).
- Paradoks lebih tajam pada 2018: ρ(TPT, KTL) = −0,45 (p = 0,009).
- **Informal naik** di Jabar (+6,7) dan DKI (+6,5): *informalisasi metropolitan*.
- **Informal turun** di NTT (−7,2), Kalsel (−6,6), Lampung (−6,1).

### 5.5 Langkah ⑤–⑥: Jawa Tengah [DATA/TERUJI]
| | Jawa Tengah 2025 | Median provinsi |
|---|---|---|
| TPT | 4,66 | 4,21 |
| Informal | 58,8 | 59,6 |
| Setengah pengangguran | 7,0 | 8,0 |
| NEET | 16,7 | 19,3 |
| Kuadran | **Relatif Layak** (stabil di 3 batas) | — |

**Paradoks di dalam Jateng (TPT pendidikan menengah vs dasar):**

| Tahun | Kab/kota dengan menengah > dasar | Median dasar | Median menengah |
|---|---|---|---|
| 2019 | **35/35** | 2,52 | 7,71 |
| 2020 | **35/35** | 4,49 | 10,48 |
| 2021 | 31/35 | 4,38 | 7,46 |
| 2022 | 30/35 | 4,60 | 7,45 |
| 2023 | **35/35** | 2,90 | 7,13 |

- Jateng 2023: **70% setengah penganggur berpendidikan ≤SMP**.
- TPT lulusan menengah di perdesaan 10,03% vs perkotaan 7,67%.
- **Analisis spasial (Moran's I, LISA):**
  - TPT 2025: **I = 0,62 (p = 0,001)**. **Hotspot (High-High): Cilacap, Banyumas, Purbalingga, Tegal, Brebes, Kota Tegal.** Coldspot: Pati.
  - TPT lulusan menengah 2023: **I = 0,37 (p = 0,001)**. Hotspot: Cilacap, Banyumas, Kebumen, Tegal, Brebes.
  - Pengeluaran per kapita: tidak mengelompok (I = 0,08; ns).
- **Tren 2019 → 2023 (TPT lulusan menengah):**
  - Memburuk: **Banjarnegara +6,5, Brebes +5,8**, Jepara +3,0.
  - Membaik: Kab. Pekalongan −7,3, Kudus −3,9, Grobogan −3,3.
- **Kuadran kab/kota (TPT × pengeluaran per kapita 2025):** masalah ganda di Brebes, Tegal, Pemalang, Cilacap, Banjarnegara, Purbalingga, Kebumen, Wonosobo, Demak.

---

## 6. Insight Final (judul visual)

| # | Insight | Langkah | Status |
|---|---|---|---|
| H1 | "SMK: pengangguran tertinggi selama 11 tahun berturut-turut, tetapi lebih formal daripada SMA" | ① | [DATA] |
| H2 | "Antrean SMK memendek, tetapi kerja tidak layak lulusan terdidik naik: lulusan PT informal 2× lipat sejak 2015" | ① | [DATA] |
| H3 | "COVID paling memukul lulusan SMK" | ① | [DATA] |
| H4 | "Pasar kerja punya dua wajah: tidak bekerja dan bekerja tidak layak, yang terbukti terpisah secara statistik" | ② | [TERUJI] |
| H5 | "Pengangguran tidak mencerminkan kerja layak: NTB peringkat 34 → 2, DKI 7 → 38" | ③ | [TERUJI] |
| H6 | "Aceh dan Maluku: prioritas di 100% skenario; terdidik tetapi tanpa kerja layak" | ③ | [TERUJI] |
| H7 | "Struktur ekonomi, bukan lama sekolah, yang membedakan besarnya kerja tidak layak" | ④ | [TERUJI] |
| H8 | "Pendidikan yang naik menurunkan NEET, tetapi belum menurunkan kerja tidak layak" | ④ | [TERUJI] |
| H9 | "Informalisasi metropolitan: informal Jabar +6,7 dan DKI +6,5 sejak 2018" | ④ | [TERUJI] |
| H10 | "Jateng terlihat layak, tetapi paradoks berlaku di 35/35 kab/kota" | ⑤ | [DATA] |
| H11 | "Hotspot pengangguran Jateng: Cilacap–Banyumas–Purbalingga–Tegal–Brebes (Moran's I 0,62)" | ⑥ | [TERUJI] |
| H12 | "Brebes: 1 dari 5 lulusan SMA/SMK menganggur, dan memburuk sejak 2019" | ⑥ | [DATA] |

---

## 7. Rekomendasi (sesuai temuan)

| Sasaran | Temuan dasar | Rekomendasi | Indikator pemantau (BPS) |
|---|---|---|---|
| **Lulusan SMK** (nasional) | H1, H3; 48% lulusan SMK bergantung pada industri dan perdagangan | Tracer study wajib; evaluasi SMK berbasis **kerja layak lulusan**, bukan TPT saja; diversifikasi jurusan ke sektor yang tumbuh; bantalan saat guncangan ekonomi (paling rentan COVID) | TPT SMK, informal non-pertanian SMK |
| **Lulusan PT & menengah** (nasional) | H2: informalisasi lulusan terdidik | Perluasan pekerjaan formal untuk lulusan, perlindungan pekerja informal terdidik (jaminan sosial), insentif formalisasi usaha | Informal non-pertanian per jenjang |
| **Rentan Ganda**: Aceh, Maluku, Malut, Sumbar | H6: terdidik tetapi tanpa kerja layak | Investasi padat karya formal; *job matching*; magang industri; program NEET *second chance* | NEET, informal, TPT 15–24 |
| **Rentan Tersembunyi**: NTB, Sulbar, NTT, Bengkulu, Lampung | H5, H7: struktur agraris | Hilirisasi pertanian dan agroindustri; formalisasi usaha mikro; pelatihan pekerja berpendidikan rendah | Informal, setengah pengangguran |
| **Antrean Kerja Formal**: DKI, Kepri, Banten, Jabar | Antrean tinggi + informalisasi metropolitan (H9) | Percepat penyerapan (bursa kerja, kemitraan kawasan industri) dan **cegah informalisasi** (perlindungan pekerja platform/informal kota) | TPT, informal |
| **Jawa Tengah: hotspot** Cilacap, Banyumas, Purbalingga, Tegal, Brebes (+ Banjarnegara, Pemalang) | H10–H12 | Program antarkabupaten berbasis kluster (bukan per kabupaten), penciptaan kerja formal di perdesaan, kemitraan SMK–industri koridor pantura dan selatan, bursa kerja regional Banyumas Raya dan eks-Karesidenan Pekalongan | TPT kab/kota, TPT lulusan menengah |
| **Flag Subsisten**: Papua Pegunungan, Papua Tengah | Indikator standar kurang sensitif | Pendidikan dasar–menengah afirmatif; indikator kerentanan khusus | RLS, informal |

**Pesan kebijakan inti:** pendidikan sudah menurunkan NEET, tetapi **belum** menurunkan kerja tidak layak. Pendidikan harus dipasangkan dengan **penciptaan kerja formal** yang sesuai struktur ekonomi daerah. Untuk Jateng, intervensinya **berbasis kluster wilayah**, karena masalahnya mengelompok secara spasial.

*Acuan target diambil dari data, misalnya laju perbaikan tercepat provinsi atau kab/kota setipe (NTT −7,2 poin informal; Kab. Pekalongan −7,3 poin TPT menengah). Tidak ada target karangan.*

---

## 8. Dashboard

### Halaman 1 — "Dua Wajah Masalah Kerja Lulusan" (Langkah ①)
```
┌──────────────────────────────────────────────────────────────────────────┐
│ Judul + pesan · KPI: TPT 4,85% | TPT SMK 8,63% | Informal PT 8%→17% | NEET 19,4% │
├──────────────────────────────────┬───────────────────────────────────────┤
│ DUMBBELL JENJANG 2025 (H1)        │ TREN 2015–2025: TPT per jenjang +     │
│ TPT vs informal vs setengah peng. │ informal per jenjang (toggle) (H2)    │
│ [slider tahun]                    │ + pita PROYEKSI 2026–2030             │
├──────────────────────────────────┼───────────────────────────────────────┤
│ KEJADIAN COVID: slope 2019→2020→  │ HEATMAP JENJANG × SEKTOR               │
│ 2025 per jenjang (H3)             │ + jembatan: "Apakah dua wajah ini juga  │
│                                  │ terlihat antarwilayah?"               │
└──────────────────────────────────┴───────────────────────────────────────┘
```

### Halaman 2 — "Pengangguran Rendah, Kerja Tidak Layak: Dari Indonesia ke Jawa Tengah" (Langkah ②–⑥)
```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Tombol: Pengangguran ↔ Kerja Tidak Layak] · KPI: ρ = −0,30 | Aceh & Maluku 100% │
├────────────┬──────────────────────────────────┬──────────────────────────┤
│ SLIDER 4   │ TILE MAP 38 PROVINSI (warna dari  │ KUADRAN DUA WAJAH        │
│ BOBOT +    │ tombol; flag subsisten)           │ (x tidak bekerja, y KTL; │
│ "Stabil x/10"│                                │ panah 2018→2025)         │
├────────────┼──────────────────────────────────┼──────────────────────────┤
│ SLOPE      │ PITA KETIDAKPASTIAN PRIORITAS      │ KARTU PANEL: "Pendidikan │
│ ranking    │                                   │ naik → NEET turun, KTL   │
│            │                                   │ belum" + biplot PCA mini │
├────────────┴──────────────────────────────────┴──────────────────────────┤
│ [STUDI KASUS JAWA TENGAH] → peta LISA hotspot 35 kab/kota + dumbbell dasar   │
│ vs menengah + tren Brebes/Banjarnegara · [Rekomendasi per kuadran] · Narasi  │
└──────────────────────────────────────────────────────────────────────────┘
```

### Fitur inovatif
| Fitur | Insight | Teknologi |
|---|---|---|
| **Tombol Pengangguran ↔ Kerja Tidak Layak** | H5: peta "berbalik" | Field parameters + bookmark |
| **Slider bobot 4 komponen + "Prioritas stabil x/10"** | H6: juri menguji sendiri | What-if parameter + DAX `RANKX` |
| **Pita ketidakpastian ranking** | H6 | Error bar / Deneb |
| **Kuadran dengan panah 2018 → 2025** | H9, transisi | Scatter dua titik / Play Axis |
| **Biplot PCA mini** (posisi indikator pada dua dimensi) | H4: dasar statistik kuadran | Scatter loading dari CSV |
| **Pita proyeksi 2026–2030** (berlabel PROYEKSI, warna berbeda) | Arah antrean SMK | Line + area interval |
| **Peta LISA hotspot Jateng** | H11 | Tile/shape map, warna kategori LISA |
| **Narasi dinamis** (DAX buatan tim) | Semua | Measure DAX (bukan Smart Narrative) |

**Dilarang:** Smart Narrative, Q&A, Key Influencers, drillthrough. Halaman tooltip dikonfirmasi dulu ke panitia.

---

## 9. Dataset

**Data nasional (BPS WebAPI, `Raw_Dataset/bps_webapi/`, CSV + JSON asli per tahun):**
- D01 TPT × pendidikan (1179)
- D02/D02b informal × pendidikan (2157/1166)
- D03 setengah pengangguran × pendidikan (1184)
- D03b setengah pengangguran × provinsi (1181)
- D04/D04b TPT × umur / jenis kelamin
- D05 TPT × provinsi (543)
- D06/D06b TPAK dan angkatan kerja × provinsi
- D07/D08/D10 informal/formal × provinsi
- D11 upah per jam × provinsi
- D14 bekerja × sektor × pendidikan
- D15/D16 NEET × provinsi / jenis kelamin
- D18 RLS × provinsi (1429)
- D25 kemiskinan × provinsi (192)
- K01 TPT × kab/kota × jenis kelamin (2824)

**Data BPS Jawa Tengah (`Raw_Dataset/bps_jateng/`, `bps_webapi/J03_*`):**
- J01 TPT kab/kota
- J02 RLS kab/kota
- **J03 TPT kab/kota × pendidikan 2019–2023** (var 1864)
- J04 pengeluaran per kapita kab/kota
- J07 TPT kab/kota × jenis kelamin
- J08 TPT × pendidikan Jateng
- J09 distribusi setengah penganggur × pendidikan

**Data pendukung:**
- Urbanisasi provinsi: tabel statis BPS (proyeksi SP2010).
- Batas wilayah kab/kota dari geoBoundaries (`Raw_Dataset/spasial_non_bps/`), **hanya untuk menentukan ketetanggaan** di analisis LISA. Tidak ditampilkan sebagai data statistik. Jika peta poligon ingin ditampilkan, konfirmasi dulu ke panitia; jika tidak, pakai tile map.

**Output analisis (`Processed_Dataset/v5/`):**
- `A_edu_trend_long.csv`, `A_kejadian_covid_jenjang.csv`, `A_proyeksi_2026_2030.csv`
- `B_prov_master_2025.csv`, `B_uji_ketahanan.csv`
- `C_loading_faktor.csv`
- `D_transisi_2018_2025.csv`, `D_matriks_transisi.csv`, `D_perubahan_2018_2025.csv`
- `E_panel_2018_2025.csv`, `E_panel_fe.csv`
- `F_jateng_tpt_pendidikan_2019_2023.csv`, `F_jateng_kabkota_spasial.csv`, `F_jateng_matriks_ketetanggaan.csv`
- `_log_v5.txt`

---

## 10. Validasi, Bias, dan Kelemahan

| Kelemahan / risiko | Penanganan | Status |
|---|---|---|
| Label jenjang tertukar karena urutan alfabet tabel | Pemetaan label eksplisit di skrip, dicek ulang terhadap rilis BPS | ✅ Diperbaiki |
| NEET tumpang tindih dengan pengangguran | Hasil PCA: NEET dipindah ke dimensi "tidak bekerja" | ✅ |
| Bobot indeks subjektif | Monte Carlo 1.000 bobot + slider | ✅ |
| Batas kuadran | Median vs rata-rata vs persentil 45: 87–89% sama; provinsi dekat batas ditandai | ✅ |
| Pengaruh Papua / leverage | Semua uji diulang tanpa Papua | ✅ |
| Urbanisasi masih proyeksi (5 provinsi pakai nilai induk) | Uji tanpa 5 provinsi tersebut: hasil sama | ⚠️ Bersyarat |
| Panel: kausalitas | FE hanya asosiasi dalam provinsi; tidak ada klaim kausal | ✅ |
| Proyeksi tidak pasti | Label PROYEKSI + interval 80%; hanya untuk jenjang nasional | ✅ |
| LISA: geometri non-BPS | Hanya untuk bobot ketetanggaan; 2 kota tanpa tetangga (Kota Magelang, Salatiga) dikecualikan otomatis | ✅ |
| Kab/kota: galat sampling | Tidak meranking selisih kecil; pakai kluster LISA | ✅ |
| Upah bias seleksi | Tidak masuk indeks; F3 terpisah di PCA | ✅ |
| Ekonomi subsisten | Flag Papua Pegunungan dan Papua Tengah | ✅ |
| Data Jateng × pendidikan hanya sampai 2023 | Label tahun di visual | ✅ |
| Ecological fallacy | Klaim individu dari jenjang; klaim wilayah dari provinsi/kab-kota | ✅ |

---

## 11. Simulasi Pertanyaan Juri
| Pertanyaan | Jawaban |
|---|---|
| "Kenapa dua dimensi, bukan satu indeks?" | Analisis faktor menunjukkan pengangguran dan kerja tidak layak adalah dimensi terpisah (KMO 0,65, Bartlett p < 0,001). Menggabungkannya akan menyembunyikan paradoks |
| "Apakah indeks kalian valid?" | Kerja tidak layak berkorelasi 0,66 dengan kemiskinan dan −0,92 dengan pekerjaan formal. Keduanya tidak dipakai dalam indeks |
| "Kenapa tidak forecasting provinsi atau ML?" | Seri pendek dan ada guncangan COVID, dan data hanya 38–256 baris. Proyeksi kami batasi di level jenjang nasional, dengan interval |
| "Apakah pendidikan tidak berguna?" | Berguna: panel menunjukkan kenaikan pendidikan menurunkan NEET. Tetapi belum menurunkan kerja tidak layak, sehingga butuh penciptaan kerja formal |
| "Bukankah ini efek kota?" | Ya, kami mengujinya. Struktur ekonomi (urbanisasi) adalah faktor terkuat, dan itu menjadi temuan kami |
| "Kenapa Jateng?" | Studi kasus wilayah panitia. Rata-rata provinsinya terlihat layak, padahal paradoks berlaku di 35/35 kab/kota dan ada kluster hotspot yang signifikan |
| "Kausal?" | Tidak. Semua asosiasi, konsisten dengan teori Lewis, Spence, dan La Porta & Shleifer |

---

## 12. Rencana Kerja Tersisa
| Hari | Tugas |
|---|---|
| Kam 19 Nov (malam) | Tim review konsep v5; unduh xlsx resmi tabel utama untuk ZIP |
| Jum 20 Nov | Desain layout (Canva) + import CSV `Processed_Dataset/v5/` ke Power BI; bangun Halaman 1 |
| Sab 21 Nov | Halaman 2 + panel Jateng (LISA) + slider + tombol |
| Min 22 Nov | Narasi DAX, poles desain, cek silang semua angka terhadap CSV, latihan Q&A |
| Sen 23 Nov | PDF + `.pbix` + ZIP + surat orisinalitas bermeterai → **kirim sebelum 18.00** |

**Checklist:**
- [ ] 2 halaman, 1900×1100, watermark asli
- [ ] Headline hanya berstatus [DATA]/[TERUJI]
- [ ] Proyeksi berlabel
- [ ] Sumber BPS di tooltip
- [ ] ZIP ≤100 MB (Raw_Dataset, Processed_Dataset, scripts, .pbix, PDF, surat)
- [ ] Tanya panitia soal halaman tooltip dan poligon peta
- [ ] **Buat ulang key WebAPI** setelah lomba (key sempat dibagikan di chat)

---

## 13. Referensi
- Chen (2009) https://doi.org/10.1596/1813-9450-4814
- Elhorst (2003) https://doi.org/10.1046/j.1467-6419.2003.00211.x
- Gustiandza dkk. (2022) https://doi.org/10.1109/iccit55355.2022.10119000
- Hanushek dkk. (2017) https://doi.org/10.3368/jhr.52.1.0415-7074R
- Koto dkk. (2022) https://doi.org/10.22202/economica.2022.v11.i1.6270
- La Porta & Shleifer (2014) https://doi.org/10.1257/jep.28.3.109
- Lewis (1954) https://doi.org/10.1111/j.1467-9957.1954.tb00021.x
- Maloney (2004) https://doi.org/10.1016/j.worlddev.2004.01.008
- Newhouse & Suryadarma (2011) https://doi.org/10.1093/wber/lhr010
- Nilsson (2018) https://doi.org/10.1080/00220388.2018.1475649
- Pattinasarany (2019) https://doi.org/10.7454/mjs.v24i1.10308
- Psacharopoulos & Patrinos (2018) https://doi.org/10.1080/09645292.2018.1484426
- Purnastuti dkk. (2013) https://doi.org/10.1080/00074918.2013.809842
- Cameron dkk. (2019) https://doi.org/10.1080/00074918.2018.1530727
- Spence (1973) https://doi.org/10.2307/1882010
- Anselin (1995, LISA) https://doi.org/10.1111/j.1538-4632.1995.tb00338.x
- Segel & Heer (2010) https://doi.org/10.1109/TVCG.2010.179
- Kale dkk. (2019) https://doi.org/10.1109/TVCG.2018.2864909

*Metadata semua referensi diverifikasi lewat Crossref. Full text rujukan inti wajib dibaca sebelum paper final.*
