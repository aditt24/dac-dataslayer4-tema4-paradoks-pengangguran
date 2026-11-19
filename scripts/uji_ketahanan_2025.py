"""
Uji ketahanan insight provinsi 2025: kontrol urbanisasi, tanpa region Papua, tumpang tindih komponen IDKK.
Input : Processed_Dataset/preliminary/prov_master_2025.csv (dari analisis_awal_2025.py)
        Raw_Dataset/bps_static/urbanisasi_proyeksi_provinsi_2010_2035.csv (BPS, proyeksi SP2010, 34 provinsi)
Catatan: 4 provinsi pemekaran Papua & Kalimantan Utara memakai nilai urbanisasi provinsi induk (ditandai).
"""
import os, re, csv, numpy as np, pandas as pd, statsmodels.api as sm
from scipy.stats import spearmanr

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = pd.read_csv(os.path.join(BASE, "Processed_Dataset", "preliminary", "prov_master_2025.csv"), index_col=0)
rows = list(csv.reader(open(os.path.join(BASE, "Raw_Dataset", "bps_static", "urbanisasi_proyeksi_provinsi_2010_2035.csv"), encoding="utf-8")))
urb = {r[0].strip().upper(): float(r[4].replace(",", ".")) for r in rows if len(r) >= 5 and re.match(r"^\d", r[4] or "")}
urb = {{"KEPULAUAN RIAU": "KEP. RIAU", "KEPULAUAN BANGKA BELITUNG": "KEP. BANGKA BELITUNG"}.get(k, k): v for k, v in urb.items()}
PAR = {"PAPUA TENGAH": "PAPUA", "PAPUA PEGUNUNGAN": "PAPUA", "PAPUA SELATAN": "PAPUA", "PAPUA BARAT DAYA": "PAPUA BARAT", "KALIMANTAN UTARA": "KALIMANTAN TIMUR"}
p["urban"] = [urb.get(i, urb.get(PAR.get(i, ""), np.nan)) for i in p.index]
p["urban_dari_induk"] = [i in PAR for i in p.index]
comp = ["tpt", "tsp", "informal", "neet", "upah_jam"]


def idx(d, cols):
    z = (d[comp] - d[comp].min()) / (d[comp].max() - d[comp].min()); z["upah_jam"] = 1 - z["upah_jam"]
    return 100 * z[cols].mean(axis=1)


def pc(d, x, y, z):
    r = d[[x, y] + z].dropna().rank()
    rx = sm.OLS(r[x], sm.add_constant(r[z])).fit().resid; ry = sm.OLS(r[y], sm.add_constant(r[z])).fit().resid
    return spearmanr(rx, ry)


out = []
for label, d in [("38 provinsi", p), ("tanpa 6 provinsi Papua", p[~p.index.str.contains("PAPUA")])]:
    d = d.copy(); d["idkk_noTPT"] = idx(d, ["tsp", "informal", "neet", "upah_jam"]); d["idkk_noTPT_noNEET"] = idx(d, ["tsp", "informal", "upah_jam"]); d["idkk"] = idx(d, comp)
    for a, b in [("tpt", "idkk_noTPT"), ("tpt", "idkk_noTPT_noNEET"), ("tpt", "informal"), ("rls", "tpt"), ("rls", "informal"), ("urban", "informal"), ("urban", "tpt"), ("urban", "idkk_noTPT"), ("rls", "idkk")]:
        r, pv = spearmanr(d[a], d[b]); out.append([label, f"{a} ~ {b}", "-", round(r, 3), round(pv, 4), len(d)])
    for y in ["tpt", "informal", "tsp", "neet"]:
        r, pv = pc(d, "rls", y, ["urban"]); out.append([label, f"rls ~ {y}", "urban", round(r, 3), round(pv, 4), len(d)])
        r, pv = pc(d, "urban", y, ["rls"]); out.append([label, f"urban ~ {y}", "rls", round(r, 3), round(pv, 4), len(d)])
res = pd.DataFrame(out, columns=["sampel", "hubungan", "dikontrol", "rho_spearman", "p", "n"])
os.makedirs(os.path.join(BASE, "Processed_Dataset", "preliminary"), exist_ok=True)
res.to_csv(os.path.join(BASE, "Processed_Dataset", "preliminary", "uji_ketahanan_2025.csv"), index=False)
print(res.to_string(index=False))
p.to_csv(os.path.join(BASE, "Processed_Dataset", "preliminary", "prov_master_2025_v2.csv"))
