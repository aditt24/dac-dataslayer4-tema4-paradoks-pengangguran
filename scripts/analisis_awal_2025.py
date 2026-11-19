"""
Analisis awal cross-section 2025 (38 provinsi + kab/kota) dari data BPS tahun terbaru.
Input : Raw_Dataset/bps_web_terbaru/*.csv
Output: Processed_Dataset/preliminary/*.csv + ringkasan di stdout
Catatan: TPT provinsi 2025 diambil dari baris provinsi tabel K01 (TPT menurut JK & kab/kota, 2025) agar tahunnya sama.
Kemiskinan = Maret 2026 (tahun default halaman), hanya sebagai variabel konteks.
"""
import os, re, numpy as np, pandas as pd
from scipy.stats import spearmanr
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, adjusted_rand_score
from sklearn.decomposition import PCA
import statsmodels.api as sm

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "Raw_Dataset", "bps_web_terbaru")
OUT = os.path.join(BASE, "Processed_Dataset", "preliminary")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(2026)


NAMEMAP = {"D I YOGYAKARTA": "DI YOGYAKARTA", "KEPULAUAN RIAU": "KEP. RIAU"}


def clean(s):
    n = re.sub(r"<[^>]+>", "", str(s)).strip().upper()
    return NAMEMAP.get(n, n)


def load(f, periode=None, turvar="Tidak ada"):
    d = pd.read_csv(os.path.join(RAW, f), comment="#")
    if periode:
        d = d[d.periode.str.strip() == periode]
    if turvar:
        d = d[d.turvar.str.strip() == turvar]
    d.index = d.wilayah_kategori.map(clean)
    return d["nilai"]


# ---------- 1. Level jenjang ----------
edu = pd.DataFrame({
    "tpt": load("D01_tpt_pendidikan.csv").values,
    "informal_nonag": load("D02b_informal_nonpertanian_pendidikan.csv").values,
    "setengah_peng": load("D03_setengah_pengangguran_pendidikan.csv").values,
}, index=["<=SD", "SMP", "SMA umum", "SMK", "Diploma", "Universitas"])
edu.to_csv(os.path.join(OUT, "edu_2025.csv"))
print("== JENJANG 2025 ==\n", edu)

# ---------- 2. Level provinsi ----------
k = pd.read_csv(os.path.join(RAW, "K01_tpt_jk_kabkota.csv"), comment="#")
k["is_prov"] = k.wilayah_kategori.str.contains("<b>")
k["nama"] = k.wilayah_kategori.map(clean)
k["turvar"] = k.turvar.str.strip()
prov_tpt = k[k.is_prov & (k.turvar == "Jumlah")].set_index("nama")["nilai"]
prov_tpt_l = k[k.is_prov & (k.turvar == "Laki-Laki")].set_index("nama")["nilai"]
prov_tpt_p = k[k.is_prov & (k.turvar == "Perempuan")].set_index("nama")["nilai"]

df = pd.DataFrame({
    "tpt": prov_tpt,
    "tpt_l": prov_tpt_l, "tpt_p": prov_tpt_p,
    "tsp": load("D03b_setengah_pengangguran_provinsi.csv"),
    "informal": load("D07_informal_provinsi.csv"),
    "informal_nonag_2024": load("D08_informal_nonpertanian_provinsi.csv"),
    "neet": load("D15_neet_provinsi.csv"),
    "upah_jam": load("D11_upah_per_jam_provinsi.csv"),
    "rls": load("D18_rls_provinsi.csv"),
    "miskin_mar2026": load("D25_kemiskinan_provinsi.csv", periode="Semester 1 (Maret)", turvar="Jumlah"),
})
nat = df.loc["INDONESIA"].copy()
p = df.drop(index="INDONESIA")
print("\nMissing per kolom:", p.isna().sum().to_dict())
p = p.dropna(subset=["tpt", "tsp", "informal", "neet", "upah_jam", "rls"])
print("n provinsi:", len(p))

