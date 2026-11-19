# DAC Data Slayer 4.0 — Advanced Methods & Dashboard Feasibility
### Tema 4: Education for the Future of Work
*Pendamping dokumen `DAC_THEME4_ADVANCED_RESEARCH_AND_CONCEPT_SELECTION.md` (disebut "Dok-1"). Kode dataset D01–D26 dan kode verifikasi (V-NILAI, V-ADA, SEKUNDER, NOT VERIFIED) mengikuti Dok-1 §6.*

---

## 1. Executive Summary

- **Prinsip:** metode dipilih sesuai pertanyaan penelitian dan struktur data BPS publik. Data BPS publik yang tersedia hanya **agregat**: nasional per jenjang dan 38 provinsi per tahun. Tidak ada data individu, dan seri provinsi yang konsisten hanya pendek. Struktur ini langsung menggugurkan banyak metode "canggih".
- **Paket metode untuk konsep pemenang (K1 "Paradoks Pengangguran Rendah"):**
  1. **Metode utama:** indeks komposit IDKK dengan uji sensitivitas bobot (Monte Carlo) dan perbandingan ranking (Spearman).
  2. **Pendukung 1:** tipologi provinsi dengan k-means yang divalidasi Ward, silhouette, dan ARI.
  3. **Pendukung 2:** korelasi parsial/OLS kecil (robust) ditambah Moran's I global berbasis kNN.
- **Tidak direkomendasikan atau tidak layak:** panel FE provinsi, SAR/SEM/GWR, LISA sebagai temuan utama, dekomposisi Oaxaca, quantile regression, multilevel, survival, network, causal inference (DiD/RDD/IV), input-output, dan forecasting.
- **Isu aturan yang perlu dikonfirmasi ke panitia:** poligon batas provinsi (shapefile BIG/Ina-Geoportal) bukan data BPS. **Solusi aman:** pakai peta bawaan Power BI/Looker yang di-geocode dari nama provinsi, atau lat/long centroid (diizinkan FAQ 12). Shapefile hanya dipakai jika panitia mengizinkan.

---

## 2. Review Lima Konsep

| Konsep | Masalah | Unit | DV | IV / kontrol | Gap | Implikasi |
|---|---|---|---|---|---|---|
| K1 Paradoks Pengangguran Rendah | TPT menyesatkan tanpa kualitas kerja | Jenjang (N) + provinsi (P) | TPT, setengah pengangguran, informal, NEET, upah | RLS, % PDRB pertanian, PDRB/kapita | Lensa multidimensi, bukti dua level | Prioritas per tipe provinsi |
| K2 Mismatch vertikal normatif | Lulusan bekerja di bawah kualifikasi | Jenjang × okupasi (N) | % overqualified | Jenjang, sektor | Ukuran mismatch dari data publik | Link-and-match, informasi pasar kerja |
| K3 Transisi pemuda / NEET | Pemuda hilang dari sekolah dan kerja | Umur, JK (N), provinsi | NEET, TPT 15–24 | JK, provinsi | Profil gender NEET | Program *second chance* |
| K4 Gap gender imbal hasil pendidikan | Pendidikan sama, hasil berbeda | Jenjang × JK (N) | Upah, TPAK, informal | JK | Lemah tanpa mikrodata | Kebijakan inklusif |
| K5 Struktur ekonomi & serapan terdidik | Struktur ekonomi tidak menyerap lulusan | Provinsi × tahun | TPT | Pangsa sektor PDRB | Sudah diteliti (Koto 2022) | Kebijakan industri daerah |

## 3. Research Questions dan Kebutuhan Bukti

| Kebutuhan | Jenis bukti | Tersedia di BPS? | Konsekuensi |
|---|---|---|---|
| Gradien pendidikan (K1, K2) | Tabel jenjang nasional, multi-tahun | Ya (D01–D03, D12–D14) | Tren dan perbandingan |
| Kesenjangan antarwilayah (K1, K3, K5) | Cross-section 38 provinsi | Ya (D05, D07, D08, D11, D18, D20) | Indeks, klaster, Moran |
| Perubahan dari waktu ke waktu | Seri provinsi konsisten | Terbatas (pemekaran Papua 2022) | Tren nasional saja; provinsi 2023–2025 |
| Hubungan antarvariabel | Data kompatibel | Ya, level provinsi | Asosiasi, bukan kausal |
| Dampak kebijakan | Variasi eksogen + data sebelum/sesudah | Tidak (data individu dan kelompok perlakuan tidak ada) | Tidak ada klaim dampak |
| Transisi sekolah ke kerja | Data individu, durasi | Tidak (mikrodata) | Proksi kelompok umur |
| Mismatch | Okupasi × pendidikan | Partially verified | Ukuran normatif agregat |

