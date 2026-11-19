"""
Analisis lanjutan v5 — data BPS WebAPI (tahun & periode seragam).
Modul:
 A. Jenjang 2015–2025: tren, gap SMK–SMA, analisis kejadian COVID (guncangan & pemulihan), proyeksi 2026–2030 (berlabel proyeksi)
 B. Provinsi 2025 (TPT Agustus 2025, kemiskinan Maret 2025): IDKK3, kuadran, Monte Carlo, uji ketahanan, validasi
 C. PCA + rotasi varimax 8 indikator (uji KMO & Bartlett) -> dua dimensi masalah kerja
 D. Transisi kuadran 2018 -> 2025 (32 provinsi konsisten, tanpa region Papua)
 E. Panel 2018–2025 two-way fixed effects (32 provinsi), SE klaster provinsi
 F. Jawa Tengah: paradoks kab/kota 2019–2023, kuadran TPT x pengeluaran, Moran's I & LISA (ketetanggaan dari batas wilayah, hanya untuk bobot)
Output: Processed_Dataset/v5/
"""
import os, re, json, glob, numpy as np, pandas as pd, statsmodels.api as sm
from scipy.stats import spearmanr, chi2

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = os.path.join(BASE, "Raw_Dataset", "bps_webapi")
OUT = os.path.join(BASE, "Processed_Dataset", "v5"); os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(2026)
NAMEMAP = {"D I YOGYAKARTA": "DI YOGYAKARTA", "KEPULAUAN RIAU": "KEP. RIAU", "KEPULAUAN BANGKA BELITUNG": "KEP. BANGKA BELITUNG"}
PAPUA = ["PAPUA", "PAPUA BARAT", "PAPUA TENGAH", "PAPUA PEGUNUNGAN", "PAPUA SELATAN", "PAPUA BARAT DAYA"]


def clean(s):
    n = re.sub(r"<[^>]+>", "", str(s)).strip().upper()
    return NAMEMAP.get(n, n)


def load(name, periode=None, turvar="Tidak ada"):
    d = pd.read_csv(os.path.join(API, name + ".csv"))
    d["wilayah"] = d.wilayah_kategori.map(clean); d["periode"] = d.periode.astype(str).str.strip(); d["turvar"] = d.turvar.astype(str).str.strip()
    if periode: d = d[d.periode == periode]
    if turvar: d = d[d.turvar == turvar]
    return d.pivot_table(index="wilayah", columns="tahun", values="nilai")


def log(t):
    print(t); LOG.append(str(t))


LOG = []
# ======================= A. JENJANG =======================
log("=== A. JENJANG 2015-2025 ===")
EDU = ["SD", "SMP", "SMA", "SMK", "Diploma", "Universitas"]
def edu_label(lab):
    l = lab.upper()
    if "KEJURUAN" in l: return "SMK"
    if "SMA" in l or "SMU" in l: return "SMA"
    if "SMP" in l or "SLTP" in l: return "SMP"
    if "DIPLOMA" in l or "AKADEMI" in l: return "Diploma"
    if "UNIV" in l: return "Universitas"
    return "SD"
def edu(name):
    t = load(name); t.index = [edu_label(i) for i in t.index]; return t.groupby(level=0).mean().reindex(EDU)
tpt_e, inf_e, tsp_e = edu("D01_tpt_pendidikan"), edu("D02b_informal_nonpertanian_pendidikan"), edu("D03_setengah_pengangguran_pendidikan")
for lab, t in [("TPT", tpt_e), ("Informal non-pertanian", inf_e), ("Setengah pengangguran", tsp_e)]:
    log(f"\n{lab}:\n{t.round(2).to_string()}")
