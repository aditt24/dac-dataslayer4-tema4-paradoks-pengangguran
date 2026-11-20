"""
Siapkan geometri kab/kota (geoBoundaries IDN ADM2, NON-BPS) supaya bisa di-join ke data BPS lewat kode BPS.
Panitia (20 Nov 2026): geometri dari sumber lain BOLEH untuk visual peta & analisis spasial,
asalkan SELURUH DATA STATISTIK tetap dari BPS. Geometri ini hanya bentuk wilayah, tanpa angka.

Pakai: python scripts/siapkan_geom.py   (setelah olah_kabkota_nasional.py)
Input : Raw_Dataset/spasial_non_bps/geoBoundaries-IDN-ADM2_simplified.geojson
        Processed_Dataset/v6/kabkota_jejak_2017_2025.csv (daftar 514 kab/kota + kode BPS)
Output: Spatial/IDN_kabkota_kode_bps.geojson               (poligon + kode, nama, nama_prov, is_kota BPS)
        Processed_Dataset/tableau/t8_geom_kabkota_kode.csv (tabel penghubung shapeName <-> kode BPS)

Catatan: batas 2020, jadi 4 provinsi Papua hasil pemekaran 2022 tetap tergambar benar per kab/kota
(nama_prov diambil dari BPS). 5 poligon bukan wilayah administratif (danau, waduk, hutan) dibuang.
"""
import os, re, json
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "Raw_Dataset", "spasial_non_bps", "geoBoundaries-IDN-ADM2_simplified.geojson")
g = json.load(open(SRC, encoding="utf-8"))
k = pd.read_csv(os.path.join(BASE, "Processed_Dataset", "v6", "kabkota_jejak_2017_2025.csv"), dtype={"kode": str})

N = lambda s: re.sub(r"[^A-Z]", "", s.upper().replace("KABUPATEN", ""))
# Ejaan geoBoundaries -> ejaan BPS (dicek manual)
ALIAS = {"Kepulauan Seribu": "Kep. Seribu", "Kota Makassar": "Kota Makasar", "Mahakam Hulu": "Mahakam Ulu",
         "Maluku Tenggara Barat": "Maluku Tenggara Barat / Kepulauan Tanimbar",
         "Mamuju Utara": "Mamuju Utara / Pasangkayu", "Toba Samosir": "Toba Samosir / Toba"}
BUKAN_WILAYAH = {"Danau", "Danau Toba", "Hutan", "Waduk Cirata", "Wadung Kedungombo"}

bps = {N(n): r for n, r in zip(k.nama, k.to_dict("records"))}
feats, rows = [], []
for f in g["features"]:
    nm = f["properties"]["shapeName"]
    if nm in BUKAN_WILAYAH:
        continue
    r = bps.get(N(ALIAS.get(nm, nm)))
    assert r is not None, f"tidak cocok: {nm}"
    props = dict(kode=r["kode"], nama=r["nama"], nama_prov=r["nama_prov"], is_kota=bool(r["is_kota"]), nama_geo=nm)
    feats.append(dict(type="Feature", properties=props, geometry=f["geometry"]))
    rows.append(props)

t = pd.DataFrame(rows)
assert t.kode.is_unique and len(t) == 514, (len(t), t.kode[t.kode.duplicated()].tolist())
os.makedirs(os.path.join(BASE, "Spatial"), exist_ok=True)
json.dump(dict(type="FeatureCollection", features=feats),
          open(os.path.join(BASE, "Spatial", "IDN_kabkota_kode_bps.geojson"), "w", encoding="utf-8"))
t.to_csv(os.path.join(BASE, "Processed_Dataset", "tableau", "t8_geom_kabkota_kode.csv"), index=False)
print("poligon cocok:", len(t), "| dibuang (bukan wilayah):", len(BUKAN_WILAYAH))
