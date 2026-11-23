# QA Report (sementara) — 22 Nov 2026, malam
Workbook: DAC_Dashboard_Tema4_FINAL.twbx (basis: FINAL buatan Codex + poles Claude Code lewat edit XML yang disetujui user, tiap langkah diverifikasi dengan membuka ulang di Tableau 2026.3). Status keseluruhan: BELUM final (uji interaksi utama sudah dilakukan, lihat tabel).
Screenshot terkini: deliverables/screenshots/hal1-final-22nov.jpg, hal2-final-22nov.jpg (presentation mode, layar 1456 px; bagian paling bawah kanvas terpotong layar).

## Lulus (dilihat langsung di Tableau)
Hal 1
- Legend 2015/2025 tidak menimpa tombol navigasi; semua 12 baris bar informal terlihat.
- Bar COVID & bar informal berjudul temuan; sumbu berlabel. Angka dicek ke t1: SMK +3,19 poin (2019→2020); informal non-pertanian naik di 6 jenjang 2015→2025.
- Pie 15+ irisan dibuang.
Hal 2
- Kuadran: 4 label kuadran (Antrean Kerja Formal ditambahkan), tidak lagi menutupi label provinsi.
- Priority Lab (Penimbang): judul + keterangan tampil (titik, pita p05–p95, ★), 15 baris muat tanpa scroll, nama provinsi utuh. Klaim ★ dicek ke t3.prob_top10: Aceh 1,000; Maluku 1,000; Maluku Utara 0,917.
- KPI kab/kota tampil utuh: "66 kab/kota persisten ganda se-Indonesia (2017–2025). Tabel: 20 tertinggi."
- Dumbbell pembanding: sumbu "Informal (%): biru muda 2018, merah 2025" (dicek ke t4: NTB 71,81 → 68,42); 4 baris tampil utuh.
Interaksi
- Tombol "Lanjut ke Halaman 2" dan "← Halaman 1" berfungsi.
Aturan lomba
- 2 halaman, 1900×1100, watermark tetap (bitmap latar tidak diubah).

## Masih lemah (belum diperbaiki)
- Mini tile map di panel Pembanding sulit dibaca (bentuk tile tidak jelas).
- Warna titik kuadran dan Penimbang tidak punya legend eksplisit (label kuadran di grafik jadi satu-satunya kunci).
- Footer bawah kedua halaman belum terverifikasi penuh (terpotong layar).
- Peta tile memakai skala biru; spek awal menyebut merah. Tidak diubah.

## Uji interaksi (23 Nov dini hari, presentation mode)
| Interaksi | Hasil | Bukti |
|---|---|---|
| Mode Peta TPT → Kerja tidak layak | LULUS: NTB 34→2, DKI 7→38, Aceh 9→3 (cocok t3.rank_tpt/rank_ktl) | screenshots/hal2-paradox-reveal-mode-ktl.jpg |
| Klik provinsi (NTB, Jawa Tengah) | LULUS: narasi, sorotan kuadran, panel pembanding (Jateng → Jatim, Sulsel, Sumsel), KPI (NTB 0; Jateng 4 = Brebes, Tegal, Cilacap, Pemalang), tabel jejak terfilter | dicek ke t3, t4, t5_kabkota_jejak |
| Slider bobot | LULUS: W TPT 0,25→0,20 mengubah urutan; semua 0 → grafik kosong + pesan | pesan sempat terpotong ("Isi m.."); perbaikan Entire View diterapkan, BELUM diverifikasi ulang |
| Pembanding Jejak Nasional ↔ Sesama | LULUS setelah perbaikan bug (lihat di bawah) | screenshots/hal2-jateng-nasional-setelah-fix-jejak.jpg |
| Tooltip peta | LULUS sebagian: TPT 2 desimal & peringkat bulat; skor KTL masih 4 desimal | |
| Langkah cerita | BELUM diuji | |

## Bug ditemukan & diperbaiki
- **Heatmap jejak kab/kota menampilkan mark "hantu"**: tiap sel bisa berisi dua kotak (mis. Banjarnegara 2017 tampil "di atas" sekaligus "di bawah acuan"). Penyebab: filter table calculation "Batas Baris" (20 teratas) dipartisi oleh dimensi warna Status Tahun → densifikasi Tableau membuat mark tanpa data (TPT kosong) berstatus "Di atas acuan". Di tampilan default Indonesia tidak terlihat (semua persisten = di atas), tetapi saat provinsi dipilih heatmap menyesatkan. Perbaikan: filter table calc dihapus; tabel kini menampilkan semua kab/kota yang lolos filter (Indonesia: 66 persisten ganda, urut abjad, bisa digulir); teks KPI disesuaikan ("Gulir tabel untuk melihat semua"). Diverifikasi: Banjarnegara (acuan nasional) terang 2017–2021, gelap 2022–2025, sesuai t5_kabkota_tren.
- KPI kab/kota tampil dobel (judul + teks mark) → teks dipindah ke Detail, mark dibuat tak terlihat.
- Label dumbbell tiga desimal → dua desimal.

## Belum diuji
Langkah cerita, ekspor PDF, Tableau Public, ukuran ZIP, pesan bobot 0 setelah perbaikan.

## Tidak dikerjakan
Riset desain eksternal, INNOVATION_*.md, JUDGE_DEMO_FLOW.md, rencana desain formal.