gap = tpt_e.loc["SMK"] - tpt_e.loc["SMA"]
log(f"\nGap TPT SMK-SMA: {gap.round(2).to_dict()}")
smk_gap_inf = inf_e.loc["SMA"] - inf_e.loc["SMK"]
log(f"Selisih informal SMA-SMK (SMK lebih formal jika +): {smk_gap_inf.round(2).to_dict()}")
# Paradoks konsisten tiap tahun?
cons = {y: bool(tpt_e[y].idxmax() == "SMK" and inf_e.loc["SMK", y] < inf_e.loc["SMA", y]) for y in tpt_e.columns}
log(f"Paradoks SMK (TPT tertinggi & informal < SMA) per tahun: {cons}")
# Kejadian COVID
ev = pd.DataFrame({"tpt_2019": tpt_e[2019], "tpt_2020": tpt_e[2020], "tpt_2025": tpt_e[2025]})
ev["guncangan_2019_2020"] = ev.tpt_2020 - ev.tpt_2019
ev["pemulihan_2020_2025"] = ev.tpt_2020 - ev.tpt_2025
ev["persen_pulih"] = (100 * ev.pemulihan_2020_2025 / ev.guncangan_2019_2020).round(0)
ev["vs_pra_covid_2025"] = ev.tpt_2025 - ev.tpt_2019
ev.round(2).to_csv(os.path.join(OUT, "A_kejadian_covid_jenjang.csv"))
log(f"\nAnalisis kejadian COVID (TPT):\n{ev.round(2).to_string()}")
# Proyeksi gap SMK-SMA & TPT SMK 2026-2030: OLS tren + dummy COVID (2020-2021), interval prediksi 80%
proj = []
for lab, s in [("gap_SMK_SMA", gap), ("TPT_SMK", tpt_e.loc["SMK"]), ("TPT_SMA", tpt_e.loc["SMA"])]:
    yrs = np.array(s.index, dtype=float); X = pd.DataFrame({"t": yrs - 2015, "covid": np.isin(yrs, [2020, 2021]).astype(float)})
    m = sm.OLS(s.values, sm.add_constant(X)).fit()
    fy = np.arange(2026, 2031); Xf = sm.add_constant(pd.DataFrame({"t": fy - 2015, "covid": 0.0}), has_constant="add")
    pr = m.get_prediction(Xf).summary_frame(alpha=0.2)
    for i, y in enumerate(fy):
        proj.append([lab, y, round(pr["mean"].iloc[i], 2), round(pr["obs_ci_lower"].iloc[i], 2), round(pr["obs_ci_upper"].iloc[i], 2), round(m.params["t"], 3), round(m.pvalues["t"], 3), round(m.rsquared, 2)])
pj = pd.DataFrame(proj, columns=["seri", "tahun", "proyeksi", "pi80_bawah", "pi80_atas", "tren_per_tahun", "p_tren", "R2"])
pj.to_csv(os.path.join(OUT, "A_proyeksi_2026_2030.csv"), index=False)
log(f"\nProyeksi (OLS tren + dummy COVID, PI 80%):\n{pj[pj.tahun.isin([2026, 2030])].to_string(index=False)}")
edu_long = pd.concat({"tpt": tpt_e, "informal_nonag": inf_e, "setengah_peng": tsp_e}, names=["indikator", "jenjang"]).stack().rename("nilai").reset_index()
edu_long.to_csv(os.path.join(OUT, "A_edu_trend_long.csv"), index=False)

