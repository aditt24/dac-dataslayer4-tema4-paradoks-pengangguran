# PROJECT PROGRESS — Datslay DA

Last updated: 2026-11-23 ±11.00 WIB · Last updated by: Claude Code
DEADLINE LOMBA: 23 Nov 2026 23.59 WIB (ZIP ≤100 MB + PDF GForm)

## STATUS v8 (23 Nov ±16.05 WIB, Claude Code)
- `DAC_Dashboard_Tema4_v8.twbx` jadi dan tersimpan dari Tableau (locale Indonesia, animasi 0,5 dtk). Build: `python scripts/redesign_tableau_v8.py <ekstrak FINAL.twbx>/DAC_Dashboard_Tema4_FINAL.twb out.twb` lalu `pack_twbx.py` (lalu set ulang locale/animasi tidak perlu: skrip sudah menulisnya).
- LULUS diuji: buka tanpa error, kartu NTB/DKI, sorot tipe, Fokus "Perbaiki mutu kerja", pesan bobot 0, koma desimal.
- BELUM DIUJI: Jateng, Papua Tengah, Maluku di kartu; Acuan pembanding; Fokus lain selain 1; ekspor gambar/PDF 1900x1100; animasi saat klik.
- Revisi desain (16.20–17.15): kartu Cek provinsimu + menu "Provinsi" (pilih tanpa klik peta; diuji Papua Tengah 28→1, 87%), grafik "Langkah per tipe" satu baris per tipe (warna tipe terpilih, lainnya pudar), latar tint 96% + garis aksen kiri pada kartu angka (biru = TPT, merah bata = informal), KPI berkoma via angka bulat+desimal, label kuadran dua baris. Referensi pola: proyek lokal ASAP Gelar Rasa (daftar prioritas satu baris, kartu KPI aksen kiri).
- Kekurangan tampilan tersisa: label kuadran "Rentan Ter-sembunyi"/"Antrea-n Kerja" patah; label tile map bertumpuk; baris Priority Lab rapat; sumbu tren 2014–2026; narasi di bawah peta masih nama kapital; P1 "3 teratas warna penuh" dan P2 lollipop tidak dikerjakan.

## STATUS TERKINI (baca ini dulu) — dihentikan user 23 Nov ±11.00 WIB untuk dilanjut nanti
- **Workbook final: `DAC_Dashboard_Tema4_FINAL.twbx` = v7c** (1.950.874 byte, 23 Nov 11:00), dicek di Tableau 2026.3 lewat Dashboard > Export Image 1900×1100. Tableau sudah ditutup; semua jendela uji ditutup TANPA simpan (jendela lama berjudul FINAL juga "No" agar v7c tidak tertimpa).
- Cadangan: `DAC_Dashboard_Tema4_FINAL_pre_v7.twbx` (versi sebelum redesain), `DAC_desain_QA_v2.twbx` (basis build, JANGAN dihapus), BACKUP/new (asli tim).
- Isi v7c: Bab 1 = KPI+sparkline, ① Cermin terbalik (kupu-kupu 2 skala), ② slope TPT turun/informal naik, ③ tren SMK + anotasi COVID, kartu alur & "Jadi". Bab 2 = ① tile map dua kacamata (TETAP tile map) + slope peringkat, ② kuadran (label kunci saja), ③ Priority Lab, ④ peta 514 kab/kota + histogram U, Kesimpulan.

## INVENTARIS UNTUK AUDIT
| File | Isi |
|---|---|
| `scripts/redesign_tableau_v7.py` | seluruh redesain (XML) dari basis QA_v2; jalankan dengan env `TPL_TWB=scripts/template_peta_kabkota.twb` |
| `scripts/pack_twbx.py` | kemas .twb + Data/Image jadi .twbx |
| `scripts/siapkan_geojson_persistensi_v7.py` | GeoJSON kab/kota disederhanakan + atribut t5 → `Spatial/IDN_kabkota_persistensi_v7.geojson` |
| `scripts/template_peta_kabkota.twb` | definisi sumber data spasial (dibuat di Tableau GUI) |
| `deliverables/REDESAIN_V7_DESIGN_SYSTEM_DAN_QA.md` | design system, audit grafik, riset, QA (bagian 9 = v7b, 10 = v7c) |
| `deliverables/screenshots/v7c_hal1_final.png`, `v7c_hal2_final.png` | tampilan akhir 1900×1100 |
| `deliverables/qa_redesign/` | tangkapan tiap putaran QA + `template_peta_kabkota.twbx` |
| `AI_PROJECT_CHANGELOG.md`, `AI_PROJECT_DECISIONS.md` | log perubahan & keputusan |

