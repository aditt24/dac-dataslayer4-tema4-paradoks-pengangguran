# Changelog (bersama Codex / Claude Code)

## 2026-11-22 — Claude Code
- Salin FINAL.twbx Codex (ChatGPT\Datslay DA) ke folder proyek sebagai basis. Dibuka di Tableau 2026.3 (Free Edition).
- DAC_Dashboard_Tema4_FINAL.twbx: pie "H1-E Donut SMK Sektor" dilepas dari Hal 1 (15+ irisan, tak terbaca; sheet-nya masih ada di workbook). Disimpan dengan Ctrl+S.
- Verifikasi: tampilan Hal 1 diperiksa di presentation mode. Ruang kosong kanan-bawah Hal 1 belum diisi.
- (Claude Code, sesi lanjutan) Percobaan melepas legend 2015/2025 yang menimpa tombol "Lanjut ke Halaman 2" via GUI gagal: legend floating tidak bisa dipilih (Delete & klik kanan tidak bereaksi), jendela Tableau memotong kanvas 1900×1100. Tidak ada perubahan tambahan tersimpan.

## 2026-11-22 (malam) — Claude Code — edit XML disetujui user
Hal 1 di FINAL.twbx: legend 2015/2025 dipindah dari atas tombol 'Lanjut ke Halaman 2' ke kanan bar H1-F; H1-F diperlebar (w 55000) & ditinggikan; judul + sumbu berjudul untuk H1-D (COVID: SMK +3,2 poin = 3,19 di t1) dan H1-F (informal naik di semua jenjang, dicek dari t1); footer 2 baris. Diverifikasi dengan membuka ulang di Tableau (presentation mode): tidak ada tumpang tindih, semua baris bar terlihat. File perantara _xml1/_xml2/_xml3 boleh dihapus.
Hal 2: axis title dumbbell pembanding ("Informal (%): biru muda 2018, merah 2025"); percobaan KPI mark Text (tidak memperbaiki pemotongan). FINAL.twbx = hasil xml5; file _xml* dihapus. Screenshot: deliverables/screenshots/hal2-setelah-poles.jpg. Laporan: deliverables/FINAL_QA_REPORT.md.

## 2026-11-22 (~23:45) — Claude Code — poles Hal 2 (XML, diverifikasi di Tableau)
- Kuadran: kotak label diperlebar; label "Antrean Kerja Formal" ditambahkan (annotation id 3, x 78–100, y 2–14).
- Penimbang: judul ditampilkan & dipendekkan (Priority Lab + keterangan titik/pita/★); label tidak di-cull; lebar header wilayah 185; viewpoint Entire View di dashboard; latar sheet 'H2-G Pesan Bobot' dibuat transparan (sebelumnya menutupi label SULAWESI UTARA).
- KPI kab/kota: teks dinamis dipindah ke judul sheet + Entire View (sebelumnya terpotong "66 ka..").
- Dumbbell pembanding: Entire View.
- FINAL.twbx = versi h2e; file perantara dihapus. Screenshot: hal1-final-22nov.jpg, hal2-final-22nov.jpg.

## 2026-11-23 (dini hari) — Claude Code — uji interaksi & perbaikan bug
- Diuji di Tableau: Mode Peta, klik provinsi (NTB, Jateng), slider bobot (termasuk semua 0), Pembanding Jejak. Hasil di deliverables/FINAL_QA_REPORT.md.
- BUG heatmap jejak (mark hantu dari densifikasi table calc 'Batas Baris' × dimensi warna Status Tahun) diperbaiki: filter Batas Baris dilepas dari sheet H2-I Jejak KabKota; tabel menampilkan semua kab/kota terfilter (urut abjad). Teks KPI: "Gulir tabel untuk melihat semua."
- KPI: teks ke Detail + mark Circle transparan (hilangkan dobel & 'Abc').
- Format angka: tooltip peta (TPT 0.00, peringkat bulat), kuadran, Penimbang, label dumbbell (Measure Values).
- Viewpoint Entire View untuk 'H2-G Pesan Bobot' (pesan bobot 0 terpotong) — belum diverifikasi ulang.
- Catatan teknis: palet warna tidak diterapkan Tableau untuk instance agregat (min:/attr:) kalkulasi Status → tetap pakai dimensi none:.

