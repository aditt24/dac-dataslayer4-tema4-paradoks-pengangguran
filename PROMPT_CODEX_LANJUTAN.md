# PROMPT HANDOVER UNTUK CODEX — DAC Data Slayer 4.0 Tema 4
Ditulis oleh Claude Code, 23 Nov 2026 dini hari. Salin seluruh isi file ini ke Codex.

---

## 0. PERAN & TARGET

Kamu (Codex) mengambil alih proyek dashboard lomba **DAC Data Slayer 4.0, Tema 4, "Paradoks Pengangguran Rendah"** dari Claude Code. Kerjakan sampai SEMUA tugas di bagian 6 selesai, terverifikasi di Tableau, dan paket pengumpulan siap. Jangan mulai dari nol, jangan membuat workbook baru, jangan membuat dokumen progres pesaing.

**DEADLINE MUTLAK: Senin 23 November 2026 pukul 23.59 WIB** (ZIP ≤ 100 MB + PDF terpisah di Google Form). Sisakan minimal 2 jam terakhir untuk PDF, ZIP, dan unggah.

Kerjakan dengan urutan prioritas P0 → P1 → P2 → Pengumpulan. Jika waktu menipis, lewati P2, jangan lewati Pengumpulan.

---

## 1. LOKASI & FILE (BACA DULU, URUT)

Folder proyek (SATU-SATUNYA tempat kerja; jangan pakai `Documents\ChatGPT\Datslay DA` lagi, itu folder lama Codex yang isinya sudah disalin ke sini):
`C:\Users\LENOVO\OneDrive\Documents\Datslay DA`

Baca berurutan sebelum menyentuh apa pun:
1. `AI_PROJECT_PROGRESS.md` — status bersama + checkpoint 1–4.
2. `AI_PROJECT_DECISIONS.md` — keputusan yang tidak boleh dibalik tanpa alasan tertulis.
3. `AI_PROJECT_CHANGELOG.md` — semua perubahan Claude Code (termasuk bug yang sudah diperbaiki).
4. `deliverables/FINAL_QA_REPORT.md` — apa yang lulus / gagal / belum diuji.
5. `KONSEP_FINAL_DAC_TEMA4.md` (v6) — SUMBER KEBENARAN isi & klaim. Perhatikan label [DATA]/[TERUJI]/[BERSYARAT]/[ESTIMASI]/[PAPER]/[GUGUR].
6. `docs/SPEK_DASHBOARD_TABLEAU.md` — spek layout, parameter, calc, palet.
7. `research/INITIAL_WORKBOOK_AUDIT.md`.
8. `GUIDEBOOK DAC.pdf` bila perlu cek aturan.

Workbook:
| File | Status |
|---|---|
| `DAC_Dashboard_Tema4_FINAL.twbx` | **VERSI KERJA TERKINI** — semua perbaikan ada di sini |
| `DAC_Dashboard_Tema4_BACKUP.twbx` / `DAC_Dashboard_Tema4_new.twbx` | asli tim (identik), JANGAN diubah/dihapus |
| `DAC_Dashboard_Tema4_WORKING.twbx` | versi lama 3 halaman, jangan dipakai |

Data dashboard: `Processed_Dataset/tableau/t1…t8*.csv`. Hasil analisis pendukung: `Processed_Dataset/v5/` (log `_log_v5.txt`, `B_uji_ketahanan.csv`, `C_loading_faktor.csv`, `D_transisi_2018_2025.csv`) dan `Processed_Dataset/v6/`.

Screenshot hasil terakhir: `deliverables/screenshots/hal1-final-22nov.jpg`, `hal2-final-22nov.jpg`, `hal2-jateng-nasional-setelah-fix-jejak.jpg`, `hal2-paradox-reveal-mode-ktl.jpg`.

Repo GitHub publik: `github.com/aditt24/dac-dataslayer4-tema4-paradoks-pengangguran` (branch main). Repo lokal = folder proyek. **Jika commit/push: WAJIB atas nama akun `aditt24`, TANPA baris atribusi AI.** Jangan push file rahasia. Key WebAPI BPS hanya lewat env var `BPS_KEY`, tidak pernah ditulis ke file.

---

