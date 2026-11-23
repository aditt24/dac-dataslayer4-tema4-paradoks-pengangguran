# Redesain v7 — design system, arsitektur cerita, audit grafik, QA
23 Nov 2026 · Claude Code · workbook: `DAC_Dashboard_Tema4_FINAL.twbx` (cadangan versi sebelumnya: `DAC_Dashboard_Tema4_FINAL_pre_v7.twbx`)
Skrip yang menghasilkan v7 dari basis `DAC_desain_QA_v2.twbx`: `scripts/redesign_tableau_v7.py` + `scripts/pack_twbx.py`.
Tangkapan 1900×1100 hasil akhir: `deliverables/screenshots/v7_hal1_final.png`, `v7_hal2_final.png`. Putaran QA: `deliverables/qa_redesign/`.

## 1. Audit sebelum redesain (ringkas, jujur)
Basis: `DAC_desain_QA_v2.twbx` (versi Codex paling mutakhir, tidak tercatat di changelog; berisi Skor KTL tooltip, judul ①–⑤, pesan Papua). File `DAC_Dashboard_Tema4_new.twbx` yang disebut di prompt ternyata salinan asli tim 3 halaman (identik dengan BACKUP), jadi tidak dipakai sebagai basis.
Masalah utama yang terlihat pada render 1900×1100:
- Tampilan default Tableau: putih/abu, satu ukuran huruf, garis tipis, tanpa hierarki; judul halaman tidak lebih menonjol dari judul grafik.
- Default tersimpan tertinggal dari pengujian (Pilih Provinsi = PAPUA TENGAH) → panel pembanding kosong "2 nulls".
- Peta tile memakai satu skala biru di kedua mode: pembalikan peringkat tidak terasa secara visual.
- Panel Pembanding (mini tile + dumbbell) lemah: tile tak terbaca, dan analisisnya sendiri gagal uji tandingan (audit sesi 2) sehingga hanya konteks deskriptif.
- Mode cerita "Langkah" menduplikasi narasi dan kontrolnya membingungkan; heatmap sektor tidak terhubung ke pesan utama.
- Legend warna dumbbell & bar 2015/2025 tidak ada / bertabrakan; label field mentah ("Jenjang Ta..", "Rank Dinamis", "W TPT").
- Teks panjang dengan perlakuan sama; kesimpulan kecil di footer.

## 2. Pelajaran dari referensi Gelar Rasa ASAP (fogline-puce.vercel.app)
Diambil prinsipnya, bukan tampilannya: (a) judul berupa pertanyaan/pernyataan, bukan nama grafik; (b) angka besar + vonis singkat + konteks kecil; (c) blok hero gelap dengan serif display untuk membuka cerita; (d) satu jalur bab bernomor; (e) teks pendek, metodologi turun ke catatan. Yang TIDAK ditiru: tema gelap penuh, peta 3D, tur terpandu (tidak andal di Tableau/PDF).

## 3. Design system
### Warna (semantik, dipakai konsisten di kedua halaman)
| Token | Hex | Arti |
|---|---|---|
| paper | #f3eee4 | latar halaman (di bawah watermark; watermark tidak diubah) |
| card | #ffffff | kartu grafik |
| ink | #14213d | teks utama, band judul, kartu kesimpulan |
| ink-2 / muted | #4a5468 / #7c8494 | teks sekunder / catatan |
| amber | #f2a93b | kicker & nomor (hanya di blok gelap) |
| cobalt | #2f5fa7 (gelap #1d3f7a, sedang #6f93c8) | **pengangguran (TPT)**, Antrean Kerja Formal |
| vermilion | #d9532b | **informal / kerja tidak layak**, Rentan Tersembunyi |
| oxblood | #8e1b10 | Rentan Ganda (buruk di dua dimensi) |
| sage | #7fa88a | Relatif Layak |
| neutral | #d6cfc2 / #ddd6ca | pembanding, jenjang/provinsi lain |
Peta: 5 kelas peringkat (1–5, 6–10, 11–19, 20–29, 30–38) dalam rampa cobalt saat kacamata TPT dan rampa merah bata saat kacamata kerja tidak layak. Makin gelap = makin rentan.

### Tipografi (font aman Tableau Desktop/Public/PDF)
Georgia (display): judul halaman 24 pt, judul grafik 13–15 pt, angka KPI 26 pt. Tableau Book/Semibold: subjudul 9 pt, isi kartu 10–11 pt, kicker 8–9 pt kapital, catatan 8 pt.