Cara build ulang: ekstrak `DAC_desain_QA_v2.twbx` ke folder X, salin `Spatial/IDN_kabkota_persistensi_v7.geojson` ke `X/Data/Spatial/`, lalu
`TPL_TWB=scripts/template_peta_kabkota.twb python scripts/redesign_tableau_v7.py X/DAC_desain_QA_v2.twb X/out.twb` dan
`python scripts/pack_twbx.py X/out.twb X DAC_Dashboard_Tema4_FINAL.twbx DAC_Dashboard_Tema4_FINAL.twb`.

Pelajaran teknis XML Tableau: atribut `<zone>` urut abjad; palet kalkulasi baru butuh `<column-instance>` level datasource + nama `Calculation_<angka>`; di sheet multi-sumber, sumber data utama harus tercantum pertama (sebelum Parameters); dimensi di Tooltip/Label pakai `attr:` (kalau `none:` garis terbelah / pill merah); urutan elemen pane: customized-tooltip sebelum customized-label; Ctrl+W = tukar baris/kolom; jangan klik tab "Data Source".

## SISA TUGAS (prioritas, deadline 23 Nov 23.59 WIB)
1. [NOT STARTED] Uji: semua bobot 0 (pesan muncul, tidak terpotong), klik satu provinsi Papua baru, Acuan pembanding Nasional↔Sesama. (LULUS: kacamata TPT↔KTL, klik NTB, klik Jawa Tengah → 12, slider, tombol Bab 1→2.)
2. [NOT STARTED] Ekspor PDF 2 halaman dari FINAL, cek watermark & teks.
3. [BLOCKED: akun user] Publish Tableau Public; tempel link ke PDF (FAQ 37).
4. [NOT STARTED] ZIP ≤100 MB: PDF, FINAL.twbx, Raw_Dataset, Processed_Dataset, Spatial (geojson v7), surat orisinalitas bermeterai (dari user).
5. Opsional: rapikan twbx perantara lama di root (h2d, h2e, desain_*, verifikasi_*, uji_bobot_nol, revisi_verifikasi_23nov); commit/push repo HANYA bila user minta (atas nama aditt24, tanpa atribusi AI).
Kekurangan kecil yang diketahui: label jenjang kupu-kupu tampil di dua sisi; label "+3,19 saat COVID" menempel garis; label slope Bab 1 dua desimal.

---
## ARSIP (status sebelum v7)

Last updated: 2026-11-22 (malam) · Last updated by: Claude Code
Directory: C:\Users\LENOVO\OneDrive\Documents\Datslay DA · Branch: main
DEADLINE LOMBA: 23 Nov 2026 23.59 WIB (ZIP ≤100 MB + PDF GForm)

## 1. Status
Fase: audit selesai, implementasi di Tableau BELUM dimulai. Estimasi selesai: tidak diklaim; workbook sudah ~80% terbangun oleh tim, polesan/QA belum.

## 2. Persyaratan asli
Master Execution Prompt + Additional Innovation Prompt (diberikan user 22 Nov di chat; tidak tersimpan sebagai file). Inti: poles workbook existing jadi dashboard kelas finalis lewat Tableau Desktop (Computer Use), riset desain, inovasi (Paradox Reveal, Priority Lab) HANYA bila berbasis data & andal, QA jujur, deliverable di research/ dan deliverables/.
Batasan wajib lomba: maks 2 halaman 1900×1100, watermark tak diubah, data BPS, tanpa Smart Narrative/Q&A, estimasi diberi label.

