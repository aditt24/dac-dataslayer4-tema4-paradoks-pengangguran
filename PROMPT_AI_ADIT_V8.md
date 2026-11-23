# PROMPT AI: Dashboard v7c → v8 (salin semua isi file ini)

Kamu melanjutkan dashboard Tableau lomba DAC Data Slayer 4.0 Tema 4, "Paradoks Pengangguran Rendah".
Folder kerja: `C:\Users\LENOVO\OneDrive\Documents\Datslay DA`. Tenggat kumpul: 23 Nov 2026 23.59 WIB. Berhenti menambah fitur pukul 20.00.
Tata letak di bawah adalah rancangan tim. Tugasmu membantu teknis (formula, XML, pengecekan). Anggota tim yang membuka, menilai, dan merapikan hasil di Tableau.

## Baca dulu (hanya ini, hemat token)
1. `AI_PROJECT_PROGRESS.md`: bagian STATUS TERKINI, INVENTARIS, dan "Pelajaran teknis XML Tableau".
2. `AI_PROJECT_DECISIONS.md`.
3. `scripts/redesign_tableau_v7.py`: fungsi pembantu (`calc`, `set_ws`, `zone`, `zsheet`, `zparam`, `ztext`, `rebuild`, `set_viewpoints`) dan blok `z1`/`z2` di akhir. Jangan baca ulang semua file lain.
4. Lihat `deliverables/screenshots/v7c_hal1_final.png` dan `v7c_hal2_final.png`.

## Aturan keras
- JANGAN timpa atau ubah `DAC_Dashboard_Tema4_FINAL.twbx` (v7c, cadangan), `DAC_desain_QA_v2.twbx`, dan BACKUP. Hasil baru: `DAC_Dashboard_Tema4_v8.twbx`.
- Tetap 2 dashboard, 1900×1100. Tidak ada Bab 3, 3D, ekstensi, Smart Narrative, atau konten tersembunyi.
- Watermark `Image/New_Watermark.png` tidak diubah, diwarnai, atau ditutup.
- Angka dan metodologi tidak diubah. Semua angka dari `Processed_Dataset/tableau/`. Tidak ada klaim kausal.
- Palet tetap v7c: navy, biru = TPT, merah bata = kerja tidak layak. Font diganti (lihat bagian Teks).
- Jangan pakai computer use untuk membangun. Edit lewat skrip Python + XML. Tableau dibuka hanya untuk cek akhir, oleh anggota tim.
- Jangan commit/push kecuali diminta. Jangan klaim "lulus" untuk hal yang belum diuji.

## Cara kerja
1. Salin `scripts/redesign_tableau_v7.py` menjadi `scripts/redesign_tableau_v8.py`, lalu ubah di sana.
2. Build sesuai perintah di `AI_PROJECT_PROGRESS.md` (ekstrak `DAC_desain_QA_v2.twbx`, salin GeoJSON, set `TPL_TWB`), lalu kemas dengan `scripts/pack_twbx.py` ke `DAC_Dashboard_Tema4_v8.twbx`.
3. Sebelum mengubah apa pun, jalankan build tanpa perubahan dan pastikan hasilnya dapat dibuka seperti v7c.
4. Kerjakan P0 per bagian sesuai urutan file ini, build, minta anggota tim membuka di Tableau, baru lanjut P1 lalu P2.

## P0: fitur "Cek Provinsimu" (Hal 2)
Sumber data `Provinsi & KabKota`. Parameter `Pilih Provinsi` = `[Parameters].[Parameter 0379056854634496]`, default tetap `Indonesia`.
Calculated field (tulis dengan nama internal yang benar di XML):
```
[Provinsi Kartu] = IF [Pilih Provinsi] = "Indonesia" THEN "NUSA TENGGARA BARAT" ELSE [Pilih Provinsi] END
[Filter Kartu]   = [wilayah] = [Provinsi Kartu]
[Med TPT]        = { FIXED : MEDIAN([z_tpt]) }
[Med NEET]       = { FIXED : MEDIAN([z_neet]) }
[Med Setengah]   = { FIXED : MEDIAN([z_tsp]) }
[Med Informal]   = { FIXED : MEDIAN([z_informal]) }
[Keyakinan]      = "10 besar di " + STR(ROUND([prob_top10]*100)) + "% dari 1.000 skenario bobot"
[Stabil]         = IF [kuadran_stabil_3batas] THEN "Tipe stabil di 3 batas" ELSE "Tipe berubah jika batas diganti" END
[Rekomendasi]    = CASE [kuadran]
  WHEN "Rentan Ganda" THEN "Padat karya formal, program NEET"
  WHEN "Rentan Tersembunyi" THEN "Formalisasi usaha mikro, hilirisasi pertanian"
  WHEN "Antrean Kerja Formal" THEN "Percepat penyerapan kerja formal"
  ELSE "Pertahankan, pantau mutu kerja" END
```
Kalimat `ELSE` adalah usulan; minta persetujuan tim. Cek tipe data `kuadran_stabil_3batas` (boolean atau teks) sebelum memakai `[Stabil]`.