### Tata letak
Kanvas 1900×1100, area isi x 44–1850, y 44–1052 (di dalam bingkai watermark; logo x≈1600–1725, y 0–95 dibiarkan bebas). Band judul gelap 44–162; baris KPI/kontrol; dua baris kartu dengan jarak 10 px; footer sumber 1000–1052. Kartu putih di atas paper, tanpa border.

### Bahasa grafik
Gridline & zeroline dimatikan; label field mentah disembunyikan; legend ditulis langsung di subjudul (● biru / ● merah bata / ■ 2015 / ■ 2025); judul = temuan; tooltip menyebut sumber BPS.

## 4. Arsitektur cerita (2 halaman sesuai aturan)
- **Bab 1 — "Pengangguran turun. Kerja layak tidak ikut naik."** KPI → cara membaca (dua penyebut) → dumbbell 2025 (utama) + tren TPT → COVID, dot plot informal 2015→2025, kartu "Yang perlu diingat" + jembatan ke Bab 2.
- **Bab 2 — "Peringkat berbalik saat mutu kerja ikut dihitung."** ① peta dua kacamata + narasi + kontrol → slope chart peringkat (baru) → ② kuadran; ③ Priority Lab, ④ jejak kab/kota, kartu Kesimpulan & rekomendasi.

## 5. Audit grafik
| Grafik | Keputusan | Alasan |
|---|---|---|
| H1-A Dumbbell TPT vs informal | KEEP (diperbesar, legend di judul) | bukti paradoks paling langsung |
| H1-B Tren TPT | KEEP | SMK tertinggi 11 tahun |
| H1-D COVID bar | KEEP (diperkecil) | konteks guncangan |
| H1-F Informal 2015 vs 2025 | REDESIGN → dot plot | bar berkelompok berdesakan |
| H1-KPI ×4 | REDESIGN (Georgia, label kapital) | — |
| H1-C Heatmap sektor | REMOVE | tidak menjawab pertanyaan utama; tetap di paper |
| H1-E Donut | REMOVE | 15 irisan, tak terbaca |
| H2-E Peta tile | REDESIGN (warna ganda per kacamata, tile lebih besar) | signature reveal |
| H2-S Slope peringkat | BARU | menampilkan pembalikan di PDF statis |
| H2-F Kuadran | KEEP (sumbu ringkas, palet semantik) | — |
| H2-G Priority Lab | REDESIGN (10 provinsi, slider 2×2, label manusiawi) | — |
| H2-I Jejak kab/kota + KPI | KEEP (legend status, judul ringkas) | — |
| H2-H Pembanding (dumbbell, mini tile, pesan) | REMOVE | analisis gagal uji tandingan; tile tak terbaca |
| H2-E Teks Cerita + kontrol Langkah | REMOVE | duplikasi narasi |
| H2-E Peta Geo (poligon) | REMOVE (tak dipakai di dashboard) | tile map lebih adil untuk provinsi kecil |
Kalkulasi lama yang tidak dipakai lagi dibiarkan di datasource (tidak memengaruhi tampilan).

## 6. Interaksi signature: "Satu provinsi, dua peringkat"
Kontrol "Lihat peringkat menurut" mengganti peta dari rampa cobalt (TPT) ke rampa merah bata (kerja tidak layak) beserta angka peringkat. Slope chart di sebelahnya memperlihatkan perpindahan yang sama sekaligus (berguna di PDF). Klik provinsi → narasi, sorotan kuadran, dan tabel kab/kota ikut provinsi itu (aksi parameter lama "Klik provinsi", sumbernya semua sheet Hal 2 kecuali yang dikecualikan; yang diuji di v7: klik di peta).

