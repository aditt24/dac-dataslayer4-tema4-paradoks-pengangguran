# KONSEP FINAL — DAC Data Slayer 4.0
# Paradoks Pengangguran Rendah
## Pendidikan, Kualitas Pekerjaan, dan Peta Kerentanan Pasar Kerja Indonesia

| | |
|---|---|
| **Tema** | Tema 4, Pendidikan untuk Masa Depan Dunia Kerja |
| **Cakupan** | Nasional (6 jenjang pendidikan + 38 provinsi) → studi kasus **Jawa Tengah** (35 kab/kota) |
| **Platform** | Power BI · 2 halaman · 1900×1100 px · watermark resmi |
| **Pengolahan** | Python (pandas, scipy, statsmodels, scikit-learn) → CSV → Power BI |
| **Deadline** | Senin, 23 November 2026, 23.59 WIB (target kirim pukul 18.00) |
| **Versi** | v4, 19 November 2026 |

> **Label bukti yang dipakai di dokumen ini**
> - **[DATA]** = angka resmi BPS.
> - **[TERUJI]** = hasil analisis yang lolos semua uji ketahanan.
> - **[BERSYARAT]** = berlaku dengan catatan.
> - **[GUGUR]** = tidak lolos uji dan tidak dipakai.
> - **[HIPOTESIS]** = belum diuji.
>
> Semua angka provinsi berasal dari tabel BPS tahun 2025 (tampilan tahun terbaru di bps.go.id). Angka-angka ini **wajib dihitung ulang** dengan data WebAPI BPS (tahun dan periode Agustus yang sama untuk semua indikator) sebelum dipasang di dashboard. Polanya sudah diuji dan diharapkan tidak berubah.

---

## 1. Ringkasan Konsep

### 1.1 Satu kalimat
> **Angka pengangguran yang rendah bisa menyembunyikan pekerjaan yang tidak layak. Pendidikan mengubah bentuk masalah kerja (dari kerja tidak layak menjadi antre kerja layak), tetapi besar kecilnya masalah suatu wilayah lebih terkait dengan struktur ekonominya.**

### 1.2 Ilustrasi sederhana
- **Desa A:** hampir semua orang "bekerja", tetapi serabutan, tanpa kontrak, dan jam kerja kurang. Pengangguran **rendah**, sehingga terlihat baik, padahal bermasalah.
- **Desa B:** banyak lulusan SMK/PT yang masih menunggu pekerjaan layak, tetapi yang sudah bekerja, pekerjaannya baik. Pengangguran **lebih tinggi**, sehingga terlihat buruk, padahal kualitas kerjanya lebih baik.

Dashboard ini membuktikan dengan data BPS bahwa pola Desa A dan Desa B benar-benar terjadi di Indonesia: antarjenjang pendidikan, antarprovinsi, sampai Jawa Tengah.

### 1.3 Temuan utama
1. **[DATA] Paradoks jenjang pendidikan (2025).**
   - Lulusan ≤SD: pengangguran 2,30%, tetapi informal non-pertanian 68,43%.
   - Lulusan SMK: pengangguran **tertinggi (8,63%)**, tetapi informal non-pertanian 35,84% dan setengah pengangguran 6,81%, lebih rendah dari semua jenjang di bawahnya.
2. **[TERUJI] Angka pengangguran tidak berhubungan dengan kualitas kerja.** Korelasi pengangguran dengan Indeks Defisit Kualitas Kerja (IDKK) di 38 provinsi: **ρ = 0,00**. Tanpa provinsi Papua −0,10. Keduanya tidak signifikan.
3. **[TERUJI] Ranking berbalik.**
   - Naik ke zona buruk: **NTB peringkat pengangguran 34 → peringkat defisit kualitas kerja 5**; Sulawesi Barat 36 → 6; NTT 32 → 9.
   - Turun ke zona baik: **Kep. Riau 5 → 36**; DKI Jakarta 7 → 37; Banten 4 → 27; Kaltim 12 → 34.
4. **[TERUJI] Prioritas yang tahan uji.** Maluku, Aceh, dan Maluku Utara masuk 10 provinsi dengan defisit terburuk di **100%** dari 1.000 skema bobot, baik dengan maupun tanpa Papua.
5. **[TERUJI] "Terdidik tetapi tanpa kerja layak".** Aceh, Maluku, Sumatera Barat, Sulawesi Utara, dan Maluku Utara punya rata-rata lama sekolah (RLS) di atas median, tetapi defisit kualitas kerjanya juga di atas median.
6. **[TERUJI] Struktur ekonomi lebih menentukan besarnya defisit daripada pendidikan.** Urbanisasi berkorelasi kuat dengan defisit (ρ parsial −0,69, bertahan di semua sampel). Setelah urbanisasi dikontrol, RLS **tidak** berasosiasi dengan defisit (ρ ≈ 0,07–0,21; tidak signifikan).
7. **[DATA] Paradoks yang sama berlaku di seluruh Jawa Tengah.**
   - Pada 2023, di **35 dari 35 kab/kota**, pengangguran lulusan pendidikan menengah lebih tinggi daripada lulusan pendidikan dasar (Jateng: 8,53% vs 3,49%).
   - Lulusan menengah di **perdesaan** paling banyak menganggur (10,03%).
   - **70% setengah penganggur di Jateng berpendidikan SMP ke bawah.**
   - Kab/kota dengan masalah ganda (pengangguran tinggi **dan** pengeluaran per kapita rendah): **Brebes, Tegal, Pemalang, Cilacap, Banjarnegara**, Purbalingga, Kebumen, Wonosobo, Demak. Di Brebes, pengangguran lulusan menengah mencapai **20,84%**.
8. **[TERUJI] Indeks kerja layak tervalidasi.** IDKK berkorelasi kuat dengan kemiskinan (ρ = 0,67), indikator yang **tidak** dipakai dalam indeks. Angka pengangguran tidak berkorelasi dengan kemiskinan (ρ = −0,22, tidak signifikan). Indeks kita menangkap kesulitan hidup yang nyata, sementara angka pengangguran tidak.

---

## 2. Latar Belakang dan Masalah

1. **Indikator yang dominan.** TPT adalah indikator utama ketenagakerjaan di rilis BPS, media, dan target pembangunan. Masalahnya, TPT hanya membedakan "bekerja" dan "tidak bekerja", tanpa melihat **kualitas** pekerjaannya.
2. **Teori menjelaskan mengapa TPT bisa menyesatkan:**
   - Penduduk berpendidikan dan berpendapatan rendah "tidak mampu menganggur", sehingga langsung masuk pekerjaan tradisional atau informal (Lewis 1954; La Porta & Shleifer 2014).
   - Lulusan terdidik punya harapan upah lebih tinggi dan mengantre pekerjaan formal (Spence 1973).
   - Akibatnya, TPT bisa rendah justru di wilayah yang pekerjaannya paling rentan.
3. **Relevansi Tema 4 (Human Capital).** Keberhasilan pendidikan perlu dinilai dari **kualitas pekerjaan** yang bisa diakses lulusan, bukan hanya dari status bekerja.
4. **Celah penelitian:**
   - Studi pengangguran di Indonesia umumnya memakai TPT sebagai satu-satunya variabel dependen (mis. Koto dkk. 2022).
   - Perdebatan soal keunggulan SMK berbasis data individu belum selesai (Newhouse & Suryadarma 2011; Chen 2009).
   - Uji spasial yang ada hanya untuk TPT (Gustiandza dkk. 2022).
   - **Belum ada pembacaan TPT bersama kualitas kerja dalam satu kerangka**, dari level jenjang sampai kab/kota.

---

## 3. Pertanyaan Penelitian dan Hipotesis

| Kode | Pertanyaan | Hipotesis | Hasil |
|---|---|---|---|
| **RQ1** | Bagaimana pendidikan berkaitan dengan **bentuk** masalah kerja (pengangguran vs kerja tidak layak)? | TPT naik sampai SMK; informal dan setengah pengangguran turun seiring pendidikan | ✅ [DATA] |
| **RQ2** | Apakah TPT mencerminkan kualitas kerja antarprovinsi? | Korelasi TPT dengan defisit kualitas kerja ≈ 0 | ✅ [TERUJI] ρ = 0,00 |
| **RQ3** | Provinsi mana yang tersembunyi atau rentan, dan apakah prioritasnya stabil? | Terbentuk 4 kuadran; ada prioritas tangguh | ✅ [TERUJI] |
| **RQ4** | Apa yang membedakan besarnya defisit: pendidikan wilayah atau struktur ekonomi? | Struktur ekonomi (urbanisasi) > RLS | ✅ [TERUJI] |
| **RQ5** | Bagaimana posisi Jawa Tengah, dan di kab/kota mana masalahnya terkonsentrasi? | Ada konsentrasi di kab/kota tertentu | ✅ [DATA] |