## 3. Warisan
| Item | Status terverifikasi |
|---|---|
| new.twbx == BACKUP.twbx | identik byte (19:07). JANGAN diubah |
| WORKING.twbx | lebih baru (20:14); 25 sheet, 3 dashboard |
| Spek: docs/SPEK_DASHBOARD_TABLEAU.md | acuan layout & calc |
Detail: research/INITIAL_WORKBOOK_AUDIT.md

## 3b. TEMUAN KONTINUITAS (penting)
Agen lain (Codex) bekerja di folder BERBEDA: `Documents\ChatGPT\Datslay DA` (FINAL.twbx 20:14, 22 sheet, hanya 2 dashboard, default Indonesia/TPT; 4 screenshot). Itu versi paling maju. Sudah disalin ke folder proyek sebagai DAC_Dashboard_Tema4_FINAL.twbx (sumber asli tidak diubah), screenshot disalin ke deliverables/screenshots. JANGAN mulai dari WORKING (masih 3 halaman, default lama). Codex tidak menulis AI_PROJECT_* maupun research/.

## 4. Tugas
- [COMPLETED] Audit XML 3 workbook, baca spek & memori
- [COMPLETED] Buka FINAL.twbx di Tableau 2026.3, audit visual Hal 1 (Computer Use disetujui)
- [IN PROGRESS] Perbaikan Hal 1: pie dibuang (selesai, NEEDS VERIFICATION setelah reopen); sisa: ruang kosong kanan-bawah, legend warna 2015/2025 menimpa tombol 'Lanjut ke Halaman 2', judul bar COVID & bar Informal 2015v2025 kurang jelas ('Nilai'), sorotan kuning di header Jenjang, footer terpotong. Hal 2 belum diaudit visual.
- [COMPLETED] Hal 3 sudah tidak ada di FINAL (hanya 2 dashboard; terverifikasi di XML)
- [NEEDS VERIFICATION] Default FINAL: Pilih Provinsi=Indonesia, Mode Peta=TPT, Langkah Cerita=2 (spek PDF minta Mode Peta=KTL & Langkah 1; putuskan)
- [NOT STARTED] Polesan visual, tooltip, navigasi, tombol reset
- [NOT STARTED] Riset desain ringkas (research/TABLEAU_DESIGN_BENCHMARK.md)
- [NOT STARTED] Inovasi: Paradox Reveal (sudah ada Mode Peta + Teks Cerita; perlu dipoles), Priority Lab (slider bobot sudah ada)
- [NOT STARTED] QA, screenshot ke deliverables/screenshots, FINAL.twbx, FINAL_QA_REPORT, CHANGELOG
- [NOT STARTED] Paket ZIP kumpul + PDF

## 5. Tugas aktif
Meminta akses Computer Use untuk "Tableau 2026.3". Next: buka WORKING.twbx, screenshot tiap dashboard.

## 7. Temuan penting
- Hanya 1 aksi (parameter action "Klik provinsi").
- Default tersimpan: Pilih Provinsi=MALUKU, Langkah Cerita=2 (spek: Indonesia, 1).
- Donut/pie (H1-E, H2-J) kemungkinan redundan.

## 8. Blocker
Computer Use perlu persetujuan user; Tableau tidak boleh diedit via XML untuk perubahan desain (instruksi user).

## 12. Instruksi agen berikut
Baca file ini + AI_PROJECT_DECISIONS.md, lalu lanjut ke tugas aktif. Kerja di WORKING.twbx, simpan FINAL sebagai DAC_Dashboard_Tema4_FINAL.twbx. Jangan hapus BACKUP/new.

## 13. Riwayat
### 2026-11-22 — Claude Code
Audit saja. File dibuat: research/INITIAL_WORKBOOK_AUDIT.md, AI_PROJECT_PROGRESS.md, AI_PROJECT_DECISIONS.md. Workbook belum diubah.