# ======================= B. PROVINSI 2025 =======================
log("\n=== B. PROVINSI 2025 (tahun seragam) ===")
tpt = load("D05_tpt_provinsi", periode="Agustus"); tsp = load("D03b_setengah_pengangguran_provinsi"); inf = load("D07_informal_provinsi")
neet = load("D15_neet_provinsi"); rls = load("D18_rls_provinsi"); upah = load("D11_upah_per_jam_provinsi"); formal = load("D10_formal_provinsi")
mis = load("D25_kemiskinan_provinsi", periode="Semester 1 (Maret)", turvar="Jumlah")
ak = load("D06b_angkatan_kerja_provinsi", periode="Agustus", turvar="Jumlah AK")
urb_rows = [r for r in __import__("csv").reader(open(os.path.join(BASE, "Raw_Dataset", "bps_static", "urbanisasi_proyeksi_provinsi_2010_2035.csv"), encoding="utf-8")) if len(r) >= 5 and re.match(r"^\d", r[4] or "")]
urb = {NAMEMAP.get(r[0].strip().upper(), r[0].strip().upper()): float(r[4].replace(",", ".")) for r in urb_rows}
PAR = {"PAPUA TENGAH": "PAPUA", "PAPUA PEGUNUNGAN": "PAPUA", "PAPUA SELATAN": "PAPUA", "PAPUA BARAT DAYA": "PAPUA BARAT", "KALIMANTAN UTARA": "KALIMANTAN TIMUR"}
Y = 2025
p = pd.DataFrame({"tpt": tpt[Y], "tsp": tsp[Y], "informal": inf[Y], "neet": neet[Y], "rls": rls[Y], "upah_jam": upah[Y], "formal": formal[Y], "miskin": mis[Y], "ak": ak.get(Y)})
nat = p.loc["INDONESIA"]; p = p.drop(index="INDONESIA")
p["urban"] = [urb.get(i, urb.get(PAR.get(i, ""), np.nan)) for i in p.index]; p["urban_dari_induk"] = p.index.isin(PAR.keys())
log(f"n provinsi {len(p)} | missing {p.isna().sum()[p.isna().sum() > 0].to_dict()} | nasional: {nat.round(2).to_dict()}")
C3 = ["tsp", "informal", "neet"]
def idx(d, cols=C3): z = (d[cols] - d[cols].min()) / (d[cols].max() - d[cols].min()); return 100 * z.mean(axis=1)
p["ktl"] = idx(p, ["tsp", "informal"])          # Dimensi "bekerja tetapi tidak layak" (hasil analisis faktor)
p["tidak_bekerja"] = idx(p, ["tpt", "neet"])   # Dimensi "tidak bekerja / antrean" (hasil analisis faktor)
p["idkk3"] = idx(p); p["rank_tpt"] = p.tpt.rank(ascending=False, method="min"); p["rank_idkk3"] = p.idkk3.rank(ascending=False, method="min"); p["geser"] = p.rank_tpt - p.rank_idkk3
for c in C3: p[f"idkk3_no_{c}"] = idx(p, [k for k in C3 if k != c])
mt, mi = p.tpt.median(), p.idkk3.median()
def kuad(t, i, mt, mi): return np.where(i >= mi, np.where(t >= mt, "Rentan Ganda", "Rentan Tersembunyi"), np.where(t >= mt, "Antrean Kerja Formal", "Relatif Layak"))
mtb, mk = p.tidak_bekerja.median(), p.ktl.median()
p["rank_ktl"] = p.ktl.rank(ascending=False, method="min"); p["geser_ktl"] = p.rank_tpt - p.rank_ktl
p["kuadran"] = kuad(p.tidak_bekerja, p.ktl, mtb, mk)
p["kuadran_batas_rata2"] = kuad(p.tidak_bekerja, p.ktl, p.tidak_bekerja.mean(), p.ktl.mean())
p["kuadran_batas_q40_60"] = kuad(p.tidak_bekerja, p.ktl, p.tidak_bekerja.quantile(.45), p.ktl.quantile(.45))
p["kuadran_idkk3_lama"] = kuad(p.tpt, p.idkk3, mt, mi)
p["kuadran_batas_nasional"] = p["kuadran_batas_q40_60"]
p["kuadran_stabil_3batas"] = (p.kuadran == p.kuadran_batas_rata2) & (p.kuadran == p.kuadran_batas_nasional)
p["flag_subsisten"] = (p.informal > 80) & (p.rls < 7)
C4 = ["tpt", "neet", "tsp", "informal"]
Z = ((p[C4] - p[C4].min()) / (p[C4].max() - p[C4].min())).values
R = pd.concat([pd.Series(Z @ rng.dirichlet(np.ones(4)), index=p.index).rank(ascending=False) for _ in range(1000)], axis=1)
p["rank_p05"], p["rank_med"], p["rank_p95"] = R.quantile(.05, axis=1), R.median(axis=1), R.quantile(.95, axis=1); p["prob_top10"] = (R <= 10).mean(axis=1)
q = p[~p.index.isin(PAPUA)]; Zq = ((q[C4] - q[C4].min()) / (q[C4].max() - q[C4].min())).values
Rq = pd.concat([pd.Series(Zq @ rng.dirichlet(np.ones(4)), index=q.index).rank(ascending=False) for _ in range(1000)], axis=1)
p["prob_top10_tanpa_papua"] = (Rq <= 10).mean(axis=1).reindex(p.index)
p["terdidik_tanpa_kerja_layak"] = (p.rls >= p.rls.median()) & (p.ktl >= mk)
rows = []
def pcorr(d, x, y, z):
    r = d[[x, y] + z].dropna().rank(); rx = sm.OLS(r[x], sm.add_constant(r[z])).fit().resid; ry = sm.OLS(r[y], sm.add_constant(r[z])).fit().resid; return spearmanr(rx, ry)
