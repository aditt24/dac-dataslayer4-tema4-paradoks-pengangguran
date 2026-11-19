"""
Rapikan TPT kab/kota nasional 2017-2025 (BPS var 2824) dari JSON WebAPI asli, lalu hitung persistensi.

Pakai: python scripts/olah_kabkota_nasional.py
Input : Raw_Dataset/bps_webapi/K01_tpt_jk_kabkota_raw_<tahun>.json
Output: Processed_Dataset/v6/kabkota_tpt_2017_2025.csv   (kab/kota x tahun, dengan kode BPS)
        Processed_Dataset/v6/kabkota_jejak_2017_2025.csv  (ringkasan persistensi per kab/kota)
"""
import os, json, glob
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN = os.path.join(BASE, "Raw_Dataset", "bps_webapi")
OUT = os.path.join(BASE, "Processed_Dataset", "v6")
os.makedirs(OUT, exist_ok=True)

rows = []
for path in sorted(glob.glob(os.path.join(IN, "K01_tpt_jk_kabkota_raw_*.json"))):
    js = json.load(open(path, encoding="utf-8"))
    tahun = {str(t["val"]): int(t["label"]) for t in js["tahun"]}
    turvar = {str(t["val"]): t["label"].strip() for t in js["turvar"]}
    for v in js["vervar"]:
        kode = str(v["val"])
        for tv, jk in turvar.items():
            for th, yr in tahun.items():
                key = f"{kode}2824{tv}{th}0"
                if key in js["datacontent"]:
                    rows.append(dict(kode=kode, label=v["label"], jk=jk, tahun=yr, nilai=js["datacontent"][key]))

d = pd.DataFrame(rows)
assert len(d), "datacontent tidak terbaca: cek format kunci JSON"
d["nama"] = d.label.str.replace(r"</?b>", "", regex=True).str.strip()
d = d.pivot_table(index=["kode", "nama", "tahun"], columns="jk", values="nilai").reset_index()
d = d.rename(columns={"Jumlah": "tpt", "Laki-Laki": "tpt_l", "Perempuan": "tpt_p"})
d["kode_prov"] = d.kode.str[:2]
d["is_prov"] = d.kode.str.endswith("00")
prov = d[d.is_prov].set_index(["kode_prov", "tahun"]).nama.groupby(level=0).last()
nas = d[d.kode == "9999"].set_index("tahun").tpt.rename("tpt_nasional")
kab = d[~d.is_prov & (d.kode != "9999")].copy()
# Tabel memuat kab Papua dua kali: di kode provinsi lama (91, 94) dan baru (92, 95, 96, 97). Simpan kode baru.
baru = set(kab[kab.kode_prov.isin(["92", "95", "96", "97"])].nama)
kab = kab[~(kab.kode_prov.isin(["91", "94"]) & kab.nama.isin(baru))]
kab["nama_prov"] = kab.kode_prov.map(prov)
kab["is_kota"] = kab.kode.str[2] == "7"  # kode BPS xx71-xx79 = kota
pv = d[d.is_prov].set_index(["kode_prov", "tahun"]).tpt.rename("tpt_prov")
kab = kab.join(pv, on=["kode_prov", "tahun"]).join(nas, on="tahun")
kab = kab[["kode", "nama", "kode_prov", "nama_prov", "is_kota", "tahun", "tpt", "tpt_l", "tpt_p", "tpt_prov", "tpt_nasional"]]
kab.sort_values(["kode", "tahun"]).to_csv(os.path.join(OUT, "kabkota_tpt_2017_2025.csv"), index=False)

g = kab.assign(atas_prov=kab.tpt > kab.tpt_prov, atas_nas=kab.tpt > kab.tpt_nasional).groupby(
    ["kode", "nama", "kode_prov", "nama_prov", "is_kota"])
agg = g.agg(n_tahun=("tahun", "nunique"), tahun_atas_prov=("atas_prov", "sum"),
            tahun_atas_nasional=("atas_nas", "sum"), rata_tpt=("tpt", "mean"), rata_prov=("tpt_prov", "mean")).reset_index()
agg["rata_selisih_prov"] = (agg.rata_tpt - agg.rata_prov).round(2)
agg["rata_tpt"] = agg.rata_tpt.round(2)
agg["persisten_tinggi"] = (agg.tahun_atas_nasional == agg.n_tahun) & (agg.n_tahun >= 8)
agg.drop(columns="rata_prov").sort_values(["tahun_atas_nasional", "rata_tpt"], ascending=False).to_csv(
    os.path.join(OUT, "kabkota_jejak_2017_2025.csv"), index=False)

# cek kewarasan
assert kab.kode.nunique() == 514, kab.kode.nunique()
assert not kab.duplicated(["kode", "tahun"]).any() and nas.notna().all()
assert abs(kab.query("nama == 'Cilacap' and tahun == 2025").tpt.iloc[0] - 7.40) < 0.01
print("kab/kota:", kab.kode.nunique(), "| baris:", len(kab), "| persisten tinggi:", int(agg.persisten_tinggi.sum()))