## 2. ATURAN LOMBA (TIDAK BOLEH DILANGGAR)

- Dashboard wajib Tableau (atau Power BI/Looker; tim memakai **Tableau**). Python/R hanya untuk olah data.
- **Maksimal 2 halaman**, ukuran **1900 × 1100** (fixed). Tab/bookmark/dynamic zone di dalam satu halaman tetap dihitung 1 halaman. Hindari drillthrough.
- **Watermark resmi** (`Image/New_Watermark.png`, latar bitmap tiap dashboard; bingkai pink) TIDAK boleh diubah, dipindah, ditutup, atau dihapus.
- Semua data statistik dari BPS. Geometri geoBoundaries DIIZINKAN panitia (hanya bentuk wilayah). Caption wajib bila peta poligon dipakai: "Batas wilayah: geoBoundaries IDN ADM2 (CC BY 3.0 IGO), hanya geometri. Seluruh angka: BPS."
- DILARANG fitur AI Tableau/Power BI: Smart Narrative, Q&A, Key Influencers, Tableau Agent/Pulse. Narasi dinamis HARUS dari calculated field biasa.
- Estimasi/proyeksi wajib diberi label (urbanisasi 2018 = interpolasi proyeksi; TPT provinsi induk untuk 4 provinsi Papua baru sebelum 2024).
- Penilaian penyisihan: Analisis 40%, Tema & pesan 30%, Desain 30%.
- Isi ZIP: PDF dashboard, `.twbx`, raw data BPS, data olahan, surat orisinalitas bermeterai. PDF juga diunggah terpisah. Link Tableau Public "Anyone with the link" dimasukkan ke PDF (FAQ 37).

---

## 3. ATURAN INTEGRITAS ANALISIS

- Jangan mengubah angka, definisi indikator, metode, atau hasil analisis. Setiap angka yang kamu tulis di judul/kartu HARUS kamu cek ke CSV di `Processed_Dataset/` (tulis buktinya di changelog).
- Tidak ada klaim kausal. Kuadran = klasifikasi relatif (batas median 38 provinsi), bukan kategori resmi.
- TPT vs KTL: klaim yang sah hanya **"TPT tidak mencerminkan kerja layak"** (ρ = −0,302; p = 0,066). DILARANG menulis "berkebalikan/terbalik".
- Stabilitas 1.000 skenario = "share skenario bobot yang diuji", BUKAN probabilitas risiko.
- Provinsi Pembanding = konteks deskriptif, TANPA target dan tanpa "bisa belajar dari".
- Forecast BUKAN headline; bacaannya: posisi kab/kota persisten/struktural.
- Klaim [GUGUR] tidak boleh muncul ("provinsi terdidik lebih formal", "kembaran memberi target").

---

## 4. CARA KERJA TEKNIS YANG TERBUKTI JALAN (PAKAI INI)

Tableau Desktop di laptop: **Tableau 2026.3 (Free Edition)**. Kanvas 1900×1100 lebih besar dari layar (1456 px) sehingga edit layout via GUI sangat lambat dan beberapa objek floating tidak bisa dipilih. User SUDAH MENGIZINKAN edit XML `.twb`, dengan syarat setiap perubahan diverifikasi dengan membuka ulang di Tableau.

Alur:
1. Ekstrak `DAC_Dashboard_Tema4_FINAL.twbx` (zip) ke folder kerja sementara (bukan di folder proyek), mis. `F2/`. Isinya: `DAC_Dashboard_Tema4_FINAL.twb`, `Data/TableauTemp*/…hyper`, `Image/New_Watermark.png`.
2. Backup `.twb` sebelum tiap batch edit.
3. Edit `.twb` dengan skrip Python (string replace / regex), BUKAN tangan; setiap replace pakai `assert count == n`.
4. Validasi XML: `xml.etree.ElementTree.parse(...)`.
5. Zip ulang dengan `.twb` sebagai entri pertama, path relatif pakai `/`:
```python
import zipfile, os, glob, sys
src, out = sys.argv[1], sys.argv[2]
twb = glob.glob(os.path.join(src, '*.twb'))[0]
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(twb, os.path.basename(twb))
    for root, _, fs in os.walk(src):
        for f in fs:
            fp = os.path.join(root, f)
            if fp != twb:
                z.write(fp, os.path.relpath(fp, src).replace(os.sep, '/'))
```
6. Simpan sebagai file perantara di folder proyek (mis. `DAC_Dashboard_Tema4_FINAL_c1.twbx`), buka di Tableau (Ctrl+O, ketik path), maksimalkan jendela, F7 (presentation mode), klik "Lanjut ke Halaman 2 →", screenshot, cek.
7. Jika benar → salin menimpa `DAC_Dashboard_Tema4_FINAL.twbx`, hapus file perantara. Jika Tableau bertanya "save changes?" pada jendela uji → pilih **No**.