for lab, d in [("38 provinsi", p), ("tanpa Papua", p[~p.index.isin(PAPUA)]), ("tanpa 5 prov urban-induk", p[~p.urban_dari_induk])]:
    d = d.copy(); d["idkk3"] = idx(d); d["ktl"] = idx(d, ["tsp", "informal"]); d["tidak_bekerja"] = idx(d, ["tpt", "neet"])
    for a, b in [("tpt", "ktl"), ("tidak_bekerja", "ktl"), ("ktl", "miskin"), ("ktl", "formal"), ("ktl", "upah_jam"), ("rls", "ktl"), ("urban", "ktl"), ("tpt", "idkk3"), ("tpt", "informal"), ("tpt", "miskin"), ("idkk3", "miskin"), ("idkk3", "upah_jam"), ("idkk3", "formal"), ("rls", "tpt"), ("rls", "idkk3"), ("urban", "idkk3")]:
        r, pv = spearmanr(d[a], d[b]); rows.append([lab, f"{a}~{b}", "-", round(r, 3), round(pv, 4), len(d)])
    for x, y, z in [("rls", "ktl", ["urban"]), ("urban", "ktl", ["rls"]), ("rls", "tpt", ["urban"]), ("rls", "idkk3", ["urban"]), ("urban", "idkk3", ["rls"]), ("rls", "informal", ["urban"])]:
        r, pv = pcorr(d, x, y, z); rows.append([lab, f"{x}~{y}", "+".join(z), round(r, 3), round(pv, 4), len(d)])
uj = pd.DataFrame(rows, columns=["sampel", "hubungan", "kontrol", "rho", "p", "n"]); uj.to_csv(os.path.join(OUT, "B_uji_ketahanan.csv"), index=False)
log(f"\nUji ketahanan 2025:\n{uj.to_string(index=False)}")
log(f"\nVarian indeks (rho vs IDKK3): " + str({c: round(spearmanr(p.idkk3, p[f'idkk3_no_{c}'])[0], 3) for c in C3}))
log(f"Median tidak_bekerja {mtb:.2f} | median KTL {mk:.2f}")
log(f"Kesesuaian kuadran: batas rata-rata {(p.kuadran == p.kuadran_batas_rata2).mean():.0%} | batas persentil 45 {(p.kuadran == p.kuadran_batas_q40_60).mean():.0%} | vs kuadran lama (TPT x IDKK3) {(p.kuadran == p.kuadran_idkk3_lama).mean():.0%}")
log("\nKuadran 2025:"); [log(f"  {k} ({len(g)}): " + ", ".join(g.index.str.title())) for k, g in p.groupby("kuadran")]
log("Stabil di 3 batas: " + ", ".join(p[p.kuadran_stabil_3batas].index.str.title()))
log("Tidak stabil: " + ", ".join(p[~p.kuadran_stabil_3batas].index.str.title()))
top = p.sort_values("prob_top10", ascending=False)[["tpt", "ktl", "tidak_bekerja", "rank_tpt", "rank_ktl", "rank_p05", "rank_p95", "prob_top10", "prob_top10_tanpa_papua", "kuadran"]].head(12)
log(f"\nPrioritas (Monte Carlo):\n{top.round(2).to_string()}")
sh = p.sort_values("geser_ktl")[["tpt", "ktl", "rank_tpt", "rank_ktl", "geser_ktl"]]
log(f"\nPergeseran ranking (naik ke zona buruk):\n{sh.tail(6).round(2).to_string()}\nTurun ke zona baik:\n{sh.head(6).round(2).to_string()}")
log("Terdidik tanpa kerja layak: " + ", ".join(p[p.terdidik_tanpa_kerja_layak].index.str.title()))
log(f"JAWA TENGAH 2025: {p.loc['JAWA TENGAH', ['tpt','tsp','informal','neet','rls','miskin','ktl','tidak_bekerja','rank_tpt','rank_ktl','kuadran','kuadran_stabil_3batas']].to_dict()}")