### Catatan lanjutan (Claude Code, 22 Nov malam)
Poles via GUI lambat: kanvas dashboard 1900x1100 terpotong di layar, legend floating (2015/2025, di atas tombol 'Lanjut ke Halaman 2') tak bisa dipilih lewat klik/Delete/klik kanan. Opsi: (a) pilih lewat Layout > Item hierarchy / perkecil layar, (b) edit layout via XML .twb lalu verifikasi di Tableau (butuh izin user karena prompt induk melarang edit XML). Exact next action: tunggu keputusan user soal (b); jika (a), perbaiki legend, beri judul bar COVID & bar 2015v2025, isi ruang kosong kanan-bawah Hal 1, lalu audit Hal 2.

### Checkpoint 2 (Claude Code, 22 Nov ~23:30)
Hal 1 dipoles & diverifikasi (lihat changelog). Hal 2 diaudit: perbaikan sumbu dumbbell selesai; KPI 66 terpotong, kotak label kuadran, legend warna kuadran/penimbang, nama provinsi terpotong di Penimbang, mini tile map = BELUM. FINAL.twbx di folder proyek adalah versi terkini. Cara kerja efektif: unzip twbx ke folder sementara, edit .twb dengan Python (urutan atribut zone alfabetis: h sebelum id; id zone dipakai ulang antar dashboard), zip ulang (pack.py: .twb pertama), buka di Tableau untuk verifikasi, tutup dengan 'No' bila ditanya simpan.
P0 berikutnya: (1) perbaiki kuadran (legend, kotak label), (2) Penimbang (lebar label, legend), (3) KPI terpotong, (4) uji interaksi satu per satu, (5) screenshot Hal 1, (6) PDF + ZIP + surat bermeterai + publish Tableau Public sebelum 23 Nov 23.59.

### Checkpoint 3 (Claude Code, 22 Nov ~23:45)
Hal 2 dipoles & diverifikasi (lihat changelog + deliverables/FINAL_QA_REPORT.md). Trik penting: sheet kecil yang teksnya terpotong → set `<zoom type='entire-view' />` di viewpoint jendela dashboard. FINAL.twbx terkini di folder proyek. Banyak jendela Tableau terbuka dari file perantara (sudah dihapus) — tutup tanpa menyimpan.
P0 berikutnya: (1) uji interaksi: klik provinsi, slider (termasuk semua 0), Mode Peta, Langkah cerita, Pembanding Jejak; (2) mini tile map panel Pembanding; (3) tentukan default Mode Peta untuk PDF (spek: KTL); (4) ekspor PDF 2 halaman, publish Tableau Public, ZIP ≤100 MB + surat bermeterai, sebelum 23 Nov 23.59 WIB.

### Checkpoint 4 (Claude Code, 23 Nov dini hari)
Uji interaksi selesai untuk Mode Peta, klik provinsi, slider, Pembanding Jejak (lulus; detail di QA report). Bug serius heatmap jejak diperbaiki (lihat changelog) — JANGAN pasang lagi filter table calc di sheet itu. FINAL.twbx = versi t5.
Sisa: (1) verifikasi pesan bobot 0, (2) skor KTL tooltip 4 desimal, (3) uji Langkah cerita, (4) mini tile map Pembanding, (5) default Mode Peta untuk PDF, (6) PDF + Tableau Public + ZIP + surat bermeterai sebelum 23 Nov 23.59 WIB.

### Checkpoint 5 (Claude Code, 23 Nov dini hari) — HANDOVER KE CODEX
Claude Code berhenti di sini atas permintaan user. Prompt lengkap untuk agen berikutnya: `PROMPT_CODEX_LANJUTAN.md` (tugas P0/P1/P2/Pengumpulan, cara kerja edit XML, jebakan, QA, protokol). Audit isi vs KONSEP_FINAL v6: belum masuk H6 struktur ekonomi, nuansa ρ −0,30 + validasi KTL, legend dumbbell Hal 1, alur bernomor Hal 2, penutup rekomendasi yang terbaca, urutan jejak menurut keparahan, mode cerita. Workbook kerja: DAC_Dashboard_Tema4_FINAL.twbx.