# Korelasi Spearman + bootstrap CI
cols = ["tpt", "tsp", "informal", "neet", "upah_jam", "rls", "miskin_mar2026"]
corr = p[cols].corr(method="spearman").round(2)
corr.to_csv(os.path.join(OUT, "korelasi_spearman_prov.csv"))
print("\n== Spearman ==\n", corr)


def boot_ci(x, y, B=2000):
    n = len(x); r = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        r.append(spearmanr(x.iloc[i], y.iloc[i])[0])
    return np.nanpercentile(r, [2.5, 97.5])


pairs = [("tpt", "informal"), ("tpt", "rls"), ("rls", "informal"), ("tpt", "tsp"), ("rls", "tsp"), ("tpt", "miskin_mar2026")]
ci_rows = []
for a, b in pairs:
    q = p[[a, b]].dropna()
    r, pv = spearmanr(q[a], q[b]); lo, hi = boot_ci(q[a], q[b])
    ci_rows.append([a, b, round(r, 3), round(pv, 4), round(lo, 3), round(hi, 3), len(q)])
ci = pd.DataFrame(ci_rows, columns=["x", "y", "rho", "p", "ci95_lo", "ci95_hi", "n"])
ci.to_csv(os.path.join(OUT, "korelasi_bootstrap.csv"), index=False)
print("\n== Spearman + CI95 bootstrap ==\n", ci)

# Korelasi parsial (Spearman via residual rank) RLS-TPT & RLS-informal | kemiskinan
def partial_spearman(d, x, y, z):
    r = d[[x, y] + z].rank()
    rx = sm.OLS(r[x], sm.add_constant(r[z])).fit().resid
    ry = sm.OLS(r[y], sm.add_constant(r[z])).fit().resid
    return spearmanr(rx, ry)


q = p.dropna(subset=["miskin_mar2026"])
for y in ["tpt", "informal", "tsp"]:
    r, pv = partial_spearman(q, "rls", y, ["miskin_mar2026"])
    print(f"Parsial rls~{y} | kemiskinan: rho={r:.3f}, p={pv:.4f}")

# ---------- 3. IDKK ----------
comp = ["tpt", "tsp", "informal", "neet", "upah_jam"]
z = (p[comp] - p[comp].min()) / (p[comp].max() - p[comp].min())
z["upah_jam"] = 1 - z["upah_jam"]
p["idkk"] = 100 * z.mean(axis=1)
p["idkk_noTPT"] = 100 * z[["tsp", "informal", "neet", "upah_jam"]].mean(axis=1)
p["idkk_noUpah"] = 100 * z[["tpt", "tsp", "informal", "neet"]].mean(axis=1)
# z-score agregasi (sensitivitas normalisasi)
zs = (p[comp] - p[comp].mean()) / p[comp].std(); zs["upah_jam"] = -zs["upah_jam"]
p["idkk_zscore"] = zs.mean(axis=1)
# PCA weights
pca = PCA().fit(StandardScaler().fit_transform(z))
w_pca = pca.components_[0] ** 2; w_pca = w_pca / w_pca.sum()
p["idkk_pca"] = 100 * (z.values @ w_pca)
print("\nPCA PC1 var explained:", round(pca.explained_variance_ratio_[0], 3), "| bobot PCA:", dict(zip(comp, w_pca.round(3))))

for c in ["tpt", "idkk", "idkk_noTPT", "idkk_noUpah", "idkk_zscore", "idkk_pca"]:
    p["rank_" + c] = p[c].rank(ascending=False, method="min")
schemes = ["idkk", "idkk_noUpah", "idkk_zscore", "idkk_pca"]
rob = pd.DataFrame([[a, b, round(spearmanr(p[a], p[b])[0], 3)] for i, a in enumerate(schemes) for b in schemes[i + 1:]], columns=["a", "b", "rho"])
rob.to_csv(os.path.join(OUT, "robust_antar_skema.csv"), index=False)
print("\n== Robustness antar skema ==\n", rob)
r1, p1 = spearmanr(p.tpt, p.idkk_noTPT)
print(f"TPT vs IDKK_noTPT: rho={r1:.3f}, p={p1:.4f} | TPT vs IDKK: rho={spearmanr(p.tpt, p.idkk)[0]:.3f}")