# ======================= C. PCA + VARIMAX =======================
log("\n=== C. ANALISIS FAKTOR (PCA + varimax) ===")
V = ["tpt", "tsp", "informal", "neet", "upah_jam", "miskin", "rls", "urban"]
X = p[V].dropna(); Zs = (X - X.mean()) / X.std(); Rm = np.corrcoef(Zs.T.values)
n, k = Zs.shape
bart = -(n - 1 - (2 * k + 5) / 6) * np.log(np.linalg.det(Rm)); bart_p = chi2.sf(bart, k * (k - 1) / 2)
Ri = np.linalg.inv(Rm); Pm = -Ri / np.sqrt(np.outer(np.diag(Ri), np.diag(Ri))); np.fill_diagonal(Pm, 0); R0 = Rm.copy(); np.fill_diagonal(R0, 0)
kmo = (R0 ** 2).sum() / ((R0 ** 2).sum() + (Pm ** 2).sum())
ev_, evec = np.linalg.eigh(Rm); o = np.argsort(ev_)[::-1]; ev_, evec = ev_[o], evec[:, o]
nf = int((ev_ > 1).sum()); L = evec[:, :nf] * np.sqrt(ev_[:nf])
def varimax(L, it=100, tol=1e-6):
    p_, k_ = L.shape; Rr = np.eye(k_); d = 0
    for _ in range(it):
        Lr = L @ Rr; u, s, vt = np.linalg.svd(L.T @ (Lr ** 3 - Lr @ np.diag((Lr ** 2).sum(0)) / p_)); Rr = u @ vt
        if s.sum() < d * (1 + tol): break
        d = s.sum()
    return L @ Rr
Lr = varimax(L) if nf > 1 else L
load_df = pd.DataFrame(Lr, index=V, columns=[f"F{i+1}" for i in range(nf)]).round(2)
load_df.to_csv(os.path.join(OUT, "C_loading_faktor.csv"))
log(f"KMO={kmo:.2f} | Bartlett chi2={bart:.1f}, p={bart_p:.2e} | eigen={np.round(ev_, 2).tolist()} | var. dijelaskan {nf} faktor = {ev_[:nf].sum() / k:.0%}")
log(f"Loading (varimax):\n{load_df.to_string()}")
scores = Zs.values @ np.linalg.pinv(Lr.T)
for i in range(nf): p.loc[X.index, f"skor_F{i+1}"] = scores[:, i]
for i in range(nf):
    log(f"F{i+1} vs TPT rho={spearmanr(p[f'skor_F{i+1}'], p.tpt)[0]:.2f} | vs IDKK3 rho={spearmanr(p[f'skor_F{i+1}'], p.idkk3)[0]:.2f}")
# tanpa Papua
Xq = X[~X.index.isin(PAPUA)]; Zq2 = (Xq - Xq.mean()) / Xq.std(); e2, v2 = np.linalg.eigh(np.corrcoef(Zq2.T.values)); o2 = np.argsort(e2)[::-1]
L2 = varimax(v2[:, o2[:nf]] * np.sqrt(e2[o2[:nf]])) if nf > 1 else v2[:, o2[:1]]
log(f"Loading tanpa Papua:\n{pd.DataFrame(L2, index=V, columns=[f'F{i+1}' for i in range(nf)]).round(2).to_string()}")

