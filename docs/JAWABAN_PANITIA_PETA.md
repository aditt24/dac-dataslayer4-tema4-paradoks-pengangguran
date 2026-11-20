# Jawaban Panitia: Data Batas Wilayah (Peta)

Ditanyakan oleh Adit (tim Boomerang) ke narahubung DAC Data Slayer 4.0, dijawab 20 Nov 2026.

## Pertanyaan 1 (19 Nov)
1. Bolehkah file batas wilayah (SHP/GeoJSON) dari sumber lain, misalnya geoBoundaries/HDX, dipakai untuk tampilan peta, sementara seluruh angka statistik tetap dari BPS?
2. Bolehkah file itu dipakai untuk menentukan kab/kota bertetangga dalam analisis spasial (Moran's I/hotspot)?
3. Apakah poligon batas wilayah termasuk ketentuan FAQ 12 (lat/long sebagai pendukung visual peta)?

**Jawaban:** ketiganya diperbolehkan, dengan ketentuan seluruh data dan sumber harus berasal dari BPS, termasuk batas wilayah. (Masih ambigu, jadi ditanyakan ulang.)

## Pertanyaan 2 (konfirmasi)
File geoBoundaries hanya berisi geometri batas wilayah, tanpa angka statistik, dan diunduh dari situs non-BPS karena portal BPS tidak menyediakan unduhannya. Boleh dipakai?

**Jawaban final:**
> File geometri batas wilayah dari sumber lain, seperti geoBoundaries, **tetap diperbolehkan** untuk digunakan sebagai pendukung visualisasi peta dan analisis spasial. Namun, **seluruh data statistik yang digunakan tetap harus bersumber dari BPS**.

## Artinya untuk tim
| Boleh | Tidak boleh |
|---|---|
| Poligon geoBoundaries untuk peta (choropleth) kab/kota & provinsi | Angka apa pun dari sumber non-BPS (populasi, luas dari geoBoundaries, dll.) |
| Matriks ketetanggaan dari poligon untuk Moran's I / LISA | Mengganti atau mengoreksi angka BPS memakai data luar |
| Memasukkan file geometri ke ZIP (tetap cantumkan sumber + lisensi CC BY 3.0 IGO) | |

Simpan tangkapan layar chat jawaban panitia sebagai bukti (taruh di folder tim, bukan di repo publik).

## Cara pakai di Tableau
1. File: `Spatial/IDN_kabkota_kode_bps.geojson` (514 kab/kota, sudah diberi `kode` BPS). Dibuat ulang dengan `python scripts/siapkan_geom.py`.
2. Data Source → tambah *Spatial file* → pilih GeoJSON itu.
3. Relationship: `kode` (GeoJSON) = `kode` di `t5_kabkota_jejak.csv` / `t5_kabkota_tren.csv`. Join pakai kode, **bukan nama**.
4. Tabel penghubung untuk dicek: `Processed_Dataset/tableau/t8_geom_kabkota_kode.csv`.
5. Caption peta: "Batas wilayah: geoBoundaries IDN ADM2 (CC BY 3.0 IGO), hanya geometri. Seluruh angka: BPS."

## Catatan teknis geometri
- Batas tahun 2020. Kab/kota di 4 provinsi Papua baru (2022) tetap tergambar benar; nama provinsinya diambil dari BPS.
- 5 poligon bukan wilayah administratif dibuang: Danau, Danau Toba, Hutan, Waduk Cirata, Wadung Kedungombo.
- 6 nama dicocokkan manual (mis. Kota Makassar → Kota Makasar, Mamuju Utara → Mamuju Utara / Pasangkayu).
- Matriks tetangga lama Jateng (`Processed_Dataset/v5/F_jateng_matriks_ketetanggaan.csv`) mencatat Kota Magelang & Kota Salatiga tanpa tetangga (kota enklave). Skrip forecast Jateng sudah menambalnya manual (Magelang ↔ Kab. Magelang, Salatiga ↔ Kab. Semarang). Kalau LISA dihitung ulang, pakai penambalan yang sama.
- Provinsi: belum ada GeoJSON provinsi. Kalau perlu, gabungkan (dissolve) poligon kab/kota per `nama_prov`, atau tetap pakai tile map.
