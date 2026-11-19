"""
Siapkan paket CSV siap-Tableau (satu file per kelompok visual) di Processed_Dataset/tableau/.

Pakai: python scripts/siapkan_tableau.py   (jalankan setelah analisis_lanjutan_v5.py, olah_kabkota_nasional.py, analisis_kembaran_v6.py)
"""
import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(BASE, "Processed_Dataset", *a)
OUT = P("tableau")
os.makedirs(OUT, exist_ok=True)
JENJANG = {"SD": 1, "SMP": 2, "SMA": 3, "SMK": 4, "Diploma": 5, "Universitas": 6}

# 1. Jenjang x tahun (Halaman 1)
e = pd.read_csv(P("v5", "A_edu_trend_long.csv"))
e["urut_jenjang"] = e.jenjang.map(JENJANG)
e["indikator_label"] = e.indikator.map({"tpt": "Pengangguran terbuka (TPT)", "informal_nonag": "Informal non-pertanian",
                                        "setengah_peng": "Setengah pengangguran"})
e.to_csv(os.path.join(OUT, "t1_jenjang_tren.csv"), index=False)

# 2. Jenjang x sektor 2025 (heatmap)
h = pd.read_csv(P("v4", "heatmap_jenjang_sektor_share.csv")).melt(id_vars="sektor", var_name="jenjang_bps", value_name="persen")
h["jenjang"] = h.jenjang_bps.map({"SD": "SD", "SLTP": "SMP", "SLTA Umum/SMU": "SMA", "SLTA Kejuruan/SMK": "SMK",
                                  "Akademi/Diploma": "Diploma", "Universitas": "Universitas"})
h = h.dropna(subset=["jenjang"])
h["urut_jenjang"] = h.jenjang.map(JENJANG)
h.to_csv(os.path.join(OUT, "t2_jenjang_sektor_2025.csv"), index=False)

# 3. Provinsi 2025 + komponen min-max untuk slider bobot + koordinat tile map
b = pd.read_csv(P("v5", "B_prov_master_2025.csv"))
for c in ["tpt", "neet", "tsp", "informal"]:
    b[f"z_{c}"] = (b[c] - b[c].min()) / (b[c].max() - b[c].min())
# Tata letak tile map buatan tim (bukan data BPS): kolom = barat->timur, baris = utara->selatan
TILE = {"ACEH": (0, 0), "SUMATERA UTARA": (1, 1), "RIAU": (2, 1), "KEP. RIAU": (3, 1), "SUMATERA BARAT": (1, 2),
        "JAMBI": (2, 2), "KEP. BANGKA BELITUNG": (3, 2), "BENGKULU": (1, 3), "SUMATERA SELATAN": (2, 3), "LAMPUNG": (2, 4),
        "DKI JAKARTA": (4, 4), "BANTEN": (3, 5), "JAWA BARAT": (4, 5), "JAWA TENGAH": (5, 5), "JAWA TIMUR": (6, 5),
        "DI YOGYAKARTA": (5, 6), "BALI": (7, 6), "NUSA TENGGARA BARAT": (8, 6), "NUSA TENGGARA TIMUR": (9, 6),
        "KALIMANTAN UTARA": (7, 1), "KALIMANTAN BARAT": (5, 2), "KALIMANTAN TENGAH": (6, 2), "KALIMANTAN TIMUR": (7, 2),
        "KALIMANTAN SELATAN": (6, 3), "GORONTALO": (10, 1), "SULAWESI UTARA": (11, 1), "SULAWESI TENGAH": (9, 2),
        "SULAWESI BARAT": (8, 3), "SULAWESI SELATAN": (9, 4), "SULAWESI TENGGARA": (10, 4), "MALUKU UTARA": (12, 2),
        "MALUKU": (12, 4), "PAPUA BARAT DAYA": (13, 2), "PAPUA BARAT": (14, 2), "PAPUA": (15, 2), "PAPUA TENGAH": (14, 3),
        "PAPUA PEGUNUNGAN": (15, 3), "PAPUA SELATAN": (15, 4)}
assert set(TILE) == set(b.wilayah) and len(set(TILE.values())) == len(TILE)
b["tile_x"] = b.wilayah.map(lambda w: TILE[w][0])
b["tile_y"] = b.wilayah.map(lambda w: TILE[w][1])
k = pd.read_csv(P("v6", "kembaran_provinsi.csv"))
kw = k.pivot(index="provinsi", columns="urutan", values="kembaran").add_prefix("kembaran_")
b = b.join(kw, on="wilayah")  # 6 provinsi Papua baru tidak punya data 2018 -> kosong
b.to_csv(os.path.join(OUT, "t3_provinsi_2025.csv"), index=False)

# 4. Kembaran provinsi + 5. kab/kota (nama provinsi diseragamkan dengan t3)
SAMA = {"KEPULAUAN RIAU": "KEP. RIAU", "D I YOGYAKARTA": "DI YOGYAKARTA"}
for src, dst in [("kembaran_provinsi.csv", "t4_kembaran.csv"), ("kembaran_uji.csv", "t4_kembaran_uji.csv"),
                 ("kabkota_tpt_2017_2025.csv", "t5_kabkota_tren.csv"), ("kabkota_jejak_2017_2025.csv", "t5_kabkota_jejak.csv")]:
    d = pd.read_csv(P("v6", src), dtype={"kode": str, "kode_prov": str})
    if "nama_prov" in d:
        d["nama_prov"] = d.nama_prov.replace(SAMA)
        assert set(d.nama_prov) <= set(b.wilayah), set(d.nama_prov) - set(b.wilayah)
    d.to_csv(os.path.join(OUT, dst), index=False)

# 6. Transisi provinsi 2018 -> 2025 (panah kuadran)
pd.read_csv(P("v5", "D_transisi_2018_2025.csv")).to_csv(os.path.join(OUT, "t6_transisi_2018_2025.csv"), index=False)
print("Selesai:", sorted(os.listdir(OUT)))