Fakta XML yang penting (sudah dipelajari, jangan diulang):
- Koordinat zona dashboard dalam satuan 0–100000 (x/w terhadap 1900 px, y/h terhadap 1100 px). Setiap zona dashboard tercatat **2 kali** (daftar datar + versi bersarang dengan `zone-style`); ubah keduanya.
- Atribut zona disimpan urut abjad (`h` sebelum `id`); jangan regex yang mengandalkan urutan lain.
- **ID zona dipakai ulang antar dashboard** (mis. id 20 ada di Hal 1 dan Hal 2) → selalu batasi ke blok `<dashboard name='…'>` atau cocokkan juga `name=`/`type-v2=`.
- Sheet kecil yang teksnya terpotong ("66 ka..", "Isi m..") → tambahkan `<zoom type='entire-view' />` di `<viewpoint name='…'>` dalam `<window class='dashboard' name='Hal 2 - Provinsi ke KabKota'>`.
- Judul sheet: `<layout-options><title><formatted-text><run fontsize='13'>…</run></formatted-text></title></layout-options>` diletakkan sebelum `<table>`; zona dashboard harus TANPA `show-title='false'` agar tampil. Judul boleh memuat field dinamis `<run><![CDATA[<[ds].[field]>]]></run>` asal field ada di sheet (boleh di Detail/`<lod>`).
- Baris baru di formatted-text = `<run>Æ&#10;</run>`.
- Format angka: `<style-rule element='cell'><format attr='text-format' field='[ds].[sum:x:qk]' value='#,##0.0' /></style-rule>` di `<style>` level tabel (yang tepat sebelum `<panes>`). HATI-HATI: jangan salah mengenali `<style-rule` sebagai `<style>` (bug skrip lama). Untuk label Measure Values pakai field `[ds].[Multiple Values]`.
- Judul sumbu: `<format attr='title' class='0' field='…' scope='cols|rows' value='…' />` dalam `<style-rule element='axis'>`.
- Palet warna disimpan di datasource (`<encoding attr='color' field='[none:…:nk]' type='palette'>`). Palet TIDAK diterapkan Tableau untuk instance agregat (`min:`/`attr:`) dari calc Status → tetap pakai dimensi `none:`.
- Datasource utama provinsi/kab-kota: `federated.0dzsn910err68y1dlgf4w1omb1y9` (caption "Provinsi & KabKota"; relasi t3↔t4 `wilayah=provinsi`, t3↔t5_jejak `wilayah=nama_prov`, t5_jejak↔t5_tren `kode=kode`, t3↔t6 `wilayah`). Jenjang: `federated.0t1aunm074zhqx179uzcf086kdei` (t1). Sektor: `federated.1auzfvc1qglsf71g09xly1cy9u96` (t2).
- Parameter (nama internal): Pilih Provinsi `[Parameter 0379056854634496]` (default "Indonesia"), Mode Peta `…379056` (default "Pengangguran (TPT)"), Pembanding Jejak `[Parameter 0379056854831106]` (default "Sesama kota/kabupaten"), Langkah Cerita `…854941699` (nilai tersimpan 2), W TPT/NEET/Setengah/Informal (0,25).
- Hanya ada 1 aksi: parameter action "Klik provinsi" (set Pilih Provinsi).

Jebakan Computer Use yang sudah terjadi:
- Klik tiga kali pada kotak parameter membuka dialog "Edit Title" dan ketikan masuk ke judul → batalkan dengan Cancel. Untuk mengubah slider, klik tombol panah `<` `>` (langkah 0,05).
- Jendela Claude/Codex bisa memegang fokus keyboard; klik dulu jendela Tableau sebelum mengirim tombol.
- Banyak jendela Tableau uji mungkin masih terbuka: tutup tanpa menyimpan.

