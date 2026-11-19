"""
Analisis final v4 (data BPS 2025): indeks defisit kualitas kerja 3 komponen (setengah pengangguran, informal, NEET),
kuadran TPT x defisit, Monte Carlo, uji ketahanan, studi kasus Jawa Tengah, heatmap jenjang x sektor.
Input : Processed_Dataset/preliminary/prov_master_2025_v2.csv (analisis_awal_2025.py + uji_ketahanan_2025.py)
        Processed_Dataset/preliminary/kabkota_tpt_2025.csv ; Raw_Dataset/bps_web_terbaru/D14_bekerja_sektor_pendidikan.csv
Output: Processed_Dataset/v4/*.csv
"""
import os, numpy as np, pandas as pd, statsmodels.api as sm
from scipy.stats import spearmanr
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(BASE, "Processed_Dataset", "preliminary"); OUT = os.path.join(BASE, "Processed_Dataset", "v4")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(2026)
p = pd.read_csv(os.path.join(PRE, "prov_master_2025_v2.csv"), index_col=0)
C3 = ["tsp", "informal", "neet"]


def idx(d, cols, method="minmax"):
    x = d[cols]
    z = (x - x.min()) / (x.max() - x.min()) if method == "minmax" else (x - x.mean()) / x.std()
    return 100 * z.mean(axis=1) if method == "minmax" else z.mean(axis=1)


p["idkk3"] = idx(p, C3)
p["idkk3_z"] = idx(p, C3, "z")
for c in C3:
    p[f"idkk3_no_{c}"] = idx(p, [k for k in C3 if k != c])
p["rank_tpt"] = p.tpt.rank(ascending=False, method="min")
p["rank_idkk3"] = p.idkk3.rank(ascending=False, method="min")
p["geser"] = p.rank_tpt - p.rank_idkk3

print("== Ketahanan varian indeks (rho vs idkk3) ==")
for c in ["idkk3_z"] + [f"idkk3_no_{c}" for c in C3]:
    print(c, round(spearmanr(p.idkk3, p[c])[0], 3))

# TPT vs indeks
rows = []
for lab, d in [("38 provinsi", p), ("tanpa Papua", p[~p.index.str.contains("PAPUA")]), ("tanpa 5 prov. urban-induk", p[~p.urban_dari_induk])]:
    dd = d.copy(); dd["idkk3"] = idx(dd, C3)
    for a, b in [("tpt", "idkk3"), ("tpt", "informal"), ("tpt", "tsp"), ("tpt", "neet"), ("rls", "tpt"), ("rls", "idkk3"), ("urban", "idkk3"), ("urban", "tpt")]:
        r, pv = spearmanr(dd[a], dd[b]); rows.append([lab, f"{a}~{b}", "-", round(r, 3), round(pv, 4), len(dd)])
    for y, x, z in [("tpt", "rls", ["urban"]), ("idkk3", "rls", ["urban"]), ("idkk3", "urban", ["rls"]), ("informal", "rls", ["urban"])]:
        rr = dd[[x, y] + z].rank()
        rx = sm.OLS(rr[x], sm.add_constant(rr[z])).fit().resid; ry = sm.OLS(rr[y], sm.add_constant(rr[z])).fit().resid
        r, pv = spearmanr(rx, ry); rows.append([lab, f"{x}~{y}", "+".join(z), round(r, 3), round(pv, 4), len(dd)])
uj = pd.DataFrame(rows, columns=["sampel", "hubungan", "kontrol", "rho", "p", "n"])
uj.to_csv(os.path.join(OUT, "uji_ketahanan_v4.csv"), index=False)
print("\n== Uji ketahanan ==\n", uj.to_string(index=False))

# Monte Carlo
Z = ((p[C3] - p[C3].min()) / (p[C3].max() - p[C3].min())).values
R = pd.concat([pd.Series(Z @ rng.dirichlet(np.ones(3)), index=p.index).rank(ascending=False) for _ in range(1000)], axis=1)
p["rank_p05"] = R.quantile(.05, axis=1); p["rank_med"] = R.median(axis=1); p["rank_p95"] = R.quantile(.95, axis=1)
p["prob_top10"] = (R <= 10).mean(axis=1)
# Monte Carlo tanpa Papua
q = p[~p.index.str.contains("PAPUA")]
Zq = ((q[C3] - q[C3].min()) / (q[C3].max() - q[C3].min())).values
Rq = pd.concat([pd.Series(Zq @ rng.dirichlet(np.ones(3)), index=q.index).rank(ascending=False) for _ in range(1000)], axis=1)
p["prob_top10_tanpa_papua"] = (Rq <= 10).mean(axis=1).reindex(p.index)

# Kuadran (median)
mt, mi = p.tpt.median(), p.idkk3.median()
def kuadran(r):
    if r.idkk3 >= mi and r.tpt < mt: return "Rentan Tersembunyi"
    if r.idkk3 >= mi and r.tpt >= mt: return "Rentan Ganda"
    if r.idkk3 < mi and r.tpt >= mt: return "Antrean Terdidik"
    return "Relatif Layak"
