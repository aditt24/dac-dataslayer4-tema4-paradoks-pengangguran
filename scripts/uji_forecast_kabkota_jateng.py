# Uji mundur forecast TPT kab/kota Jateng (naif vs linear vs GB, dengan/tanpa tetangga).
# Pakai: python scripts/uji_forecast_kabkota_jateng.py Raw_Dataset/bps_jateng/J01_tpt_kabkota.csv Processed_Dataset/v5/F_jateng_matriks_ketetanggaan.csv
# Output: Processed_Dataset/v6/uji_forecast_kabkota_jateng.csv
# Catatan: matriks tetangga diturunkan dari geoBoundaries (non-BPS) -> hasil ini hanya untuk paper, menunggu jawaban panitia.
# Uji tanpa tetangga untuk 514 kab/kota ada di scripts/uji_forecast_kabkota_nasional.py
import pandas as pd, numpy as np, sys
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from scipy.stats import spearmanr
w = pd.read_csv(sys.argv[1], comment="#").rename(columns={"wilayah_kategori": "wilayah", "nilai": "tpt"})
prov = w.wilayah.str.startswith("3300")
jt = w[prov].set_index("tahun").tpt
k = w[~prov].copy()
k["nama"] = k.wilayah.str.replace(r"^\d+ (Kabupaten )?", "", regex=True).str.upper()
adj = pd.read_csv(sys.argv[2], index_col=0)
nb = {r: list(adj.columns[adj.loc[r] > 0]) for r in adj.index}
nb["KOTA MAGELANG"] = ["MAGELANG"]; nb["KOTA SALATIGA"] = ["SEMARANG"]
for a, bs in list(nb.items()):
    for b in bs:
        if a not in nb[b]: nb[b].append(a)
yrs = sorted(k.tahun.unique()); nxt = dict(zip(yrs[:-1], yrs[1:]))
p = k.pivot(index="nama", columns="tahun", values="tpt")
assert set(p.index) == set(nb), set(p.index) ^ set(nb)
rows = []
for n in p.index:
    for i, t in enumerate(yrs[:-1]):
        past = [p.loc[n, y] for y in yrs[max(0, i-2):i+1]]
        rows.append(dict(nama=n, tahun=t, target=nxt[t], tpt=p.loc[n, t], rata3=np.mean(past),
             lama=p.loc[n, yrs[:i+1]].mean(), tetangga=p.loc[nb[n], t].mean(),
             kota=int(n.startswith("KOTA")), jt=jt[t], y=p.loc[n, nxt[t]], jt_next=jt[nxt[t]]))
d = pd.DataFrame(rows); d["gap"] = d.tpt - d.jt; d["gap_tet"] = d.tetangga - d.jt
d["y_gap"] = d.y - d.jt_next
print("Spearman ranking TPT t vs t+1 (rata2 per tahun):",
      round(np.mean([spearmanr(g.tpt, g.y)[0] for _, g in d.groupby("tahun")]), 2))
F = {"B_tanpa_tetangga": ["gap", "rata3", "lama", "kota", "jt"],
     "C_dengan_tetangga": ["gap", "rata3", "lama", "kota", "jt", "gap_tet"]}
res = []; store = {}
for T in [2021, 2022, 2023, 2024, 2025]:
    tr = d[d.target < T]; te = d[d.target == T]
    base = te.tpt - te.jt                         # naif relatif: posisi thd Jateng sama
    r = dict(target=T, naif_abs=np.mean(np.abs(te.tpt - te.y)),
             naif_relatif=np.mean(np.abs(base - te.y_gap)))
    for m, f in F.items():
        for alg, mdl in [("lin", LinearRegression()), ("gb", GradientBoostingRegressor(max_depth=2, n_estimators=150, learning_rate=0.05, random_state=2026))]:
            pr = mdl.fit(tr[f], tr.y_gap).predict(te[f])
            r[f"{m}_{alg}"] = np.mean(np.abs(pr - te.y_gap)); store[(T, m, alg)] = pr
    # klasifikasi: di atas Jateng tahun depan?
    r["akurasi_atasJT_naif"] = np.mean((base > 0) == (te.y_gap > 0))
    r["akurasi_atasJT_C_lin"] = np.mean((store[(T, "C_dengan_tetangga", "lin")] > 0) == (te.y_gap > 0))
    res.append(r)
R = pd.DataFrame(res).set_index("target").round(3); R.to_csv(sys.argv[3] if len(sys.argv) > 3 else "Processed_Dataset/v6/uji_forecast_kabkota_jateng.csv"); print(R.T.to_string()); print("RATA2:\n", R.mean().round(3).to_string())
lin = LinearRegression().fit(d[d.target < 2026][F["C_dengan_tetangga"]], d[d.target < 2026].y_gap)
print("koef C_lin:", dict(zip(F["C_dengan_tetangga"], lin.coef_.round(3))))