Tiga sheet baru, semua difilter `[Filter Kartu]` = True:
- `H2-K1 Peringkat`: nama provinsi, lalu `rank_tpt → rank_ktl` besar. Judul "Cek Provinsimu". Subjudul: "Contoh: NTB. Klik provinsi lain di peta" saat parameter `Indonesia`.
- `H2-K2 Penyebab`: 4 batang horizontal `z_tpt`, `z_neet`, `z_tsp`, `z_informal` (AVG), penanda median 38 provinsi. Label: TPT, NEET, Setengah pengangguran, Informal. Keterangan: "Skala 0–1 (min–maks), makin tinggi makin rentan; | = median".
- `H2-K3 Diagnosis`: `kuadran`, `Rekomendasi`, `Keyakinan`, `Stabil`.

Aksi parameter `Klik provinsi`: tambahkan ketiga sheet baru ke `exclude-sheet`, supaya klik pada kartu tidak mengubah parameter.

Nilai uji (wajib cocok):
| Provinsi | Peringkat TPT → KTL | Tipe | Stabil | 10 besar | TPT / NEET / Setengah / Informal |
|---|---|---|---|---|---|
| NTB | 34 → 2 | Rentan Tersembunyi | ya | 35% | 0,287 / 0,456 / 0,791 / 0,560 |
| DKI Jakarta | 7 → 38 | Antrean Kerja Formal | ya | 3% | 0,834 / 0,310 / 0,030 / 0,039 |
| Jawa Tengah | 14 → 26 | Relatif Layak | ya | 0% | 0,580 / 0,469 / 0,298 / 0,402 |
| Papua Tengah | 28 → 1 | Rentan Tersembunyi | ya | 87% | 0,389 / 0,655 / 1,000 / 0,827 |
| Maluku | 6 → 7 | Rentan Ganda | ya | 100% | 0,874 / 0,957 / 0,617 / 0,521 |

Median 38 provinsi: 0,497 / 0,579 / 0,368 / 0,416. Jika berbeda, baris provinsi tergandakan oleh relasi data: perbaiki formulanya, jangan ubah data.

## P0: tata letak Hal 2 (x, y, w, h dalam piksel)
| Elemen | x, y, w, h |
|---|---|
| `H2-E Peta Berbalik` | 44, 172, 836, 364 |
| `H2-Narasi` | 44, 536, 600, 56 |
| Parameter Lihat peringkat menurut | 644, 536, 236, 56 |
| K1 / K2 / K3 | 890, 172, 510, 110 / 890, 282, 510, 180 / 890, 462, 510, 130 |
| `H2-F Kuadran` | 1410, 172, 440, 420 |
| `H2-G Penimbang` | 44, 602, 680, 240 |
| Parameter `Fokus kebijakan` (daftar pilihan, satu baris) | 44, 842, 680, 46 |
| 4 slider bobot (nama terbaca utuh) | 2 kolom × 2 baris: x = 44 dan 384, y = 890 dan 941, w = 340, h = 50 |
| `H2-G Pesan Bobot` | 64, 710, 640, 40 |
| `H2-K Peta KabKota` | 734, 602, 668, 258 |
| `H2-K Sebaran Tahun` | 734, 860, 480, 132 |
| Parameter Acuan pembanding | 1214, 860, 188, 132 |
| Keputusan: judul / `H2-R Keputusan` / angka 135 | 1412, 602, 438, 50 / 1412, 652, 438, 250 / 1412, 902, 438, 90 |

Keluarkan `H2-S Lereng Peringkat` dari dashboard (sheet-nya disimpan). Header, tombol, footer, dan watermark tetap.

## P0: "Fokus kebijakan" (Priority Lab jadi alat keputusan)
Parameter baru `Fokus kebijakan` (teks, daftar): `Seimbang` (default), `Kurangi pengangguran`, `Perbaiki mutu kerja`, `Anak muda (NEET)`, `Atur sendiri`.
Bobot (TPT / NEET / setengah pengangguran / informal):
- Seimbang: 0,25 / 0,25 / 0,25 / 0,25
- Kurangi pengangguran: 0,4 / 0,4 / 0,1 / 0,1
- Perbaiki mutu kerja: 0,1 / 0,1 / 0,4 / 0,4
- Anak muda (NEET): 0,2 / 0,6 / 0,1 / 0,1
- Atur sendiri: pakai 4 slider lama

