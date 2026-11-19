# DAC Data Slayer 4.0 — Eksplorasi Fitur Dashboard Inovatif
### Konsep: "Paradoks Pengangguran Rendah" (Tema 4) · Platform: Power BI · 1900×1100 · Maksimal 2 halaman

*Dokumen pendamping:*
- *Dok-1 = `DAC_THEME4_ADVANCED_RESEARCH_AND_CONCEPT_SELECTION.md`*
- *Dok-2 = `DAC_THEME4_ADVANCED_METHODS_AND_DASHBOARD_FEASIBILITY.md`*

*IDKK = Indeks Defisit Kualitas Kerja (Dok-1 §13).*

---

## 0. Prinsip seleksi

Sebuah fitur dianggap "wow" **hanya jika** juri bisa *menemukan* sesuatu yang tidak terlihat di grafik biasa:
- menguji asumsi kami,
- membandingkan kondisi, atau
- memahami konsekuensi sebuah pilihan.

Fitur yang hanya mempercantik tampilan langsung gugur.

**Enam syarat yang wajib dipenuhi setiap fitur:**
1. Punya tujuan analitis.
2. Menghasilkan insight baru.
3. Bisa dibangun di Power BI dalam waktu yang tersedia.
4. Datanya valid (BPS atau hasil olahan tim).
5. Tetap terbaca di PDF statis.
6. Tanpa AI generatif. Fitur seperti *Smart Narrative*, *Q&A*, *Key Influencers*, dan *Decomposition Tree AI split* **dilarang dipakai**, karena berisiko melanggar FAQ 9.

**Tiga batasan teknis yang harus dipegang:**

| Batasan | Dampak pada desain |
|---|---|
| **Juri mungkin hanya melihat PDF.** Power BI gratis tidak bisa membuat link publik (FAQ 23). | Setiap fitur wajib punya **"PDF state"**: tampilan default yang sudah memuat insight terkuat, plus label kecil "interaktif di .pbix". |
| **Halaman drillthrough dan halaman tooltip secara teknis adalah halaman tambahan.** FAQ 36 hanya menjamin bookmark atau tombol *di halaman yang sama* dihitung 1 halaman. | **Hindari drillthrough.** Halaman tooltip berupa overlay kemungkinan aman, tetapi **konfirmasi ke panitia**. Siapkan alternatif berupa panel bookmark di halaman yang sama. |
| Semua angka hasil olahan, seperti indeks, residual, klaster, dan kemiripan provinsi, harus dihitung di Python lalu diekspor ke CSV. | Power BI hanya menghitung ulang bagian yang ringan (bobot dan ranking) dengan DAX. |

---

## 1. Daftar panjang: 20 ide