**JANGAN pasang lagi filter table calculation (RANK/INDEX) pada sheet `H2-I Jejak KabKota`.** Itu penyebab bug "mark hantu" (densifikasi Tableau membuat kotak "Di atas acuan" tanpa data). Bug sudah diperbaiki dengan melepas filter `Batas Baris`.

---

## 5. KONDISI SAAT INI (TERVERIFIKASI)

Halaman 1 "Dua Wajah Masalah Kerja Lulusan": 4 KPI (TPT nasional 4,85%, TPT SMK 8,63%, informal PT 8,2→16,6%, NEET 19,4%), A Dumbbell TPT vs informal 2025, B Tren TPT 2015–2025 (SMK & SMA disorot, garis COVID), D Bar kenaikan TPT 2019→2020 (judul: SMK +3,2 poin, cek t1 = 3,19), C Heatmap jenjang × sektor 2025, F Bar informal non-pertanian 2015 vs 2025 per jenjang (legend di kanan), 2 kalimat insight, footer definisi + sumber, tombol "Lanjut ke Halaman 2 →". Pie 15 irisan sudah dibuang.

Halaman 2 "Pengangguran Rendah, Kerja Tidak Layak — Dari Provinsi ke Kab/Kota": Mode Peta (dropdown), narasi dinamis provinsi, Langkah (dropdown), E Peta berbalik (tile map, angka = peringkat, 1 = paling buruk), F Kuadran (4 label kuadran, garis median), G Priority Lab (4 slider, 15 provinsi, pita p05–p95, ★ Aceh/Maluku/Maluku Utara), H Panel Pembanding (mini tile map + dumbbell informal 2018 vs 2025 + kartu metode), I KPI kab/kota + Pembanding Jejak + heatmap kab/kota × 2017–2025 (Indonesia = 66 persisten ganda, urut ABJAD), kartu metode forecast, footer rekomendasi, tombol "← Halaman 1".

Interaksi LULUS (diuji): Mode Peta (NTB 34→2, DKI 7→38, Aceh 9→3), klik provinsi (NTB, Jawa Tengah: narasi, kuadran, pembanding Jatim/Sulsel/Sumsel, KPI 0 / 4, tabel jejak), slider (urutan berubah; semua 0 → kosong + pesan), Pembanding Jejak (setelah fix), navigasi 2 arah.

---

## 6. DAFTAR TUGAS SAMPAI SELESAI

Untuk SETIAP tugas: kerjakan → verifikasi di Tableau (screenshot) → cek angka ke CSV → catat di `AI_PROJECT_CHANGELOG.md` dan status di `AI_PROJECT_PROGRESS.md`.

### P0 — Isi & alur (wajib)

P0-1. **Legend dumbbell Hal 1 (H1-A).** Pembaca tidak tahu titik mana TPT dan mana informal. Tambahkan legend yang jelas (mis. ubah judul/subjudul: "● biru = pengangguran (TPT, % angkatan kerja) · ● oranye = informal non-pertanian (% pekerja non-pertanian)") — cek dulu warna sebenarnya di XML/Tableau. Jelaskan bahwa denominator berbeda.

P0-2. **Alur Hal 2 bernomor + jembatan.** Beri nomor ①–⑤ pada judul panel sesuai alur corong konsep §3: ① Peta berbalik, ② Empat tipe masalah, ③ Priority Lab, ④ Provinsi pembanding, ⑤ Jejak kab/kota. Tambahkan kalimat jembatan singkat (konsep §3): sebelum ④ "Provinsi mana yang kondisinya mirip pada 2018, dan bagaimana perubahannya?"; sebelum ⑤ "Apakah rata-rata provinsi juga menyembunyikan sesuatu?". Pastikan urutan baca kiri→kanan, atas→bawah masuk akal. Perbesar/tebalkan judul halaman Hal 2 agar hierarki jelas.