Buat 4 calc bobot efektif `[B TPT]`, `[B NEET]`, `[B Setengah]`, `[B Informal]` (CASE parameter), lalu pakai di `Total Bobot` dan `Skor Dinamis`. Pesan bobot 0 hanya muncul pada `Atur sendiri`. Subjudul: "Bobot pilihan tim, slider berlaku untuk Atur sendiri".
3 provinsi teratas berwarna penuh, sisanya pudar. Pita dan bintang 1.000 skenario tetap.

Nilai uji 5 teratas:
| Fokus | Urutan (skor) |
|---|---|
| Seimbang | Maluku 74,2 · Papua Tengah 71,8 · Aceh 70,5 · Papua 64,7 · Sulut 62,7 |
| Kurangi pengangguran | Maluku 84,6 · Papua 81,9 · Sulut 79,8 · Papua Barat Daya 78,5 · Jabar 78,2 |
| Perbaiki mutu kerja | Papua Tengah 83,5 · Aceh 66,3 · Maluku 63,8 · NTB 61,4 · Sulbar 56,2 |
| Anak muda (NEET) | Maluku 86,3 · Sulut 83,3 · Papua 79,3 · Aceh 75,5 · Papua Barat Daya 75,1 |

## P0: kesimpulan jadi grafik (ganti kotak paragraf)
**Hal 2, judul "Langkah per tipe masalah".** Sheet baru `H2-R Keputusan`: satu baris per tipe, batang = jumlah provinsi (COUNTD), label angka besar, aksi maksimal 5 kata. Urutan dan nilai:
- Rentan Ganda, 8: Padat karya dan program NEET
- Rentan Tersembunyi, 11: Formalisasi usaha mikro
- Antrean Kerja Formal, 11: Percepat penyerapan kerja
- Relatif Layak, 8: Pertahankan, pantau mutu kerja

Sorot tipe provinsi di kartu, baris lain pudar:
`[Tipe Kartu] = { FIXED : MAX(IF [Filter Kartu] THEN [kuadran] END) }`, `[Sorot Tipe] = [kuadran] = [Tipe Kartu]`.
Di bawahnya angka besar **135** dengan teks "kab/kota 9 tahun di atas median sejenis". Tambahkan `H2-R Keputusan` ke `exclude-sheet`. Kalimat urbanisasi (ρ parsial) pindah ke footer.

**Hal 1, kotak "Jadi" diganti 3 kartu angka sejajar** (angka minimal 28 pt, keterangan maksimal 7 kata, tanpa paragraf):
- **68,4%** · pekerja ≤SD informal, pengangguran hanya 2,3%
- **6 dari 6** · jenjang: informal naik sejak 2015
- **8,6%** · pengangguran SMK, tertinggi sejak 2015

Keterangan "informal = % pekerja nonpertanian" tetap ada di subjudul grafik atau footer.

## P0: tata letak Hal 1
Hapus kartu "ALUR HALAMAN INI" dan nomor ①②③ yang berulang. Legenda warna sudah ada di subjudul grafik.
| Elemen | x, y, w, h |
|---|---|
| 4 KPI | y 172, h 104, w 442; x = 44, 498, 953, 1408 (sparkline ikut digeser di kiri kartu) |
| Cermin (header / kiri / kanan) | 44, 288, 900, 70 / 44, 358, 360, 330 / 404, 358, 540, 330 |
| `H1-S TPT Satu Dekade` / `H1-S Informal Satu Dekade` | 954, 288, 442, 400 / 1406, 288, 444, 400 |
| `H1-B Tren TPT` | 44, 698, 1000, 294 |
| 3 kartu angka | y 698, h 294, w 258; x = 1054, 1323, 1592 |

## P0: teks
Semua font: `Tableau Bold` / `Tableau Semibold` / `Tableau Book`. Georgia dibuang (tinggi angkanya tidak rata).
| Peran | Ukuran |
|---|---|
| Judul halaman | 28 Bold |
| Angka KPI dan kartu | 28–34 Bold |
| Judul grafik | 14 Semibold |
| Subjudul, label | 10–11 Book |
| Footer | 9 Book |

Kapitalisasi: kalimat biasa di semua teks, tanpa HURUF KAPITAL untuk label. Nama provinsi: "Nusa Tenggara Barat". Singkatan (NTB, DKI, TPT, NEET, SMK) tetap kapital. Ubah nama hanya di calc tampilan; nilai `wilayah` asli jangan diubah.