| # | Ide | Kategori | Lolos tahap 1? | Alasan |
|---|---|---|---|---|
| 1 | **Slider Bobot Indeks + Uji Stabilitas Prioritas** | What-if / sensitivitas | ✔ | Juri menguji asumsi terbesar kami sendiri |
| 2 | **Tombol Ranking Terbalik (TPT ↔ IDKK)** | Ranking dinamis | ✔ | Inti pesan dalam satu klik |
| 3 | **"Melampaui Ekspektasi": provinsi yang hasilnya lebih baik atau buruk dari prediksi** | Anomali / *positive deviance* | ✔ | Menemukan provinsi teladan dan provinsi yang perlu diselidiki |
| 4 | **Provinsi Kembar: konteks serupa, hasil berbeda** | Benchmark / decision support | ✔ | Mengubah perbandingan menjadi pembelajaran kebijakan |
| 5 | **Pita Ketidakpastian Ranking** (interval 5–95% dari 1.000 bobot acak) | Uncertainty | ✔ | Jujur secara statistik, jarang ada di lomba |
| 6 | **Dumbbell Paradoks per Jenjang dengan pemilih tahun** | Storytelling | ✔ | Bukti level individu (jenjang) |
| 7 | **Bar Kontribusi Komponen: "Kenapa provinsi ini buruk?"** | Dekomposisi indeks | ✔ | Membuka isi indeks, tidak jadi kotak hitam |
| 8 | **Penjelajah Tipologi (klik klaster)** | Cluster exploration | ✔ | Menghubungkan klaster ke rekomendasi |
| 9 | **Distribusi "Di Mana Posisi Provinsi Ini?"** (strip plot per komponen) | Distribusi | ✔ | Konteks sebaran, bukan hanya rata-rata |
| 10 | **Kuadran dengan Garis Ambang yang Bisa Digeser** | What-if ambang | ✔ (digabung ke #2) | Menguji definisi "tinggi/rendah" |
| 11 | **Waterfall Dekomposisi TPT: efek komposisi vs efek tingkat** | Dekomposisi / before-after | ✔ (bersyarat data) | "TPT turun karena orang makin terdidik, atau karena tiap jenjang membaik?" |
| 12 | **Simulator Komposisi Pendidikan 2030** | Skenario | △ | Simulasi akuntansi; risiko disalahartikan sebagai prediksi |
| 13 | **Narasi Dinamis (DAX buatan tim)** | Storytelling | ✔ (pelengkap semua fitur) | Teks ikut berubah sesuai pilihan juri |
| 14 | **"Tebak Dulu": juri menebak sebelum jawabannya dibuka (bookmark reveal)** | Interactive storytelling | △ | Menarik, tetapi tidak berfungsi di PDF |
| 15 | **Heatmap "Di Sektor Mana SMK Dibayar?"** (upah pendidikan × 17 sektor) | Eksplorasi | ✔ | Insight vokasi yang spesifik sektor |
| 16 | **Moran Scatter terhubung ke peta** | Spasial | △ | Interpretasinya sulit bagi juri nonspasial; n=38 |
| 17 | **Pemilih Kriteria Prioritas Kebijakan (TPT / informal / NEET / IDKK)** | Policy trade-off | ✔ (digabung ke #1) | Menunjukkan prioritas bergantung pada definisi masalah |
| 18 | **Play-axis animasi tren** | Animasi | ✘ | Tidak terbaca di PDF; data provinsi pendek |
| 19 | **Peta 3D / globe** | Estetika | ✘ | Tidak ada nilai analitis |
| 20 | **Chatbot / Q&A visual** | AI | ✘ | Melanggar semangat FAQ 9 |

---

## 2. Sepuluh fitur terbaik (dikembangkan)

### F1. Slider Bobot + Uji Stabilitas Prioritas

| Aspek | Isi |
|---|---|
| Interaksi | Lima slider (0–5) untuk pengangguran, setengah pengangguran, informal, NEET, dan upah. Peta, ranking, dan teks berubah seketika. Ada tombol "Reset ke bobot sama". |
| Pengalaman juri | "Saya coba buang komponen pengangguran sama sekali… ternyata 8 provinsi prioritas tetap sama." Juri merasa sedang **menguji** penelitian kami, bukan sekadar membacanya. |
| Contoh insight (hipotesis, diuji setelah data diolah) | Sebagian provinsi selalu masuk 10 prioritas apa pun bobotnya ("prioritas tangguh"). Provinsi lain hanya masuk jika TPT diberi bobot tinggi. |
| RQ | RQ2 (apakah prioritas bergantung pada TPT) dan robustness indeks |
| Data | `z_tpt, z_tsp, z_inf, z_neet, z_upah` (min-max, dari CSV), `rank_default` |
| Cara kerja | `IDKK_dyn = Σ wᵢ·zᵢ / Σ wᵢ`, lalu ranking ulang dengan `RANKX`. Stabilitas = jumlah provinsi 10 teratas yang sama dengan default. |
| Visual | Panel kiri: slider. Tengah: peta. Kanan: bar ranking 10 teratas dengan penanda ▲▼ dibanding default. KPI: "Stabilitas prioritas: 8/10". |
| Power BI | *What-if parameter* ×5 ([dok](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-what-if)). DAX di bawah. |
| Kesulitan / waktu | Sedang · 3–4 jam |
| Risiko | Bobot 0 semua → bagi nol, jadi tangani dengan `DIVIDE`. Juri bisa membuat bobot ekstrem, jadi tampilkan peringatan jika satu bobot lebih dari 60%. |
| PDF state | Bobot sama + teks "Prioritas stabil: X dari 10 provinsi tetap teratas di 1.000 skema bobot acak" (dari Monte Carlo F5). |

```DAX
IDKK Dinamis =
VAR w1 = [W TPT Value]   VAR w2 = [W TSP Value]   VAR w3 = [W Informal Value]
VAR w4 = [W NEET Value]  VAR w5 = [W Upah Value]
RETURN 100 * DIVIDE(
    w1*SELECTEDVALUE(prov[z_tpt]) + w2*SELECTEDVALUE(prov[z_tsp]) + w3*SELECTEDVALUE(prov[z_inf])
  + w4*SELECTEDVALUE(prov[z_neet]) + w5*SELECTEDVALUE(prov[z_upah]),
    w1+w2+w3+w4+w5)

Rank Dinamis = RANKX(ALL(prov[nama_prov]), [IDKK Dinamis], , DESC, Dense)

Stabilitas Top10 =
COUNTROWS(FILTER(ALL(prov[nama_prov]), [Rank Dinamis] <= 10 && CALCULATE(MAX(prov[rank_default])) <= 10))
```

### F2. Tombol Ranking Terbalik (TPT ↔ IDKK) + Slope Chart

| Aspek | Isi |
|---|---|
| Interaksi | Satu tombol mengganti metrik peta dan bar (*field parameter*). Di sampingnya ada slope chart ranking TPT → ranking IDKK yang menyorot 5 provinsi dengan perubahan terbesar. |
| Pengalaman juri | Momen "aha" dalam 3 detik: peta yang tadinya "hijau" di wilayah tertentu berubah menjadi "merah". |
| Contoh insight (H) | Provinsi dengan TPT rendah naik jauh dalam ranking defisit kualitas kerja (H2 di Dok-1: Spearman < 0,5). |
| RQ | RQ2 |
| Data | `rank_tpt`, `rank_idkk` |
| Cara kerja | Spearman ρ dihitung di Python lalu ditampilkan sebagai KPI ("ρ = 0,xx"). |
| Visual | Peta besar + slope chart (garis abu-abu, 5 garis berwarna dengan label). |
| Power BI | *Field parameters* ([dok](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters)). Slope chart dibuat dari line chart dengan 2 titik x (kolom "Metrik"). |
| Kesulitan / waktu | Rendah · 2 jam |
| Risiko | Peta choropleth memberi bobot visual sesuai luas wilayah, sehingga Papua terlihat dominan. Imbangi dengan bar ranking di sampingnya. |
| PDF state | Tampilkan **berdampingan**: peta kecil TPT dan peta besar IDKK, plus slope chart. |

### F3. "Melampaui Ekspektasi" (Positive / Negative Deviance)

| Aspek | Isi |
|---|---|
| Interaksi | Scatter "IDKK yang diprediksi dari konteks" (x) vs "IDKK aktual" (y), dengan garis 45°. Provinsi di bawah garis artinya lebih baik dari ekspektasi. Klik titik untuk menyorot provinsi itu di peta. |
| Pengalaman juri | "Oh, ternyata ada provinsi yang konteksnya sulit (RLS rendah, agraris) tetapi kualitas kerjanya lebih baik dari perkiraan. Apa yang mereka lakukan?" Ini mengubah dashboard dari *menghakimi* menjadi *belajar*. |
| Contoh insight (H) | 3–5 provinsi menyimpang lebih dari ±1 standar deviasi residual. Mereka jadi kandidat studi kasus kebijakan. |
| RQ | RQ3 (asosiasi pendidikan dan struktur) + rekomendasi |
| Data | `idkk`, `rls`, `share_agri`, `pdrb_kap` → `idkk_pred`, `resid` (dari Python) |
| Cara kerja | OLS robust IDKK ~ RLS + share_agri (maksimal 3 regresor, n=38). Residual distandardisasi. Kategori: lebih baik / sesuai / lebih buruk dari ekspektasi (±1 SD). Uji leave-one-out untuk memastikan status tidak berubah karena satu outlier. |
| Visual | Scatter dengan pita ±1 SD, warna = kategori, label hanya untuk outlier. |
| Power BI | Scatter + garis konstan (Analytics pane) + conditional formatting. |
| Kesulitan / waktu | Sedang · 3 jam (sebagian besar di Python) |
| Risiko | **Paling sensitif secara metodologis.** Residual memuat semua faktor yang tidak diukur (biaya hidup, upah minimum, migrasi), sehingga label "lebih baik" ≠ "kebijakannya lebih baik". Wajib diberi teks: "hasil di luar yang dijelaskan RLS & struktur ekonomi; perlu studi lanjut". Dengan n=38, prediksinya kasar. |
| PDF state | Scatter dengan 3–5 outlier berlabel + satu kalimat insight. |

### F4. Provinsi Kembar

| Aspek | Isi |
|---|---|
| Interaksi | Pilih satu provinsi di slicer. Muncul 3 provinsi yang **konteksnya paling mirip** (RLS, pangsa pertanian, PDRB/kapita). Lalu ditampilkan perbandingan hasilnya (5 komponen IDKK) dalam *bar berpasangan*. |
| Pengalaman juri | "Kalimantan X dan Sulawesi Y mirip secara struktur, tetapi informalitasnya beda 15 poin." Ini langsung memicu pertanyaan kebijakan yang spesifik. |
| Contoh insight (H) | Ada pasangan provinsi dengan konteks hampir sama tetapi outcome berbeda jauh. Di situ ruang kebijakan terlihat. |
| RQ | RQ3–4, decision support |
| Data | Variabel konteks (z-score) → tabel `kembar(prov, kembar, jarak, urutan)` |
| Cara kerja | Jarak Euclidean pada z-score konteks, 3 tetangga terdekat (Python). **Konteks dan outcome dipisah** supaya tidak sirkular. |
| Visual | Kartu provinsi terpilih + 3 kartu kembar + bar komponen + teks "selisih terbesar: informal (+15 poin)". |
| Power BI | Relasi `kembar[prov]` → slicer. Small multiples ([dok](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-small-multiples)). |
| Kesulitan / waktu | Sedang · 3 jam |
| Risiko | Kemiripan bergantung pada pilihan variabel konteks, jadi sebutkan variabelnya. "Kembar" tidak berarti bisa disalin kebijakannya. |
| PDF state | Satu pasangan contoh yang paling kontras (dipilih dari data, bukan dikarang). |

### F5. Pita Ketidakpastian Ranking

| Aspek | Isi |
|---|---|
| Interaksi | Setiap provinsi punya pita horizontal berisi rentang ranking 5–95% dari 1.000 skema bobot acak (Dirichlet) dan titik median. Bisa diurutkan. |
| Pengalaman juri | "Provinsi A *pasti* masuk 5 terburuk. Provinsi B bisa peringkat 6 sampai 20, jadi tidak kuat dijadikan prioritas." Juri melihat tim yang paham ketidakpastian. |
| Contoh insight (H) | Hanya sebagian provinsi yang pitanya sempit di zona prioritas. Merekalah "prioritas tangguh". |
| RQ | Robustness RQ2 |
| Data | `rank_p05, rank_med, rank_p95` (Python) |
| Cara kerja | Monte Carlo bobot, lalu kuantil ranking per provinsi. |
| Visual | *Error-bar style* (bar dari p05 ke p95 + titik median), 38 baris, zona prioritas diarsir. |
| Power BI | Bar chart dengan error bars (Analytics pane, Power BI versi terbaru), atau Deneb (FAQ 26 mengizinkan). |
| Kesulitan / waktu | Rendah–sedang · 2 jam |
| Risiko | Ketidakpastian hanya dari bobot, bukan dari sampling error survei. Sebutkan ini. |
| PDF state | Langsung terbaca, karena visual ini statis. |
| Rujukan | Tampilan ketidakpastian membantu keputusan (Fernandes dkk. 2018, [10.1145/3173574.3173718](https://doi.org/10.1145/3173574.3173718)); *hypothetical outcomes* (Kale dkk. 2019, [10.1109/TVCG.2018.2864909](https://doi.org/10.1109/TVCG.2018.2864909)). |

### F6. Dumbbell Paradoks per Jenjang

| Aspek | Isi |
|---|---|
| Interaksi | Untuk setiap jenjang, dua titik: TPT dan proporsi informal (skala persen). Ada slicer tahun. Toggle menambah titik setengah pengangguran. |
| Pengalaman juri | Pembuka halaman 1. Langsung terlihat: SMK punya TPT tertinggi tetapi informalnya rendah, sedangkan SD ke bawah kebalikannya. |
| Insight (fakta, Dok-1 §6) | TPT 2025: SMK 8,63%, ≤SD 2,30%. Informal 2023: SMK 38,97%, SD 77,35%. **Samakan tahunnya sebelum dipakai.** |
| RQ | RQ1 |
| Data | D01, D02, D03 |
| Visual | Dumbbell horizontal, 6 baris jenjang, dua warna. |
| Power BI | Deneb, atau trik line chart + marker (2 seri). |
| Kesulitan / waktu | Rendah · 1,5 jam |
| Risiko | Dua indikator dengan populasi berbeda (angkatan kerja vs pekerja) ditaruh di satu sumbu. Beri label populasi yang jelas. |
| PDF state | Langsung terbaca. |

### F7. Bar Kontribusi Komponen ("Kenapa provinsi ini di sini?")

| Aspek | Isi |
|---|---|
| Interaksi | Stacked bar horizontal per provinsi: panjang total = IDKK, segmen = kontribusi wᵢ·zᵢ. Ikut berubah saat slider F1 digeser. |
| Pengalaman juri | "Dua provinsi skornya sama, tetapi yang satu karena NEET, yang lain karena informal." Dari sini juri paham mengapa rekomendasinya berbeda. |
| RQ | RQ4 → rekomendasi |
| Power BI | Stacked bar dengan 5 measure DAX kontribusi. |
| Kesulitan / waktu | Rendah · 1,5 jam |
| Risiko | Kontribusi bergantung pada normalisasi min-max, karena nilai ekstrem satu provinsi menarik skala. |
| PDF state | 10 provinsi teratas. |

### F8. Penjelajah Tipologi

| Aspek | Isi |
|---|---|
| Interaksi | Legenda klaster berupa tombol. Klik satu klaster: peta menyorot anggotanya, profil radar atau bar z-score muncul, dan panel rekomendasi berganti (bookmark). |
| Pengalaman juri | Dari "angka" langsung ke "apa yang harus dilakukan untuk tipe ini". |
| Data | `cluster` (k-means, divalidasi silhouette dan ARI), profil rata-rata per klaster |
| Power BI | Slicer tombol + bookmark panel rekomendasi ([bookmark](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-bookmarks), [buttons](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-buttons)) |
| Kesulitan / waktu | Rendah · 2 jam |
| Risiko | Nama klaster dibuat setelah melihat profil. Tampilkan silhouette di catatan metode. |
| PDF state | Peta berwarna klaster + 4 kartu ringkas tipe. |

### F9. Distribusi "Di Mana Posisi Provinsi Ini?"

| Aspek | Isi |
|---|---|
| Interaksi | Lima strip plot (satu per komponen) berisi 38 titik abu-abu. Provinsi yang dipilih menyala dan diberi persentil ("lebih buruk dari 85% provinsi"). |
| Pengalaman juri | Konteks distribusi, misalnya "ternyata TPT-nya biasa saja, tetapi NEET-nya ekstrem". |
| Power BI | Scatter dengan sumbu y kategori + conditional color (bisa dibantu jitter dari CSV). |
| Kesulitan / waktu | Sedang · 2 jam |
| Risiko | Tidak tertimbang jumlah penduduk. Sebutkan. |
| PDF state | Default menyorot provinsi outlier dari F3. |

### F10. Narasi Dinamis (pelengkap)

| Aspek | Isi |
|---|---|
| Interaksi | Kotak teks yang **ditulis tim lewat DAX** dan berubah sesuai provinsi atau klaster yang dipilih. Contoh: "Sulawesi X: TPT peringkat 30 dari 38, tetapi defisit kualitas kerja peringkat 4. Penyumbang terbesar: informalitas (62%). Tipe: Rentan Tersembunyi." |
| Kenapa tidak melanggar aturan | Template kalimat dibuat manual, angkanya dari measure. Tidak ada AI. |
| Kesulitan / waktu | Rendah · 1,5 jam |
| PDF state | Narasi untuk kondisi default. |

```DAX
Narasi Provinsi =
VAR p = SELECTEDVALUE(prov[nama_prov], "Indonesia")
RETURN p & ": TPT peringkat " & SELECTEDVALUE(prov[rank_tpt]) & " dari 38, defisit kualitas kerja peringkat "
 & [Rank Dinamis] & ". Penyumbang terbesar: " & [Komponen Dominan] & ". Tipe: " & SELECTEDVALUE(prov[nama_klaster]) & "."
```

**Ide yang tidak masuk 10 besar dan alasannya:**
- **#11 Waterfall dekomposisi.** Nilainya tinggi, tetapi bergantung pada ketersediaan jumlah angkatan kerja per jenjang. Jadikan cadangan pengganti F9 jika datanya ada.
- **#12 Simulator 2030.** Risiko disalahartikan sebagai ramalan.
- **#14 "Tebak Dulu".** Mati di PDF.
- **#15 Heatmap sektor.** Bagus, tetapi hanya untuk 1 tahun. Tetap masuk sebagai visual biasa di halaman 1, bukan fitur interaktif.
- **#16 Moran scatter.** Cukup ditampilkan sebagai satu angka di catatan metode.

---

## 3. Ranking 5 Fitur Paling Potensial

Skala 1–5. Bobot: insight 25%, kebaruan 15%, dampak visual 15%, relevansi penelitian 20%, kelayakan 15%, aha moment 10%.

| Fitur | Insight | Kebaruan | Visual | Relevansi | Kelayakan | Aha | **Skor** |
|---|---|---|---|---|---|---|---|
| **F2 Ranking Terbalik** | 5 | 3 | 5 | 5 | 5 | 5 | **4,70** |
| **F1 Slider Bobot + Stabilitas** | 5 | 4 | 4 | 5 | 4 | 5 | **4,55** |
| **F3 Melampaui Ekspektasi** | 5 | 5 | 4 | 4 | 3 | 5 | **4,35** |
| **F4 Provinsi Kembar** | 4 | 5 | 4 | 4 | 4 | 4 | **4,15** |
| **F5 Pita Ketidakpastian** | 4 | 4 | 3 | 5 | 5 | 3 | **4,10** |
| F6 Dumbbell Paradoks | 4 | 2 | 4 | 5 | 5 | 4 | 4,05 |
| F7 Kontribusi | 4 | 3 | 3 | 4 | 5 | 3 | 3,75 |
| F8 Tipologi | 4 | 2 | 4 | 4 | 5 | 3 | 3,75 |

*F6 tipis di bawah F5 dan tetap dipakai sebagai visual pembuka Halaman 1, bukan sebagai "fitur" interaktif.*

---

## 4. Desain Akhir: Satu Alur Eksplorasi Utuh

**Prinsip:** maksimal 4 fitur interaktif + 2 visual pendukung per halaman. Fitur yang tidak masuk: F4 dan F9 dimasukkan ke dalam satu panel bookmark ("Bandingkan") di halaman 2. Itu tetap 1 halaman (FAQ 36), tetapi **jangan dijadikan default**.

**Alur cerita (Segel & Heer 2010, pola *martini glass*):** narasi terarah di awal → eksplorasi bebas di akhir.

### Halaman 1 — "Pendidikan Menaikkan Kualitas Kerja, Bukan Selalu Menurunkan Pengangguran" *(terarah)*
```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Judul + 1 kalimat pesan                                    [watermark]        │
│ KPI: TPT nasional | TPT SMK | Informal ≤SD vs PT | NEET 15–24                 │
├───────────────────────────────┬──────────────────────────────────────────────┤
│ F6 DUMBBELL PARADOKS          │ Tren TPT per jenjang 2015–2025               │
│ (TPT vs informal per jenjang) │ (sorot SMK/SMA, anotasi COVID & 2016)        │
│ [slicer tahun]                │                                              │
├───────────────────────────────┼──────────────────────────────────────────────┤
│ Setengah pengangguran / jenjang │ Heatmap upah: pendidikan × 17 sektor (2024) │
├───────────────────────────────┴──────────────────────────────────────────────┤
│ Kotak insight (3 temuan) · Definisi & populasi tiap indikator · Sumber BPS   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Halaman 2 — "Di Mana TPT Rendah Menyembunyikan Pekerjaan Buruk?" *(eksplorasi)*
```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Judul · [F2 tombol: TPT | IDKK]  · KPI: Spearman ρ | Stabilitas Top-10 | Moran I │
├──────────────┬──────────────────────────────────┬────────────────────────────┤
│ F1 SLIDER    │ PETA (metrik dari F2, warna/klaster)│ F5 PITA KETIDAKPASTIAN   │
│ 5 bobot      │                                  │ ranking (urut)             │
│ + reset      │                                  │                            │
├──────────────┼──────────────────────────────────┼────────────────────────────┤
│ F2 SLOPE     │ F3 MELAMPAUI EKSPEKTASI (scatter) │ F8 TIPOLOGI → panel        │
│ TPT→IDKK     │                                  │ rekomendasi per klaster    │
├──────────────┴──────────────────────────────────┴────────────────────────────┤
│ F10 Narasi dinamis · [tombol "Bandingkan": bookmark F4 Kembar + F7 Kontribusi] │
│ Catatan metode: normalisasi, bobot, 1.000 simulasi, silhouette, n=38, asosiasi │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Bagaimana fitur saling melengkapi:**

| Langkah juri | Pertanyaan | Fitur |
|---|---|---|
| 1 | "Apakah pendidikan gagal?" | F6: tidak. Kualitas kerja naik meski TPT naik |
| 2 | "Jadi TPT menyesatkan di level wilayah juga?" | F2: ranking terbalik |
| 3 | "Ah, itu karena bobot indeks kalian." | F1 + F5: juri menguji sendiri, dan prioritas tetap stabil |
| 4 | "Lalu apa yang bisa dipelajari?" | F3: provinsi yang melampaui ekspektasi. F4: kembar dengan hasil berbeda |
| 5 | "Apa yang harus dilakukan?" | F8: rekomendasi per tipe + F10 narasi |

**PDF state final:** halaman 2 dicetak dengan bobot sama, toggle di posisi IDKK, provinsi outlier F3 berlabel, dan narasi untuk provinsi paling kontras. Tambahkan label kecil: "Fitur interaktif (slider bobot, provinsi kembar) tersedia di file .pbix."

**Total tambahan waktu:** sekitar 16–20 jam kerja tim. Ini bisa dibagi untuk 3 orang pada 21–22 Nov, **dengan syarat** semua CSV olahan (indeks, Monte Carlo, residual, kembar, klaster) selesai pada 20 Nov.

**Urutan pemotongan jika waktu habis:** F4 → F3 → F5 (pertahankan F2, F1, F6, dan F8).

---

## 5. Daftar File CSV yang Harus Disiapkan dari Python

| File | Kolom | Untuk fitur |
|---|---|---|
| `prov_master.csv` | kode, nama, lat, lon, komponen mentah, z_*, rank_tpt, rank_default, cluster, nama_klaster | F1, F2, F7, F8, F9, F10 |
| `rank_uncertainty.csv` | kode, rank_p05, rank_med, rank_p95 | F5 |
| `deviance.csv` | kode, idkk_pred, resid_std, kategori, stabil_LOO | F3 |
| `kembar.csv` | kode, kode_kembar, jarak, urutan | F4 |
| `edu_trend.csv` | tahun, jenjang, tpt, informal, tsp, is_estimate | F6, tren |
| `wage_sector.csv` | jenjang, sektor, upah | heatmap |

---

## 6. Risiko dan Mitigasi Lintas Fitur

| Risiko | Mitigasi |
|---|---|
| Juri tidak membuka .pbix | PDF state dirancang sebagai cerita lengkap |
| Halaman tooltip atau drillthrough dihitung sebagai halaman tambahan | Tidak memakai drillthrough. Tooltip page dikonfirmasi dulu ke panitia; alternatifnya tooltip standar + bookmark |
| Fitur terlalu banyak sehingga ramai | Maksimal 4 interaksi per halaman; F4/F7 disembunyikan di balik tombol |
| Klaim berlebihan dari F3 | Kalimat wajib soal faktor yang tidak terukur; uji leave-one-out |
| Performa slider lambat | 38 baris saja, jadi ringan |
| Angka belum diverifikasi | Semua contoh angka di dokumen ini berstatus **hipotesis** kecuali yang bertanda fakta (F6) |

---

## 7. Referensi

**Riset visualisasi** (metadata diverifikasi via Crossref):
- Segel, E., & Heer, J. (2010). Narrative Visualization: Telling Stories with Data. *IEEE TVCG*. https://doi.org/10.1109/TVCG.2010.179 (pola *martini glass*, alur desain akhir)
- Shneiderman, B. (1996). The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations. *IEEE Symp. Visual Languages*. https://doi.org/10.1109/VL.1996.545307 (*overview first, zoom and filter, details on demand*, urutan Halaman 2)
- Hullman, J., & Diakopoulos, N. (2011). Visualization Rhetoric: Framing Effects in Narrative Visualization. *IEEE TVCG*. https://doi.org/10.1109/TVCG.2011.255 (kewaspadaan framing pada F2/F3)
- Borkin, M. A., dkk. (2013). What Makes a Visualization Memorable? *IEEE TVCG*. https://doi.org/10.1109/TVCG.2013.234 (judul dan anotasi yang kuat menaikkan daya ingat)
- Kale, A., dkk. (2019). Hypothetical Outcome Plots Help Untrained Observers Judge Trends in Ambiguous Data. *IEEE TVCG*. https://doi.org/10.1109/TVCG.2018.2864909 (F5)
- Fernandes, M., dkk. (2018). Uncertainty Displays Using Quantile Dotplots or CDFs Improve Transit Decision-Making. *CHI*. https://doi.org/10.1145/3173574.3173718 (F5)

**Metodologi** (lihat Dok-1 §21): Rousseeuw (1987), Anselin (1995), OECD/JRC (2008).

**Dokumentasi Power BI** (URL dicek aktif, 18 Nov 2026):
- What-if parameters: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-what-if
- Field parameters: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters
- Bookmarks: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-bookmarks
- Buttons: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-buttons
- Report page tooltips: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-tooltips
- Drillthrough (sengaja **tidak** dipakai): https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough
- Conditional formatting: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-conditional-table-formatting
- Small multiples: https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-small-multiples