## 7. QA (dilihat langsung di Tableau 2026.3, ekspor 1900×1100)
| Cek | Hasil |
|---|---|
| 2 halaman, 1900×1100, watermark tidak diubah/tertutup | LULUS |
| Tidak ada grafik/teks tumpang tindih atau terpotong (render ekspor) | LULUS, dengan catatan kecil: label tile peta rapat; anotasi kuadran "Rentan Tersem-bunyi" terpenggal; nama "Kota Lhokseu.." terpotong; label PATENG di tepi atas kuadran |
| Kacamata TPT ↔ kerja tidak layak | LULUS: TPT → NTB 34, DKI 7, Kepri 5; KTL → NTB 2, DKI 38, Kepri 37 (cocok t3) |
| Klik NTB | LULUS: narasi, sorotan kuadran, tabel kab/kota NTB |
| Slider bobot | LULUS: Bobot TPT 0,25→0,35 mengubah urutan (Aceh naik ke 2) |
| Tombol Bab 1 ↔ Bab 2 | LULUS (Bab 1 → Bab 2 diuji) |
| Workbook dibuka di Bab 1, default Indonesia + kacamata kerja tidak layak | LULUS |
| Angka teks vs CSV | LULUS: t1 (TPT 2015→2025 turun di 6 jenjang; informal naik di 6 jenjang; SMK 8,63; SMA 6,88; ≤SD 2,30; informal SD 68,43, SMA 43,75, SMK 35,84; PT 8,19→16,63; COVID SMK +3,19), t3 (peringkat di atas; Malut prob_top10 0,917), t5 (66 persisten ganda), ρ TPT~KTL −0,302 p 0,066 |
| Pesan semua bobot 0, klik Jawa Tengah/Papua baru, Acuan pembanding | BELUM diuji ulang di v7 (logika tidak diubah; lulus di sesi sebelumnya) |
| Ekspor PDF, Tableau Public | BELUM (lihat sisa tugas) |

## 8. Keterbatasan & sisa
- Tableau Desktop Free Edition: publish ke Tableau Public perlu akun user sendiri.
- Slider di ekspor gambar/PDF tampil sebagai teks nilai (perilaku Tableau).
- Label tile peta rapat untuk singkatan panjang (SUMBAR, KALTENG) — terbaca, tidak rapi sempurna.


---
## 9. Revisi v7b (23 Nov, setelah umpan balik user) — audit informativeness
Tangkapan akhir: `deliverables/screenshots/v7b_hal1_final.png`, `v7b_hal2_final.png`.

### Audit "apa yang dikatakan grafik ini?"
| Grafik | Informasi yang didapat | Keputusan |
|---|---|---|
| Tabel jejak kab/kota (heatmap 66 baris × 9 tahun) | Di tampilan Indonesia **hampir nol**: tabel hanya memuat kab/kota yang menurut definisinya di atas acuan tiap tahun, jadi semua sel pasti gelap (tautologi). Baru berguna saat provinsi dipilih. | DIGANTI peta kab/kota + histogram |
| COVID bar (perubahan 2019→2020) | Satu fakta (SMK +3,19) yang sudah terlihat sebagai lonjakan di grafik tren | DIGABUNG ke subjudul tren |
| Dot plot informal 2015 vs 2025 | Hanya separuh pesan Bab 1 (informal naik); sisi TPT turun tidak tampil | DIGANTI slope ganda |
| Pesan inti Bab 1 "TPT turun di 6 jenjang, informal naik di 6 jenjang" | Sebelumnya hanya ada di teks, tidak divisualkan | BARU: slope ganda |
| Pola persistensi kab/kota | Sebaran "berapa tahun di atas acuan (0–9)" berbentuk U: 111 tidak pernah vs 135 selalu (acuan median sejenis); acuan nasional: 270 vs 81. Status kab/kota jarang berpindah → masalah struktural | BARU: histogram U (sekaligus legenda peta) |
| Sebaran geografis kab/kota persisten | Belum ada di dashboard | BARU: peta 514 kab/kota (geometri geoBoundaries yang diizinkan panitia, angka BPS) |

### Visual baru
- **Bab 1, "TPT turun ↘ | Informal naik ↗"**: dua slope chart berdampingan 2015→2025, satu garis per jenjang, label jenjang + nilai di kedua ujung. Pesan terbaca tanpa teks: semua garis biru turun, semua garis merah bata naik.
- **Bab 2 ④ peta kab/kota + histogram U**: warna = jumlah tahun TPT kab/kota di atas acuan (Tidak pernah / 1-3 / 4-6 / 7-8 / 9 dari 9). Ikut parameter "Acuan pembanding" (Nasional / Sesama kota-kabupaten) dan ikut provinsi yang diklik: klik NTB atau Jawa Tengah di peta provinsi → peta kab/kota memperbesar ke provinsi itu, histogram dan judul dinamis ikut berubah ("12 kab/kota di atas median kab/kota sejenis pada 9 dari 9 tahun · JAWA TENGAH").
- Latar peta: washout 100% (tidak bergantung tile Mapbox saat dibuka offline).
- Data spasial: `Spatial/IDN_kabkota_persistensi_v7.geojson` dari `scripts/siapkan_geojson_persistensi_v7.py` (geometri disederhanakan, atribut dari t5_kabkota_jejak). Caption geoBoundaries ada di footer Bab 2 dan tooltip.

