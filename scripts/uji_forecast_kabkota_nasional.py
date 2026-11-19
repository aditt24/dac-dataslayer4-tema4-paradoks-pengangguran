"""
Uji mundur forecast TPT kab/kota NASIONAL (514 kab/kota, 2017-2025): naif vs regresi linear vs gradient boosting.
Tanpa matriks tetangga (tidak butuh batas wilayah non-BPS).

Pakai: python scripts/uji_forecast_kabkota_nasional.py
Input : Processed_Dataset/v6/kabkota_tpt_2017_2025.csv
Output: Processed_Dataset/v6/uji_forecast_kabkota_nasional.csv (per tahun target + baris RATA2)

Target = selisih TPT kab/kota terhadap TPT provinsinya tahun depan (posisi relatif), supaya guncangan
nasional (COVID 2020) tidak mendominasi. Naif = "selisih tahun depan sama dengan selisih tahun ini".
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
k = pd.read_csv(os.path.join(BASE, "Processed_Dataset", "v6", "kabkota_tpt_2017_2025.csv"), dtype={"kode": str})
k = k.dropna(subset=["tpt"]).sort_values(["kode", "tahun"])
k["gap"] = k.tpt - k.tpt_prov
g = k.groupby("kode")
k["gap_rata3"] = g.gap.transform(lambda s: s.rolling(3, min_periods=1).mean())
k["gap_lama"] = g.gap.transform(lambda s: s.expanding().mean())
k["tahun_next"] = g.tahun.shift(-1)
k["y_gap"] = g.gap.shift(-1)
d = k[(k.tahun_next == k.tahun + 1)].dropna(subset=["y_gap"]).copy()
d["kota"] = d.is_kota.astype(int)
F = ["gap", "gap_rata3", "gap_lama", "kota", "tpt_prov"]

res = []
for T in [2021, 2022, 2023, 2024, 2025]:
    tr, te = d[d.tahun_next < T], d[d.tahun_next == T]
    r = dict(target=T, n_uji=len(te), mae_naif=np.mean(np.abs(te.gap - te.y_gap)),
             spearman_ranking_t_vs_t1=spearmanr(te.gap, te.y_gap)[0])
    for nama, mdl in [("linear", LinearRegression()),
                      ("gb", GradientBoostingRegressor(max_depth=2, n_estimators=150, learning_rate=0.05, random_state=2026))]:
        pr = mdl.fit(tr[F], tr.y_gap).predict(te[F])
        r[f"mae_{nama}"] = np.mean(np.abs(pr - te.y_gap))
        r[f"akurasi_atas_prov_{nama}"] = np.mean((pr > 0) == (te.y_gap > 0))
    r["akurasi_atas_prov_naif"] = np.mean((te.gap > 0) == (te.y_gap > 0))
    res.append(r)
R = pd.DataFrame(res)
R = pd.concat([R, R.drop(columns="target").mean().to_frame().T.assign(target="RATA2")], ignore_index=True)
R = R.round(3)
R.to_csv(os.path.join(BASE, "Processed_Dataset", "v6", "uji_forecast_kabkota_nasional.csv"), index=False)
print(R.to_string(index=False))
