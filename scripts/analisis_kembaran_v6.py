"""
Kembaran Provinsi (kNN): pasangkan provinsi menurut kondisi awal 2018, lalu bandingkan perubahan 2018 -> 2025.

Pakai: python scripts/analisis_kembaran_v6.py
Input : Processed_Dataset/v5/E_panel_2018_2025.csv (32 provinsi, Sakernas Agustus)
        Raw_Dataset/bps_static/urbanisasi_proyeksi_provinsi_2010_2035.csv (2018 = interpolasi linear 2015-2020, ESTIMASI)
        Raw_Dataset/bps_webapi/D25_kemiskinan_provinsi.csv (Jumlah, September 2018)
Output: Processed_Dataset/v6/kembaran_provinsi.csv  (1 baris = provinsi x kembaran)
        Processed_Dataset/v6/kembaran_uji.csv       (uji stabilitas & uji vs acak)
"""
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "Processed_Dataset", "v6")
os.makedirs(OUT, exist_ok=True)
K, SEED = 3, 2026
norm = lambda s: s.str.upper().str.replace("KEPULAUAN", "KEP.").str.replace("DAERAH ISTIMEWA ", "DI ").str.strip()

p = pd.read_csv(os.path.join(BASE, "Processed_Dataset", "v5", "E_panel_2018_2025.csv"))
u = pd.read_csv(os.path.join(BASE, "Raw_Dataset", "bps_static", "urbanisasi_proyeksi_provinsi_2010_2035.csv"),
                skiprows=4, header=None, names=["prov", "y2010", "y2015", "y2020", "y2025", "y2030", "y2035"], decimal=",")
u = u[~u.prov.str.contains("nbsp", na=True)].copy()  # buang baris pemisah tabel
for c in ["y2015", "y2020"]:
    u[c] = u[c].str.replace(",", ".").astype(float)
u["prov"] = norm(u.prov)
u["urban"] = u.y2015 + 0.6 * (u.y2020 - u.y2015)  # estimasi 2018
m = pd.read_csv(os.path.join(BASE, "Raw_Dataset", "bps_webapi", "D25_kemiskinan_provinsi.csv"))
m = m[(m.tahun == 2018) & (m.turvar.str.strip() == "Jumlah") & m.periode.str.contains("September")]
m = m.assign(prov=norm(m.wilayah_kategori.str.replace(r"</?b>", "", regex=True)))[["prov", "nilai"]].rename(columns={"nilai": "miskin"})

a = p[p.tahun == 2018].set_index("prov")
a = a.join(u.set_index("prov").urban).join(m.set_index("prov").miskin)
a.loc["KALIMANTAN UTARA", "urban"] = u.set_index("prov").urban["KALIMANTAN TIMUR"]  # proyeksi SP2010 belum pisahkan Kaltara: pakai induk (sama dengan v5)
assert a[["urban", "miskin"]].notna().all().all(), a[a[["urban", "miskin"]].isna().any(axis=1)].index.tolist()
OUTC = ["tpt", "tsp", "informal", "neet"]
FIT = OUTC + ["rls", "urban", "miskin"]
delta = p[p.tahun == 2025].set_index("prov")[OUTC] - a[OUTC]
names = a.index.to_numpy()


def twins(cols):
    X = StandardScaler().fit_transform(a[cols])
    dist, idx = NearestNeighbors(n_neighbors=K + 1).fit(X).kneighbors(X)
    return dist[:, 1:], idx[:, 1:]  # kolom 0 = provinsi itu sendiri


dist, idx = twins(FIT)

# Uji 1 - stabilitas: buang satu fitur bergantian, berapa kembaran yang bertahan
stab = []
for f in FIT:
    _, i2 = twins([c for c in FIT if c != f])
    stab.append(np.mean([len(set(idx[r]) & set(i2[r])) / K for r in range(len(names))]))

# Uji 2 - apakah perubahan 2018-2025 lebih mirip ke kembaran daripada ke 3 provinsi acak?
Z = StandardScaler().fit_transform(delta.loc[names])
err = lambda r, nb: np.linalg.norm(Z[r] - Z[nb].mean(axis=0))
obs = np.mean([err(r, idx[r]) for r in range(len(names))])
rng = np.random.default_rng(SEED)
null = [np.mean([err(r, rng.choice(np.delete(np.arange(len(names)), r), K, replace=False)) for r in range(len(names))])
        for _ in range(1000)]
p_val = (np.sum(np.array(null) <= obs) + 1) / (len(null) + 1)

rows = []
for r, prov in enumerate(names):
    tw = names[idx[r]]
    for j, t in enumerate(tw):
        row = dict(provinsi=prov, kembaran=t, urutan=j + 1, kemiripan=round(100 / (1 + dist[r, j]), 1))
        for c in OUTC:
            row[f"awal_{c}"] = a.loc[prov, c]
            row[f"d_{c}_sendiri"] = round(delta.loc[prov, c], 2)
            row[f"d_{c}_kembaran"] = round(delta.loc[t, c], 2)
        rows.append(row)
    best = delta.loc[tw, "informal"].idxmin()
    rows[-K]["target_informal_dari"] = best
    rows[-K]["target_informal"] = round(delta.loc[best, "informal"], 2)
    rows[-K]["selisih_vs_kembaran_informal"] = round(delta.loc[prov, "informal"] - delta.loc[tw, "informal"].mean(), 2)
res = pd.DataFrame(rows)
res.to_csv(os.path.join(OUT, "kembaran_provinsi.csv"), index=False)

uji = pd.DataFrame([dict(uji=f"stabilitas_tanpa_{f}", nilai=round(s, 3)) for f, s in zip(FIT, stab)] +
                   [dict(uji="stabilitas_rata2", nilai=round(np.mean(stab), 3)),
                    dict(uji="galat_kembaran", nilai=round(obs, 3)),
                    dict(uji="galat_acak_rata2", nilai=round(np.mean(null), 3)),
                    dict(uji="p_kembaran_lebih_mirip_dari_acak", nilai=round(p_val, 4))])
uji.to_csv(os.path.join(OUT, "kembaran_uji.csv"), index=False)
print(uji.to_string(index=False))
print(res.dropna(subset=["target_informal"])[["provinsi", "kembaran", "target_informal_dari", "target_informal",
                                               "d_informal_sendiri", "selisih_vs_kembaran_informal"]].to_string(index=False))