## 2026-11-23 (siang) — Claude Code — REDESAIN v7 (desain, cerita, interaksi)
- Basis `DAC_desain_QA_v2.twbx` → `DAC_Dashboard_Tema4_FINAL.twbx` lewat `scripts/redesign_tableau_v7.py` (8 putaran, tiap putaran dibuka & diekspor 1900×1100 di Tableau; arsip di deliverables/qa_redesign/).
- Design system: paper/ink/cobalt(TPT)/vermilion(kerja tidak layak)/oxblood/sage; Georgia + Tableau Book; band judul gelap; kartu putih; gridline mati.
- Teks ditulis ulang: judul = temuan; kartu "Yang perlu diingat" (Bab 1) dan "Kesimpulan" (Bab 2); footer definisi & sumber.
- Peta: warna per kacamata (5 kelas, rampa biru TPT / merah bata KTL) via calc baru Calculation_9100000000000001; tile lebih besar.
- Baru: slope chart "Peringkat berbalik" (H2-S Lereng Peringkat; calc ..002 warna, ..003 label; alias Measure Names TPT/Kerja tidak layak).
- Dibuang dari dashboard & workbook: H1-C Heatmap Sektor, H1-E Donut, H2-E Teks Cerita (+ kontrol Langkah), H2-H Dumbbell/Mini Tile/Pesan Pembanding, H2-E Peta Geo.
- Default: Indonesia, kacamata "Kerja tidak layak", workbook dibuka di Bab 1. Caption kontrol: Bobot TPT/NEET/setengah pengangguran/informal, "Lihat peringkat menurut", "Acuan pembanding".
- Priority Lab: 10 provinsi (sebelumnya 15). Informal 2015 vs 2025: dot plot.
- Verifikasi: kacamata (NTB 34↔2, DKI 7↔38, Kepri 5↔37), klik NTB, slider, tombol Bab 1→2, angka teks dicek ke t1/t3/t5. Detail: deliverables/REDESAIN_V7_DESIGN_SYSTEM_DAN_QA.md.

## 2026-11-23 (siang) — Claude Code — v7b: audit informativeness
- Bab 1: COVID bar & dot plot informal dibuang; slope ganda baru `H1-S TPT Satu Dekade` + `H1-S Informal Satu Dekade`; tren TPT jadi baris bawah lebar (subjudul memuat COVID +3,19).
- Bab 2: tabel jejak + KPI kab/kota dibuang (tautologis di tampilan default); diganti `H2-K Peta KabKota` (sumber data spasial baru dari Spatial/IDN_kabkota_persistensi_v7.geojson) + `H2-K Sebaran Tahun` (histogram U). Keduanya ikut Pilih Provinsi & Acuan pembanding.
- Kesimpulan: "135 kab/kota selalu di atas median sejenis (66 juga di atas TPT nasional)" — dicek ke t5.
- Build: `TPL_TWB=scripts/template_peta_kabkota.twb python scripts/redesign_tableau_v7.py <QA_v2.twb> out.twb`; folder ekstrak harus berisi Data/Spatial/IDN_kabkota_persistensi_v7.geojson sebelum pack.
- Diverifikasi: render 1900×1100 kedua halaman, klik NTB, klik Jawa Tengah.

## 2026-11-23 (siang) — Claude Code — v7c: Bab 1 lebih hidup
- KPI sparkline (H1-P Spark TPT/SMK/NEET), "Cermin terbalik" (H1-C Cermin TPT/Informal) menggantikan H1-A Dumbbell, anotasi COVID di tren (calc Label Tren, ATTR agar garis tidak pecah), kartu alur & kartu "Jadi" bernomor, label kuadran hanya provinsi kunci.
- Palet kuadran/KTL diganti versi yang lolos validator dataviz (#e0603a, #a12a1c, #3f9363).
- Tile map provinsi dipertahankan (keputusan: peta poligon akan kembar dengan peta kab/kota).
- Diverifikasi: ekspor 1900×1100 kedua halaman (v7c_hal1_final.png, v7c_hal2_final.png).

## 2026-11-23 (±11.00) — Claude Code — sesi dihentikan user
- Semua jendela Tableau ditutup tanpa simpan (file perantara r1–r17 sudah dihapus). FINAL.twbx = v7c tidak berubah setelah verifikasi. Progres & memori diperbarui untuk dilanjutkan.

## 2026-11-23 sore — Claude Code — v8
- `scripts/redesign_tableau_v8.py` (basis = v7c FINAL.twb, bukan build ulang v7) → `DAC_Dashboard_Tema4_v8.twbx`. FINAL.twbx (v7c) tidak diubah.
- Hal 2: kartu H2-K1/K2/K3, sheet H2-R Keputusan, parameter Fokus (CASE di Total Bobot & Skor Dinamis), alias nama provinsi (nilai wilayah asli tetap), label Papua Tengah di kuadran, slope dikeluarkan dari dashboard.
- Hal 1: tata letak baru, 3 kartu angka, judul kalimat biasa, label 1 desimal (kode format Tableau diawali `*`; `#,##0.0` diabaikan pada label).
- GUI Tableau: Workbook Locale = Indonesian (Indonesia), animasi On 0,5 detik Simultaneous, lalu Ctrl+S. Skrip kini menulis keduanya juga.
- Diuji di Tableau 2026.3: buka tanpa error; NTB 34→2 / Rentan Tersembunyi / 35% / selisih −21 −12 +42 +14; klik DKI → 7→38, baris Antrean Kerja Formal disorot; Fokus "Perbaiki mutu kerja" → Papua Tengah, Aceh, Maluku, NTB, Sulbar; Atur sendiri + semua bobot 0 → pesan muncul. Screenshot: deliverables/screenshots/v8_hal1.jpg, v8_hal2.jpg.