P0-3. **Kotak penutup "Kesimpulan & rekomendasi" yang terbaca** (gantikan footer rekomendasi kecil yang terpotong). Isi diambil dari konsep §7 (tanpa angka target): Rentan Ganda (Aceh, Maluku, Malut) → padat karya formal, job matching, program NEET second chance; Rentan Tersembunyi (NTB, Sulbar, NTT) → hilirisasi pertanian, formalisasi usaha mikro; Antrean Kerja Formal (DKI, Kepri, Banten) → percepat penyerapan, cegah informalisasi metropolitan; 66 kab/kota persisten ganda → program jangka panjang; lulusan SMK → evaluasi berbasis kerja layak (tracer study). Satu kalimat takeaway: "Angka agregat (TPT, rata-rata provinsi) menyembunyikan kerja tidak layak dan kantong pengangguran yang bertahan." Font ≥ 10 pt, tidak menabrak tombol "← Halaman 1" atau watermark.

P0-4. **Kartu H6 "Struktur ekonomi, bukan lama sekolah"** (insight final konsep yang belum ada). Bukti di `Processed_Dataset/v5/_log_v5.txt` baris 62–78 & 84–100 dan `B_uji_ketahanan.csv`: 38 provinsi urban~KTL ρ = −0,722; parsial urban~KTL | RLS = −0,669 (p < 0,001); RLS~KTL | urban = −0,144 (p = 0,39); tanpa Papua parsial urban −0,720, RLS 0,009. Opsi implementasi (pilih yang muat): (a) kartu teks ringkas dengan angka di atas, atau (b) scatter kecil t3 `urban` vs `ktl` (kolom ada di `t3_provinsi_2025.csv`; tandai provinsi `urban_dari_induk`=TRUE sebagai ESTIMASI). Jangan klaim kausal ("lebih terkait", bukan "menyebabkan").

P0-5. **Nuansa T5 + validitas KTL** di catatan metode/tooltip kuadran (kalimat pendek): "Peringkat TPT dan kerja tidak layak hanya berkorelasi lemah (ρ = −0,30; p = 0,066): TPT tidak bisa dipakai menilai kerja layak. Skor kerja tidak layak sejalan dengan kemiskinan (ρ = 0,66) dan berlawanan dengan pekerja formal (ρ = −0,92); keduanya tidak dipakai menyusun skor. Dua dimensi terpisah menurut PCA (KMO 0,65; Bartlett p < 0,001)." Cek angka di `B_uji_ketahanan.csv` dan `C_loading_faktor.csv`.

P0-6. **Urutkan tabel jejak menurut keparahan**, bukan abjad: urut `rata_tpt` menurun (kolom ada di t5_kabkota_jejak; di sheet berperan dimension ordinal). Cara aman tanpa table calc: computed-sort `nama` menurut agregat rata_tpt, ATAU taruh field urut sebagai dimensi baris tersembunyi (header disembunyikan). Verifikasi: tampilan Indonesia dibuka dengan Kota Ambon (≈12,0%), Kota Makassar, Kota Padang, Kab. Serang, Kota Sorong di atas (konsep §5.4). Pastikan jumlah baris Indonesia = 66 dan Jateng (Pilih Provinsi) = 35 baris dengan 4 persisten ganda; status per tahun tetap benar (Banjarnegara acuan Nasional: di bawah 2017–2021, di atas 2022–2025).

P0-7. **Mode cerita (Langkah 1–4)**: uji. Calc `Teks Cerita` (CASE 4 langkah) ditampilkan di sheet `H2-E Teks Cerita`, tapi teksnya tidak terlihat di layar. Pastikan: dropdown Langkah mengubah teks sorotan yang terlihat jelas (ukuran cukup, tidak tertutup peta), isi tiap langkah benar terhadap data, dan default PDF masuk akal. Jika tidak bisa dibuat andal, sembunyikan kontrolnya (jangan biarkan kontrol yang tak berfungsi).

P0-8. **Verifikasi sisa perbaikan Claude Code**: (a) pesan saat semua bobot 0 tidak terpotong (Entire View sudah dipasang untuk `H2-G Pesan Bobot`); (b) skor KTL di tooltip peta masih 4 desimal (67.5168) walau format `#,##0.0` sudah ada — perbaiki (mis. ROUND di calc tooltip atau format default kolom `ktl`).