p["kuadran"] = p.apply(kuadran, axis=1)
# jarak ke batas (dalam SD) -> label "dekat batas"
p["jarak_batas_sd"] = np.minimum(abs(p.tpt - mt) / p.tpt.std(), abs(p.idkk3 - mi) / p.idkk3.std()).round(2)
p["dekat_batas"] = p.jarak_batas_sd < 0.15
# stabilitas kuadran: bootstrap median
stab = []
for _ in range(500):
    i = rng.choice(len(p), len(p), replace=True); b = p.iloc[i]
    m1, m2 = b.tpt.median(), b.idkk3.median()
    stab.append(p.apply(lambda r: ("T" if r.idkk3 >= m2 else "L") + ("H" if r.tpt >= m1 else "R"), axis=1))
S = pd.concat(stab, axis=1)
base = p.apply(lambda r: ("T" if r.idkk3 >= mi else "L") + ("H" if r.tpt >= mt else "R"), axis=1)
p["stabilitas_kuadran"] = (S.eq(base, axis=0)).mean(axis=1).round(2)
# pembanding kmeans k=4
X = StandardScaler().fit_transform(p[["tpt", "idkk3"]].rank())
km = KMeans(4, n_init=50, random_state=0).fit(X)
print("\nARI kuadran vs k-means(k=4, tpt & idkk3):", round(adjusted_rand_score(p.kuadran, km.labels_), 3))
print(f"Median TPT={mt:.2f}, median IDKK3={mi:.2f}")

# Terdidik tanpa kerja layak: RLS >= median & IDKK3 >= median
mr = p.rls.median()
p["terdidik_tanpa_kerja_layak"] = (p.rls >= mr) & (p.idkk3 >= mi)
# residual informal | rls + urban
m = sm.OLS(p.informal, sm.add_constant(p[["rls", "urban"]])).fit()
p["resid_informal_ctx"] = ((p.informal - m.fittedvalues) / (p.informal - m.fittedvalues).std()).round(2)
p["flag_subsisten"] = (p.informal > 80) & (p.rls < 7)

cols = ["tpt", "tsp", "informal", "neet", "rls", "urban", "miskin_mar2026", "idkk3", "rank_tpt", "rank_idkk3", "geser", "rank_p05", "rank_med", "rank_p95",
        "prob_top10", "prob_top10_tanpa_papua", "kuadran", "stabilitas_kuadran", "dekat_batas", "terdidik_tanpa_kerja_layak", "resid_informal_ctx", "flag_subsisten"]
p[cols].round(3).to_csv(os.path.join(OUT, "prov_master_v4.csv"))
print("\n== Provinsi (urut IDKK3) ==\n", p.sort_values("idkk3", ascending=False)[cols].round(2).to_string())
print("\n== Ringkasan kuadran ==\n", p.groupby("kuadran")[["tpt", "tsp", "informal", "neet", "rls", "urban", "idkk3"]].mean().round(2).assign(n=p.groupby("kuadran").size()))
for k, g in p.groupby("kuadran"):
    print(k, "->", ", ".join(g.index.str.title()))
print("\nTerdidik tanpa kerja layak:", ", ".join(p[p.terdidik_tanpa_kerja_layak].index.str.title()))
print("JAWA TENGAH:\n", p.loc["JAWA TENGAH", cols])
nat_med = p[C3 + ["tpt", "rls"]].median()
print("Median provinsi:", nat_med.round(2).to_dict())

# Kab/kota Jawa Tengah
k = pd.read_csv(os.path.join(PRE, "kabkota_tpt_2025.csv"))
jt = k[k.provinsi == "JAWA TENGAH"].copy().sort_values("tpt", ascending=False)
jt["rank"] = range(1, len(jt) + 1)
jt.to_csv(os.path.join(OUT, "jateng_kabkota_2025.csv"), index=False)
print("\nJateng n=%d | median %.2f | kota %.2f vs kab %.2f | gap P-L median %.2f, P>L di %d kab/kota" % (
    len(jt), jt.tpt.median(), jt[jt.is_kota].tpt.mean(), jt[~jt.is_kota].tpt.mean(), (jt.tpt_p - jt.tpt_l).median(), ((jt.tpt_p - jt.tpt_l) > 0).sum()))
print(jt[["nama", "tpt", "tpt_l", "tpt_p", "is_kota"]].head(8).to_string(index=False))
print("terendah:", jt[["nama", "tpt"]].tail(4).to_string(index=False))

# Heatmap jenjang x sektor (Agustus 2025)
d = pd.read_csv(os.path.join(BASE, "Raw_Dataset", "bps_web_terbaru", "D14_bekerja_sektor_pendidikan.csv"), comment="#")
d = d[d.periode.str.strip() == "Agustus"].copy()
d["sektor"] = d.wilayah_kategori.str.strip(); d["jenjang"] = d.turvar.str.strip()
pv = d.pivot_table(index="sektor", columns="jenjang", values="nilai", aggfunc="sum")
pv = pv.drop(index=[i for i in pv.index if i.lower() == "total"], errors="ignore")
share = (pv / pv.sum()).mul(100).round(1)
share.to_csv(os.path.join(OUT, "heatmap_jenjang_sektor_share.csv"))
want = [c for c in ["SD", "SLTP", "SLTA Umum/SMU", "SLTA Kejuruan/SMK", "Akademi/Diploma", "Universitas"] if c in share.columns]
print("\n== % pekerja tiap jenjang menurut sektor (Agustus 2025), 6 sektor terbesar ==")
top = pv["Total"].sort_values(ascending=False).head(8).index if "Total" in pv.columns else share.index
print(share.loc[top, want].to_string())
