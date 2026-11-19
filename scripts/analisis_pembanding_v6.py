"""
Provinsi Pembanding (kNN): cari 3 provinsi yang kondisi awalnya (2018) paling mirip, lalu tampilkan perubahan
2018 -> 2025 berdampingan. Ini alat BANDING DESKRIPTIF, bukan alat prediksi atau penentu target.

Pakai: python scripts/analisis_pembanding_v6.py
Input : Processed_Dataset/v5/E_panel_2018_2025.csv (32 provinsi, Sakernas Agustus; Papua & Papua Barat tidak ada
        karena pemekaran 2022 membuat 2018 vs 2025 tidak sebanding)
        Raw_Dataset/bps_static/urbanisasi_proyeksi_provinsi_2010_2035.csv (2018 = interpolasi linear 2015-2020, ESTIMASI)
        Raw_Dataset/bps_webapi/D25_kemiskinan_provinsi.csv (Jumlah, MARET 2018 - seragam dengan v5 yang memakai Maret)
Output: Processed_Dataset/v6/pembanding_provinsi.csv  (1 baris = provinsi x pembanding)
        Processed_Dataset/v6/pembanding_uji.csv       (stabilitas, uji vs acak, uji vs regresi ke rata-rata)

Kenapa bukan "kembaran" + "target": uji ketat menunjukkan rata-rata perubahan 3 pembanding TIDAK lebih akurat
daripada regresi sederhana pada tingkat awal (provinsi yang awalnya tinggi cenderung turun = regresi ke rata-rata).
Jadi pembanding tidak dipakai untuk memprediksi atau memasang target, hanya untuk membandingkan.
"""
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LinearRegression

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
m = m[(m.tahun == 2018) & (m.turvar.str.strip() == "Jumlah") & m.periode.str.contains("Maret")]
m = m.assign(prov=norm(m.wilayah_kategori.str.replace(r"</?b>", "", regex=True)))[["prov", "nilai"]].rename(columns={"nilai": "miskin"})

a = p[p.tahun == 2018].set_index("prov")
a = a.join(u.set_index("prov").urban).join(m.set_index("prov").miskin)
a.loc["KALIMANTAN UTARA", "urban"] = u.set_index("prov").urban["KALIMANTAN TIMUR"]  # proyeksi SP2010 belum pisahkan Kaltara: pakai induk (sama dengan v5)
assert a[["urban", "miskin"]].notna().all().all(), a[a[["urban", "miskin"]].isna().any(axis=1)].index.tolist()
OUTC = ["tpt", "tsp", "informal", "neet"]
FIT = OUTC + ["rls", "urban", "miskin"]
akhir = p[p.tahun == 2025].set_index("prov")[OUTC]
delta = akhir - a[OUTC]
names = a.index.to_numpy()
n = len(names)


def pembanding(cols, X_df=a):
    X = StandardScaler().fit_transform(X_df[cols])
    dist, idx = NearestNeighbors(n_neighbors=K + 1).fit(X).kneighbors(X)
    return dist[:, 1:], idx[:, 1:]  # kolom 0 = provinsi itu sendiri


dist, idx = pembanding(FIT)
uji = []

# Uji 1 - stabilitas: buang satu fitur bergantian, berapa pembanding yang bertahan
stab = []
for f in FIT:
    _, i2 = pembanding([c for c in FIT if c != f])
    s = np.mean([len(set(idx[r]) & set(i2[r])) / K for r in range(n)])
    stab.append(s)
    uji.append(dict(uji=f"stabilitas_tanpa_{f}", nilai=round(s, 3)))
uji.append(dict(uji="stabilitas_rata2", nilai=round(np.mean(stab), 3)))

# Uji 2 - perubahan 2018-2025 pembanding vs 3 provinsi acak (4 indikator sekaligus, terstandar)
Z = StandardScaler().fit_transform(delta.loc[names])
err = lambda r, nb: np.linalg.norm(Z[r] - Z[nb].mean(axis=0))
obs = np.mean([err(r, idx[r]) for r in range(n)])
rng = np.random.default_rng(SEED)
null = [np.mean([err(r, rng.choice(np.delete(np.arange(n), r), K, replace=False)) for r in range(n)]) for _ in range(1000)]
uji += [dict(uji="galat_pembanding", nilai=round(obs, 3)), dict(uji="galat_acak_rata2", nilai=round(np.mean(null), 3)),
        dict(uji="p_pembanding_lebih_mirip_dari_acak", nilai=round((np.sum(np.array(null) <= obs) + 1) / 1001, 4))]

# Uji 3 (tandingan ketat) - apakah pembanding lebih baik daripada regresi ke rata-rata?
# Per indikator: MAE tebakan "perubahan = rata-rata perubahan 3 pembanding" vs regresi LOO "perubahan ~ tingkat awal".
for c in OUTC:
    y = delta.loc[names, c].to_numpy()
    x = a.loc[names, [c]].to_numpy()
    tebak_pb = np.array([y[idx[r]].mean() for r in range(n)])
    tebak_rg = np.array([LinearRegression().fit(np.delete(x, r, 0), np.delete(y, r)).predict(x[[r]])[0] for r in range(n)])
    tebak_rt = np.array([np.delete(y, r).mean() for r in range(n)])
    uji += [dict(uji=f"mae_{c}_pembanding", nilai=round(np.mean(np.abs(y - tebak_pb)), 3)),
            dict(uji=f"mae_{c}_regresi_tingkat_awal", nilai=round(np.mean(np.abs(y - tebak_rg)), 3)),
            dict(uji=f"mae_{c}_rata2_semua", nilai=round(np.mean(np.abs(y - tebak_rt)), 3)),
            dict(uji=f"korelasi_awal_vs_perubahan_{c}", nilai=round(np.corrcoef(x[:, 0], y)[0, 1], 3))]

rows = []
for r, prov in enumerate(names):
    for j, t in enumerate(names[idx[r]]):
        row = dict(provinsi=prov, pembanding=t, urutan=j + 1, kemiripan=round(100 / (1 + dist[r, j]), 1))
        for c in OUTC:
            row[f"awal_{c}"] = a.loc[prov, c]
            row[f"akhir_{c}"] = akhir.loc[prov, c]
            row[f"awal_{c}_pembanding"] = a.loc[t, c]
            row[f"akhir_{c}_pembanding"] = akhir.loc[t, c]
            row[f"d_{c}_sendiri"] = round(delta.loc[prov, c], 2)
            row[f"d_{c}_pembanding"] = round(delta.loc[t, c], 2)
        rows.append(row)
res = pd.DataFrame(rows)
res.to_csv(os.path.join(OUT, "pembanding_provinsi.csv"), index=False)
uji = pd.DataFrame(uji)
uji.to_csv(os.path.join(OUT, "pembanding_uji.csv"), index=False)
print(uji.to_string(index=False))