# Monte Carlo
Z = z[comp].values; R = []
for _ in range(1000):
    w = rng.dirichlet(np.ones(5)); R.append(pd.Series(Z @ w, index=p.index).rank(ascending=False))
R = pd.concat(R, axis=1)
p["rank_p05"] = R.quantile(0.05, axis=1); p["rank_med"] = R.median(axis=1); p["rank_p95"] = R.quantile(0.95, axis=1)
p["prob_top10"] = (R <= 10).mean(axis=1)
p["shift_tpt_to_idkk"] = p.rank_tpt - p.rank_idkk

# ---------- 4. Klaster ----------
FEAT = ["tpt", "tsp", "informal", "neet", "upah_jam", "rls"]
X_raw = StandardScaler().fit_transform(p[FEAT])
X = StandardScaler().fit_transform(p[FEAT].rank())  # rank-transform: tahan pencilan (Papua Pegunungan/Tengah)
print("ARI klaster k=4 (data mentah vs rank):", round(adjusted_rand_score(KMeans(4, n_init=50, random_state=0).fit(X_raw).labels_, KMeans(4, n_init=50, random_state=0).fit(X).labels_), 3))
res = []
for kk in range(2, 7):
    km = KMeans(kk, n_init=50, random_state=0).fit(X)
    wd = AgglomerativeClustering(kk, linkage="ward").fit(X)
    gm = GaussianMixture(kk, covariance_type="diag", n_init=10, random_state=0).fit(X)
    res.append([kk, silhouette_score(X, km.labels_), davies_bouldin_score(X, km.labels_), adjusted_rand_score(km.labels_, wd.labels_), adjusted_rand_score(km.labels_, gm.predict(X)), gm.bic(X)])
cl = pd.DataFrame(res, columns=["k", "silhouette", "davies_bouldin", "ARI_kmeans_ward", "ARI_kmeans_gmm", "BIC_gmm"]).round(3)
cl.to_csv(os.path.join(OUT, "evaluasi_klaster.csv"), index=False)
print("\n== Evaluasi klaster ==\n", cl)
K = int(os.environ.get("K_CLUSTER", cl.sort_values("silhouette", ascending=False).iloc[0].k))
km = KMeans(K, n_init=50, random_state=0).fit(X)
gm = GaussianMixture(K, covariance_type="diag", n_init=10, random_state=0).fit(X)
p["cluster"] = km.labels_
# bootstrap stabilitas (Jaccard rata2 co-assignment)
co = np.zeros((len(p), len(p))); cnt = np.zeros((len(p), len(p)))
for _ in range(200):
    i = rng.choice(len(p), len(p), replace=True); ui = np.unique(i)
    lab = KMeans(K, n_init=10, random_state=int(rng.integers(1e6))).fit(X[ui]).labels_
    same = lab[:, None] == lab[None, :]
    co[np.ix_(ui, ui)] += same; cnt[np.ix_(ui, ui)] += 1
cons = np.divide(co, cnt, out=np.zeros_like(co), where=cnt > 0)
p["stabilitas_klaster"] = [cons[i, km.labels_ == km.labels_[i]].mean() for i in range(len(p))]
# GMM probabilitas: selaraskan label GMM ke label k-means via mayoritas
gl = gm.predict(X); prob = gm.predict_proba(X)
mapg = {g: pd.Series(km.labels_[gl == g]).mode()[0] for g in np.unique(gl)}
P = np.zeros((len(p), K))
for g, c in mapg.items():
    P[:, c] += prob[:, g]
for c in range(K):
    p[f"prob_tipe{c}"] = P[:, c].round(3)