---

## 4. Alur Cerita: Corong Satu Kasus

Kasusnya **satu dari awal sampai akhir**: *"Angka pengangguran bisa menyesatkan dalam menilai hasil pendidikan di pasar kerja."* Setiap langkah menjawab pertanyaan yang muncul dari langkah sebelumnya.

```
LANGKAH 1 ─ JENJANG (nasional)
  Temuan  : ≤SD jarang menganggur tapi 68% informal; SMK paling banyak menganggur tapi lebih formal.
  Makna   : pendidikan mengubah BENTUK masalah kerja.
  Lanjut  : "Apakah pola ini juga terjadi antarwilayah?"
        ▼
LANGKAH 2 ─ 38 PROVINSI
  Temuan  : TPT tidak berhubungan dengan defisit kualitas kerja (ρ = 0,00). NTB 34 → 5, Kepri 5 → 36.
  Makna   : TPT menyesatkan sebagai ukuran pasar kerja.
  Lanjut  : "Kalau begitu, provinsi mana yang rentan, dan seberapa yakin kita?"
        ▼
LANGKAH 3 ─ KUADRAN 4 TIPE + PRIORITAS
  Temuan  : Rentan Tersembunyi (NTB, Sulbar, NTT), Rentan Ganda (Maluku, Aceh), Antrean Kerja Formal (DKI, Kepri),
            Relatif Layak (Bali, DIY). Maluku, Aceh, Malut prioritas di 100% skenario.
  Lanjut  : "Mengapa besarnya masalah berbeda-beda? Karena pendidikan?"
        ▼
LANGKAH 4 ─ PENJELASAN
  Temuan  : besar defisit paling terkait struktur ekonomi (urbanisasi); RLS saja tidak menurunkan defisit.
            Aceh, Maluku, Sumbar = "terdidik tetapi tanpa kerja layak".
  Makna   : pendidikan perlu berjalan bersama penciptaan kerja formal.
  Lanjut  : "Bagaimana dengan daerah kita, Jawa Tengah?"
        ▼
LANGKAH 5 ─ STUDI KASUS JAWA TENGAH (lensa yang sama: pendidikan → bentuk masalah kerja)
  Temuan  : paradoks berlaku di 35/35 kab/kota: TPT pendidikan menengah > dasar (Jateng 8,53 vs 3,49).
            70% setengah penganggur Jateng berpendidikan ≤SMP (pola "asal kerja").
            Kualitas kerja Jateng relatif baik di tingkat nasional (peringkat defisit 30/38), tetapi TPT di atas median provinsi.
  Lanjut  : "Di kab/kota mana masalahnya paling berat?"
        ▼
LANGKAH 6 ─ KAB/KOTA JATENG → REKOMENDASI
  Temuan  : kuadran kab/kota (TPT × pengeluaran per kapita):
            masalah ganda = Brebes, Tegal, Pemalang, Cilacap, Banjarnegara, Purbalingga, Kebumen, Wonosobo, Demak;
            TPT lulusan menengah tertinggi: Brebes 20,8 · Banjarnegara 16,6 · Cilacap 16,2 · Pemalang 12,9.
  Aksi    : rekomendasi per kuadran + prioritas kab/kota Jateng.
```

**Kenapa alurnya tidak melompat:** Jawa Tengah bukan topik baru. Jateng adalah penerapan lensa yang sama (pengangguran vs kualitas kerja) pada wilayah panitia. Jateng juga memperlihatkan **sisi lain paradoks**: pengangguran yang lebih tinggi tidak selalu berarti pekerjaan yang lebih buruk.

---

## 5. Kerangka Teori

| Teori | Prediksi | Diuji dengan |
|---|---|---|
| Human Capital (Psacharopoulos & Patrinos 2018) | Pendidikan → akses kerja formal dan produktif | Informal, setengah pengangguran per jenjang |
| Signaling / Job Search (Spence 1973) | Lulusan terdidik mengantre kerja formal → TPT lebih tinggi | TPT per jenjang; RLS vs TPT |
| Dualisme Lewis (1954) | Tenaga berpendidikan rendah diserap sektor tradisional → TPT rendah, informal tinggi | Kuadran "Rentan Tersembunyi" |
| Informality & Development (La Porta & Shleifer 2014; Maloney 2004) | Informalitas turun seiring pembangunan dan urbanisasi; informal ≠ otomatis miskin | Urbanisasi vs defisit |
| Disparitas regional (Elhorst 2003) | Perbedaan antarwilayah dipengaruhi struktur ekonomi | Kuadran, kab/kota |
| Decent Work (ILO) | Kualitas kerja multidimensi | IDKK |

```
LEVEL INDIVIDU (jenjang)                  LEVEL WILAYAH (provinsi / kab-kota)
Pendidikan ─► BENTUK masalah kerja         Struktur ekonomi (urbanisasi) ─► BESARNYA defisit kualitas kerja
 rendah: bekerja tapi tidak layak          Pendidikan wilayah (RLS) ─► TPT (+, antrean)
 tinggi: antre kerja layak (TPT↑)          RLS ─► defisit: tidak signifikan setelah urbanisasi dikontrol
                 └──────────────► Kebijakan: pendidikan + penciptaan kerja formal ◄──────────────┘
```

---

## 6. Keputusan Desain dan Alasannya

| Keputusan | Pilihan | Alasan |
|---|---|---|
| **Cakupan** | Nasional sebagai inti → Jawa Tengah sebagai studi kasus | Paradoks hanya bisa dibuktikan dengan membandingkan wilayah. Di level kab/kota tidak tersedia data informal dan NEET, sehingga indeks kerja layak hanya bisa dibangun di level provinsi. BPS Jateng menyediakan **TPT kab/kota × tingkat pendidikan (2019–2023)**, sehingga Jateng bisa dianalisis dengan **lensa yang sama** (pendidikan → bentuk masalah kerja) sebagai ujung alur. FAQ 17 menegaskan Jateng **tidak wajib**; banyak tim memakai Jateng, jadi kerangka nasional menjadi pembeda |
| **Indeks kualitas kerja** | IDKK **3 komponen**: setengah pengangguran, pekerja informal, NEET 15–24 | **TPT dikeluarkan** agar konsisten dengan pesan "TPT menyesatkan" (TPT ditampilkan sebagai sumbu tersendiri). **Upah dikeluarkan** karena terbukti bias seleksi (hanya buruh/karyawan; di Papua Pegunungan "tinggi" karena didominasi segelintir pegawai formal) |
| **Pengelompokan** | **Kuadran 2×2**: TPT × IDKK (batas = median provinsi) | Langsung memvisualkan paradoks, transparan, dan mudah dijelaskan. Klaster k-means sebelumnya lemah (silhouette 0,27). K-means dipakai sebagai pembanding (ARI 0,74) |
| **Unit klaim** | Klaim individu hanya dari data jenjang; klaim wilayah hanya dari data provinsi/kab-kota | Menghindari *ecological fallacy* |
| **Bahasa** | Asosiatif ("berkaitan", "berasosiasi"), tidak kausal | Data agregat, tanpa desain kausal |
| **Klaim yang dibuang** | "Provinsi lebih terdidik → lebih formal" | **[GUGUR]**: setelah urbanisasi dikontrol dan Papua dikeluarkan, ρ = −0,08 (tidak signifikan) |
| **Target kebijakan** | Tidak memakai angka karangan | Acuan diambil dari data (laju perbaikan provinsi setipe pada data panel) |

---

## 7. Dataset

