# DAC Data Slayer 4.0 — Advanced Research Report
### Tema 4: Pendidikan untuk Masa Depan Dunia Kerja
*Disusun 18 November 2026 · Deadline dashboard 23 November 2026, 23.59 WIB*

> **Status verifikasi (baca dulu).**
> - **[V-NILAI]**: tabel BPS sudah dibuka langsung di bps.go.id dan angkanya dibaca pada 18 Nov 2026.
> - **[V-ADA]**: halaman tabel atau publikasi BPS terbukti ada (judul resmi terkonfirmasi), tetapi angkanya belum dibaca karena halaman BPS dimuat dinamis.
> - **[SEKUNDER]**: angka berasal dari media yang mengutip BPS. Jangan dipakai di dashboard sebelum dicek ke tabel BPS.
> - **[NOT VERIFIED]**: belum ditemukan bukti.
> - Literatur: metadata (penulis, tahun, judul, jurnal, DOI) **diverifikasi lewat Crossref API**. Ringkasan temuan disusun dari abstrak dan pengetahuan umum tentang karya-karya tersebut. **Full text belum dibaca satu per satu**, jadi wajib dibaca sebelum dikutip di paper final.

---

## 1. Executive Summary

**Rekomendasi:** pilih **Konsep 1: "Paradoks Pengangguran Rendah: Pendidikan, Kualitas Pekerjaan, dan Peta Kerentanan Pasar Kerja Indonesia"**.

**Tesis inti.** TPT adalah indikator yang menyesatkan jika dibaca sendirian, baik antarjenjang pendidikan maupun antarwilayah.
- **Antarjenjang.** Lulusan berpendidikan lebih tinggi bisa punya TPT lebih tinggi tetapi kualitas kerja jauh lebih baik. Data BPS yang sudah terverifikasi: TPT 2025 lulusan SMK 8,63% dan SD ke bawah 2,30%. Sebaliknya, proporsi pekerja informal 2023 lulusan SMK 38,97% sementara lulusan SD 77,35%.
- **Antarwilayah.** Provinsi dengan TPT rendah belum tentu punya pasar kerja yang sehat. TPT rendah bisa saja menutupi informalitas dan setengah pengangguran yang tinggi.

**Kontribusinya** bukan menemukan bahwa "SMK banyak menganggur", karena itu sudah diketahui umum dan juri pasti bosan. Kontribusinya adalah tiga hal:
1. Mengganti lensa TPT dengan **lensa multidimensi kualitas kerja**: pengangguran, setengah pengangguran, informalitas, NEET, dan upah.
2. Membuktikan pola "*unemployment as a queue for good jobs*" pada dua level, yaitu jenjang pendidikan dan provinsi.
3. Menghasilkan **tipologi provinsi** yang langsung bisa diterjemahkan menjadi intervensi yang berbeda per tipe.

**Mengapa konsep ini menang:**
- Datanya paling aman. Hampir semuanya tabel dinamis BPS nasional dan provinsi, tanpa mikrodata.
- Konsep ini menjawab kritik juri tahun lalu ("variabel penting tidak dimasukkan"), karena kerangkanya sejak awal multidimensi.
- Hasilnya bisa disajikan rapi dalam 2 halaman: Halaman 1 untuk gradien pendidikan, Halaman 2 untuk peta dan tipologi provinsi.

**Konsep cadangan terkuat:** Konsep 2 (mismatch vertikal normatif). Konsep ini paling orisinal, tetapi data okupasi × pendidikan baru PARTIALLY VERIFIED. Jika tabelnya ditemukan pada 19 Nov, bagian ini bisa dimasukkan ke Konsep 1 sebagai satu visual tambahan.

---

## 2. Competition Context and Research Strategy

| Aspek | Implikasi untuk strategi |
|---|---|
| Analisis Data 40% | Butuh metode yang lebih dari deskriptif tetapi tetap bisa dipertanggungjawabkan: indeks komposit dengan uji sensitivitas, klaster tervalidasi, korelasi parsial, dan Moran's I. |
| Kesesuaian Tema & Pesan 30% | Satu kalimat pesan: *"TPT rendah bukan berarti pasar kerja baik."* |
| Desain 30% | 2 halaman, 1900×1100. Halaman 1 = jenjang pendidikan (nasional, tren), Halaman 2 = wilayah (peta + tipologi). |
| Final 60% (paper + presentasi + tanya jawab) | Kerangka teori dan keterbatasan harus siap sejak sekarang. Juri akan bertanya "mengapa variabel X tidak dimasukkan". |
| Aturan data | Semua angka dashboard dari BPS. Literatur hanya untuk teori dan metode. Lat/long boleh untuk peta (FAQ 12). |

**Strategi waktu:**
- *Essential research*: §4–§6 dan §12–§13 dokumen ini.
- *High-value additional*: mismatch okupasi (Konsep 2), Moran's I.
- *Future research*: mikrodata Sakernas (SILASTIK), dekomposisi Oaxaca, dan analisis kausal. Semuanya ditulis di paper sebagai agenda lanjutan.

---

## 3. Research Landscape

| Kluster | Pertanyaan inti dalam literatur | Status bukti |
|---|---|---|
| A. Education–employment mismatch | Apakah pendidikan cocok dengan pekerjaan? Ukurannya: *job analysis* (normatif), *worker self-assessment*, *realized matches*. | Mapan (McGuinness 2006; Quintini 2011). Studi Indonesia masih jarang dan biasanya memakai mikrodata. |
| B. Vokasi & employability | Apakah SMK memberi keunggulan? | **Diperdebatkan.** Untuk Indonesia, premi upah SMK negeri melemah pada kohort muda (Newhouse & Suryadarma 2011). Setelah koreksi seleksi, keunggulannya kecil (Chen 2009). Secara global, vokasi memudahkan masuk kerja tetapi keunggulannya memudar seiring usia (Hanushek dkk. 2017). |
| C. Pendidikan & ketimpangan sosial-ekonomi | Latar belakang rumah tangga → akses pendidikan → hasil kerja. | Mapan, tetapi butuh mikrodata untuk analisis level individu. |
| D. Struktur ekonomi | Transformasi struktural (Lewis 1954), deindustrialisasi prematur (Rodrik 2016) → daya serap tenaga terdidik. | Mapan secara teori. Untuk Indonesia ada studi panel provinsi (mis. Koto 2022). |
| E. Gender | Partisipasi kerja perempuan Indonesia stagnan sekitar 50% dan berbentuk U terhadap pendidikan (Cameron dkk. 2019). | Mapan. |
| F. Kualitas kerja & kerentanan | Informalitas sebagai segmentasi atau pilihan (Maloney 2004; La Porta & Shleifer 2014), setengah pengangguran, upah rendah. | Mapan secara global. **Di Indonesia jarang diintegrasikan dengan pendidikan dalam satu kerangka regional.** ← celah utama |
| G. Demografi & wilayah | Disparitas pengangguran regional bersifat persisten dan berkorelasi spasial (Elhorst 2003; Rios 2016). | Mapan secara global. Di Indonesia uji spasial pengangguran masih sederhana (mis. Gustiandza 2022). |
| H. Human capital & return to education | Mincer, signaling (Spence 1973), return global sekitar 9% per tahun sekolah (Psacharopoulos & Patrinos 2018). Di Indonesia return menurun (Purnastuti dkk. 2013). | Mapan. |

---

## 4. Literature Review Matrix

*Metadata dan DOI diverifikasi lewat Crossref. Kolom "Temuan" berasal dari abstrak dan isi yang dikenal luas; wajib dicek ke full text sebelum dikutip di paper.*