p["prob_tipe_max"] = P.max(axis=1).round(3)
prof = p.groupby("cluster")[["tpt", "tsp", "informal", "neet", "upah_jam", "rls", "idkk"]].mean().round(2)
prof["n"] = p.groupby("cluster").size()
prof["anggota"] = p.groupby("cluster").apply(lambda d: ", ".join(d.index.str.title()))
prof.to_csv(os.path.join(OUT, "profil_klaster.csv"))
print(f"\n== Profil klaster (k={K}) ==\n", prof.drop(columns="anggota"))
for c, row in prof.iterrows():
    print(c, "->", row.anggota)

# ---------- 5. Melampaui ekspektasi ----------
m = sm.OLS(p.idkk, sm.add_constant(p[["rls"]])).fit(cov_type="HC3")
p["idkk_pred"] = m.predict(sm.add_constant(p[["rls"]]))
p["resid_std"] = (p.idkk - p.idkk_pred) / (p.idkk - p.idkk_pred).std()
# leave-one-out stabilitas label
lab = []
for nm in p.index:
    d = p.drop(index=nm); mm = sm.OLS(d.idkk, sm.add_constant(d[["rls"]])).fit()
    pr = mm.params["const"] + mm.params["rls"] * p.loc[nm, "rls"]
    lab.append((p.loc[nm, "idkk"] - pr) / (d.idkk - mm.fittedvalues).std())
p["resid_loo"] = lab
p["kategori_ekspektasi"] = np.where((p.resid_std <= -1) & (p.resid_loo <= -1), "Lebih baik dari ekspektasi",
                            np.where((p.resid_std >= 1) & (p.resid_loo >= 1), "Lebih buruk dari ekspektasi", "Sesuai ekspektasi"))
print("\nOLS IDKK~RLS (HC3): b=%.2f p=%.4f R2=%.3f" % (m.params["rls"], m.pvalues["rls"], m.rsquared))
print(p[p.kategori_ekspektasi != "Sesuai ekspektasi"][["idkk", "idkk_pred", "resid_std", "kategori_ekspektasi"]].round(2))

for yv in ["tpt", "informal"]:
    mm = sm.OLS(p[yv], sm.add_constant(p[["rls"]])).fit(cov_type="HC3")
    rs = (p[yv] - mm.fittedvalues) / (p[yv] - mm.fittedvalues).std()
    loo = []
    for nm in p.index:
        d = p.drop(index=nm); m2 = sm.OLS(d[yv], sm.add_constant(d[["rls"]])).fit()
        loo.append((p.loc[nm, yv] - (m2.params["const"] + m2.params["rls"] * p.loc[nm, "rls"])) / (d[yv] - m2.fittedvalues).std())
    p[f"resid_{yv}_rls"] = rs; p[f"resid_{yv}_rls_loo"] = loo
    print(f"OLS {yv}~RLS (HC3): b={mm.params['rls']:.2f} p={mm.pvalues['rls']:.4f} R2={mm.rsquared:.3f}")
    sel = p[(rs.abs() >= 1) & (pd.Series(loo, index=p.index).abs() >= 1)]
    print(sel[[yv, "rls", f"resid_{yv}_rls", f"resid_{yv}_rls_loo"]].round(2).sort_values(f"resid_{yv}_rls"))

# ---------- 6. Outlier komponen (robust z, MAD) ----------
out = []
for c in comp + ["rls"]:
    med = p[c].median(); mad = (p[c] - med).abs().median() * 1.4826
    rz = (p[c] - med) / mad
    for nm in rz[rz.abs() >= 2.5].index:
        out.append([nm, c, p.loc[nm, c], round(rz[nm], 2)])
outl = pd.DataFrame(out, columns=["provinsi", "indikator", "nilai", "robust_z"])
outl.to_csv(os.path.join(OUT, "outlier_robust.csv"), index=False)
print("\n== Outlier robust (|z|>=2.5) ==\n", outl)