### Riset singkat fitur Tableau yang dipertimbangkan
| Fitur | Keputusan | Alasan |
|---|---|---|
| Mark animation | DIPAKAI (sudah aktif di workbook: AnimationOnByDefault) | transisi warna peta/kuadran saat ganti kacamata atau provinsi; tidak memengaruhi PDF |
| Parameter action (klik provinsi) | DIPAKAI, diperluas ke peta kab/kota (lewat filter parameter) | interaksi andal di Desktop/Public |
| Viz in Tooltip | DITUNDA | perlu filter lintas sumber data (t3 ↔ GeoJSON); risiko gagal saat dikemas |
| Dynamic zone visibility / tab | DITOLAK | isi tersembunyi tidak ikut ke PDF yang dinilai |
| Ekstensi / 3D / autoplay | DITOLAK | tidak andal di Tableau Public/PDF juri |
Rujukan: blog Tableau "Bring your data to life with viz animations" (2020), artikel InterWorks soal parameter action untuk storytelling, pengumuman Viz in Tooltip (Tableau 10.5). Kriteria Iron Viz (analisis, desain, storytelling) dipakai sebagai cek.

### QA v7b (Tableau 2026.3, ekspor 1900×1100)
- Tidak ada tumpang tindih/teks terpotong di kedua halaman; Kesimpulan muat penuh.
- Klik NTB: peta kab/kota NTB + histogram (5/3/1/1). Klik Jawa Tengah: judul 12 (cocok t5: 12 dari 35 di atas median sejenis 9/9 tahun).
- Default Indonesia: 135 (sejenis) cocok t5; 66 persisten ganda cocok t5.
- Catatan: label slope Bab 1 tampil 2 desimal (nilai asli BPS), sesuai tabel.
- Belum diuji ulang di v7b: semua bobot 0 (logika tidak diubah), ekspor PDF, Tableau Public.


---
## 10. Revisi v7c (23 Nov) — Bab 1 lebih hidup, alur ①→②→③→Jadi
Tangkapan akhir: `deliverables/screenshots/v7c_hal1_final.png`, `v7c_hal2_final.png`.
- **Keputusan peta Bab 2: tetap tile map.** Peta poligon provinsi akan kembar dengan peta kab/kota di ④; tile map menyamakan ukuran provinsi kecil (DKI, DIY, Bali) dan memuat angka peringkat.
- **KPI + sparkline**: TPT nasional (2017–2025, t5), TPT SMK (2015–2025, t1), NEET (sumber NEET Nasional). Informal PT memakai angka 8,2% → 16,6% (tanpa sparkline karena ruang).
- **① Cermin terbalik** (menggantikan dumbbell): kupu-kupu 2025, TPT ke kiri dan informal ke kanan dengan dua skala terpisah (penyebut berbeda, sesuai aturan "satu sumbu per ukuran"). ≤SD dan SMK disorot. Pesannya terbaca dari bentuk: batang kiri ≤SD terpendek, batang kanan ≤SD terpanjang.
- **② Dua arah**: slope TPT turun ↘ dan informal naik ↗ (tetap).
- **③ Kasus SMK**: tren dengan anotasi "+3,19 saat COVID" di titik SMK 2020 (t1: 10,36 → 13,55) dan subjudul yang menyambung ke paradoks formal (informal SMK 35,8% vs SMA 43,8%).
- **Kartu alur** (menggantikan "Cara membaca"): ① Potret 2025 → ② Satu dekade → ③ Kasus SMK → Bab 2, dengan keterangan dua penyebut.
- **Kartu "Jadi"** mengikuti nomor yang sama, lalu menjembatani ke Bab 2.
- **Bab 2**: label kuadran hanya untuk provinsi kunci + yang dipilih (sebelumnya 38 label bertumpuk).
- **Palet kategori divalidasi** dengan `validate_palette.js` (skill dataviz): cobalt #2f5fa7, merah bata #e0603a, oxblood #a12a1c, hijau #3f9363 → lolos kecerahan, kroma, separasi buta warna (ΔE ≥ 12,5), dan kontras ≥ 3:1. Versi sebelumnya gagal (oxblood terlalu gelap, sage terlalu abu-abu).
- Catatan jujur: label baris kiri grafik kupu-kupu tetap tampil (lebar header 0 tidak dihormati Tableau), sehingga nama jenjang muncul di dua sisi; label "+3,19 saat COVID" sedikit menempel garis SMK.