| # | Penulis (tahun) | Judul | Wilayah | DV | IV utama | Metode | Temuan utama | Keterbatasan | Relevansi / Pengembangan | DOI |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Newhouse & Suryadarma (2011) | The Value of Vocational Education: High School Type and Labor Market Outcomes in Indonesia | Indonesia | Upah, status kerja | Jenis SMA (umum/kejuruan, negeri/swasta) | Regresi upah, kontrol seleksi, IFLS/Sakernas | Premi SMK negeri melemah pada kohort muda. SMK swasta tidak menunjukkan premi yang jelas. | Data individu, sebelum ekspansi SMK besar-besaran | Inti untuk Konsep 1 & 3. Kami menambahkan dimensi kualitas kerja (informalitas, setengah pengangguran) yang lebih baru. | [10.1093/wber/lhr010](https://doi.org/10.1093/wber/lhr010) |
| 2 | Chen (2009) | Vocational Schooling, Labor Market Outcomes, and College Entry | Indonesia | Upah, kerja, masuk PT | SMK vs SMA | Regresi + koreksi seleksi | Keunggulan SMK kecil setelah koreksi seleksi. SMK menurunkan peluang masuk PT. | WP World Bank, data lama | Pembanding untuk paradoks SMK | [10.1596/1813-9450-4814](https://doi.org/10.1596/1813-9450-4814) |
| 3 | Hanushek, Schwerdt, Woessmann & Zhang (2017) | General Education, Vocational Education, and Labor-Market Outcomes over the Lifecycle | 11 negara | Employment menurut usia | Vokasi vs umum | DiD antarkelompok umur (IALS) | Vokasi memberi keunggulan kerja di usia muda yang memudar, bahkan berbalik, di usia tua | Negara maju | Landasan untuk analisis kelompok umur di Konsep 3 | [10.3368/jhr.52.1.0415-7074R](https://doi.org/10.3368/jhr.52.1.0415-7074R) |
| 4 | Pasay (2015) | Rates of Returns to Vocational and General Upper Secondary Education… Hollow Middle | Indonesia | Return to education | Vokasi vs umum, pengalaman | Mincer | Membahas return SMK vs SMA dalam konteks *hollow middle* | Jurnal nasional, data lama | Konteks Indonesia untuk H & B | [10.7454/efi.v58i3.50](https://doi.org/10.7454/efi.v58i3.50) |
| 5 | Purnastuti, Miller & Salim (2013) | Declining Rates of Return to Education: Evidence for Indonesia | Indonesia | Upah | Lama sekolah | Mincer, IFLS | Return pendidikan menurun seiring ekspansi pendidikan | Individu, 1990-an–2000-an | Mendukung argumen "pendidikan lebih tinggi ≠ otomatis hasil lebih baik" | [10.1080/00074918.2013.809842](https://doi.org/10.1080/00074918.2013.809842) |
| 6 | Duflo (2001) | Schooling and Labor Market Consequences of School Construction in Indonesia | Indonesia | Lama sekolah, upah | Program SD INPRES | Kuasi-eksperimen (DiD) | Pembangunan sekolah menaikkan pendidikan dan upah | Diperdebatkan oleh Roodman (2023, komentar) | Contoh desain kausal yang tidak bisa direplikasi dengan data agregat → masuk bagian keterbatasan | [10.1257/aer.91.4.795](https://doi.org/10.1257/aer.91.4.795) |
| 7 | Psacharopoulos & Patrinos (2018) | Returns to Investment in Education: A Decennial Review | Global | Return | Pendidikan | Meta-review | Return privat sekitar 9% per tahun sekolah; tertinggi di PT | Heterogen antarstudi | Landasan human capital | [10.1080/09645292.2018.1484426](https://doi.org/10.1080/09645292.2018.1484426) |
| 8 | Spence (1973) | Job Market Signaling | Teori | — | — | Teori | Pendidikan sebagai sinyal | Teoretis | Menjelaskan mengapa lulusan PT "mengantre" pekerjaan formal | [10.2307/1882010](https://doi.org/10.2307/1882010) |
| 9 | McGuinness (2006) | Overeducation in the Labour Market | Global | Mismatch | — | Survei literatur | Overeducation umum terjadi; penalti upah; hasil sangat bergantung pada cara pengukuran | Belum ada konteks Indonesia | Dasar Konsep 2 | [10.1111/j.0950-0804.2006.00284.x](https://doi.org/10.1111/j.0950-0804.2006.00284.x) |
| 10 | Quintini (2011) | Over-Qualified or Under-Skilled | OECD | Mismatch kualifikasi vs keterampilan | — | Review | Mismatch kualifikasi ≠ mismatch keterampilan | OECD | Mencegah klaim berlebihan: kami hanya mengukur *qualification* mismatch | [10.1787/5kg58j9d7b6d-en](https://doi.org/10.1787/5kg58j9d7b6d-en) |
| 11 | Nilsson (2018) | The School-to-Work Transition in Developing Countries | Negara berkembang | Transisi | — | Review | Transisi panjang; pekerjaan pertama sering informal | Review | Landasan Konsep 3 | [10.1080/00220388.2018.1475649](https://doi.org/10.1080/00220388.2018.1475649) |
| 12 | Pattinasarany (2019) | NEET Among the Youth in Indonesia… | Indonesia | Status NEET | Aktivitas sosial, akses informasi, dll. | Regresi logistik | Faktor sosial dan akses informasi berkaitan dengan status NEET | Satu periode | Landasan Konsep 3 | [10.7454/mjs.v24i1.10308](https://doi.org/10.7454/mjs.v24i1.10308) |
| 13 | Cameron, Contreras Suarez & Rowell (2019) | Female Labour Force Participation in Indonesia: Why Has It Stalled? | Indonesia | Partisipasi kerja perempuan | Pendidikan, pernikahan, anak, wilayah | Dekomposisi, Sakernas/Susenas | Partisipasi stagnan; hubungan pendidikan–partisipasi tidak linear | Mikrodata | Konsep 4 dan kontrol gender | [10.1080/00074918.2018.1530727](https://doi.org/10.1080/00074918.2018.1530727) |
| 14 | Maloney (2004) | Informality Revisited | Amerika Latin | Informalitas | — | Empiris + review | Sebagian informalitas bersifat sukarela, bukan selalu segmentasi | Konteks Amerika Latin | Mencegah kesalahan "informal = miskin" | [10.1016/j.worlddev.2004.01.008](https://doi.org/10.1016/j.worlddev.2004.01.008) |
| 15 | La Porta & Shleifer (2014) | Informality and Development | Global | Informalitas | Pembangunan | Review | Informalitas turun seiring pembangunan; produktivitas sektor informal rendah | Level perusahaan | Landasan teori kualitas kerja | [10.1257/jep.28.3.109](https://doi.org/10.1257/jep.28.3.109) |
| 16 | Comola & de Mello (2011) | How Does Decentralized Minimum Wage Setting Affect Employment and Informality? | Indonesia | Kerja, informalitas | Upah minimum provinsi | Panel provinsi | Kenaikan upah minimum berkaitan dengan pergeseran ke informal | Sebelum 2010 | Kontrol regional: upah minimum | [10.1111/j.1475-4991.2011.00451.x](https://doi.org/10.1111/j.1475-4991.2011.00451.x) |
| 17 | Elhorst (2003) | The Mystery of Regional Unemployment Differentials | Global | Pengangguran regional | Penawaran, permintaan, upah, struktur | Survei literatur | Disparitas regional persisten; daftar determinan baku | Negara maju | Daftar variabel kontrol Konsep 1 & 5 | [10.1046/j.1467-6419.2003.00211.x](https://doi.org/10.1046/j.1467-6419.2003.00211.x) |
| 18 | Rios (2016) | What Drives Unemployment Disparities in European Regions? A Dynamic Spatial Panel Approach | Eropa | Pengangguran regional | Struktur, demografi | Dynamic spatial panel | Ketergantungan spasial signifikan | Eropa, n besar | Pembenaran Moran's I; n=38 kami terlalu kecil untuk model spasial penuh | [10.1080/00343404.2016.1216094](https://doi.org/10.1080/00343404.2016.1216094) |
| 19 | Koto (2022) | Determination of Sectoral Economic Growth on Educated Unemployment in All Provinces of Indonesia | Indonesia | Pengangguran terdidik | Pertumbuhan sektoral | Panel provinsi | Pertumbuhan sektoral berkaitan dengan pengangguran terdidik | Jurnal nasional; cek kualitas | Pembanding langsung Konsep 5 | [10.22202/economica.2022.v11.i1.6270](https://doi.org/10.22202/economica.2022.v11.i1.6270) |
| 20 | Gustiandza dkk. (2022) | Spatial Autocorrelation Test on the Average Unemployment in Indonesia | Indonesia | TPT | — | Moran's I | Uji autokorelasi spasial TPT | Prosiding; hanya TPT | **Gap:** belum ada uji spasial pada indikator kualitas kerja multidimensi | [10.1109/iccit55355.2022.10119000](https://doi.org/10.1109/iccit55355.2022.10119000) |
| 21 | Rodrik (2016) | Premature Deindustrialization | Global | Pangsa manufaktur | Pendapatan | Panel negara | Negara berkembang mengalami deindustrialisasi lebih awal | Level negara | Konsep 5 | [10.1007/s10887-015-9122-3](https://doi.org/10.1007/s10887-015-9122-3) |
| 22 | Lewis (1954) | Economic Development with Unlimited Supplies of Labour | Teori | — | — | Teori dualisme | Sektor tradisional menyerap surplus tenaga kerja | Teoretis | Menjelaskan mengapa TPT rendah di provinsi agraris | [10.1111/j.1467-9957.1954.tb00021.x](https://doi.org/10.1111/j.1467-9957.1954.tb00021.x) |
| 23 | di Gropello, Kruse & Tandon (2011) | Skills for the Labor Market in Indonesia | Indonesia | Permintaan keterampilan | — | Survei pemberi kerja | Permintaan keterampilan meningkat; ada kesenjangan keterampilan | 2011 | Konteks kebijakan vokasi | [10.1596/9780821386149_over](https://doi.org/10.1596/9780821386149_over) |
| 24 | Anselin (1995) | Local Indicators of Spatial Association—LISA | Metodologi | — | — | — | Dasar LISA | — | Metode Konsep 1 | [10.1111/j.1538-4632.1995.tb00338.x](https://doi.org/10.1111/j.1538-4632.1995.tb00338.x) |
| 25 | Rousseeuw (1987) | Silhouettes… | Metodologi | — | — | — | Validasi klaster | — | Metode Konsep 1 | [10.1016/0377-0427(87)90125-7](https://doi.org/10.1016/0377-0427(87)90125-7) |
| 26 | Oaxaca (1973) | Male-Female Wage Differentials in Urban Labor Markets | Metodologi | — | — | Dekomposisi | Dasar Oaxaca–Blinder | Butuh mikrodata | Konsep 4 (future research) | [10.2307/2525981](https://doi.org/10.2307/2525981) |

**Catatan integritas.** Ada beberapa preprint yang relevan, misalnya Candrarini (2026) tentang pemetaan *education-job mismatch* di Indonesia ([10.21203/rs.3.rs-10228564/v1](https://doi.org/10.21203/rs.3.rs-10228564/v1)) dan Tjitrajaya (2025) tentang segregasi gender ([10.3897/arphapreprints.e152732](https://doi.org/10.3897/arphapreprints.e152732)). Keduanya **belum peer-reviewed**, jadi hanya boleh dikutip sebagai indikasi bahwa topik ini aktual.

---

## 5. Research Gap Synthesis

1. **Sudah banyak diteliti:** TPT menurut pendidikan, "paradoks SMK", serta determinan TPT provinsi dengan regresi panel (PDRB, IPM, upah minimum). **Mengulangnya tidak memberi nilai tambah.**
2. **Sering diabaikan:** kualitas pekerjaan. Studi pengangguran Indonesia hampir selalu memakai TPT sebagai satu-satunya variabel dependen. Padahal informalitas, setengah pengangguran, dan NEET mengubah ranking provinsi.
3. **Hasil yang bertentangan:** premi SMK positif di sebagian studi dan hilang di studi lain (Newhouse & Suryadarma vs Chen). Literatur informalitas terbelah antara pandangan "segmentasi" dan "pilihan sukarela" (Maloney).
4. **Keterbatasan variabel di studi Indonesia:** sebagian besar studi panel provinsi hanya memakai 3–5 variabel makro tanpa dimensi kualitas kerja dan tanpa uji ketergantungan spasial. Studi mismatch umumnya bergantung pada mikrodata.
5. **Celah yang realistis diisi dengan data BPS publik:**
   - (a) Indikator kualitas kerja multidimensi di level provinsi, disertai uji sensitivitas bobot.
   - (b) Pengujian dua level (jenjang pendidikan dan provinsi) atas hipotesis *queuing* atau *luxury unemployment*.
   - (c) Tipologi provinsi yang divalidasi (silhouette dan stabilitas).
   - (d) Uji autokorelasi spasial pada indikator gabungan, bukan hanya pada TPT.
6. **Novelty yang jujur:** novelty-nya ada pada **integrasi dan lensa**, bukan pada metode baru. Klaimnya: *"Kami menunjukkan bahwa membaca TPT tanpa kualitas kerja menghasilkan prioritas kebijakan yang berbeda."* Klaim ini bisa diuji langsung dengan korelasi ranking TPT vs ranking indeks.

---

## 6. BPS Dataset Inventory

Unit: N = nasional, P = provinsi, K = kab/kota. Semua dari Sakernas kecuali disebutkan lain.

| ID | Indikator (nama resmi BPS) | Unit | Dimensi | Satuan | Tahun / catatan | Status | URL |
|---|---|---|---|---|---|---|---|
| D01 | Tingkat Pengangguran Terbuka Berdasarkan Tingkat Pendidikan | N | 6 jenjang (≤SD, SMP, SMA umum, SMK, Diploma, Universitas) | % | Ada selektor tahun; nilai 2025 terbaca, diperbarui 30 Jan 2026 | **V-NILAI** | [link](https://www.bps.go.id/id/statistics-table/2/MTE3OSMy/tingkat-pengangguran-terbuka-berdasarkan-tingkat-pendidikan.html) |
| D02 | Proporsi Lapangan Kerja Informal Menurut Tingkat Pendidikan | N | 8 jenjang + total | % | Tahun terbaru yang tampil 2023 (diperbarui 6 Mei 2024) | **V-NILAI** | [link](https://www.bps.go.id/id/statistics-table/2/MjE1NyMy/proporsi-lapangan-kerja-informal-menurut-tingkat-pendidikan.html) |
| D03 | Tingkat Setengah Pengangguran Menurut Tingkat Pendidikan | N | Jenjang | % | Perlu cek tahun | V-ADA | [link](https://www.bps.go.id/id/statistics-table/2/MTE4NCMy/tingkat-setengah-pengangguran-menurut-tingkat-pendidikan.html) |
| D04 | TPT Berdasarkan Kelompok Umur | N | Umur | % | — | V-ADA | [link](https://www.bps.go.id/id/statistics-table/2/MTE4MCMy/tingkat-pengangguran-terbuka-berdasarkan-kelompok-umur.html) |
| D05 | TPT Menurut Provinsi | P | 38 provinsi | % | Ada juga versi **triwulanan** | V-ADA | [link](https://www.bps.go.id/en/statistics-table/2/NTQzIzI=/tingkat-pengangguran-terbuka-menurut-provinsi.html) |
| D06 | TPT dan TPAK Menurut Provinsi | P | — | % | Per tahun | V-ADA | [link 2023](https://www.bps.go.id/id/statistics-table/3/V2pOVWJWcHJURGg0U2pONFJYaExhVXB0TUhacVFUMDkjMw==/tingkat-pengangguran-terbuka--tpt--dan-tingkat-partisipasi-angkatan-kerja--tpak--menurut-provinsi--2023) |
| D07 | Proporsi Lapangan Kerja Informal Menurut Provinsi | P | — | % | — | V-ADA | [link](https://www.bps.go.id/id/statistics-table/2/MjE1MyMy/proporsi-lapangan-kerja-informal-menurut-provinsi.html) |
| D08 | Proporsi Lapangan Kerja Informal Sektor Non-Pertanian Menurut Provinsi | P | — | % | Mengontrol efek pertanian | V-ADA | [link](https://www.bps.go.id/id/statistics-table/2/MTE2MiMy/proporsi-lapangan-kerja-informal-sektor-non-pertanian-menurut-provinsi.html) |
| D09 | Proporsi informal menurut jenis kelamin / kelompok umur / daerah / status disabilitas | N | — | % | — | V-ADA | [JK](https://bps.go.id/indicator/6/2155/1/proporsi-lapangan-kerja-informal-menurut-jenis-kelamin.html), [umur](https://www.bps.go.id/id/statistics-table/2/MjE1NiMy/proporsi-lapangan-kerja-informal-menurut-kelompok-umur.html), [daerah](https://www.bps.go.id/id/statistics-table/2/MjE1NCMy/proporsi-lapangan-kerja-informal-menurut-daerah-tempat-tinggal.html) |
| D10 | Persentase Tenaga Kerja Formal Menurut Provinsi | P | — | % | — | V-ADA | [link](https://www.bps.go.id/en/statistics-table/2/MTE2OCMy/persentase-tenaga-kerja-formal-menurut-provinsi.html) |
| D11 | Upah Rata-rata per Jam Pekerja Menurut Provinsi | P | — | Rp/jam | Upah **buruh/karyawan** saja | V-ADA | [link](https://www.bps.go.id/en/statistics-table/2/MTE3MiMy/upah-rata---rata-per-jam-pekerja-menurut-provinsi.html) |
| D12 | Rata-rata Upah/Gaji Bersih Sebulan Buruh menurut Pendidikan Tertinggi & Lapangan Pekerjaan (17 sektor), 2024 | N | Pendidikan × sektor | Rp | Hanya 2024 (tabel statis) | V-ADA | [link](https://www.bps.go.id/en/statistics-table/1/MjI2MSMx/rata-rata-upah-gaji-bersih-sebulan-buruh-karyawan-pegawai-menurut-pendidikan-tertinggi-yang-ditamatkan-dan-lapangan-pekerjaan-utama-di-17-sektor--rupiah---2024.html) |
| D13 | Rata-rata Upah Buruh menurut Pendidikan & Jenis Pekerjaan Utama, 2022 | N | Pendidikan × okupasi | Rp | Mengindikasikan ada tabulasi okupasi × pendidikan | V-ADA | [link](https://www.bps.go.id/en/statistics-table/1/MjE5NCMx/rata-rata-upah-gaji-bersih-sebulan-buruh-karyawan-pegawai-menurut-pendidikan-tertinggi-dan-jenis-pekerjaan-utama-2022.html) |
| D14 | Penduduk 15+ yang Bekerja menurut Lapangan Pekerjaan Utama (17 sektor) & Pendidikan | N | Sektor × pendidikan | Orang | — | V-ADA | [link](https://www.bps.go.id/id/statistics-table/2/MTk3MSMy/penduduk-berumur-15-tahun-ke-atas-yang-bekerja-selama-seminggu-yang-lalu-menurut-lapangan-pekerjaan-utama--17-sektor--dan-pendidikan-tertinggi-yang-ditamatkan--orang-.html) |
| D15 | Persentase Usia Muda (15–24) yang Tidak Sekolah, Bekerja, atau Pelatihan (NEET) | N/P (cek) | — | % | — | V-ADA | [link](https://www.bps.go.id/en/statistics-table/2/MTE4NiMy/persentase-usia-muda-15-24-tahun-yangsedang-tidak-sekolah-bekerja-atau-mengikuti-pelatihan.htm) |
| D16 | NEET menurut Jenis Kelamin (SDG 8.6.1) | N | JK | % | — | V-ADA | [link](https://www.bps.go.id/en/statistics-table/2/MjY1NSMy/8-6-1--persentase-usia-muda--15-24-tahun--yang-sedang-tidak-sekolah--bekerja-atau-mengikuti-pelatihan-menurut-jenis-kelamin.html) |
| D17 | TPT menurut Status Disabilitas (SDG 8.5.2) | N | Disabilitas | % | — | V-ADA | (ada di "Tabel Terkait" D01) |
| D18 | Rata-rata Lama Sekolah Penduduk 15+ Menurut Provinsi | P | — | Tahun | Susenas | V-ADA | [link](https://www.bps.go.id/en/statistics-table/2/MTQyOSMy/rata-rata-lama-sekolah-penduduk-umur-15-tahun-ke-atas-menurut-provinsi.html) |
| D19 | RLS 15+ menurut Jenis Kelamin | N/P | JK | Tahun | — | V-ADA | [link](https://www.bps.go.id/id/statistics-table/2/MTQzMSMy/rata-rata-lama-sekolah-penduduk-umur-15-tahun-ke-atas-menurut-jenis-kelamin.html) |
| D20 | PDRB Provinsi menurut Lapangan Usaha 2021–2025 (publikasi) | P | 17 sektor | Rp, % | Rilis 13 Apr 2026 | V-ADA | [link](https://www.bps.go.id/id/publication/2026/04/13/71d97fa95c70c5049deecbab/produk-domestik-regional-bruto-provinsi-provinsi-di-indonesia-menurut-lapangan-usaha-2021-2025.html) |
| D21 | Keadaan Angkatan Kerja di Indonesia Agustus 2025 (publikasi) | N/P | Banyak | — | Rilis 19 Des 2025, tabel 2022–2025 | V-ADA | [link](https://www.bps.go.id/id/publication/2025/12/19/42a75ee61332755586fdfcdd/keadaan-angkatan-kerja-di-indonesia-agustus-2025.html) |
| D22 | Keadaan Pekerja di Indonesia Agustus 2025 (publikasi) | N | Upah, jam kerja | — | Rilis 23 Des 2025 | V-ADA | [link](https://www.bps.go.id/id/publication/2025/12/23/5fe58c9723acafc73fb95bff/keadaan-pekerja-di-indonesia-agustus-2025.html) |
| D23 | Indikator Pasar Tenaga Kerja Indonesia Februari 2026 (KILM ILO) | N/P | 14 indikator KILM | — | Rilis 26 Jun 2026 | V-ADA | [link](https://www.bps.go.id/id/publication/2026/06/26/f00a5821056e518c20d1546e/indikator-pasar-tenaga-kerja-indonesia-februari-2026.html) |
| D24 | Keadaan Angkatan Kerja Provinsi Jawa Tengah Agustus 2025 | K (Jateng) | — | — | Untuk studi kasus | V-ADA | [link](https://jateng.bps.go.id/id/publication/2026/04/15/846da24bda153c43f5cb0330/keadaan-angkatan-kerja-provinsi-jawa-tengah-agustus-2025.html) |
| D25 | Persentase penduduk miskin menurut provinsi | P | — | % | Rilis Maret/September | NOT VERIFIED (URL belum ditemukan, tabelnya pasti ada) | cari di bps.go.id "Persentase Penduduk Miskin Menurut Provinsi" |
| D26 | TPT provinsi × pendidikan | P | — | % | **Tidak ada di tabel dinamis nasional.** Tersebar di portal BPS provinsi atau lampiran publikasi | PARTIALLY VERIFIED | contoh Jabar Mei 2026 [SEKUNDER](https://data.goodstats.id/statistic/10-lulusan-smk-di-jawa-barat-menganggur-pada-mei-2026-b9dPT) |

**Angka resmi yang sudah dibaca langsung (V-NILAI):**
- **D01, TPT 2025:** ≤SD 2,30 · SMP 3,80 · SMA umum 6,88 · **SMK 8,63** · Diploma 4,31 · Universitas 5,39.
- **D02, proporsi informal 2023:** Tidak sekolah 93,00 · Tidak tamat SD 85,04 · SD 77,35 · SMP 68,09 · SMA umum 50,34 · **SMK 38,97** · Diploma 27,35 · Universitas 17,30 · Indonesia 59,11.
- ⚠️ D01 dan D02 berasal dari **tahun yang berbeda**. Untuk perbandingan resmi, ambil D01 tahun 2023 lewat selektor tahun.

**Jebakan sekunder.** Media menulis "TPT SMA 29,61%, SMK 26,12%" untuk November 2025. Itu kemungkinan besar adalah **komposisi penganggur menurut pendidikan**, bukan TPT. Jangan sampai tertukar.

---

## 7. Variable Universe and Supporting Factors

| Faktor | Peran | Landasan | Dataset BPS | Ketersediaan | Metode | Status |
|---|---|---|---|---|---|---|
| TPT | Outcome 1 | Elhorst 2003 | D01, D05 | Penuh | Deskriptif, indeks | CORE |
| Setengah pengangguran | Outcome 2 (*underemployment*) | ILO decent work | D03, provinsi (cek publikasi D21/D23) | Nasional pasti, provinsi perlu dicek | Indeks | CORE |
| Informalitas | Outcome 3 | La Porta & Shleifer 2014; Maloney 2004 | D02, D07, D08 | Penuh | Indeks, korelasi | CORE |
| NEET 15–24 | Outcome 4 (pemuda) | Nilsson 2018; Pattinasarany 2019 | D15, D16 | Nasional pasti, provinsi perlu dicek | Indeks | IMPORTANT |
| Upah per jam | Outcome 5 (buruh saja) | Mincer; Psacharopoulos & Patrinos 2018 | D11, D12 | Penuh | Indeks (arah dibalik), deflator antarprovinsi tidak ada | IMPORTANT (risiko perbedaan harga antarwilayah) |
| RLS / komposisi pendidikan angkatan kerja | Penjelas utama | Human capital | D18, D21 | Penuh | Korelasi parsial | CORE |
| Pangsa PDRB pertanian / industri | Kontrol struktur | Lewis 1954; Rodrik 2016 | D20 | Penuh | Regresi, kontrol | IMPORTANT |
| PDRB per kapita | Kontrol pembangunan | La Porta & Shleifer | D20 + penduduk | Penuh | Kontrol | IMPORTANT |
| Urbanisasi (% penduduk perkotaan) | Kontrol / moderator | Elhorst 2003 | SUPAS 2025 / proyeksi | NOT VERIFIED | Kontrol | OPTIONAL |
| Kemiskinan | Kontrol sosial-ekonomi | — | D25 | Hampir pasti ada | Kontrol | OPTIONAL (risiko kolinear dengan informalitas) |
| Gender (TPAK/NEET perempuan) | Moderator | Cameron dkk. 2019 | D16, D09 | Nasional | Panel tambahan | OPTIONAL untuk Konsep 1, CORE untuk Konsep 4 |
| Upah minimum provinsi | Kontrol | Comola & de Mello 2011 | Bukan data BPS (Kemnaker) → **tidak boleh dipakai** | — | — | NOT FEASIBLE |
| Fasilitas pendidikan, rasio guru | — | Tidak ada mekanisme langsung ke kualitas kerja jangka pendek | Ada di BPS | — | — | Ditolak (tidak relevan) |
| Kesesuaian bidang studi (horizontal mismatch) | — | Quintini 2011 | Butuh mikrodata | — | — | NOT FEASIBLE |
| Durasi menganggur | — | Job search theory | Butuh mikrodata/longitudinal | — | — | NOT FEASIBLE |

---

## 8. Dataset Compatibility and Feasibility Audit

| Isu | Temuan | Keputusan |
|---|---|---|
| Periode survei | Sakernas Agustus (tahunan), Februari, dan sekarang ada TPT provinsi **triwulanan** | Pakai **Agustus** secara konsisten. Jangan campur periode. |
| Jumlah provinsi | 34 provinsi sampai 2022, 38 provinsi setelah pemekaran Papua | **Cross-section utama: 38 provinsi tahun terbaru.** Tren provinsi: agregasikan kembali ke 34 (gabungan Papua) atau batasi pada 2023–2025. |
| Kategori pendidikan | D01 punya 6 kategori; D02 punya 8 | Harmonisasi: gabungkan Tidak Sekolah, Tidak Tamat SD, dan SD menjadi "≤SD". Rata-rata tertimbang butuh jumlah pekerja per jenjang (D14); jika tidak ada, tampilkan apa adanya dengan catatan. |
| Populasi | TPT dihitung dari angkatan kerja; informal dari penduduk bekerja; upah dari **buruh/karyawan saja**; NEET dari penduduk 15–24 | Setiap indikator diberi label populasi di tooltip. Jangan dijumlahkan langsung. |
| Sumber | RLS dari Susenas (Maret), TPT dari Sakernas (Agustus) | Bisa digabung di level provinsi-tahun sebagai **indikator kontekstual**, bukan relasi individu. |
| Ecological fallacy | Korelasi provinsi tidak menggambarkan individu | Kalimat wajib di dashboard dan paper: "hubungan antarwilayah, bukan antarindividu". |
| Perubahan metodologi | Klasifikasi informal BPS dan KBJI bisa berubah antartahun | Cek catatan kaki tiap tabel. Tandai *structural break* di grafik tren. |
| Missing | Informal per pendidikan mungkin berhenti di 2023 | Pakai tahun yang lengkap. Jika interpolasi diperlukan, beri tanda berbeda (FAQ 15). |

**Matriks integrasi (level provinsi, tahun terbaru):**

| | D05 TPT | D07/08 Informal | D11 Upah | D15 NEET | D18 RLS | D20 PDRB |
|---|---|---|---|---|---|---|
| D05 | — | ✔ | ✔ (buruh) | ✔ jika ada data provinsi | ✔ (beda survei) | ✔ |
| D07/08 | | — | ✔ | ✔ | ✔ | ✔ |
| D11 | | | — | ✔ | ✔ | ✔ (catatan harga) |

**Mikrodata.** Konsep 1 **tidak memerlukan** mikrodata. Dekomposisi Oaxaca, analisis durasi, dan mismatch individu memerlukan Sakernas melalui SILASTIK. Itu tidak realistis dalam 5 hari, jadi dimasukkan ke *future research*.

---

## 9. Five Proposed Research Concepts

### 9.1 Concept Rank 1 — "Paradoks Pengangguran Rendah"

**1. Identitas**

| | |
|---|---|
| Judul | *Paradoks Pengangguran Rendah: Pendidikan, Kualitas Pekerjaan, dan Peta Kerentanan Pasar Kerja Indonesia* |
| Subtema | Keterkaitan pendidikan, pengangguran, dan kesiapan SDM |
| Fokus | TPT vs kualitas kerja, menurut jenjang pendidikan dan provinsi |
| Cakupan | Nasional (jenjang) + 38 provinsi |
| Periode | Tren 2015–2025 (nasional); cross-section 2024/2025 (provinsi) |
| Populasi | Penduduk usia kerja 15+ dan pemuda 15–24 |
| Pesan utama | **"Pengangguran rendah bisa menyembunyikan pekerjaan yang buruk. Pendidikan menaikkan kualitas kerja, meskipun sering juga menaikkan TPT."** |

**2. Latar belakang.**
- Pola data BPS (D01, D02): jenjang dengan TPT tertinggi (SMK, Universitas) justru punya proporsi informal jauh lebih rendah dibanding jenjang ≤SD.
- Secara teori, orang berpendidikan rendah dan miskin "tidak mampu menganggur", sehingga mereka masuk sektor informal (Lewis 1954; La Porta & Shleifer 2014). Sebaliknya, lulusan menengah dan tinggi bisa mengantre pekerjaan formal (Spence 1973; teori job search).
- Akibatnya, kebijakan yang hanya menargetkan TPT berisiko salah sasaran.
- Kelompok terdampak: pekerja berpendidikan rendah di sektor informal, pemuda NEET, dan provinsi yang TPT-nya "terlihat baik".

**3. Rumusan masalah**
1. Bagaimana gradien pendidikan berbeda antara TPT dan indikator kualitas kerja (informalitas, setengah pengangguran, upah), dan apakah gradien itu berubah sepanjang 2015–2025?
2. Apakah ranking provinsi menurut TPT berbeda signifikan dari ranking menurut indeks kerentanan kualitas kerja multidimensi?
3. Bagaimana capaian pendidikan (RLS) dan struktur ekonomi provinsi berasosiasi dengan TPT dan dengan kualitas kerja? Apakah arah asosiasinya berlawanan?
4. Tipologi provinsi apa yang terbentuk, dan apakah kerentanan itu mengelompok secara geografis?

**4. Tujuan.**
- Umum: membangun lensa multidimensi untuk membaca keberhasilan pendidikan di pasar kerja.
- Khusus: (a) mengukur gradien pendidikan; (b) menyusun Indeks Defisit Kualitas Kerja (IDKK) provinsi beserta uji sensitivitas; (c) menguji asosiasi parsial; (d) menyusun tipologi dan rekomendasi per tipe.

**5. Teori.**

| Teori | Hubungan dengan variabel |
|---|---|
| Human Capital Theory | Pendidikan → produktivitas → upah dan pekerjaan formal |
| Signaling / Job Search | Lulusan terdidik punya *reservation wage* lebih tinggi → mengantre → TPT tinggi |
| Dualisme Lewis / segmentasi pasar kerja | Sektor tradisional menyerap tenaga berpendidikan rendah → TPT rendah tetapi informal |
| Decent Work (ILO) | Kualitas kerja bersifat multidimensi |

**6. Literatur dan gap:** #1, #2, #3, #8, #14, #15, #17, #20, #22. Gap: lihat §5 butir 2, 4, dan 5.

**7. Kerangka konseptual**
```
           [Struktur ekonomi: % PDRB pertanian, PDRB/kapita] ──┐ (kontrol)
                                                              ▼
[Pendidikan: RLS / jenjang] ──(+)──► TPT ("antre kerja formal")
            │
            └──(−)──► Defisit kualitas kerja (informal, setengah pengangguran, NEET, upah rendah)
                         ▲
        [Moderator: perkotaan/perdesaan, gender]  (opsional)
```

**8. Variabel:** lihat §7 (status CORE dan IMPORTANT).

**9. Audit dataset:** D01, D02, D03, D04, D05, D07, D08, D11, D15, D18, D20 masuk kategori Fully available atau available with limitations (V-ADA). D26 tidak dipakai.

**10. Metodologi:** deskriptif tren, Spearman antar-ranking, korelasi parsial atau OLS kecil (n=38, maksimal 3 regresor, *robust SE*), indeks komposit (min-max, bobot sama + PCA + uji sensitivitas Monte Carlo), k-means dan Ward dengan silhouette, Moran's I (kNN). Rincian ada di §14.

**11. Potensi insight** (H = hipotesis yang akan diuji, F = fakta dari sumber)

| # | Insight | Status | Metode | Implikasi |
|---|---|---|---|---|
| 1 | Gradien TPT naik seiring pendidikan, sedangkan gradien informalitas turun tajam | F (D01, D02) | Grafik dua sumbu atau *dumbbell* | Keberhasilan pendidikan harus diukur dengan kualitas kerja |
| 2 | Korelasi ranking TPT vs IDKK lemah atau negatif | H | Spearman | Prioritas provinsi berubah jika hanya memakai TPT |
| 3 | RLS berasosiasi positif dengan TPT tetapi negatif dengan informalitas, setelah dikontrol pangsa pertanian | H | Korelasi parsial | Hipotesis *luxury unemployment* di level wilayah |
| 4 | Provinsi bisa dikelompokkan ke 3–4 tipe | H | Klaster | Intervensi berbeda per tipe |
| 5 | IDKK mengelompok secara spasial, misalnya di timur | H | Moran's I | Kebijakan berbasis kawasan |
| 6 | Kesenjangan SMK vs SMA menyempit atau melebar dari waktu ke waktu | H | Tren | Evaluasi revitalisasi SMK (tanpa klaim kausal) |

**12. Problem solving**

| Temuan potensial | Kelompok | Faktor | Intervensi | Indikator keberhasilan |
|---|---|---|---|---|
| Tipe "TPT rendah, informal tinggi" | Pekerja ≤SMP di provinsi agraris | Struktur ekonomi tradisional | Formalisasi usaha mikro, perluasan jaminan sosial pekerja informal, pelatihan *upskilling* nonformal | Proporsi informal, setengah pengangguran |
| Tipe "TPT tinggi, berpendidikan" | Lulusan SMK/PT di provinsi industri dan urban | Antrean pekerjaan formal, mismatch | Layanan *job matching*, magang terstruktur, tracer study SMK | TPT SMK/PT, TPT 15–24 |
| Tipe "rentan ganda" | Pemuda NEET di provinsi tertinggal | Akses pendidikan dan kerja | Program *second chance* dan pelatihan berbasis wilayah | NEET 15–24 |
| Tipe "relatif baik" | — | — | Pertahankan, jadikan rujukan | — |

*Semua rekomendasi bersifat berbasis asosiasi, bukan dampak kausal.*

**13. Dashboard:** lihat §16.

**14. Kritik juri dan mitigasi**

| Kritik | Mitigasi |
|---|---|
| "Indeks Anda subjektif" | Tampilkan 3 skema bobot dan stabilitas ranking (Spearman antar-skema, interval ranking Monte Carlo). |
| "n=38 terlalu kecil untuk regresi" | Maksimal 3 regresor, *robust SE*, bootstrap, dan disajikan sebagai asosiasi. |
| "Upah tidak dikoreksi biaya hidup" | Catat sebagai keterbatasan. Uji sensitivitas indeks tanpa komponen upah. |
| "Informal ≠ miskin" | Sebutkan eksplisit (Maloney 2004). Pakai informal non-pertanian (D08) sebagai uji ketahanan. |
| "Ecological fallacy" | Pisahkan level individu (jenjang nasional) dan level wilayah. Gunakan bahasa yang hati-hati. |
| "Mengapa bukan TPT per pendidikan per provinsi?" | Tabel nasionalnya tidak tersedia (D26). Jelaskan sebagai keterbatasan, dan jadikan studi kasus Jawa Tengah opsional jika sempat. |

**15. Kelayakan:** data publik ±10 tabel, cleaning ringan, metode ringan sampai sedang. **Layak dikerjakan dalam 5 hari. Risiko: rendah.**

---

### 9.2 Concept Rank 2 — "Ijazah Melebihi Pekerjaan: Mismatch Vertikal Normatif"

| Komponen | Isi |
|---|---|
| Pesan | Berapa persen lulusan SMA/SMK/PT yang bekerja pada jabatan dengan tingkat keterampilan di bawah kualifikasinya, dan apakah angkanya naik? |
| Rumusan masalah | (1) Tren *overqualification* normatif per jenjang; (2) di sektor mana paling tinggi; (3) apakah upah lulusan PT pada jabatan rendah mendekati upah lulusan SMA? |
| Teori | Overeducation (McGuinness 2006), *qualification vs skill mismatch* (Quintini 2011), signaling |
| Metode | **Pendekatan normatif ILO.** Grup jabatan utama KBJI dipetakan ke skill level ISCO, lalu ke jenjang pendidikan yang "seharusnya". Contoh: lulusan PT pada jabatan tenaga usaha penjualan, jasa, atau pekerja kasar dihitung sebagai *overqualified*. Dihitung dari tabulasi okupasi × pendidikan (agregat). |
| Data | Penduduk bekerja menurut jenis pekerjaan utama × pendidikan (**PARTIALLY VERIFIED**; keberadaannya tersirat dari tabel upah D13), plus D12/D13 untuk upah |
| Gap | Studi mismatch Indonesia hampir semuanya memakai mikrodata. Ukuran normatif dari tabulasi publik bisa diulang setiap tahun oleh pemda. |
| Kritik juri | Pemetaan normatif kasar; grup jabatan terlalu agregat; KBJI berubah. Mitigasi: dua aturan pemetaan (ketat dan longgar) dan dinyatakan sebagai *qualification* mismatch. |
| Kelayakan | Sedang. Bergantung pada ditemukannya tabel okupasi × pendidikan. **Rekomendasi: jadikan modul tambahan Konsep 1 jika tabelnya ada.** |

### 9.3 Concept Rank 3 — "Transisi Sekolah ke Kerja Pemuda: NEET, Pengangguran Muda, dan Jalur SMK"

| Komponen | Isi |
|---|---|
| Pesan | Masalah utama pemuda bukan hanya menganggur, tetapi "hilang" dari pendidikan dan kerja (NEET), terutama pada perempuan. |
| Rumusan masalah | (1) Komposisi pemuda: menganggur vs NEET tidak aktif; (2) kesenjangan gender NEET; (3) sebaran provinsi; (4) TPT 15–24 vs usia dewasa (pola Hanushek) |
| Teori | School-to-work transition (Nilsson 2018), lifecycle vokasi (Hanushek dkk. 2017), Cameron dkk. 2019 |
| Metode | Analisis kelompok umur (repeated cross-section, **bukan kohort**), gap gender, peta, korelasi NEET provinsi dengan struktur ekonomi |
| Data | D04, D15, D16, D09. NEET provinsi × JK **belum terverifikasi** |
| Kritik juri | Data agregat tidak bisa menjelaskan *mengapa* seseorang NEET (pernikahan, pengasuhan). Mitigasi: posisikan sebagai deskriptif-kontekstual; penjelasan dari literatur. |
| Kelayakan | Tinggi untuk data, tetapi kedalaman analisis terbatas tanpa mikrodata |

### 9.4 Concept Rank 4 — "Pendidikan Sama, Hasil Berbeda: Ketimpangan Gender dalam Imbal Hasil Pendidikan"

| Komponen | Isi |
|---|---|
| Pesan | Pada jenjang yang sama, perempuan menghadapi partisipasi, formalitas, dan upah yang berbeda. |
| Metode ideal | Dekomposisi Oaxaca–Blinder (butuh mikrodata) → **tidak layak**. Alternatif agregat: rasio upah P/L per jenjang, gap TPAK, dan informal menurut JK |
| Data | D09 JK, D16, D19. Upah menurut pendidikan × JK **belum terverifikasi** |
| Kritik juri | Tanpa mikrodata, tidak bisa memisahkan efek karakteristik dan diskriminasi |
| Kelayakan | Sedang. **Lebih cocok untuk Tema 3 (Inklusif)** sehingga ada risiko dinilai kurang relevan dengan Tema 4 |

### 9.5 Concept Rank 5 — "Struktur Ekonomi Daerah dan Daya Serap Tenaga Terdidik"

| Komponen | Isi |
|---|---|
| Pesan | Provinsi dengan ekonomi yang didominasi pertanian atau pertambangan tidak menciptakan cukup pekerjaan bagi lulusan menengah ke atas. |
| Metode | Location Quotient sektor, panel provinsi 2021–2025 (FE) TPT ~ pangsa industri/jasa + RLS, shift-share pekerja per sektor |
| Data | D20 (PDRB), D14 (nasional). Pekerja sektor × pendidikan **per provinsi** tidak ada di tabel nasional |
| Gap | Koto (2022) sudah melakukan hal serupa sehingga nilai kebaruan rendah |
| Kritik juri | Panel 5 tahun × 38 provinsi dengan variasi dalam-provinsi kecil membuat FE lemah; ada risiko kausalitas terbalik |
| Kelayakan | Sedang. Lebih baik dijadikan **variabel kontrol** di Konsep 1 |

---

## 10. Comparative Scoring Matrix

Skala 1–10. Bobot sesuai directive.

| Kriteria (bobot) | K1 Paradoks | K2 Mismatch | K3 NEET | K4 Gender | K5 Struktur |
|---|---|---|---|---|---|
| Masalah & relevansi tema (10%) | 9 | 9 | 8 | 6 | 7 |
| Teori & literatur (15%) | 8 | 8 | 7 | 8 | 7 |
| Gap & kebaruan (15%) | 8 | 9 | 6 | 5 | 4 |
| Data BPS (20%) | 9 | 5 | 7 | 5 | 6 |
| Kedalaman metode (15%) | 8 | 7 | 6 | 4 | 7 |
| Potensi insight (10%) | 9 | 8 | 7 | 6 | 6 |
| Problem solving (10%) | 8 | 7 | 8 | 6 | 6 |
| Kelayakan 5 hari (5%) | 9 | 5 | 8 | 6 | 6 |
| **Skor tertimbang** | **8,45** | **7,25** | **6,95** | **5,65** | **6,10** |

**Alasan skor kunci:**
- K2 dapat 5 untuk data karena tabel okupasi × pendidikan belum terverifikasi. Penalti ini sesuai aturan directive.
- K4 dapat 4 untuk metode karena metode yang tepat butuh mikrodata.
- K5 dapat 4 untuk kebaruan karena sudah ada studi serupa (Koto 2022).
- K1 tidak mendapat 10 di mana pun karena n=38 dan indeks konstruksi tetap rentan dikritik.

**Ringkasan per kategori:**

| Kategori | Konsep |
|---|---|
| Gap terkuat | K2 |
| Data paling aman | K1 |
| Insight tertinggi | K1 |
| Paling menarik juri | K1 (paradoks yang kontra-intuitif) |
| Risiko metodologis terendah | K3 (deskriptif), lalu K1 |
| **Urutan akhir** | **K1 > K2 > K3 > K5 > K4** |

---

## 11. Critical Jury Simulation

| Pertanyaan juri | K1 | K2 | K3 | K4 | K5 |
|---|---|---|---|---|---|
| Kontribusi sebenarnya? | Lensa multidimensi + uji dua level + tipologi tervalidasi | Ukuran mismatch dari data publik | Profil pemuda | Gap gender agregat | Struktur → TPT |
| Hanya mengulang? | Sebagian bahan (paradoks SMK) dikenal, tetapi lensanya baru | Tidak | Sebagian | Ya, tanpa mikrodata | Ya |
| Faktor belum terukur | Biaya hidup, upah minimum (non-BPS), kualitas sekolah | Keterampilan aktual | Alasan NEET | Diskriminasi | Investasi |
| Data cukup kuat? | Ya | Belum pasti | Ya | Lemah | Cukup |
| Kesimpulan dapat dipertanggungjawabkan? | Ya, jika bahasanya asosiatif | Ya, jika diberi label "normatif" | Ya | Terbatas | Berisiko kausal |
| Muat 2 halaman? | Ya | Ya | Ya | Ya | Ya |

**Keputusan: K1**, dengan opsi menyisipkan satu visual dari K2 jika tabelnya tersedia. Analisis pemuda dari K3 masuk ke K1 sebagai komponen NEET di indeks.

---

## 12. Selected Winning Concept

**Judul final:** *Paradoks Pengangguran Rendah: Pendidikan, Kualitas Pekerjaan, dan Peta Kerentanan Pasar Kerja Indonesia*

**Executive summary.** Indonesia biasanya mengukur keberhasilan pendidikan di pasar kerja melalui TPT. Data BPS menunjukkan TPT tertinggi justru terjadi pada lulusan SMK dan universitas. Padahal kelompok yang sama memiliki proporsi pekerja informal terendah. Penelitian ini membangun Indeks Defisit Kualitas Kerja (IDKK) untuk 38 provinsi, menguji apakah pendidikan berasosiasi berlawanan arah dengan TPT dan dengan kualitas kerja, serta menyusun tipologi provinsi sebagai dasar prioritas kebijakan pendidikan dan ketenagakerjaan.

**Hipotesis**
- H1: gradien TPT terhadap jenjang pendidikan berbentuk ∩ (naik sampai SMK, lalu turun di diploma), sedangkan gradien informalitas turun monoton.
- H2: korelasi Spearman ranking TPT vs ranking IDKK di 38 provinsi < 0,5.
- H3: RLS berasosiasi positif dengan TPT dan negatif dengan informalitas, setelah dikontrol pangsa PDRB pertanian.
- H4: IDKK berautokorelasi spasial positif (Moran's I > 0, p < 0,05).

**Novelty dan kontribusi:** (1) integrasi lima dimensi kualitas kerja dari data BPS publik; (2) bukti dua level; (3) tipologi yang bisa diulang tiap tahun oleh pemda karena memakai tabel publik.

---

## 13. Complete Research Framework

**Data dictionary awal (provinsi × tahun terbaru)**

| Kolom | Definisi | Sumber | Satuan | Arah di IDKK |
|---|---|---|---|---|
| kode_prov, nama_prov | Kode BPS 2 digit | — | — | — |
| lat, lon | Centroid (FAQ 12) | Visual saja | ° | — |
| tpt | TPT Agustus | D05 | % | + (buruk) |
| tsp | Tingkat setengah pengangguran | D21/D23 | % | + |
| informal | Proporsi informal | D07 | % | + |
| informal_nonag | Informal non-pertanian | D08 | % | + (uji ketahanan) |
| neet | NEET 15–24 | D15 | % | + |
| upah_jam | Upah per jam buruh | D11 | Rp | − (dibalik) |
| rls | RLS 15+ | D18 | tahun | Penjelas |
| share_agri | % PDRB pertanian, kehutanan, perikanan | D20 | % | Kontrol |
| pdrb_kap | PDRB ADHB / penduduk | D20 + penduduk | Rp | Kontrol |

**Formula indikator turunan**
- Normalisasi: `z_i = (x_i − min)/(max − min)`. Untuk upah: `1 − z`.
- `IDKK_eq = mean(z_tpt, z_tsp, z_informal, z_neet, z_upah)` → dikalikan 100.
- `IDKK_pca`: bobot = loading PC1 yang dikuadratkan dan dinormalisasi (OECD/JRC 2008, *Handbook on Constructing Composite Indicators*; DOI belum terverifikasi).
- `IDKK_noTPT`: tanpa TPT, untuk menguji paradoks secara langsung.
- Sensitivitas: 1.000 bobot acak Dirichlet. Hasilnya median ranking dan interval 5–95% per provinsi.
- `Gap_SMK_SMA = TPT_SMK − TPT_SMA` per tahun.

**Tahapan kerja**

| Tahapan | Input | Proses | Output | Validasi |
|---|---|---|---|---|
| 1 Unduh | URL §6 | Unduh xlsx/JSON BPS ke `Raw_Dataset/` | 10–12 file | Cek tahun dan periode Agustus |
| 2 Cleaning | Raw | Seragamkan nama provinsi dan kode, pemekaran Papua, desimal koma → titik | `prov_clean.csv`, `edu_clean.csv` | 38 baris, tanpa duplikat |
| 3 Integrasi | Clean | Join berdasarkan kode_prov | `master_prov.csv` | Cek nilai kosong |
| 4 Analisis jenjang | `edu_clean` | Tren, gap | `edu_trend.csv` | Bandingkan dengan rilis BPS |
| 5 Indeks | master | Normalisasi, 3 skema, Monte Carlo | `idkk.csv` | Spearman antar-skema > 0,8? |
| 6 Asosiasi | master | Spearman, korelasi parsial, OLS robust | Tabel koefisien | VIF < 5, residual |
| 7 Klaster | z-score | k-means k=2..6, Ward | `cluster.csv` | Silhouette, ARI k-means vs Ward |
| 8 Spasial | lat/lon | kNN (k=4), Moran's I, 999 permutasi | I, p | Sensitivitas k=3,5 |
| 9 Dashboard | CSV | Power BI/Looker | 2 halaman | Cek 1900×1100, watermark |

---

## 14. Statistical and Analytical Methodology

| Metode | Tujuan | Asumsi / syarat | Kelebihan | Keterbatasan | Dipakai? |
|---|---|---|---|---|---|
| Deskriptif dan tren | RQ1 | Definisi stabil | Jelas | Tidak menjelaskan sebab | Ya |
| Spearman ranking TPT vs IDKK | RQ2 | Ordinal | Robust untuk n kecil | — | Ya |
| Korelasi parsial / OLS (≤3 regresor, HC3) | RQ3 | Linear, tidak multikolinear | Sederhana | n=38, asosiatif | Ya |
| Indeks komposit + sensitivitas | RQ2, 4 | Kerangka teori | Ringkas | Subjektivitas bobot → diuji | Ya |
| k-means + Ward, silhouette, ARI | RQ4 | Variabel distandardisasi | Tipologi tervalidasi | Sensitif terhadap pilihan variabel | Ya |
| Moran's I (kNN) | RQ4 | Matriks bobot | Uji pengelompokan geografis | Provinsi kepulauan, n kecil | Ya, sebagai uji pendukung |
| LISA | Lokal | n cukup | Peta hotspot | Dengan n=38 hasilnya tidak stabil, perlu koreksi multiple testing | Opsional |
| Panel FE | — | T cukup panjang | — | Hanya ±5 tahun konsisten dengan 38 provinsi | **Tidak** (tren saja) |
| Model spasial SAR/SEM/GWR | — | n besar | — | n=38 terlalu kecil | **Tidak** |
| Oaxaca, survival, multilevel | — | Mikrodata | — | Tidak tersedia | Future research |

**Robustness checks:** IDKK tanpa upah; IDKK dengan informal non-pertanian; IDKK tanpa TPT; klaster dengan k ±1; Moran dengan k=3/5.

---

## 15. Problem Solving and Policy Recommendations

Lihat tabel di §9.1 butir 12. Prinsip penyusunannya:
1. Rekomendasi **per tipe klaster**, bukan generik.
2. Setiap rekomendasi menyebut indikator BPS yang dipakai untuk memantau keberhasilannya.
3. Bahasanya "berasosiasi" atau "mengindikasikan", bukan "menyebabkan".
4. Untuk SMK: rekomendasikan **tracer study dan sistem informasi kebutuhan kerja daerah** sebagai syarat evaluasi. Jangan menyimpulkan "SMK gagal", karena lulusan SMK justru paling sedikit bekerja informal di antara lulusan menengah.

---

## 16. Two-Page Dashboard Blueprint (1900 × 1100)

**Halaman 1 — "Pendidikan Menaikkan Kualitas Kerja, Bukan Selalu Menurunkan Pengangguran"** (level jenjang, nasional)
- **Header + 4 KPI:** TPT nasional; TPT SMK; proporsi informal ≤SD vs Universitas; NEET 15–24.
- **A. Dumbbell / dual-bar:** TPT vs proporsi informal per jenjang (tahun yang sama). Ini visual paradoks utama.
- **B. Line chart 2015–2025:** TPT per jenjang. Sorot SMK dan SMA; tandai *structural break* (COVID 2020).
- **C. Bar:** setengah pengangguran per jenjang.
- **D. Heatmap:** upah buruh menurut pendidikan × 17 sektor (2024), untuk melihat sektor mana yang memberi imbal hasil pada SMK.
- **Kotak insight** (3 kalimat) dan catatan definisi (populasi tiap indikator).
- **Filter:** tahun, jenjang.

**Halaman 2 — "Di Mana TPT Rendah Menyembunyikan Pekerjaan Buruk?"** (level provinsi)
- **A. Peta:** IDKK per provinsi, dengan toggle TPT ↔ IDKK lewat bookmark (FAQ 36: tetap 1 halaman).
- **B. Scatter kuadran:** TPT (x) vs IDKK_noTPT (y), warna = klaster, ukuran = angkatan kerja.
- **C. Slope chart:** ranking TPT → ranking IDKK untuk 10 provinsi dengan perubahan terbesar.
- **D. Profil klaster:** radar atau bar dari z-score komponen.
- **E. Panel rekomendasi** per klaster, ditambah indikator pemantauan.
- **Catatan metode** (singkat): normalisasi, bobot, Spearman antar-skema, Moran's I.
- **Tooltip:** semua komponen mentah, ditambah sumber tabel BPS.
- **Watermark** resmi Data Slayer tanpa perubahan.

---

## 17. Data Collection and Processing Plan

1. Folder `Raw_Dataset/` berisi file asli dengan nama `Dxx_namatabel_tahun.xlsx`. Folder `Processed_Dataset/` berisi CSV hasil.
2. Jika tombol "Unduh" BPS sulit dipakai, gunakan menu **JSON** di setiap tabel. Simpan juga tangkapan layar halaman tabel sebagai bukti sumber.
3. Notebook Python (pandas, scikit-learn, esda/libpysal) disimpan untuk lampiran paper.
4. Sumber dicantumkan di dashboard: "Sumber: BPS, Sakernas Agustus [tahun]; Susenas; PDRB Provinsi menurut Lapangan Usaha 2021–2025".

---

## 18. Five-Day Execution Roadmap

| Hari | Target | Output |
|---|---|---|
| **Rab 18 Nov** | Kunci konsep. Unduh D01–D05, D07, D08. Cari tabel okupasi × pendidikan (keputusan K2). | Raw data tahap 1 |
| **Kam 19 Nov** | Unduh D11, D15, D18, D20. Cleaning dan integrasi. Gap tahun D01 vs D02 diselesaikan. | `master_prov.csv` |
| **Jum 20 Nov** | Indeks + sensitivitas, korelasi, klaster, Moran. Tulis 6 insight. | `idkk.csv`, `cluster.csv`, catatan insight |
| **Sab 21 Nov** | Bangun Halaman 1 dan 2 | Draf dashboard |
| **Min 22 Nov** | Review (pakai daftar kritik §9.1), poles desain, tooltip, watermark | Versi final |
| **Sen 23 Nov** | Ekspor PDF + link publik, ZIP (Raw/Processed/pbix), surat orisinalitas bermeterai. **Kirim sebelum 18.00.** | Submit |

---

## 19. Limitations and Research Risks

1. Data agregat → ecological fallacy, tidak bisa menarik inferensi individu atau kausal.
2. n=38 → daya statistik rendah, model spasial penuh tidak layak.
3. Upah hanya mencakup buruh/karyawan, tanpa koreksi harga antarprovinsi.
4. Informal tidak sama dengan miskin; setengah pengangguran tidak sama dengan *skills mismatch*.
5. IDKK adalah konstruksi analitis tim, **bukan indikator resmi BPS**.
6. Pemekaran provinsi Papua 2022 membatasi analisis tren provinsi.
7. Indikator tertentu mungkin hanya tersedia sampai 2023 (informal per pendidikan).
8. Faktor penting yang tidak bisa diukur dengan data BPS: upah minimum (Kemnaker), kualitas sekolah, keterampilan aktual, dan migrasi kerja yang rinci.

---

## 20. Final Recommendation

**Kerjakan Konsep 1.** Mulai hari ini dengan pengunduhan data. Pada 19 Nov siang, putuskan apakah modul mismatch (K2) bisa masuk: jika tabel okupasi × pendidikan ditemukan, tambahkan satu visual di Halaman 1. Jangan menambah metode selain yang tercantum di §14.

---

## 21. References

- Anselin, L. (1995). Local Indicators of Spatial Association—LISA. *Geographical Analysis*. https://doi.org/10.1111/j.1538-4632.1995.tb00338.x
- Cameron, L., Contreras Suarez, D., & Rowell, W. (2019). Female Labour Force Participation in Indonesia: Why Has It Stalled? *BIES*. https://doi.org/10.1080/00074918.2018.1530727
- Chen, D. (2009). *Vocational Schooling, Labor Market Outcomes, and College Entry*. World Bank PRWP 4814. https://doi.org/10.1596/1813-9450-4814
- Comola, M., & de Mello, L. (2011). How Does Decentralized Minimum Wage Setting Affect Employment and Informality? The Case of Indonesia. *Review of Income and Wealth*. https://doi.org/10.1111/j.1475-4991.2011.00451.x
- di Gropello, E., Kruse, A., & Tandon, P. (2011). *Skills for the Labor Market in Indonesia*. World Bank. https://doi.org/10.1596/9780821386149_over
- Duflo, E. (2001). Schooling and Labor Market Consequences of School Construction in Indonesia. *AER*. https://doi.org/10.1257/aer.91.4.795
- Elhorst, J. P. (2003). The Mystery of Regional Unemployment Differentials. *Journal of Economic Surveys*. https://doi.org/10.1046/j.1467-6419.2003.00211.x
- Gustiandza, dkk. (2022). Spatial Autocorrelation Test on the Average Unemployment in Indonesia. *IEEE ICCIT*. https://doi.org/10.1109/iccit55355.2022.10119000
- Hanushek, E. A., Schwerdt, G., Woessmann, L., & Zhang, L. (2017). General Education, Vocational Education, and Labor-Market Outcomes over the Lifecycle. *Journal of Human Resources*. https://doi.org/10.3368/jhr.52.1.0415-7074R
- Koto, dkk. (2022). Determination of Sectoral Economic Growth on Educated Unemployment in All Provinces of Indonesia. *Economica*. https://doi.org/10.22202/economica.2022.v11.i1.6270
- La Porta, R., & Shleifer, A. (2014). Informality and Development. *JEP*. https://doi.org/10.1257/jep.28.3.109
- Lewis, W. A. (1954). Economic Development with Unlimited Supplies of Labour. *The Manchester School*. https://doi.org/10.1111/j.1467-9957.1954.tb00021.x
- Maloney, W. F. (2004). Informality Revisited. *World Development*. https://doi.org/10.1016/j.worlddev.2004.01.008
- McGuinness, S. (2006). Overeducation in the Labour Market. *Journal of Economic Surveys*. https://doi.org/10.1111/j.0950-0804.2006.00284.x
- Newhouse, D., & Suryadarma, D. (2011). The Value of Vocational Education: High School Type and Labor Market Outcomes in Indonesia. *World Bank Economic Review*. https://doi.org/10.1093/wber/lhr010
- Nilsson, B. (2018). The School-to-Work Transition in Developing Countries. *Journal of Development Studies*. https://doi.org/10.1080/00220388.2018.1475649
- Oaxaca, R. (1973). Male-Female Wage Differentials in Urban Labor Markets. *IER*. https://doi.org/10.2307/2525981
- Pasay, N. H. A. (2015). Rates of Returns to Vocational and General Upper Secondary Education… *Economics and Finance in Indonesia*. https://doi.org/10.7454/efi.v58i3.50
- Pattinasarany, I. R. I. (2019). Not in Employment, Education or Training (NEET) Among the Youth in Indonesia. *MASYARAKAT: Jurnal Sosiologi*. https://doi.org/10.7454/mjs.v24i1.10308
- Psacharopoulos, G., & Patrinos, H. A. (2018). Returns to Investment in Education: A Decennial Review. *Education Economics*. https://doi.org/10.1080/09645292.2018.1484426
- Purnastuti, L., Miller, P. W., & Salim, R. (2013). Declining Rates of Return to Education: Evidence for Indonesia. *BIES*. https://doi.org/10.1080/00074918.2013.809842
- Quintini, G. (2011). *Over-Qualified or Under-Skilled*. OECD SEM WP. https://doi.org/10.1787/5kg58j9d7b6d-en
- Rios, V. (2016). What Drives Unemployment Disparities in European Regions? *Regional Studies*. https://doi.org/10.1080/00343404.2016.1216094
- Rodrik, D. (2016). Premature Deindustrialization. *Journal of Economic Growth*. https://doi.org/10.1007/s10887-015-9122-3
- Rousseeuw, P. J. (1987). Silhouettes. *J. Computational and Applied Mathematics*. https://doi.org/10.1016/0377-0427(87)90125-7
- Spence, M. (1973). Job Market Signaling. *QJE*. https://doi.org/10.2307/1882010
- OECD/JRC (2008). *Handbook on Constructing Composite Indicators*. OECD Publishing. **DOI NOT VERIFIED**

*Nama penulis kedua dan seterusnya pada beberapa entri (Koto, Gustiandza, Pasay, Pattinasarany) perlu dilengkapi dari halaman DOI. Crossref hanya mengembalikan penulis pertama dalam pencarian ini.*

## 22. Source and Verification Register

| Item | Status | Cara verifikasi |
|---|---|---|
| D01 nilai 2025 | V-NILAI | Dibuka di browser, 18 Nov 2026 |
| D02 nilai 2023 | V-NILAI | Dibuka di browser, 18 Nov 2026 |
| D03–D20 | V-ADA | Judul resmi dari halaman BPS dan daftar "Tabel Terkait" |
| D21–D24 | V-ADA | Halaman publikasi BPS (tanggal rilis terkonfirmasi) |
| D25 | NOT VERIFIED | Belum dicari langsung |
| D26 | PARTIALLY | Hanya sumber sekunder dan portal provinsi |
| Tabel okupasi × pendidikan (untuk K2) | PARTIALLY | Tersirat dari D13 |
| 26 referensi | Metadata VERIFIED (Crossref) | Full text **belum** dibaca |
| Angka media (NEET 20,31% 2024; 52,81% buruh di bawah UMP Feb 2026; TPAK 70,59% Agt 2025) | SEKUNDER | Jangan dipakai sebelum dicek ke BPS |