# ---------- 7. Gender gap provinsi ----------
p["gap_tpt_p_minus_l"] = p.tpt_p - p.tpt_l
print("\nGap TPT P-L provinsi: median %.2f, min %s %.2f, max %s %.2f" % (p.gap_tpt_p_minus_l.median(), p.gap_tpt_p_minus_l.idxmin(), p.gap_tpt_p_minus_l.min(), p.gap_tpt_p_minus_l.idxmax(), p.gap_tpt_p_minus_l.max()))

p.round(4).to_csv(os.path.join(OUT, "prov_master_2025.csv"))

# ---------- 8. Kab/kota ----------
kk_ = k.copy()
prov_name = None; provcol = []
for _, r in kk_.iterrows():
    if r.is_prov:
        prov_name = r.nama
    provcol.append(prov_name)
kk_["provinsi"] = provcol
kab = kk_[~kk_.is_prov].pivot_table(index=["provinsi", "nama"], columns="turvar", values="nilai").reset_index()
kab = kab.rename(columns={"Jumlah": "tpt", "Laki-Laki": "tpt_l", "Perempuan": "tpt_p"})
print("\nKab/kota baris:", len(kab), "| unik nama:", kab.nama.nunique(), "| tpt NaN:", kab.tpt.isna().sum())
kab = kab.dropna(subset=["tpt"])
NEWP = ["PAPUA TENGAH", "PAPUA PEGUNUNGAN", "PAPUA SELATAN", "PAPUA BARAT DAYA"]
innew = set(kab[kab.provinsi.isin(NEWP)].nama)
before = len(kab)
kab = kab[~(kab.provinsi.isin(["PAPUA", "PAPUA BARAT"]) & kab.nama.isin(innew))]
print("Dedup Papua: dibuang", before - len(kab), "baris ganda (kab di provinsi induk lama) -> n =", len(kab), "| unik:", kab.nama.nunique())
kab["is_kota"] = kab.nama.str.startswith("KOTA")
# dekomposisi varians antar vs dalam provinsi
gm_ = kab.tpt.mean(); tot = ((kab.tpt - gm_) ** 2).sum()
between = kab.groupby("provinsi").tpt.apply(lambda s: len(s) * (s.mean() - gm_) ** 2).sum()
print("Varians TPT kab/kota: antarprovinsi %.1f%% | dalam provinsi %.1f%%" % (100 * between / tot, 100 * (1 - between / tot)))
print("TPT kota rata2 %.2f vs kabupaten %.2f" % (kab[kab.is_kota].tpt.mean(), kab[~kab.is_kota].tpt.mean()))
kab["gap_p_l"] = kab.tpt_p - kab.tpt_l
print("Gap P-L kab/kota: median %.2f; %% kab/kota TPT perempuan > laki-laki: %.1f%%" % (kab.gap_p_l.median(), 100 * (kab.gap_p_l > 0).mean()))
print("Top 10 TPT kab/kota:\n", kab.nlargest(10, "tpt")[["provinsi", "nama", "tpt"]])
print("Bottom 5:\n", kab.nsmallest(5, "tpt")[["provinsi", "nama", "tpt"]])
sd_within = kab.groupby("provinsi").tpt.agg(["count", "mean", "std", "min", "max"]).round(2).sort_values("std", ascending=False)
sd_within.to_csv(os.path.join(OUT, "kabkota_variasi_dalam_provinsi.csv"))
print("Provinsi dengan ketimpangan TPT internal terbesar:\n", sd_within.head(6))
kab.round(3).to_csv(os.path.join(OUT, "kabkota_tpt_2025.csv"), index=False)
# Jawa Tengah
jt = kab[kab.provinsi == "JAWA TENGAH"].sort_values("tpt", ascending=False)
print("\nJawa Tengah n=%d, rentang %.2f-%.2f; top 5:\n" % (len(jt), jt.tpt.min(), jt.tpt.max()), jt.head(5)[["nama", "tpt"]])
print("\nNasional:", nat.to_dict())