### P1 — Kejelasan & buang yang tidak informatif

P1-1. Panel Pembanding: mini tile map tidak terbaca → ganti dengan daftar teks dinamis "Pembanding [provinsi]: P1, P2, P3 (kemiripan kondisi 2018)" memakai calc `P1/P2/P3 Terpilih` yang sudah ada; atau perbaiki tile agar terbaca. Pertahankan kartu metode + `Pesan Pembanding` untuk provinsi Papua pemekaran.
P1-2. KPI NEET 19,4% di Hal 1 menggantung (tidak dibahas). Pilih: beri konteks singkat (NEET 15–24 tahun, dipakai di dimensi "tidak bekerja" Hal 2) atau ganti dengan KPI yang lebih relevan dan terverifikasi (mis. "TPT turun, informal naik di 6/6 jenjang").
P1-3. Heatmap sektor: ganti header field mentah ("Jenjang Tampil", "Sektor Singkat") dengan label manusiawi atau sembunyikan; angka 1 desimal + "%"; jelaskan basis persentase (persen pekerja per jenjang).
P1-4. Tren TPT: label akhir garis Diploma/Universitas/SMP bertumpuk → rapikan (label hanya SMK, SMA, ≤SD; sisanya lewat tooltip/abu-abu).
P1-5. Legend/arti warna titik kuadran & Priority Lab (warna = tipe kuadran) jika belum jelas setelah P0-2.
P1-6. Konsistensi istilah & desimal: pilih satu (judul memakai koma desimal Indonesia; angka di grafik mengikuti locale Tableau) dan tulis konsisten di teks.
P1-7. Default untuk PDF (spek §7): `Pilih Provinsi` = Indonesia; `Mode Peta` = "Kerja tidak layak" (agar paradoks langsung terlihat di PDF) — putuskan, dokumentasikan di DECISIONS; panel pembanding tampil "Contoh: NTB" saat Indonesia (sudah ada calc `Judul H`/`Provinsi H`).
P1-8. Pastikan semua tooltip punya sumber BPS dan label ESTIMASI di tempat yang relevan (Papua baru sebelum 2024, urbanisasi 2018).

### P2 — Peningkatan (hanya jika waktu cukup, ≥ 6 jam sebelum deadline)

P2-1. Peta poligon kab/kota (konsep §8 fitur 4): `Spatial/IDN_kabkota_kode_bps.geojson` + `t8_geom_kabkota_kode.csv`, join via `kode`, warna = persisten ganda, ikut Pilih Provinsi, caption geoBoundaries wajib. Hanya jika muat tanpa merusak layout; jika berisiko, catat sebagai [PAPER].
P2-2. Transisi kuadran 2018→2025 (T10, `t6_transisi_2018_2025.csv`, 32 provinsi; 25/32 tetap) sebagai kalimat/tooltip.
P2-3. Dokumen yang diminta master prompt (singkat & jujur, jangan mengarang riset yang tidak dilakukan): `research/TABLEAU_DESIGN_BENCHMARK.md`, `research/FINAL_DASHBOARD_DESIGN_PLAN.md`, `research/INNOVATION_CANDIDATES.md`, `research/INNOVATION_FEASIBILITY.md`, `deliverables/INNOVATION_IMPLEMENTATION.md` (Paradox Reveal = Mode Peta; Priority Lab = slider; ekstensi/3D ditolak, lihat DECISIONS), `deliverables/JUDGE_DEMO_FLOW.md` (demo 60–120 detik memakai fitur nyata: Hal 1 paradoks SMK → Hal 2 Mode Peta TPT→KTL (NTB/DKI) → klik NTB → Priority Lab geser bobot → klik Jawa Tengah → jejak 4 kab/kota → kesimpulan), `deliverables/CHANGELOG.md` (boleh merujuk AI_PROJECT_CHANGELOG).

### PENGUMPULAN (WAJIB, sisakan ≥ 2 jam)