---

## 4. Methodological Discovery Matrix

Skor 1–5 per kriteria (bobot: relevansi 20%, data 20%, validitas 20%, insight 15%, nilai dashboard 10%, interpretasi 5%, kelayakan 10%), dievaluasi untuk K1.

| Metode | Rel | Data | Valid | Insight | Dash | Interp | Feas | **Skor** | Status |
|---|---|---|---|---|---|---|---|---|---|
| Deskriptif + tren | 5 | 5 | 5 | 3 | 5 | 5 | 5 | **4,70** | RECOMMENDED |
| Indeks komposit + sensitivitas | 5 | 5 | 4 | 5 | 5 | 4 | 4 | **4,65** | RECOMMENDED (utama) |
| Spearman ranking | 5 | 5 | 5 | 4 | 4 | 5 | 5 | **4,75** | RECOMMENDED |
| Klaster (k-means + Ward) | 4 | 5 | 4 | 4 | 5 | 4 | 4 | **4,30** | RECOMMENDED |
| Korelasi parsial / OLS kecil | 4 | 5 | 3 | 4 | 3 | 4 | 5 | **4,00** | RECOMMENDED (pendukung) |
| Moran's I global | 3 | 4 | 3 | 3 | 4 | 3 | 4 | **3,40** | OPTIONAL |
| LISA | 3 | 4 | 2 | 3 | 4 | 3 | 4 | **3,20** | OPTIONAL (lampiran) |
| PCA (bobot / reduksi) | 3 | 5 | 4 | 2 | 2 | 3 | 5 | **3,55** | OPTIONAL (sensitivitas) |
| Location Quotient | 3 | 4 | 4 | 3 | 3 | 4 | 4 | **3,55** | OPTIONAL (K5) |
| Shift-share | 2 | 3 | 4 | 2 | 2 | 3 | 3 | **2,75** | NOT RECOMMENDED |
| Panel FE / RE | 3 | 2 | 2 | 3 | 2 | 3 | 3 | **2,50** | NOT RECOMMENDED |
| SAR / SEM / GWR | 2 | 3 | 1 | 2 | 2 | 2 | 2 | **2,00** | NOT FEASIBLE (n=38) |
| Gini/Lorenz antarprovinsi | 2 | 4 | 2 | 2 | 3 | 2 | 4 | **2,70** | NOT RECOMMENDED |
| Quantile regression | 2 | 1 | 2 | 2 | 1 | 2 | 1 | **1,60** | NOT FEASIBLE |
| Oaxaca / Fairlie | 2 | 1 | 2 | 3 | 2 | 2 | 1 | **1,85** | NOT FEASIBLE (mikrodata) |
| Multilevel | 2 | 1 | 2 | 3 | 1 | 2 | 1 | **1,75** | NOT FEASIBLE |
| Survival / transisi | 2 | 1 | 1 | 3 | 1 | 2 | 1 | **1,55** | NOT FEASIBLE |
| Network / mobilitas | 1 | 1 | 1 | 2 | 2 | 2 | 1 | **1,30** | NOT FEASIBLE |
| DiD / RDD / IV / ITS | 2 | 1 | 1 | 3 | 1 | 2 | 1 | **1,55** | NOT FEASIBLE |
| Input-Output | 1 | 3 | 3 | 2 | 1 | 2 | 1 | **2,00** | NOT RECOMMENDED |
| Forecasting / skenario | 2 | 3 | 2 | 2 | 3 | 3 | 3 | **2,45** | NOT RECOMMENDED |
| MCDA / TOPSIS / AHP | 3 | 5 | 3 | 3 | 4 | 3 | 4 | **3,60** | OPTIONAL (setara indeks; pilih salah satu) |

*Contoh hitungan untuk indeks:* 5(.2)+5(.2)+4(.2)+5(.15)+5(.1)+4(.05)+4(.1) = 4,65.