### 7.1 Katalog BPS (terverifikasi ada, 19 Nov 2026)
| Kode | Tabel BPS | var_id | Tahun | Unit | Link |
|---|---|---|---|---|---|
| D01 | Tingkat Pengangguran Terbuka Berdasarkan Tingkat Pendidikan | 1179 | 2015–2025 | 6 jenjang | [link](https://www.bps.go.id/id/statistics-table/2/MTE3OSMy/tingkat-pengangguran-terbuka-berdasarkan-tingkat-pendidikan.html) |
| D02 | Proporsi Lapangan Kerja Informal Menurut Tingkat Pendidikan | 2157 | 2018–2023 | 8 jenjang | [link](https://www.bps.go.id/id/statistics-table/2/MjE1NyMy/proporsi-lapangan-kerja-informal-menurut-tingkat-pendidikan.html) |
| D02b | Proporsi Lapangan Kerja Informal Sektor Non-Pertanian Menurut Tingkat Pendidikan | 1166 | 2015–2025 | 6 jenjang | [link](https://www.bps.go.id/id/statistics-table/2/MTE2NiMy/proporsi-lapangan-kerja-informal-sektor-non-pertanian-menurut-tingkat-pendidikan.html) |
| D03 | Tingkat Setengah Pengangguran Menurut Tingkat Pendidikan | 1184 | 2015–2025 | 6 jenjang | [link](https://www.bps.go.id/id/statistics-table/2/MTE4NCMy/tingkat-setengah-pengangguran-menurut-tingkat-pendidikan.html) |
| D03b | Tingkat Setengah Pengangguran Menurut Provinsi | 1181 | 2015–2025 | 38 prov | [link](https://www.bps.go.id/id/statistics-table/2/MTE4MSMy/tingkat-setengah-pengangguran-menurut-provinsi.html) |
| D04 | TPT Berdasarkan Kelompok Umur | 1180 | 2015–2025 | 11 kelompok | [link](https://www.bps.go.id/id/statistics-table/2/MTE4MCMy/tingkat-pengangguran-terbuka-berdasarkan-kelompok-umur.html) |
| D05 | Tingkat Pengangguran Terbuka Menurut Provinsi | 543 | 1986–2026 | 38 prov | [link](https://www.bps.go.id/id/statistics-table/2/NTQzIzI=/tingkat-pengangguran-terbuka-menurut-provinsi.html) |
| D06b | Angkatan Kerja menurut Provinsi (ukuran titik/bobot) | — | cek | 38 prov | [link](https://www.bps.go.id/id/statistics-table/2/MjM5NCMy/angkatan-kerja-ak-menurut-provinsi.html) |
| D07 | Proporsi Lapangan Kerja Informal Menurut Provinsi | 2153 | 2018–2025 | 38 prov | [link](https://www.bps.go.id/id/statistics-table/2/MjE1MyMy/proporsi-lapangan-kerja-informal-menurut-provinsi.html) |
| D14 | Penduduk Bekerja menurut Lapangan Usaha (17 Sektor) dan Pendidikan | 1971 | 2018–2025 | sektor × jenjang | [link](https://www.bps.go.id/id/statistics-table/2/MTk3MSMy/penduduk-berumur-15-tahun-ke-atas-yang-bekerja-selama-seminggu-yang-lalu-menurut-lapangan-usaha-17-sektor-dan-pendidikan-tertinggi-yang-ditamatkan.html) |
| D15 | Persentase Usia Muda (15–24) Tidak Sekolah, Bekerja, atau Pelatihan (NEET) | 1186 | 2015–2025 | 38 prov | [link](https://www.bps.go.id/id/statistics-table/2/MTE4NiMy/persentase-usia-muda-15-24-tahun-yang-sedang-tidak-sekolah-bekerja-atau-mengikuti-pelatihan.html) |
| D18 | Rata-Rata Lama Sekolah 15+ Menurut Provinsi | 1429 | 2015–2025 | 38 prov | [link](https://www.bps.go.id/id/statistics-table/2/MTQyOSMy/rata-rata-lama-sekolah-penduduk-umur-15-tahun-ke-atas-menurut-provinsi.html) |
| D25 | Persentase Penduduk Miskin (P0) Menurut Provinsi dan Daerah | 192 | 2007–2026 | 38 prov | [link](https://www.bps.go.id/id/statistics-table/2/MTkyIzI=/persentase-penduduk-miskin-p0-menurut-provinsi-dan-daerah.html) |
| U01 | Persentase Penduduk Daerah Perkotaan Hasil Proyeksi menurut Provinsi 2015–2035 | — | proyeksi 2025 | 34 prov | [link](https://www.bps.go.id/id/statistics-table/1/MTI3NiMx/persentase-penduduk-daerah-perkotaan-hasil-proyeksi-penduduk-menurut-provinsi-2015---2035.html) |
| K01 | TPT menurut Jenis Kelamin dan Kabupaten/Kota | 2824 | 2017–2025 | 514 kab/kota | [link](https://www.bps.go.id/id/statistics-table/2/MjgyNCMy/tingkat-pengangguran-terbuka-menurut-jenis-kelamin-dan-kabupaten-kota.html) |
| J01 | TPT Menurut Kabupaten/Kota di Provinsi Jawa Tengah | — | 2007–2025 | 35 kab/kota | [link](https://jateng.bps.go.id/id/statistics-table/2/NjQjMg==/tingkat-pengangguran-terbuka--tpt--menurut-kabupaten-kota-di-provinsi-jawa-tengah.html) |
| J02 | [Indikator Strategis IPM] RLS menurut Kab/Kota di Jawa Tengah | — | 2020–2026 | 35 kab/kota | [link](https://jateng.bps.go.id/id/statistics-table/2/MjQxNCMy/-indikator-strategis---ipm--rata-rata-lama-sekolah--menurut-kabupaten-kota-di-provinsi-jawa-tengah.html) |
| **J03** | **TPT Menurut Kabupaten/Kota dan Tingkat Pendidikan di Provinsi Jawa Tengah** (dasar / menengah / tinggi) | — | **2019–2023** | 35 kab/kota | [link](https://jateng.bps.go.id/id/statistics-table/2/MTg2NCMy/tingkat-pengangguran-terbuka-menurut-kabupaten-kota-dan-tingkat-pendidikan-di-provinsi-jawa-tengah.html) |
| J04 | Rata-Rata Pengeluaran per Kapita per Bulan Menurut Kab/Kota Jawa Tengah | — | 2021–2025 | 35 kab/kota | [link](https://jateng.bps.go.id/id/statistics-table/2/NDQ4MiMy/rata-rata-pengeluaran-per-kapita-per-bulan-menurut-kabupaten-kota-provinsi-jawa-tengah.html) |
| J07 | TPT Menurut Kabupaten/Kota dan Jenis Kelamin di Jawa Tengah | — | 2019–2023 | 35 kab/kota | [link](https://jateng.bps.go.id/id/statistics-table/2/MTg2MiMy/tingkat-pengangguran-terbuka-menurut-kabupaten-kota-dan-jenis-kelamin-di-provinsi-jawa-tengah.html) |
| J08 | TPT Menurut Tingkat Pendidikan di Jawa Tengah (× jenis kelamin, × kota/desa) | — | 2019–2023 | 4 jenjang | [link](https://jateng.bps.go.id/id/statistics-table/2/MTgyOCMy/tingkat-pengangguran-terbuka-menurut-tingkat-pendidikan-di-provinsi-jawa-tengah.html) |
| J09 | Distribusi Setengah Penganggur menurut Tingkat Pendidikan dan Daerah di Jawa Tengah | — | 2019–2023 | 6 jenjang | [link](https://jateng.bps.go.id/id/statistics-table/2/MjM0MiMy/distribusi-setengah-penganggur-menurut-tingkat-pendidikan-yang-ditamatkan-dan-daerah-tempat-tinggal.html) |

*Catatan audit:* tabel Jateng "TPT menurut Klasifikasi Wilayah dan Tingkat Pendidikan" (MjI5NyMy) **tidak konsisten** dengan tabel J08 (label kota/desa tampak tertukar), sehingga **tidak dipakai**. Data kab/kota Jateng × pendidikan hanya sampai **2023**, jadi analisis Jateng memakai tahun 2023 (TPT total kab/kota tersedia sampai 2025).

**Tabel pendukung opsional:** D08 informal non-pertanian per provinsi (2015–2024), D10 tenaga kerja formal per provinsi, D11 upah per jam per provinsi (konteks saja), D16 NEET per jenis kelamin, D17 TPT per disabilitas, D06 TPAK per provinsi.

**Publikasi:**
- [Keadaan Angkatan Kerja Agustus 2025](https://www.bps.go.id/id/publication/2025/12/19/42a75ee61332755586fdfcdd/keadaan-angkatan-kerja-di-indonesia-agustus-2025.html)
- [Keadaan Angkatan Kerja Provinsi Jawa Tengah Agustus 2025](https://jateng.bps.go.id/id/publication/2026/04/15/846da24bda153c43f5cb0330/keadaan-angkatan-kerja-provinsi-jawa-tengah-agustus-2025.html), untuk mengecek apakah ada data informal/setengah pengangguran per kab/kota Jateng
- [Direktori SUPAS 2025](https://direktori.web.bps.go.id/supas2025), untuk mencari % perkotaan 38 provinsi yang menggantikan proyeksi lama

### 7.2 Data spasial (hanya untuk visual)
- **Default: tile map buatan tim.** Setiap provinsi digambar sebagai kotak berukuran sama, sehingga tidak bias luas wilayah dan tidak butuh file eksternal.
- **Peta kab/kota Jawa Tengah:** peta bawaan Power BI (geocoding nama kab/kota) atau tile map 35 kotak.
- Poligon non-BPS (BIG, GADM) **hanya dipakai jika panitia mengizinkan**. geoBoundaries **tidak dipakai** karena versi 2017 dengan 34 provinsi.

### 7.3 Struktur dataset final (`Processed_Dataset/`)
| File | Grain | Kolom |
|---|---|---|
| `edu_trend.csv` | jenjang × tahun | tahun, jenjang, tpt, informal_nonag, setengah_peng, is_estimate |
| `edu_sector_2025.csv` | sektor × jenjang | sektor, jenjang, share_pekerja |
| `prov_master.csv` | provinsi (2025) | kode, nama, tpt, tsp, informal, neet, rls, urban, miskin, ak, idkk3, rank_tpt, rank_idkk3, geser, rank_p05/med/p95, prob_top10, kuadran, stabilitas_kuadran, dekat_batas, terdidik_tanpa_kerja_layak, flag_subsisten |
| `prov_panel.csv` | provinsi × tahun (2018–2025) | kolom komponen untuk panah perubahan |
| `jateng_kabkota.csv` | kab/kota Jateng | nama, tpt, tpt_l, tpt_p, is_kota, rls (+ indikator lain jika ada) |
| `uji_ketahanan.csv` | hubungan × sampel | rho, p, n, kontrol |
| `metadata_sumber.csv` | indikator | tabel, var_id, URL, populasi, satuan |

Versi awal dari semua file ini sudah ada di `Processed_Dataset/v4/` (hasil `scripts/analisis_final_v4.py`).

---

## 8. Metodologi

| Langkah | Metode | Rumus / detail | Validasi |
|---|---|---|---|
| Gradien jenjang | Deskriptif + tren | Perbandingan TPT, informal non-pertanian, dan setengah pengangguran per jenjang | Cocokkan dengan rilis BPS |
| Indeks | **IDKK3** | `z = (x − min)/(max − min)` untuk setengah pengangguran, informal, NEET; `IDKK3 = 100 × rata-rata(z)` | Varian z-score, tanpa tiap komponen |
| Uji paradoks | Spearman | ρ(TPT, IDKK3) | Tanpa Papua; tanpa 5 provinsi dengan urbanisasi dari provinsi induk |
| Kuadran | Batas median | TPT ≥ 4,21 → tinggi; IDKK3 ≥ 48,44 → tinggi | Bootstrap median 500× (stabilitas kuadran); pembanding k-means |
| Prioritas | Monte Carlo | 1.000 bobot `w ~ Dirichlet(1,1,1)` → ranking → P(masuk 10 terburuk) | Ulang tanpa Papua |
| Penjelasan | Korelasi parsial Spearman | RLS vs IDKK3 dikontrol urbanisasi; urbanisasi vs IDKK3 dikontrol RLS | Tiga sampel |
| Terdidik tanpa kerja layak | Aturan | RLS ≥ median dan IDKK3 ≥ median | — |
| Ekspektasi | OLS | Informal ~ RLS + urbanisasi → residual terstandar | Leave-one-out |
| Jenjang × sektor | Komposisi | % pekerja tiap jenjang per sektor (Agustus 2025) | — |
| Jateng | Deskriptif kab/kota | TPT total, laki-laki, perempuan; kota vs kabupaten | Tidak meranking selisih kecil (galat sampling) |

**Aturan pencilan:** pencilan tidak dibuang. Metode berbasis ranking dipakai, dan provinsi dengan informal >80% serta RLS <7 diberi **flag "Ekonomi Subsisten"** (Papua Pegunungan, Papua Tengah).

---

## 9. Hasil Analisis

### 9.1 Langkah 1: Paradoks jenjang 2025 [DATA]
| Jenjang | TPT | Informal non-pertanian | Setengah pengangguran |
|---|---|---|---|
| ≤SD | 2,30 | 68,43 | 8,81 |
| SMP | 3,80 | 60,10 | 8,58 |
| SMA umum | 6,88 | 43,75 | 8,34 |
| **SMK** | **8,63** | **35,84** | **6,81** |
| Diploma | 4,31 | 25,63 | 4,58 |
| Universitas | 5,39 | 16,63 | 5,29 |

**Ke mana lulusan bekerja (% pekerja tiap jenjang, Agustus 2025) [DATA]:**

| Sektor | SD | SMP | SMA | **SMK** | Diploma | Universitas |
|---|---|---|---|---|---|---|
| Pertanian | **44,8** | 29,0 | 18,5 | 10,6 | 6,1 | 4,3 |
| Perdagangan | 15,2 | 20,4 | 23,5 | **25,7** | 17,2 | 12,4 |
| Industri Pengolahan | 12,5 | 16,0 | 15,0 | **22,3** | 10,7 | 6,2 |
| Jasa Pendidikan | 0,4 | 0,8 | 3,4 | 1,8 | 6,2 | **34,1** |

**Bacaan:**
- Hampir separuh lulusan SD bekerja di pertanian (sektor yang identik dengan pekerjaan informal).
- **Lulusan SMK paling bergantung pada industri dan perdagangan** (48% gabungan). Karena itu antrean SMK berkaitan dengan daya serap kedua sektor ini.
- Sepertiga lulusan universitas terserap di **jasa pendidikan**, menunjukkan daya serap PT yang sempit.

### 9.2 Langkah 2: TPT vs kualitas kerja [TERUJI]
| Uji | 38 provinsi | Tanpa Papua (32) | Tanpa 5 prov. urban-induk (33) |
|---|---|---|---|
| ρ(TPT, IDKK3) | **0,00** (p = 0,98) | −0,10 (p = 0,57) | −0,09 (p = 0,62) |
| ρ(TPT, informal) | −0,45 (p = 0,005) | −0,39 (p = 0,03) | −0,41 (p = 0,02) |
| ρ(TPT, setengah peng.) | 0,01 | −0,05 | −0,06 |

**Pergeseran ranking terbesar (1 = terburuk):**

| Naik ke zona buruk (TPT → IDKK3) | Turun ke zona baik |
|---|---|
| Sulbar 36 → 6 (+30) · NTB 34 → 5 (+29) · Papua Tengah 28 → 1 · NTT 32 → 9 · Bengkulu, Sulteng, Papua Pegunungan (+17) | Kep. Riau 5 → 36 (−31) · DKI 7 → 37 (−30) · Banten 4 → 27 (−23) · Kaltim 12 → 34 (−22) · **Jateng 14 → 30 (−16)** |

### 9.3 Langkah 3: Kuadran dan prioritas [TERUJI]
Batas kuadran: median TPT 4,21% dan median IDKK3 48,44.

| Kuadran | n | TPT | Setengah peng. | Informal | NEET | RLS | Urbanisasi | Anggota |
|---|---|---|---|---|---|---|---|---|
| **Rentan Tersembunyi** (TPT rendah, defisit tinggi) | 9 | 3,37 | 10,40 | 68,0 | 20,0 | 8,77 | 36,3 | **NTB, Sulbar, NTT**, Sumsel, Bengkulu, Sulteng, Gorontalo, Papua Selatan, Papua Tengah* |
| **Rentan Ganda** (TPT tinggi, defisit tinggi) | 10 | 5,74 | 9,98 | 60,5 | **24,6** | 10,06 | 44,7 | **Maluku, Aceh**, Malut, Sumbar, Sulut, Jabar, Lampung, Papua, Papua Barat, Papua Barat Daya |
| **Antrean Kerja Formal** (TPT tinggi, defisit rendah) | 10 | 5,21 | 6,96 | 50,1 | 18,2 | 9,77 | **62,8** | **DKI, Kepri**, Banten, Kaltim, **Jateng**, Sumut, Jambi, Babel, Kalbar, Sulsel |
| **Relatif Layak** (TPT rendah, defisit rendah) | 9 | 3,33 | 6,14 | 58,5 | 15,9 | 9,13 | 54,8 | **Bali, DIY**, Jatim, Kalteng, Kalsel, Kaltara, Riau, Sultra, Papua Pegunungan* |

\* Flag **Ekonomi Subsisten**: indikator Sakernas kurang sensitif di wilayah ini. Papua Pegunungan (informal 95%, RLS 4,8) **tidak boleh dibaca sebagai "Relatif Layak"**.

- **Dekat batas kuadran** (stabilitas bootstrap <0,6): Lampung, Jambi, Sulsel, Papua Selatan, Papua Pegunungan. Ditandai di visual, dan rekomendasinya bersifat campuran.
- **Kesesuaian dengan k-means:** ARI 0,74.

**Prioritas tangguh (P masuk 10 terburuk dari 1.000 bobot):**

| Provinsi | Semua 38 | Tanpa Papua | Rentang ranking 5–95% |
|---|---|---|---|
| Maluku | 1,00 | 1,00 | 1–6 |
| Aceh | 1,00 | 1,00 | 2–7 |
| Maluku Utara | 1,00 | 1,00 | 3–9 |
| Papua Tengah | 0,98 | — | 1–7 |
| Papua Barat | 0,85 | — | 6–12 |
| Sulawesi Barat | 0,79 | 0,98 | 3–15 |
| NTB | 0,75 | 0,88 | 2–26 |
| NTT | 0,67 | 0,89 | 5–24 |

### 9.4 Langkah 4: Mengapa besarnya defisit berbeda? [TERUJI]
| Hubungan | 38 provinsi | Tanpa Papua | Tanpa 5 prov. urban-induk |
|---|---|---|---|
| Urbanisasi ~ IDKK3 | −0,67 | −0,73 | −0,71 |
| Urbanisasi ~ IDKK3 \| RLS | **−0,69** | **−0,69** | **−0,69** |
| RLS ~ IDKK3 | −0,15 (ns) | −0,23 (ns) | −0,17 (ns) |
| RLS ~ IDKK3 \| urbanisasi | 0,21 (ns) | 0,08 (ns) | 0,07 (ns) |
| RLS ~ TPT \| urbanisasi | **+0,46** | +0,30 (p = 0,09) | **+0,42** |

**Interpretasi:**
- Di level wilayah, besarnya defisit kualitas kerja paling kuat berkaitan dengan **struktur ekonomi** (urbanisasi/non-agraris).
- Rata-rata lama sekolah saja **tidak** berkaitan dengan defisit yang lebih rendah, tetapi berkaitan dengan **TPT yang lebih tinggi** (antrean).
- **Terdidik tetapi tanpa kerja layak** (RLS ≥ median dan IDKK3 ≥ median): Aceh, Maluku, Sumbar, Sulut, Malut, Bengkulu, Papua Barat, Papua Barat Daya, Papua.
- Sumbar (+1,8 SD), Maluku (+1,9), dan Aceh (+1,2) punya pekerja informal **di atas ekspektasi** dari pendidikan dan urbanisasinya.

### 9.5 Langkah 5–6: Jawa Tengah [DATA/TERUJI]
| Indikator | Jawa Tengah | Median provinsi | Nasional |
|---|---|---|---|
| TPT | **4,66** | 4,21 | 4,85 |
| Setengah pengangguran | 7,00 | 7,99 | 7,91 |
| Informal | 58,79 | 59,62 | 57,80 |
| NEET | 16,67 | 19,33 | 19,44 |
| RLS | 8,62 | 9,57 | 9,41 |
| Ranking TPT → IDKK3 | **14 → 30** | — | — |
| Kuadran | **Antrean Kerja Formal**, tetapi **dekat batas**: dengan garis batas TPT nasional (4,85), Jateng masuk Relatif Layak | — | — |

**Bacaan Jateng di tingkat nasional:**
- Kualitas kerja Jateng relatif lebih baik dari mayoritas provinsi (setengah pengangguran dan NEET di bawah median).
- TPT Jateng di atas median provinsi, tetapi di bawah angka nasional. Karena posisi kuadrannya sensitif terhadap garis batas, **narasi Jateng tidak bertumpu pada label kuadran provinsi**, melainkan pada analisis di dalam Jateng (di bawah).

**Paradoks di dalam Jawa Tengah (lensa yang sama dengan nasional) [DATA]:**

| Tingkat pendidikan (Jateng 2023) | TPT | TPT perkotaan | TPT perdesaan | Porsi dari seluruh setengah penganggur |
|---|---|---|---|---|
| Dasar ke bawah | 3,49 | 3,95 | 3,11 | **70,4%** (≤SD 49,1% + SMP 21,4%) |
| **Menengah (SMA+SMK)** | **8,53** | 7,67 | **10,03** | 24,8% |
| Tinggi | 5,49 | 5,64 | 5,02 | 4,8% |

- **Di 35 dari 35 kab/kota, TPT lulusan menengah > lulusan dasar.** Median kab/kota: dasar 2,90 · menengah 7,13 · tinggi 5,63.
- Pola "Desa A" (asal kerja, tidak layak) terlihat jelas: **7 dari 10 setengah penganggur Jateng berpendidikan SMP ke bawah.**
- Pola "Desa B" (antre) terlihat jelas: lulusan menengah **di perdesaan** paling banyak menganggur (10,03%). Ini mengindikasikan minimnya pekerjaan formal di desa untuk lulusan SMA/SMK.

**Kuadran kab/kota Jateng (TPT 2025 × pengeluaran per kapita 2025; batas = median):**

| Kuadran | Kab/kota |
|---|---|
| **Masalah ganda** (TPT tinggi, pengeluaran rendah) | **Brebes, Tegal, Pemalang, Cilacap, Banjarnegara**, Purbalingga, Kebumen, Wonosobo, Demak |
| **Tersembunyi** (TPT rendah, pengeluaran rendah) | Purworejo, Magelang, Wonogiri, Grobogan, Blora, Rembang, Jepara, Temanggung |
| **Antrean di wilayah maju** (TPT tinggi, pengeluaran tinggi) | Kota Semarang, Kota Surakarta, Kota Magelang, Kota Pekalongan, Kota Tegal, Banyumas, Sukoharjo, Kendal, Batang |
| **Relatif baik** (TPT rendah, pengeluaran tinggi) | Boyolali, Klaten, Karanganyar, Sragen, Pati, Kudus, Kab. Semarang, Kab. Pekalongan, Kota Salatiga |

- **TPT tidak berkorelasi dengan pengeluaran per kapita** di kab/kota Jateng (ρ = −0,02). Temuan nasional ("TPT tidak mencerminkan kesejahteraan atau kualitas kerja") terulang di level lokal.
- **TPT lulusan menengah tertinggi:** Brebes 20,84 · Banjarnegara 16,61 · Cilacap 16,19 · Pemalang 12,94 · Kab. Tegal 11,92 · Banyumas 11,11.
- *Catatan:* pengeluaran per kapita adalah proksi kesejahteraan, **bukan** ukuran kualitas kerja. Data informal per kab/kota tidak tersedia, jadi labelnya ditulis jujur.

**35 kab/kota Jateng (TPT 2025):**
- Median 3,99.
- **Brebes 8,07** (laki-laki 10,01), **Tegal 7,61**, **Cilacap 7,40** (perempuan 9,07), **Pemalang 6,61**, **Banyumas 6,26**, Kota Tegal 5,82, Kota Semarang 5,65, Banjarnegara 5,39 (perempuan 7,56).
- Terendah: Wonogiri 2,16, Temanggung 2,31, Rembang 2,90.
- Kota 4,80 vs kabupaten 4,34 (selisih kecil).
- **Pola:** konsentrasi di **koridor pantura barat (Brebes, Tegal, Pemalang) dan barat daya (Cilacap, Banyumas)**. Di Brebes, Pemalang, dan Kota Tegal, TPT laki-laki sangat tinggi; di Cilacap dan Banjarnegara, TPT perempuan yang tinggi.

### 9.6 Validasi indeks dan batas kuadran [TERUJI]
- **Validasi konvergen:** IDKK3 ~ kemiskinan ρ = **0,67** (tanpa Papua 0,68). TPT ~ kemiskinan ρ = −0,22 (tidak signifikan). Indeks menangkap kesulitan hidup, sementara TPT tidak.
- **Batas kuadran:**
  - Dengan batas rata-rata, 84% provinsi tetap di kuadran yang sama.
  - Dengan batas TPT nasional (4,85), 79% tetap.
  - **Maluku, Aceh (Rentan Ganda), NTB, Sulbar (Rentan Tersembunyi), dan DKI (Antrean) tidak berubah di semua batas.**
  - Yang berubah (provinsi dekat batas): Jambi, Lampung, Babel, Sulsel, Sultra, Kalbar, Maluku Utara, Papua Barat, **Jawa Tengah**.
  - Provinsi dekat batas ditampilkan dengan tanda khusus dan **tidak dijadikan contoh utama narasi**.

---

## 10. Insight Final (judul visual)

| # | Insight | Status | Visual |
|---|---|---|---|
| H1 | "SMK: pengangguran tertinggi, tetapi kerja paling formal di jenjang menengah" | [DATA] | Dumbbell jenjang |
| H2 | "SMK bergantung pada industri & perdagangan; sepertiga sarjana terserap di jasa pendidikan" | [DATA] | Heatmap jenjang × sektor |
| H3 | "Angka pengangguran tidak mencerminkan kualitas kerja (ρ = 0,00 di 38 provinsi)" | [TERUJI] | KPI + tombol ranking terbalik |
| H4 | "NTB & Sulbar: pengangguran rendah, kualitas kerja terburuk (peringkat 34 → 5, 36 → 6)" | [TERUJI] | Slope chart |
| H5 | "Maluku, Aceh, Maluku Utara: prioritas di 100% skenario" | [TERUJI] | Pita ketidakpastian |
| H6 | "Terdidik tetapi tanpa kerja layak: Aceh, Maluku, Sumbar" | [TERUJI] | Scatter RLS × IDKK3 |
| H7 | "Struktur ekonomi, bukan rata-rata lama sekolah, yang paling membedakan besarnya defisit" | [TERUJI] | Scatter urbanisasi × IDKK3 (warna = RLS) |
| H8 | "Di 35 dari 35 kab/kota Jateng, lulusan menengah lebih banyak menganggur daripada lulusan dasar; 70% setengah penganggur berpendidikan ≤SMP" | [DATA] | Dumbbell kab/kota Jateng (dasar vs menengah) |
| H9 | "Masalah ganda (TPT tinggi + pengeluaran rendah): Brebes, Tegal, Pemalang, Cilacap, Banjarnegara; TPT lulusan menengah Brebes 20,8%" | [DATA] | Kuadran kab/kota Jateng |
| H9b | "Indeks kerja layak berkorelasi dengan kemiskinan (0,67); TPT tidak (−0,22)" | [TERUJI] | KPI validasi di catatan metode |
| H10 | Tren 2018–2025: provinsi mana yang membaik? | [HIPOTESIS] | Panah 2018 → 2025 |

---

## 11. Rekomendasi Kebijakan

| Sasaran | Temuan dasar | Intervensi | Indikator BPS pemantau | Acuan |
|---|---|---|---|---|
| **Rentan Tersembunyi** (NTB, Sulbar, NTT, dll.) | TPT rendah, informal 68% dan setengah pengangguran 10,4% | Hilirisasi pertanian dan agroindustri; formalisasi usaha mikro (NIB, kredit); jaminan sosial pekerja informal; pelatihan nonformal berbasis komoditas | Informal, setengah pengangguran | Laju perbaikan tercepat di kuadran yang sama (2018–2025) |
| **Rentan Ganda** (Maluku, Aceh, Malut, Sumbar, dll.) | Terdidik tetapi tanpa kerja layak; NEET 24,6% | Investasi padat karya formal; *job matching*; magang industri; program NEET *second chance*; pusat karier sekolah dan kampus | NEET, TPT 15–24, informal | Idem |
| **Antrean Kerja Formal** (DKI, Kepri, Banten, Jateng, dll.) | TPT tinggi, kualitas kerja relatif baik | Percepat penyerapan: bursa kerja daerah, kemitraan kawasan industri, penyelarasan jurusan SMK dengan industri dan perdagangan lokal | TPT, TPT SMK, TPT 15–24 | Idem |
| **Relatif Layak** (Bali, DIY, Kalimantan) | Kedua indikator baik | Dijadikan rujukan praktik baik | — | — |
| **Flag Subsisten** (Papua Pegunungan, Papua Tengah) | Informal >80%, RLS <7 | Pendidikan dasar–menengah afirmatif; layanan kerja berbasis kampung; usulan indikator kerentanan khusus | RLS, informal | Laju kenaikan RLS |
| **Jawa Tengah: masalah ganda** (Brebes, Tegal, Pemalang, Cilacap, Banjarnegara, Purbalingga, Kebumen, Wonosobo, Demak) | TPT tinggi (lulusan menengah hingga 20,8%) + pengeluaran per kapita rendah; lulusan menengah di desa paling banyak menganggur | Penciptaan kerja formal di perdesaan (agroindustri, kemitraan SMK–industri koridor pantura dan selatan), bursa kerja kab/kota, program khusus pencari kerja laki-laki muda (Brebes, Pemalang) dan perempuan (Cilacap, Banjarnegara) | TPT menengah kab/kota, TPT L/P, pengeluaran per kapita | Kab/kota Jateng di kuadran "relatif baik" sebagai rujukan |
| **Jawa Tengah: tersembunyi** (Purworejo, Magelang, Wonogiri, Grobogan, Blora, Rembang, Jepara, Temanggung) | TPT rendah tetapi pengeluaran rendah; 70% setengah penganggur Jateng berpendidikan ≤SMP | Peningkatan produktivitas dan pelatihan pekerja berpendidikan rendah; perlindungan pekerja informal | Setengah pengangguran, pengeluaran per kapita | Idem |
| **SMK** (nasional) | Antrean tertinggi, kualitas kerja lebih baik; bergantung pada industri dan perdagangan | Tracer study wajib; evaluasi SMK berbasis kualitas kerja lulusan; diversifikasi jurusan ke sektor yang tumbuh | TPT SMK, informal non-pertanian SMK | Tren gap SMK–SMA |

**Pesan kebijakan inti:** menambah lama sekolah saja tidak menurunkan defisit kualitas kerja. Pendidikan harus **dipasangkan dengan penciptaan kerja formal** yang sesuai dengan struktur ekonomi daerah.

---

## 12. Rancangan Dashboard

### 12.1 Halaman 1 — "Pendidikan Mengubah Bentuk Masalah Kerja" (Langkah 1)
```
┌──────────────────────────────────────────────────────────────────────────┐
│ JUDUL + kalimat pesan                                           [WATERMARK] │
│ KPI: TPT 4,85% | TPT SMK 8,63% | Informal ≤SD 68% vs PT 17% | NEET 19,4%    │
├─────────────────────────────────┬────────────────────────────────────────┤
│ DUMBBELL JENJANG (H1)            │ TREN TPT PER JENJANG 2015–2025           │
│ TPT • informal • setengah peng.  │ (sorot SMK & SMA)                        │
├─────────────────────────────────┼────────────────────────────────────────┤
│ HEATMAP JENJANG × SEKTOR (H2)    │ 3 kotak insight + jembatan ke Halaman 2: │
│                                  │ "Apakah pola ini juga terjadi antarwilayah?" │
├─────────────────────────────────┴────────────────────────────────────────┤
│ Definisi & populasi tiap indikator · Sumber BPS                            │
└──────────────────────────────────────────────────────────────────────────┘
```

### 12.2 Halaman 2 — "Pengangguran Rendah, Pekerjaan Tidak Layak: Dari Indonesia ke Jawa Tengah" (Langkah 2–6)
```
┌──────────────────────────────────────────────────────────────────────────┐
│ JUDUL · [Tombol: TPT | Kualitas Kerja] · KPI: ρ = 0,00 | 3 prioritas | Jateng │
├────────────┬──────────────────────────────────┬──────────────────────────┤
│ SLIDER     │ TILE MAP 38 PROVINSI              │ KUADRAN TPT × IDKK3      │
│ BOBOT 3    │ (metrik dari tombol; ikon flag)   │ (warna = kuadran,        │
│ KOMPONEN   │                                  │  ukuran = angkatan kerja) │
├────────────┼──────────────────────────────────┼──────────────────────────┤
│ SLOPE      │ PITA KETIDAKPASTIAN PRIORITAS      │ SCATTER URBANISASI ×     │
│ TPT→IDKK3  │ (+ "Stabilitas: x/10")             │ IDKK3, warna = RLS (H6–7) │
├────────────┴──────────────────────────────────┴──────────────────────────┤
│ [Tombol: STUDI KASUS JAWA TENGAH] → panel: dumbbell dasar vs menengah 35   │
│ kab/kota + kuadran TPT × pengeluaran · [Rekomendasi per kuadran] · Narasi │
└──────────────────────────────────────────────────────────────────────────┘
```

### 12.3 Fitur interaktif
| Fitur | Fungsi analitis | Power BI | Di PDF |
|---|---|---|---|
| Tombol TPT ↔ Kualitas Kerja | Momen "aha": peta berubah warna | Field parameters + bookmark | Dua peta berdampingan |
| Slider bobot 3 komponen | Juri menguji sendiri kestabilan prioritas | What-if parameter + DAX `RANKX` | Hasil Monte Carlo |
| Pita ketidakpastian | Prioritas mana yang pasti | Error bar / Deneb | Statis |
| Kuadran interaktif | Klik kuadran → peta dan rekomendasi | Scatter + garis median + bookmark | Statis |
| Tombol Studi Kasus Jateng | Corong ke wilayah panitia: paradoks dasar vs menengah di 35 kab/kota + kuadran TPT × pengeluaran (tetap 1 halaman, FAQ 36) | Bookmark panel | Panel kecil |
| Panah 2018 → 2025 | Siapa yang membaik | Scatter dua titik / Play Axis | Panah statis |
| Narasi dinamis | Kalimat berubah sesuai provinsi yang dipilih | Measure DAX buatan tim (bukan Smart Narrative) | Narasi default |

**DAX inti:**
```DAX
IDKK3 Dinamis = VAR a=[W TSP Value] VAR b=[W Informal Value] VAR c=[W NEET Value]
RETURN 100*DIVIDE(a*SELECTEDVALUE(prov[z_tsp]) + b*SELECTEDVALUE(prov[z_informal]) + c*SELECTEDVALUE(prov[z_neet]), a+b+c)
Rank IDKK3 = RANKX(ALL(prov[nama]), [IDKK3 Dinamis], , DESC, Dense)
Stabilitas Top10 = COUNTROWS(FILTER(ALL(prov[nama]), [Rank IDKK3]<=10 && CALCULATE(MAX(prov[rank_idkk3]))<=10))
Narasi = SELECTEDVALUE(prov[nama],"Indonesia") & ": peringkat pengangguran " & SELECTEDVALUE(prov[rank_tpt]) & ", peringkat defisit kualitas kerja " & [Rank IDKK3] & " dari 38. Kuadran: " & SELECTEDVALUE(prov[kuadran]) & "."
```

**Desain:**
- Judul setiap visual berupa **kalimat temuan**.
- 4 warna kuadran yang konsisten di semua visual.
- Font ≥10 pt.
- Sumber BPS di setiap tooltip.
- PDF dicetak dalam kondisi default yang paling informatif.

---

## 13. Aturan Main

**Aturan lomba:**
- Tema 4 di formulir.
- Data hanya dari BPS.
- Power BI, 2 halaman, 1900×1100, watermark asli.
- Tanpa AI generatif (Smart Narrative, Q&A, Key Influencers).
- Tanpa drillthrough.
- Estimasi diberi tanda.
- ZIP ≤100 MB.
- Surat orisinalitas bermeterai.

**Aturan analisis:**
1. Headline harus lolos 3 uji: signifikan di n=38, bertahan tanpa Papua, dan bertahan dengan kontrol urbanisasi atau tanpa provinsi berdata urbanisasi induk.
2. Tidak ada klaim kausal.
3. Klaim individu hanya dari data jenjang; klaim wilayah dari data provinsi/kab-kota.
4. Setiap angka bisa ditelusuri ke CSV dan tabel BPS.
5. Pencilan diberi tanda, tidak dibuang.
6. Kab/kota tidak diranking berdasarkan selisih kecil.
7. Tidak ada target kebijakan karangan.

---

## 13b. Register Kelemahan dan Solusi (audit data, 19 Nov 2026)

| # | Kelemahan | Dampak | Solusi | Status |
|---|---|---|---|---|
| K1 | Data multi-tahun belum diambil (halaman BPS hanya menampilkan tahun terbaru) | Tidak ada dimensi waktu; juri bisa bertanya "apakah pola ini baru?" | WebAPI BPS (`scripts/ambil_panel_bps.py`) atau unduh manual 2018 & 2025 | ⏳ Tim (prioritas 1) |
| K2 | Posisi kuadran Jawa Tengah sensitif terhadap garis batas | Label "Antrean Kerja Formal" untuk Jateng bisa dipersoalkan | Narasi Jateng bertumpu pada analisis di dalam Jateng (35/35 kab/kota), bukan pada label provinsi | ✅ |
| K3 | Indeks buatan tim berpotensi dianggap tidak valid | Kritik "indeks subjektif" | Validasi konvergen dengan kemiskinan (ρ = 0,67) + 1.000 simulasi bobot + varian indeks | ✅ |
| K4 | Data kab/kota Jateng × pendidikan hanya sampai 2023, TPT total sampai 2025 | Tahun berbeda di panel Jateng | Analisis paradoks Jateng memakai 2023; peta prioritas memakai 2025 dan diberi label tahun | ✅ |
| K5 | Tabel Jateng "TPT menurut klasifikasi wilayah & pendidikan" tidak konsisten dengan tabel lain | Angka kota/desa bisa salah | Tabel tersebut tidak dipakai; pakai J08 | ✅ |
| K6 | Pengeluaran per kapita bukan ukuran kualitas kerja | Salah tafsir | Label "proksi kesejahteraan" | ✅ |
| K7 | Urbanisasi provinsi masih proyeksi SP2010 (34 provinsi) | Kontrol kurang presisi untuk 5 provinsi | Uji tanpa 5 provinsi menghasilkan hasil sama; cari SUPAS 2025 | ⚠️ Bersyarat |
| K8 | Kategori pendidikan Jateng kab/kota digabung (SMA+SMK = "menengah") | Tidak bisa memisahkan SMK di level kab/kota | Pemisahan SMK vs SMA hanya di level nasional; di Jateng dipakai "menengah" | ✅ |
| K9 | Dekomposisi TPT (efek komposisi pendidikan) belum bisa dihitung | Insight tambahan hilang | Butuh jumlah angkatan kerja per jenjang (cek via WebAPI); opsional | ⏳ Opsional |

---

## 14. Validasi dan Bias

| Risiko | Penanganan | Hasil |
|---|---|---|
| Bobot indeks subjektif | Monte Carlo 1.000 bobot + slider | Prioritas tangguh stabil (P = 1,00) |
| Komponen tumpang tindih | Varian tanpa tiap komponen | ρ terhadap IDKK3: 0,85–0,93; z-score 0,998 |
| Faktor pengganggu urbanisasi | Korelasi parsial | Klaim RLS → informal dibuang; urbanisasi jadi penjelas |
| Pengaruh Papua | Semua uji tanpa 6 provinsi Papua | Headline bertahan |
| Data urbanisasi lemah (proyeksi SP2010, 5 provinsi memakai nilai induk) | Uji tanpa 5 provinsi tersebut | Hasil sama (ρ parsial −0,69) |
| Bias seleksi upah | Upah dikeluarkan dari indeks | — |
| Batas kuadran | Bootstrap median; label "dekat batas" | 5 provinsi dekat batas |
| Galat sampling kab/kota | Tidak meranking selisih kecil; cukup kelompok tinggi/rendah | — |
| Ecological fallacy | Level dipisah | — |
| Validitas indeks | Korelasi dengan kemiskinan (di luar indeks) | ρ = 0,67 ✅ |
| Batas kuadran | Median vs rata-rata vs nasional | 79–84% sama; contoh utama tidak berubah ✅ |
| Reproduktibilitas | Skrip + seed 2026 + data mentah | ✅ |

---

## 15. Keterbatasan
1. Data agregat, sehingga tidak ada inferensi individu atau kausal.
2. n=38 provinsi; beberapa uji tanpa Papua menjadi marginal (p ≈ 0,09).
3. Urbanisasi masih proyeksi SP2010 (34 provinsi). Perlu diganti SUPAS 2025 jika tersedia.
4. Indikator Sakernas kurang sensitif di ekonomi subsisten.
5. Kab/kota Jateng: tidak ada data informal atau NEET; dipakai TPT × pendidikan (2023) dan pengeluaran per kapita (proksi kesejahteraan, bukan kualitas kerja).
6. IDKK3 adalah konstruksi analitis tim, **bukan indikator resmi BPS**.
7. Tren 2018–2025 menunggu data WebAPI.

**Untuk paper final:** mikrodata Sakernas (SILASTIK) untuk model individu × provinsi, pangsa PDRB sektoral, tracer study SMK, dan indikator kerentanan wilayah subsisten.

---

## 16. Simulasi Pertanyaan Juri

| Pertanyaan | Jawaban |
|---|---|
| "Kenapa tidak cukup TPT?" | Korelasi TPT dengan defisit kualitas kerja = 0,00 di 38 provinsi. Silakan klik tombol TPT ↔ Kualitas Kerja |
| "Kenapa TPT dan upah tidak ada di indeks?" | TPT dibandingkan **terhadap** indeks, jadi tidak boleh di dalamnya. Upah terbukti bias seleksi (hanya buruh/karyawan) |
| "Bobot indeks subjektif?" | Silakan geser slider. Dari 1.000 skema bobot, Maluku, Aceh, dan Malut selalu masuk 10 terburuk |
| "Bukankah ini efek kota?" | Ya, dan kami mengujinya. Besarnya defisit paling terkait urbanisasi. Karena itu klaim pendidikan di level wilayah kami batasi, dan mekanisme pendidikan ditunjukkan di level jenjang |
| "Kenapa Jateng bukan prioritas nasional?" | Di tingkat provinsi, kualitas kerja Jateng relatif baik dan posisinya dekat batas kuadran. Tetapi di dalam Jateng ada 9 kab/kota bermasalah ganda dan 8 kab/kota tersembunyi, dan paradoksnya berlaku di 35/35 kab/kota |
| "Kenapa tidak fokus Jateng saja?" | Indeks kerja layak (informal, NEET) hanya tersedia di level provinsi, jadi paradoks antarwilayah harus dibuktikan secara nasional. Jateng dianalisis dengan lensa yang sama (TPT × pendidikan per kab/kota) sebagai ujung alur |
| "Papua Pegunungan kok Relatif Layak?" | Itu temuan audit: indikator standar tidak sensitif di ekonomi subsisten, sehingga diberi flag dan tidak dibaca sebagai layak |
| "Kausal?" | Tidak. Seluruhnya asosiasi, konsisten dengan teori Lewis, Spence, dan La Porta & Shleifer |

---

## 17. Rencana Kerja

| Hari | Tugas | PJ |
|---|---|---|
| **Kam 19 Nov** | Daftar key WebAPI → jalankan `scripts/ambil_panel_bps.py`. Jika key tidak ada, unduh manual tahun **2018 dan 2025** untuk D03b, D05, D07, D15, D18 + jenjang D01, D02b, D03. Cari % perkotaan SUPAS 2025; unduh xlsx resmi tabel J01–J09 | A |
| **Jum 20 Nov** | Jalankan ulang `analisis_awal_2025.py` → `uji_ketahanan_2025.py` → `analisis_final_v4.py` dengan data final; hitung panah 2018 → 2025; finalisasi angka §9–§10 | A + B |
| **Sab 21 Nov** | Build Halaman 1 dan Halaman 2 (fitur inti) | C |
| **Min 22 Nov** | Panel Jateng, narasi dinamis, poles desain, cek silang semua angka, latihan Q&A §16 | Semua |
| **Sen 23 Nov** | Ekspor PDF + `.pbix` + ZIP + surat bermeterai → **kirim sebelum 18.00** | C |

**Checklist pengumpulan:**
- [ ] 2 halaman, 1900×1100, watermark asli
- [ ] Semua headline berstatus [DATA]/[TERUJI]; tidak ada klaim [GUGUR]
- [ ] Sumber BPS di tooltip; estimasi ditandai
- [ ] `DAC_NamaTim.pdf` (juga diunggah di GForm) + `DAC_NamaTim.zip` ≤100 MB (PDF, .pbix, Raw_Dataset, Processed_Dataset, scripts, surat)
- [ ] Surat orisinalitas ditandatangani + bermeterai
- [ ] Konfirmasi panitia: halaman tooltip dan poligon peta non-BPS

**File pendukung di folder proyek:**
- `scripts/`: `ambil_panel_bps.py`, `analisis_awal_2025.py`, `uji_ketahanan_2025.py`, `analisis_final_v4.py`
- `Raw_Dataset/`
- `Processed_Dataset/v4/`
- `HASIL_CEK_DATA_19NOV.md`
- Dokumen riset: `DAC_THEME4_*.md`

---

## 18. Referensi
- Chen, D. (2009). Vocational Schooling, Labor Market Outcomes, and College Entry. https://doi.org/10.1596/1813-9450-4814
- Elhorst, J. P. (2003). The Mystery of Regional Unemployment Differentials. https://doi.org/10.1046/j.1467-6419.2003.00211.x
- Gustiandza dkk. (2022). Spatial Autocorrelation Test on the Average Unemployment in Indonesia. https://doi.org/10.1109/iccit55355.2022.10119000
- Hanushek, E. A., dkk. (2017). General Education, Vocational Education, and Labor-Market Outcomes over the Lifecycle. https://doi.org/10.3368/jhr.52.1.0415-7074R
- Koto dkk. (2022). Determination of Sectoral Economic Growth on Educated Unemployment in All Provinces of Indonesia. https://doi.org/10.22202/economica.2022.v11.i1.6270
- La Porta, R., & Shleifer, A. (2014). Informality and Development. https://doi.org/10.1257/jep.28.3.109
- Lewis, W. A. (1954). Economic Development with Unlimited Supplies of Labour. https://doi.org/10.1111/j.1467-9957.1954.tb00021.x
- Maloney, W. F. (2004). Informality Revisited. https://doi.org/10.1016/j.worlddev.2004.01.008
- Newhouse, D., & Suryadarma, D. (2011). The Value of Vocational Education. https://doi.org/10.1093/wber/lhr010
- Nilsson, B. (2018). The School-to-Work Transition in Developing Countries. https://doi.org/10.1080/00220388.2018.1475649
- Pattinasarany, I. R. I. (2019). NEET Among the Youth in Indonesia. https://doi.org/10.7454/mjs.v24i1.10308
- Psacharopoulos, G., & Patrinos, H. A. (2018). Returns to Investment in Education. https://doi.org/10.1080/09645292.2018.1484426
- Purnastuti, L., dkk. (2013). Declining Rates of Return to Education: Evidence for Indonesia. https://doi.org/10.1080/00074918.2013.809842
- Cameron, L., dkk. (2019). Female Labour Force Participation in Indonesia. https://doi.org/10.1080/00074918.2018.1530727
- Spence, M. (1973). Job Market Signaling. https://doi.org/10.2307/1882010
- Segel, E., & Heer, J. (2010). Narrative Visualization: Telling Stories with Data. https://doi.org/10.1109/TVCG.2010.179
- Kale, A., dkk. (2019). Hypothetical Outcome Plots. https://doi.org/10.1109/TVCG.2018.2864909

*Metadata semua referensi diverifikasi lewat Crossref. Full text rujukan inti wajib dibaca sebelum paper final (1–7 Desember).*