Batas: judul ≤7 kata, subjudul ≤12 kata, satu kalimat. Tebalkan hanya angka atau kata kunci. Hindari pola "Bukan X, tapi Y", pertanyaan retoris berulang, slogan dramatis, panah dan simbol sebagai hiasan, serta istilah Inggris yang tidak perlu. Panah hanya untuk perubahan angka (34 → 2).
| Lama | Baru |
|---|---|
| Pengangguran turun. Kerja layak tidak ikut naik. | Pengangguran turun, kerja informal naik |
| Sejak 2015 TPT turun di keenam jenjang... | Berlaku di enam jenjang pendidikan, 2015–2025 |
| Cermin terbalik: paling jarang menganggur... | Lulusan ≤SD jarang menganggur, paling banyak informal |
| TPT turun di keenam jenjang / Informal naik... | Pengangguran turun / Kerja informal naik |
| Kasus SMK: TPT tertinggi sebelas tahun... | Pengangguran SMK tertinggi sejak 2015 |
| Peringkat berbalik saat mutu kerja ikut dihitung. | Pengangguran rendah belum tentu kerja layak |
| Satu provinsi, dua peringkat | Peringkat 38 provinsi |
| Empat tipe kerentanan | Empat tipe masalah kerja |
| Priority Lab: siapa yang tetap di atas? | Provinsi yang didahulukan |
| Judul peta kab/kota | Tetap dinamis, potong ke ≤10 kata |

Judul halaman, 3 kartu angka, dan judul grafik harus cukup untuk memahami cerita. Detail metode pindah ke tooltip dan footer.

## P0: gerak (fitur bawaan Tableau)
- Aktifkan animasi: Format > Animations > Workbook Default = On, durasi 0,5 detik, Simultaneous. Dilakukan anggota tim lewat menu jika XML tidak yakin.
- Teks, pie, reference line, serta peta/poligon di browser TIDAK beranimasi. Maka K2, `H2-R Keputusan`, dan Penimbang memakai batang/lingkaran. Penanda median K2 memakai mark, bukan reference line.
- Gerak hanya muncul saat klik atau ganti parameter. Tidak ada putar otomatis. PDF tetap harus jelas tanpa gerak.

## P1: rapikan
- Jarak antarkartu 10–12 px, padding seragam 12 px, tepi kartu sejajar. Garis bantu dan sumbu yang tidak dipakai dihapus.
- Tile map: perkecil tanda kotak sampai tidak bertumpuk; singkatan dan angka terbaca.
- Kuadran: label tipe dan provinsi tidak bertumpuk atau terpotong.
- Hal 1: "+3,19 saat COVID" tidak menempel garis. Sumbu tahun hanya 2015–2025. Label jenjang cermin tampil sekali.
- Semua angka: koma desimal, satu desimal untuk persen. Kecuali angka uji/statistik.

## P2: hanya jika P0 dan P1 selesai sebelum 19.00
Cermin Hal 1 diubah dari batang tebal ke lollipop (garis tipis + lingkaran) supaya tidak monoton. Jangan menambah grafik lain.

## QA yang harus dilaporkan (LULUS / GAGAL / BELUM DIUJI)
1. Workbook terbuka tanpa error; tidak ada pill merah.
2. Lima baris nilai uji dan median di atas.
3. Klik NTB, DKI, Jateng, Papua Tengah: kartu dan visual lain ikut. Klik ulang: kembali ke `Indonesia` dan kartu NTB.
4. Semua bobot 0: pesan muncul dan tidak terpotong.
5. Acuan pembanding Nasional ↔ Sesama; kacamata TPT ↔ Kerja tidak layak; tombol Bab 1 ↔ Bab 2.
6. Ekspor gambar 1900×1100 kedua halaman: teks tidak terpotong, watermark utuh.
7. Lima fokus kebijakan: urutan cocok tabel; baris Keputusan menyorot tipe yang benar saat klik NTB, DKI, Jateng.
8. Animasi berjalan saat klik provinsi dan ganti fokus. Tidak ada judul melewati batas kata atau teks terpotong.
9. Default tersimpan: `Indonesia`, `Seimbang`, `Kerja tidak layak`, `Sesama kota/kabupaten`, semua bobot 0,25.

Jika P0 belum stabil pukul 20.00, pakai v7c untuk pengumpulan.

## Akhir
Perbarui `AI_PROJECT_PROGRESS.md` (status, sisa tugas) dan `AI_PROJECT_CHANGELOG.md`. Catat di `AI_PROJECT_DECISIONS.md`: slope peringkat diganti Cek Provinsimu; kesimpulan paragraf diganti grafik; Georgia diganti font Tableau; Fokus kebijakan ditambah. Lapor singkat: apa yang berubah, hasil QA, apa yang harus dicek manusia. Publish, ZIP, dan unggah dikerjakan tim.

Mulai sekarang dari P0.