# ======================= D. TRANSISI 2018 -> 2025 =======================
log("\n=== D. TRANSISI KUADRAN 2018 -> 2025 (32 provinsi, tanpa region Papua) ===")
trans = {}
for y in [2018, 2025]:
    d = pd.DataFrame({"tpt": tpt[y], "tsp": tsp[y], "informal": inf[y], "neet": neet[y], "rls": rls[y]}).drop(index="INDONESIA", errors="ignore")
    d = d[~d.index.isin(PAPUA)].dropna(); d["idkk3"] = idx(d); d["ktl"] = idx(d, ["tsp", "informal"]); d["tb"] = idx(d, ["tpt", "neet"])
    d["kuadran"] = kuad(d.tb, d.ktl, d.tb.median(), d.ktl.median()); trans[y] = d
T = trans[2018][["tpt", "idkk3", "kuadran", "informal", "tsp", "neet", "rls"]].join(trans[2025][["tpt", "idkk3", "kuadran", "informal", "tsp", "neet", "rls"]], lsuffix="_2018", rsuffix="_2025")
T["pindah"] = T.kuadran_2018 != T.kuadran_2025
T.round(2).to_csv(os.path.join(OUT, "D_transisi_2018_2025.csv"))
mat = pd.crosstab(T.kuadran_2018, T.kuadran_2025); mat.to_csv(os.path.join(OUT, "D_matriks_transisi.csv"))
log(f"Matriks transisi (baris 2018, kolom 2025):\n{mat.to_string()}")
log(f"Tetap di kuadran sama: {(~T.pindah).sum()}/{len(T)}")
for _, r in T[T.pindah].iterrows(): log(f"  {_.title()}: {r.kuadran_2018} -> {r.kuadran_2025}")
for y in [2018, 2025]:
    r_, p_ = spearmanr(trans[y].tpt, trans[y].ktl); log(f"rho(TPT, KTL) {y} (32 prov) = {r_:.2f} (p={p_:.3f})")
chg = pd.DataFrame({c: T[f"{c}_2025"] - T[f"{c}_2018"] for c in ["tpt", "informal", "tsp", "neet", "rls"]})
log(f"Perubahan rata-rata 2018->2025 (32 prov): {chg.mean().round(2).to_dict()}")
log(f"Perbaikan informal terbesar: {chg.informal.nsmallest(5).round(2).to_dict()} | memburuk: {chg.informal.nlargest(3).round(2).to_dict()}")
chg.round(2).to_csv(os.path.join(OUT, "D_perubahan_2018_2025.csv"))

# ======================= E. PANEL FE 2018-2025 =======================
log("\n=== E. PANEL TWO-WAY FE 2018-2025 (32 provinsi) ===")
recs = []
for y in range(2018, 2026):
    for w in tpt.index:
        if w == "INDONESIA" or w in PAPUA: continue
        try: recs.append(dict(prov=w, tahun=y, tpt=tpt.loc[w, y], tsp=tsp.loc[w, y], informal=inf.loc[w, y], neet=neet.loc[w, y], rls=rls.loc[w, y]))
        except KeyError: pass
pan = pd.DataFrame(recs).dropna(); pan.to_csv(os.path.join(OUT, "E_panel_2018_2025.csv"), index=False)
log(f"Panel: {pan.prov.nunique()} provinsi x {pan.tahun.nunique()} tahun = {len(pan)} obs")
pres = []
for ycol in ["tpt", "informal", "tsp", "neet"]:
    Xp = pd.get_dummies(pan[["prov", "tahun"]].astype(str), drop_first=True).astype(float); Xp.insert(0, "rls", pan.rls.values)
    m = sm.OLS(pan[ycol].values, sm.add_constant(Xp)).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(pan.prov)[0]})
    pres.append([ycol, round(m.params["rls"], 3), round(m.bse["rls"], 3), round(m.pvalues["rls"], 4), round(m.rsquared, 3), len(pan)])