---

## 5. Literature Review untuk Metode yang Relevan

*Metadata diverifikasi via Crossref; full text belum dibaca.*

| Metode | Penulis/Tahun | Konteks | Data | Temuan / peran | Keterbatasan | Relevansi |
|---|---|---|---|---|---|---|
| Indeks komposit | OECD/JRC (2008), *Handbook on Constructing Composite Indicators* | Metodologi | — | Langkah normalisasi, pembobotan, uji sensitivitas | DOI NOT VERIFIED | Prosedur IDKK |
| Indeks + tipologi | Raychev (2026), *Regional Adaptation Capacity and Labour-market Vulnerability: A Grey-informed Typology of EU Regions*, [10.1007/s12061-026-10062-7](https://doi.org/10.1007/s12061-026-10062-7) | Wilayah UE | Agregat regional | Indeks kerentanan pasar kerja → tipologi wilayah | Eropa; metode *grey* | Preseden langsung "indeks → tipologi" |
| Klaster validasi | Rousseeuw (1987), [10.1016/0377-0427(87)90125-7](https://doi.org/10.1016/0377-0427(87)90125-7) | Metodologi | — | Silhouette | — | Pemilihan k |
| Autokorelasi spasial | Anselin (1995), [10.1111/j.1538-4632.1995.tb00338.x](https://doi.org/10.1111/j.1538-4632.1995.tb00338.x) | Metodologi | — | Moran lokal (LISA) | Multiple testing | Uji pendukung |
| Spasial pengangguran | Gustiandza dkk. (2022), [10.1109/iccit55355.2022.10119000](https://doi.org/10.1109/iccit55355.2022.10119000) | Indonesia | TPT provinsi | Uji Moran pada TPT | Hanya TPT | Pembanding: kami menguji indeks multidimensi |
| Spasial pengangguran | Rios (2016), [10.1080/00343404.2016.1216094](https://doi.org/10.1080/00343404.2016.1216094) | Eropa | Panel regional | Ketergantungan spasial signifikan | n besar | Pembenaran uji spasial; juga menunjukkan model penuh butuh n besar |
| Panel provinsi | Koto dkk. (2022), [10.22202/economica.2022.v11.i1.6270](https://doi.org/10.22202/economica.2022.v11.i1.6270) | Indonesia | Panel provinsi | Pertumbuhan sektoral vs pengangguran terdidik | Kausal lemah | Alasan **tidak** mengulang panel FE |
| Kelompok umur (pseudo-kohort) | Hanushek dkk. (2017), [10.3368/jhr.52.1.0415-7074R](https://doi.org/10.3368/jhr.52.1.0415-7074R) | 11 negara | IALS | Pola vokasi menurut usia | Mikro | K3 |
| Dekomposisi | Oaxaca (1973), [10.2307/2525981](https://doi.org/10.2307/2525981); Cameron dkk. (2019), [10.1080/00074918.2018.1530727](https://doi.org/10.1080/00074918.2018.1530727) | Metodologi; Indonesia | Mikro | Dekomposisi gap | Butuh mikrodata | Alasan K4 tidak layak |
| Kausal | Duflo (2001), [10.1257/aer.91.4.795](https://doi.org/10.1257/aer.91.4.795) | Indonesia | Variasi program INPRES | DiD | Diperdebatkan (Roodman 2023, [10.2139/ssrn.4333118](https://doi.org/10.2139/ssrn.4333118)) | Menunjukkan syarat desain kausal yang **tidak** kita punya |
| Mismatch normatif | McGuinness (2006), [10.1111/j.0950-0804.2006.00284.x](https://doi.org/10.1111/j.0950-0804.2006.00284.x); Quintini (2011), [10.1787/5kg58j9d7b6d-en](https://doi.org/10.1787/5kg58j9d7b6d-en) | Review | — | Metode *job analysis* dan keterbatasannya | Pemetaan kasar | K2 |

**Kekurangan bukti.** Untuk Moran's I pada indikator kualitas kerja di Indonesia, kami belum menemukan studi empiris kedua yang peer-reviewed. Ini **sekaligus gap**, tetapi juga **risiko**, karena preseden metodologisnya berasal dari luar Indonesia.

---

## 6. Spatial Data and Shapefile Feasibility

| Aspek | Temuan | Keputusan |
|---|---|---|
| Unit | 38 provinsi | — |
| Geometri | Batas resmi dari BIG/Ina-Geoportal (non-BPS) | **Belum jelas diizinkan.** FAQ 12 hanya menyebut lat/long sebagai pendukung peta. → **Tanyakan panitia** |
| Alternatif aman | (a) Peta bawaan Power BI / Looker (geocoding nama provinsi; cek ejaan "Papua Barat Daya", "Papua Pegunungan", dll.). (b) Bubble map dari centroid lat/long | Pakai (a). Jika provinsi baru tidak dikenali, pakai (b) |
| Matriks bobot | Contiguity (queen) bermasalah karena banyak provinsi kepulauan yang terisolasi (Maluku, Maluku Utara, NTT, NTB, Bali, Kepri, Babel, dll.) | **kNN (k=4) dari centroid**, sensitivitas k=3 dan 5. Jarak centroid **bukan** ukuran aksesibilitas |
| n | 38 | Hanya Moran global (999 permutasi). LISA sebagai lampiran dengan koreksi FDR |
| Interpretasi | — | "Provinsi berdekatan cenderung punya kerentanan serupa", **bukan** "spillover" |

## 7. Panel and Longitudinal Data Feasibility

| Variabel | Unit | Periode konsisten | Masalah |
|---|---|---|---|
| TPT provinsi | P | 2023–2025 untuk 38 provinsi; lebih lama untuk 34 provinsi | Pemekaran Papua 2022 |
| Informal provinsi | P | Cek | Definisi informal BPS berbasis status pekerjaan |
| PDRB sektoral | P | 2021–2025 (D20) | Tahun dasar 2010 |
| RLS | P | Panjang | Susenas Maret vs Sakernas Agustus |

**Keputusan:** T ≈ 3–5 dengan variasi dalam-provinsi yang kecil membuat FE tidak informatif dan rentan autokorelasi. Ada juga *reverse causality* (TPT ↔ RLS) dan omitted variables. **Gunakan tren nasional dan cross-section tahun terbaru.** Panel provinsi hanya ditampilkan sebagai perubahan 2023→2025 (*slope chart*), bukan model.

## 8. Cohort and Distributional Analysis Feasibility

- **Kelompok umur:** D04 (TPT menurut umur) dan D15/D16 (NEET) layak sebagai *repeated cross-section*. Kalimat wajib: "perbandingan kelompok umur pada satu periode, bukan pelacakan kohort".
- **Distribusi:** box plot atau *strip plot* IDKK dan komponennya antar-38 provinsi untuk menunjukkan sebaran, bukan hanya rata-rata.
- **Gini/Lorenz antarprovinsi** dari data agregat **tidak** boleh ditafsirkan sebagai ketimpangan individu. Jika ditampilkan, beri label "ketimpangan antarprovinsi (tidak tertimbang penduduk)". Status: tidak direkomendasikan.
- **Quantile regression:** butuh distribusi individu → tidak layak.

## 9. Decomposition Analysis Feasibility

| Metode | Kebutuhan | Status | Alternatif |
|---|---|---|---|
| Oaxaca–Blinder (upah gender) | Mikrodata Sakernas | NOT FEASIBLE | Rasio upah P/L per jenjang (jika tabelnya ada) |
| Fairlie (TPT biner) | Mikrodata | NOT FEASIBLE | — |
| Dekomposisi komposisi (*shift-share* sederhana TPT nasional) | Komposisi angkatan kerja per jenjang + TPT per jenjang | **Layak jika jumlah angkatan kerja per jenjang tersedia (D21)** | ΔTPT = efek komposisi pendidikan + efek tingkat. Menjawab: "apakah TPT turun karena komposisi pendidikan berubah atau karena TPT tiap jenjang turun?" → **OPTIONAL, bernilai tinggi** |

*Rumus:* `TPT_t = Σ_j s_jt · u_jt`, dengan `s` = pangsa angkatan kerja jenjang j dan `u` = TPT jenjang j.
`ΔTPT = Σ Δs_j · ū_j + Σ s̄_j · Δu_j` (dekomposisi rata-rata dua periode). Ini identitas akuntansi, **bukan kausal**.

## 10. Clustering and Composite Index Feasibility

**Indeks (IDKK)**

| Langkah | Pilihan | Justifikasi |
|---|---|---|
| Kerangka | Decent work: kurangnya pekerjaan (TPT), kurangnya jam (setengah pengangguran), perlindungan (informal), pemuda tidak terserap (NEET), pendapatan (upah) | ILO, La Porta & Shleifer 2014 |
| Normalisasi | Min-max (utama); z-score (sensitivitas) | OECD/JRC 2008 |
| Bobot | Sama rata (utama); PCA (sensitivitas); 1.000 bobot Dirichlet acak | Transparansi |
| Validitas | Korelasi antarkomponen (redundansi jika r > 0,9); Cronbach α hanya sebagai informasi | — |
| Output | Skor 0–100, ranking + interval 5–95% | Tampil di tooltip |
| Label | "Konstruksi analitis tim, bukan indikator resmi BPS" | Aturan integritas |

**Klaster**

| Langkah | Pilihan |
|---|---|
| Variabel | 5 komponen IDKK (z-score) + RLS. Jangan memasukkan IDKK sekaligus komponennya karena dobel hitung |
| Algoritma | k-means (n_init=50) dan Ward hierarchical |
| Penentuan k | Silhouette dan Davies-Bouldin untuk k=2..6, ditambah keterbacaan substantif |
| Stabilitas | ARI antara k-means dan Ward; bootstrap 100× (Jaccard per klaster) |
| Nama klaster | Diberikan **setelah** melihat profil z-score, bukan sebelumnya |
| DBSCAN | Tidak cocok untuk n=38 |

## 11. Causal Inference Feasibility

| Kandidat | Kebijakan | Masalah | Status |
|---|---|---|---|
| DiD revitalisasi SMK (Inpres 9/2016) | Ada | Tidak ada kelompok kontrol yang jelas, semua provinsi terdampak, data level provinsi × jenis sekolah tidak tersedia | NOT FEASIBLE |
| ITS TPT SMK di sekitar 2016 | Ada seri waktu | Satu seri nasional, banyak *confounder* (COVID, siklus ekonomi) | NOT RECOMMENDED. Boleh hanya sebagai anotasi di grafik tren tanpa klaim |
| RDD / IV / PSM | — | Butuh data individu | NOT FEASIBLE |

## 12. Economic Structure Analysis Feasibility

- **Location Quotient** (pangsa sektor PDRB provinsi / pangsa nasional) dari D20: layak dan murah. Dipakai sebagai **variabel kontrol dan deskripsi klaster** (misalnya "klaster ini dominan pertanian, LQ > 1").
- **Shift-share** pekerja per sektor per provinsi butuh pekerja sektor × provinsi × 2 periode. Belum terverifikasi → tidak direkomendasikan.
- **Input-Output:** tabel I-O BPS ada di level nasional, tetapi tidak menjawab RQ. Ditolak.
- **Peringatan:** pertumbuhan sektor ≠ penciptaan kerja (Rodrik 2016). Jangan disamakan.

## 13. Microdata and Multilevel Feasibility

Mikrodata Sakernas/Susenas diakses lewat **SILASTIK** (berbayar atau melalui permohonan, ada perjanjian penggunaan; FAQ 30 mengizinkan tidak menyertakan raw data). Waktu prosesnya tidak pasti, dan analisis yang benar memerlukan bobot survei serta desain sampel kompleks (strata, PSU). **Tidak realistis dalam 5 hari.** Dimasukkan ke agenda *future research* di paper final, misalnya logit multilevel status informal dengan prediktor individu (pendidikan, jenis SMA) dan provinsi (LQ, IDKK).

## 14. Network and Survival Analysis Feasibility

- **Network:** tidak ada data arus komuter/migrasi kerja antarprovinsi yang dipakai di sini (data migrasi risen SUPAS 2025 mungkin ada tetapi **NOT VERIFIED**). Membangun jaringan dari kedekatan geografis **bukan** jaringan mobilitas. → NOT FEASIBLE.
- **Survival:** tidak ada durasi menganggur atau waktu menuju kerja dalam tabel publik. → NOT FEASIBLE. Jangan mengklaim "waktu tunggu kerja" dari TPT.

## 15. Forecasting and Scenario Feasibility

Seri TPT per jenjang cukup panjang (satu titik per tahun), tetapi ada *structural break* (COVID 2020) dan perubahan definisi, sementara n tahunan kecil. Proyeksi akan punya interval lebar dan nilai tambahnya rendah. **What-if** sederhana yang sah: memakai identitas §9 ("jika komposisi pendidikan angkatan kerja 2030 = X dan TPT per jenjang tetap, TPT agregat = Y"). Ini simulasi akuntansi dan harus diberi label "simulasi". Status: OPTIONAL, prioritas rendah.

## 16. BPS Data Availability and Integration Inventory

Lihat **Dok-1 §6** (D01–D26 lengkap dengan URL dan status). Tambahan khusus metode:

| Kebutuhan metode | Dataset | Status |
|---|---|---|
| Dekomposisi komposisi (§9) | Angkatan kerja per jenjang (D21, lampiran publikasi) | V-ADA (publikasi), tabel spesifik NOT VERIFIED |
| LQ (§12) | D20 | V-ADA |
| Peta (§6) | Nama provinsi BPS; lat/long centroid | Nama: V-ADA. Centroid: dihitung sendiri (non-statistik) |
| Mismatch K2 | Pekerja menurut jenis pekerjaan × pendidikan | PARTIALLY VERIFIED |

## 17. Data Compatibility Audit

Lihat Dok-1 §8. Ringkasan aturan join:
1. Satu periode (Agustus) per tahun.
2. Kunci join `kode_prov` 2 digit BPS (bukan nama).
3. Tidak menggabungkan indikator berbeda populasi menjadi satu angka kecuali lewat normalisasi indeks.
4. Indikator Susenas (RLS) diperlakukan sebagai konteks wilayah.
5. Setiap nilai hasil interpolasi diberi kolom `is_estimate = 1`.

## 18. Method-to-Dashboard Feasibility Matrix

| Metode | T1 Relevansi | T2 Data | T3 Validitas | T4 Output dashboard | T5 Kompetisi | Lolos? |
|---|---|---|---|---|---|---|
| Tren jenjang | ✔ RQ1 | ✔ | ✔ | Line chart + anotasi | ✔ | **Ya** |
| Dumbbell TPT vs informal | ✔ RQ1 | ✔ (samakan tahun) | ✔ | Visual paradoks | ✔ | **Ya** |
| IDKK + sensitivitas | ✔ RQ2 | ✔ | ✔ (diuji) | Peta + interval ranking di tooltip | ✔ | **Ya** |
| Spearman ranking | ✔ RQ2 | ✔ | ✔ | Slope chart + KPI "ρ = …" | ✔ | **Ya** |
| Korelasi parsial | ✔ RQ3 | ✔ | ⚠ n kecil | Scatter + garis tren + catatan | ✔ | **Ya (catatan)** |
| Klaster | ✔ RQ4 | ✔ | ✔ (silhouette) | Warna peta + profil | ✔ | **Ya** |
| Moran's I | ✔ RQ4 | ✔ | ⚠ | Satu KPI kecil + Moran scatter (opsional) | ✔ | **Ya (pendukung)** |
| Dekomposisi komposisi | ✔ | ⚠ | ✔ | Waterfall | ⚠ | Jika data ada |
| Panel FE, spatial models, Oaxaca, dll. | — | ✘ | ✘ | — | ✘ | Tidak |

## 19. Candidate Method Combinations

| Kombinasi | Isi | Logika | Redundansi / risiko | Nilai tambah | Kelayakan |
|---|---|---|---|---|---|
| **A\*. Regional Job-Quality Intelligence (DIPILIH)** | Tren jenjang → IDKK → Spearman → klaster → Moran → rekomendasi per klaster | Masalah → bukti → beda wilayah → prioritas | PCA dan klaster bisa redundan → PCA hanya untuk sensitivitas | Tinggi | Tinggi |
| B. Hidden Inequality | Distribusi + Oaxaca + quantile | — | Butuh mikrodata | Tinggi | **Rendah** |
| C. School-to-Work | Kelompok umur + NEET + mismatch normatif | Fokus pemuda | Data provinsi × JK belum pasti | Sedang | Sedang |
| D. Struktur ekonomi | LQ + panel + shift-share | — | Mengulang Koto 2022; panel lemah | Rendah–sedang | Sedang |
| E. Policy Priority | Indeks + TOPSIS + skenario | — | TOPSIS ≈ indeks (redundan) | Sedang | Tinggi |
| **A + modul C-mismatch** | A, ditambah 1 visual mismatch normatif | Memperkuat sisi "kesiapan SDM" | Ruang dashboard | **Tertinggi** | Bergantung pada tabel K2 |

## 20. Critical Jury Simulation

| Kritik juri | Risiko | Bukti yang diperlukan | Mitigasi | Keterbatasan tersisa |
|---|---|---|---|---|
| Mengapa indeks, bukan TPT saja? | Sedang | Spearman TPT vs IDKK rendah | Tampilkan slope chart perubahan ranking | — |
| Bobot indeks subjektif | Tinggi | Ranking stabil antar-skema | Monte Carlo + interval ranking | Pilihan komponen tetap normatif |
| Klaster stabil? | Sedang | Silhouette, ARI, bootstrap Jaccard | Laporkan nilainya di catatan metode | n=38 |
| Autokorelasi spasial nyata? | Sedang | Moran I, p permutasi, sensitivitas k | Laporkan untuk k=3/4/5 | Kepulauan; jarak ≠ akses |
| Ecological fallacy | Tinggi | — | Pisahkan level jenjang dan wilayah; bahasa asosiatif | Inheren |
| Omitted variables (upah minimum, biaya hidup, migrasi) | Sedang | — | Sebutkan; upah minimum non-BPS tidak boleh dipakai | Inheren |
| Kausal? | Tinggi bila salah bicara | — | Tidak ada klaim kausal | — |
| Konsistensi tahun antartabel | Sedang | Tabel tahun yang sama | Selaraskan D01 dengan D02 (2023) | Informal per jenjang mungkin hanya sampai 2023 |
| Visual menyesatkan (peta luas wilayah) | Sedang | — | Tambahkan bar ranking di samping peta; skala warna sekuensial | — |
| Rekomendasi tidak mengikuti hasil | Sedang | Tautan klaster → rekomendasi | Panel rekomendasi per klaster dengan indikator pemantauan | — |

## 21. Recommended Methods for Each Concept

| Konsep | Utama | Pendukung (maks. 3) | Tidak direkomendasikan | Struktur data | Kelayakan |
|---|---|---|---|---|---|
| **K1** | Indeks IDKK + sensitivitas | Spearman; klaster; korelasi parsial (+ Moran) | Panel FE, SAR/GWR, kausal | Jenjang × tahun (N); provinsi cross-section | **Tinggi** |
| K2 | Mismatch normatif ILO (2 aturan pemetaan) | Tren; heatmap pendidikan × okupasi; rasio upah | Self-assessment, horizontal mismatch | Jenjang × okupasi × tahun (N) | Sedang (data) |
| K3 | Profil kelompok umur dan gender (repeated cross-section) | Peta NEET; korelasi NEET–LQ | Cohort tracking, survival | Umur/JK × tahun; provinsi | Tinggi, kedalaman terbatas |
| K4 | Rasio gap gender agregat | Tren gap | Oaxaca, quantile | Jenjang × JK | Sedang; relevansi tema lemah |
| K5 | LQ + deskripsi | Korelasi struktur–TPT | Panel FE kausal, I-O | Provinsi × sektor | Sedang; kebaruan rendah |

## 22. Dashboard Blueprint for Each Concept

| Konsep | Halaman 1 | Halaman 2 |
|---|---|---|
| **K1** | Paradoks jenjang: KPI, dumbbell TPT vs informal, tren TPT per jenjang, setengah pengangguran, heatmap upah pendidikan × sektor | Peta IDKK (toggle TPT), kuadran TPT vs IDKK_noTPT, slope chart ranking, profil klaster, panel rekomendasi + catatan metode |
| K2 | Tren % overqualified per jenjang; stacked bar okupasi per jenjang | Heatmap pendidikan × okupasi; upah PT di okupasi rendah vs SMA |
| K3 | TPT per umur; NEET per JK | Peta NEET; tipologi pemuda |
| K4 | Gap TPAK/informal per JK × jenjang | Tren gap; provinsi |
| K5 | Struktur PDRB, LQ | Scatter struktur vs TPT; peta |

Detail K1 ada di Dok-1 §16. **Visual yang dibuang dengan sengaja:** gauge, pie chart untuk lebih dari 3 kategori, treemap (tidak ada struktur hierarki yang bermakna), Sankey dan network (data arus tidak ada), fan chart forecast.

## 23. Comparative Ranking of Five Concepts

Skala 1–5.

| Kriteria | K1 | K2 | K3 | K4 | K5 |
|---|---|---|---|---|---|
| Research gap | 4 | 5 | 3 | 2 | 2 |
| Literature support | 4 | 4 | 4 | 4 | 3 |
| BPS data availability | 5 | 3 | 4 | 2 | 3 |
| Methodological validity | 4 | 4 | 4 | 2 | 3 |
| Analytical depth | 4 | 4 | 3 | 2 | 3 |
| Novelty | 4 | 5 | 3 | 2 | 2 |
| Insight potential | 5 | 4 | 4 | 3 | 3 |
| Dashboard potential | 5 | 4 | 4 | 3 | 3 |
| Policy relevance | 5 | 4 | 4 | 3 | 3 |
| Feasibility | 5 | 3 | 4 | 3 | 4 |
| **Total (dari 50)** | **45** | **40** | **37** | **26** | **29** |

| Kategori | Konsep |
|---|---|
| Fondasi penelitian terkuat | K1 |
| Insight terbesar | K1 |
| Visualisasi terbaik | K1 |
| Risiko metodologis terendah | K3 |
| Kontribusi kebijakan terkuat | K1 |
| Terbaik keseluruhan | **K1** (+ modul K2 jika data ada) |

Urutan ini konsisten dengan Dok-1 §10: K1 > K2 > K3 > K5 > K4.

## 24. Final Methodological Recommendation

1. **Kerjakan:** tren jenjang → IDKK (min-max, bobot sama) → Monte Carlo bobot → Spearman TPT vs IDKK → korelasi parsial RLS (kontrol % PDRB pertanian) → klaster k-means/Ward (silhouette, ARI) → Moran's I kNN.
2. **Opsional jika waktu tersisa:** dekomposisi komposisi TPT (§9) dan modul mismatch K2.
3. **Jangan kerjakan:** semua metode berstatus NOT FEASIBLE atau NOT RECOMMENDED. Metode tersebut disebut di paper sebagai *future research* beserta alasannya. Ini menunjukkan kepada juri bahwa pilihan metode disengaja, bukan karena tidak tahu.
4. **Tools:** Python (pandas, scikit-learn, scipy, esda/libpysal) untuk analisis, hasil diekspor ke CSV, lalu **Power BI** (bookmark untuk toggle, tooltip page). Alternatifnya Looker Studio jika tim lebih nyaman.

## 25. Limitations and Unresolved Verification Issues

| Isu | Dampak | Tindakan (tanggal) |
|---|---|---|
| Poligon peta non-BPS | Kepatuhan aturan | Tanya narahubung panitia (18–19 Nov); pakai peta bawaan sebagai default |
| Informal per jenjang terakhir 2023? | Perbandingan dengan TPT | Cek selektor tahun D02 (19 Nov) |
| Setengah pengangguran dan NEET per provinsi | Komponen IDKK | Cek D03/D15 per provinsi atau publikasi D21/D23 (19 Nov). Jika tidak ada, IDKK memakai 3 komponen + sensitivitas |
| Tabel okupasi × pendidikan | Modul K2 | Cari 19 Nov; jika tidak ada, K2 dibatalkan |
| Full text literatur | Ketepatan kutipan di paper | Baca 8 rujukan inti sebelum 1 Des |
| DOI handbook OECD/JRC | Referensi | Verifikasi manual |
| Ketidakpastian Moran (n=38, kepulauan) | Kekuatan klaim spasial | Posisikan sebagai pendukung |

## 26. References and Source URLs

Semua referensi dan URL BPS ada di **Dok-1 §21–§22**. Referensi tambahan di dokumen ini:
- Raychev (2026). Regional Adaptation Capacity and Labour-market Vulnerability: A Grey-informed Typology of EU Regions. *Applied Spatial Analysis and Policy*. https://doi.org/10.1007/s12061-026-10062-7
- Roodman, D. (2023). Schooling and Labor Market Consequences of School Construction in Indonesia: Comment. SSRN. https://doi.org/10.2139/ssrn.4333118