S-1. Set parameter ke default PDF, simpan `DAC_Dashboard_Tema4_FINAL.twbx` lewat Tableau (Ctrl+S) agar state tersimpan; buka ulang dan cek kedua halaman.
S-2. Ekspor PDF 2 halaman (File → Print to PDF / Export as PDF, ukuran sesuai 1900×1100, kedua dashboard). Cek watermark utuh, tidak ada teks terpotong. Nama: `DAC_Tema4_Boomerang_Dashboard.pdf` (konfirmasi nama tim ke user bila ragu).
S-3. Publish ke Tableau Public (butuh login akun user — minta user login sendiri; jangan masukkan kredensial). Set "Anyone with the link"; masukkan link ke PDF (teks kecil di footer, tanpa menutupi watermark) lalu ekspor ulang PDF. Jika publish tidak bisa dilakukan, catat di PROGRESS dan beri tahu user.
S-4. Susun folder ZIP (≤ 100 MB): PDF, `DAC_Dashboard_Tema4_FINAL.twbx`, `Raw_Dataset/` (raw BPS), `Processed_Dataset/` (olahan), `Spatial/` + `Raw_Dataset/spasial_non_bps/` (dengan keterangan sumber geoBoundaries), surat orisinalitas bermeterai (DISIAPKAN USER — tanyakan file-nya; jangan buat palsu). JANGAN masukkan file `.env`, key, BACKUP/WORKING/new twbx, folder `research/`/`deliverables/` kecuali diminta. Cek ukuran.
S-5. Jangan mengunggah ke Google Form sendiri: serahkan ZIP + PDF ke user untuk diunggah (aksi kirim adalah keputusan user).
S-6. Opsional: commit & push repo (atas nama aditt24, tanpa atribusi AI) HANYA jika user meminta.

---

## 7. QA AKHIR (centang di FINAL_QA_REPORT, jujur)

- [ ] Semua angka di judul/kartu cocok dengan CSV (sebutkan file & nilai).
- [ ] Tidak ada klaim kausal, "berkebalikan", target pembanding, atau klaim [GUGUR].
- [ ] 2 halaman, 1900×1100, watermark utuh, font ≥ 10 pt, tidak ada teks terpotong/tumpang tindih.
- [ ] Interaksi: Mode Peta, klik provinsi (uji NTB, DKI, Jawa Tengah, satu provinsi Papua baru → pesan pembanding tidak tersedia), slider (termasuk semua 0), Langkah cerita, Pembanding Jejak, navigasi.
- [ ] Heatmap jejak: satu kotak per sel, status per tahun benar (uji Banjarnegara & Kota Pekalongan 2017 = "Tidak ada data", Lombok Utara 2018 = "Tidak ada data").
- [ ] Tooltip rapi (desimal, sumber BPS, label ESTIMASI).
- [ ] Workbook dibuka ulang setelah simpan terakhir dan dicek lagi.
- [ ] PDF diekspor dan diperiksa halaman per halaman.
- [ ] ZIP ≤ 100 MB, isi lengkap.
Tandai yang tidak diuji sebagai "Belum diuji", jangan "Lulus".

---

## 8. PROTOKOL KONTINUITAS

- Awal sesi: baca AI_PROJECT_PROGRESS/DECISIONS/CHANGELOG, cek file nyata (jangan percaya buta).
- Update `AI_PROJECT_PROGRESS.md` setelah tiap tugas selesai, sebelum pindah tugas, dan SEGERA bila mendekati batas kuota/konteks (tulis: tugas aktif, yang sudah, sisa, file terlibat, langkah persis berikutnya).
- Catat perubahan berarti di `AI_PROJECT_CHANGELOG.md` (waktu, agen=Codex, file, apa, kenapa, verifikasi). Keputusan baru/berubah di `AI_PROJECT_DECISIONS.md`.
- Status hanya: [NOT STARTED] / [IN PROGRESS] / [COMPLETED] / [BLOCKED] / [NEEDS VERIFICATION]. Jangan mengklaim selesai tanpa uji di Tableau.
- Jika berhenti sebelum selesai, tinggalkan workbook FINAL dalam kondisi konsisten (selalu dapat dibuka) dan tulis instruksi persis untuk agen berikutnya.

Mulai sekarang dari P0-1. Laporkan ke user secara singkat setiap selesai satu kelompok (P0, P1, Pengumpulan), sertakan screenshot.