pr_ = pd.DataFrame(pres, columns=["y", "beta_rls", "se_klaster", "p", "R2", "n"]); pr_.to_csv(os.path.join(OUT, "E_panel_fe.csv"), index=False)
log(f"FE (efek provinsi + tahun), y ~ RLS:\n{pr_.to_string(index=False)}")
# Placebo/robust: first difference 2018->2025
fd = chg.dropna(); fdr = []
for ycol in ["tpt", "informal", "tsp", "neet"]:
    m = sm.OLS(fd[ycol], sm.add_constant(fd[["rls"]])).fit(cov_type="HC3"); fdr.append([ycol, round(m.params["rls"], 3), round(m.pvalues["rls"], 4), round(spearmanr(fd.rls, fd[ycol])[0], 2)])
log(f"First-difference 2018->2025 (Δy ~ ΔRLS): {fdr}")

# ======================= F. JAWA TENGAH =======================
log("\n=== F. JAWA TENGAH ===")
def decode(js):
    vv = {str(v["val"]): v["label"] for v in js.get("vervar", [])}; tv = {str(v["val"]): v["label"] for v in js.get("turvar", [])}
    tt = {str(v["val"]): v["label"] for v in js.get("tahun", [])}; th = {str(v["val"]): v["label"] for v in js.get("turtahun", [])}
    var = str(js["var"][0]["val"]) if js.get("var") else ""; out = []
    for kk, val in js.get("datacontent", {}).items():
        for vc in sorted(vv, key=len, reverse=True):
            if not kk.startswith(vc + var): continue
            r = kk[len(vc + var):]
            for tc in sorted(tv, key=len, reverse=True):
                if r.startswith(tc):
                    r2 = r[len(tc):]
                    for yc in tt:
                        if r2.startswith(yc) and r2[len(yc):] in th: out.append((vv[vc], tv[tc], int(tt[yc]), val))
                    break
            break
    return out
jr = []
for f in sorted(glob.glob(os.path.join(API, "J03_*_raw_*.json"))):
    jr += decode(json.load(open(f, encoding="utf-8")))
J = pd.DataFrame(jr, columns=["kab", "jenjang", "tahun", "tpt"]); J["kab"] = J.kab.map(lambda s: re.sub(r"^\d+\s*", "", clean(s)).replace("KABUPATEN ", ""))
J["jenjang"] = J.jenjang.map({"Pendidikan Dasar ke Bawah": "dasar", "Pendidikan Menengah": "menengah", "Pendidikan Tinggi": "tinggi"})
Jw = J.pivot_table(index=["kab", "tahun"], columns="jenjang", values="tpt").reset_index()
Jw = Jw[~Jw.kab.str.contains("JAWA TENGAH")]
Jw.to_csv(os.path.join(OUT, "F_jateng_tpt_pendidikan_2019_2023.csv"), index=False)
par_y = Jw.groupby("tahun").apply(lambda g: pd.Series({"n_kab": len(g), "menengah_gt_dasar": int((g.menengah > g.dasar).sum()), "median_dasar": g.dasar.median(), "median_menengah": g.menengah.median()}))
log(f"Paradoks Jateng per tahun:\n{par_y.to_string()}")
jw23, jw19 = Jw[Jw.tahun == 2023].set_index("kab"), Jw[Jw.tahun == Jw.tahun.min()].set_index("kab")
dj = (jw23.menengah - jw19.menengah).dropna().sort_values()
log(f"Perubahan TPT menengah {Jw.tahun.min()}->2023 — membaik: {dj.head(5).round(2).to_dict()} | memburuk: {dj.tail(5).round(2).to_dict()}")
# kab/kota pengeluaran per kapita & TPT 2025
jt = pd.read_csv(os.path.join(BASE, "Processed_Dataset", "v4", "jateng_kabkota_master.csv"))
jt["kab"] = jt.nm.map(lambda s: re.sub(r"^\d+\s*", "", clean(s)).replace("KABUPATEN ", ""))
jt = jt.set_index("kab").join(jw23[["dasar", "menengah", "tinggi"]], rsuffix="_23")
# --- Ketetanggaan dari batas wilayah (geoBoundaries ADM2; hanya untuk bobot spasial) ---
gj = json.load(open(os.path.join(BASE, "Raw_Dataset", "spasial_non_bps", "geoBoundaries-IDN-ADM2_simplified.geojson"), encoding="utf-8"))
def norm(s):
    s = clean(s); s = s.replace("KABUPATEN ", ""); return s
polys = {}
for ft in gj["features"]:
    nm = ft["properties"]["shapeName"]; g = ft["geometry"]
    rings = [poly[0] for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]])]
    pts = np.vstack([np.array(r) for r in rings])
    cx, cy = pts[:, 0].mean(), pts[:, 1].mean()
    if 108.5 <= cx <= 111.8 and -8.4 <= cy <= -5.8: polys.setdefault(norm(nm), []).append(pts)
names = [n for n in jt.index if n in polys]
log(f"Kab/kota Jateng cocok dengan batas wilayah: {len(names)}/35 | tidak cocok: {[n for n in jt.index if n not in polys]}")
P = {n: np.vstack(polys[n]) for n in names}
W = np.zeros((len(names), len(names)))
for i, a in enumerate(names):
    for j, b in enumerate(names):
        if j <= i: continue
        A, Bp = P[a], P[b]
        if A[:, 0].min() > Bp[:, 0].max() + .05 or Bp[:, 0].min() > A[:, 0].max() + .05 or A[:, 1].min() > Bp[:, 1].max() + .05 or Bp[:, 1].min() > A[:, 1].max() + .05: continue
        dmin = np.sqrt(((A[::2, None, :] - Bp[None, ::2, :]) ** 2).sum(-1)).min()
        if dmin < 0.012: W[i, j] = W[j, i] = 1
iso = [names[i] for i in range(len(names)) if W[i].sum() == 0]
log(f"Rata-rata tetangga {W.sum(1).mean():.1f} | tanpa tetangga: {iso}")
Wr = W / W.sum(1, keepdims=True).clip(min=1)
def moran(x, Wr, perm=999):
    z = (x - x.mean()) / x.std(); I = (z @ Wr @ z) / (z @ z)
    sims = np.array([(zz @ Wr @ zz) / (zz @ zz) for zz in (rng.permutation(z) for _ in range(perm))])
    p_ = (1 + (np.abs(sims) >= abs(I)).sum()) / (perm + 1)
    lag = Wr @ z; Ii = z * lag
    pl = []
    for i in range(len(z)):
        others = np.delete(z, i); nb = W[i] > 0; k_ = int(nb.sum())
        if k_ == 0: pl.append(1.0); continue
        sim = np.array([z[i] * rng.choice(others, k_, replace=False).mean() for _ in range(perm)])
        pl.append((1 + (np.abs(sim) >= abs(Ii[i])).sum()) / (perm + 1))
    cl = np.where(np.array(pl) < 0.05, np.where(z > 0, np.where(lag > 0, "High-High (hotspot)", "High-Low"), np.where(lag < 0, "Low-Low (coldspot)", "Low-High")), "Tidak signifikan")
    return I, p_, cl, np.array(pl)
Jn = jt.loc[names]
res = {}
for col in ["tpt25", "menengah", "peng_kap"]:
    I, pI, cl, pl = moran(Jn[col].values.astype(float), Wr)
    res[col] = (I, pI); Jn[f"lisa_{col}"] = cl; Jn[f"lisa_p_{col}"] = pl.round(3)
    log(f"Moran's I {col}: I={I:.3f}, p={pI:.3f} | " + "; ".join(f"{k}: {', '.join(Jn.index[Jn[f'lisa_{col}'] == k].str.title())}" for k in ["High-High (hotspot)", "Low-Low (coldspot)", "High-Low", "Low-High"] if (Jn[f"lisa_{col}"] == k).any()))
Jn.round(4).to_csv(os.path.join(OUT, "F_jateng_kabkota_spasial.csv"))
pd.DataFrame(W, index=names, columns=names).to_csv(os.path.join(OUT, "F_jateng_matriks_ketetanggaan.csv"))

p.round(4).to_csv(os.path.join(OUT, "B_prov_master_2025.csv"))
open(os.path.join(OUT, "_log_v5.txt"), "w", encoding="utf-8").write("\n".join(LOG))
print("\nSELESAI ->", OUT)
