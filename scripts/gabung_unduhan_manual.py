"""
Menggabungkan file hasil UNDUH MANUAL dari tabel BPS menjadi CSV rapi.

Cara pakai:
1. Simpan file unduhan ke folder  Raw_Dataset/manual/  dengan nama:  <KODE>_<TAHUN>.<ext>
   contoh: D07_2018.json , D07_2025.json , D05_2018.json , D01_2015.json , J03_2019.json
   (format JSON dari tombol "JSON" di halaman tabel BPS paling dianjurkan; .xlsx/.csv juga dicoba dibaca)
2. Jalankan:  python scripts/gabung_unduhan_manual.py
3. Hasil: Processed_Dataset/manual/<KODE>.csv (format panjang) + _laporan_cek.csv (cek kelengkapan)
"""
import os, re, json, glob
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN = os.path.join(BASE, "Raw_Dataset", "manual")
OUT = os.path.join(BASE, "Processed_Dataset", "manual")
os.makedirs(IN, exist_ok=True); os.makedirs(OUT, exist_ok=True)

# kode -> (judul singkat, jumlah kategori yang diharapkan)
EXPECT = {
    "D01": ("TPT menurut pendidikan", 6), "D02b": ("Informal non-pertanian menurut pendidikan", 6),
    "D03": ("Setengah pengangguran menurut pendidikan", 6), "D03b": ("Setengah pengangguran menurut provinsi", 39),
    "D05": ("TPT menurut provinsi", 39), "D07": ("Informal menurut provinsi", 39), "D15": ("NEET menurut provinsi", 39),
    "D18": ("RLS menurut provinsi", 39), "D25": ("Kemiskinan menurut provinsi", 39), "D06b": ("Angkatan kerja menurut provinsi", 39),
    "J03": ("TPT kab/kota x pendidikan Jateng", 36),
}


def decode_json(js):
    """Format JSON BPS: vervar, turvar, tahun, turtahun, datacontent (kunci = vervar+var+turvar+tahun+turtahun)."""
    if "data" in js and isinstance(js["data"], dict) and "datacontent" not in js:
        js = js["data"]
    vv = {str(v["val"]): v["label"] for v in js.get("vervar", [])}
    tv = {str(v["val"]): v["label"] for v in js.get("turvar", [])} or {"0": "Tidak ada"}
    tt = {str(v["val"]): v["label"] for v in js.get("tahun", [])}
    th = {str(v["val"]): v["label"] for v in js.get("turtahun", [])} or {"0": "Tahun"}
    var = ""
    if js.get("var"):
        v0 = js["var"][0] if isinstance(js["var"], list) else js["var"]
        var = str(v0.get("val", "")) if isinstance(v0, dict) else ""
    rows = []
    for k, val in (js.get("datacontent") or {}).items():
        hit = None
        for vc in sorted(vv, key=len, reverse=True):
            if not k.startswith(vc):
                continue
            r = k[len(vc):]
            if var and r.startswith(var):
                r = r[len(var):]
            for tc in sorted(tv, key=len, reverse=True):
                if not r.startswith(tc):
                    continue
                r2 = r[len(tc):]
                for yc in tt:
                    if r2.startswith(yc) and r2[len(yc):] in th:
                        hit = (vv[vc], tv[tc], tt[yc], th[r2[len(yc):]]); break
                if hit:
                    break
            if hit:
                break
        if hit:
            rows.append(dict(wilayah_kategori=re.sub(r"<[^>]+>", "", hit[0]).strip(), turvar=hit[1].strip(), tahun=hit[2], periode=hit[3].strip(), nilai=val))
    return rows


def read_table(path, tahun):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        with open(path, encoding="utf-8") as f:
            return decode_json(json.load(f))
    # xlsx/csv: ambil kolom pertama sebagai kategori, kolom angka terakhir sebagai nilai (cek manual hasilnya!)
    df = pd.read_excel(path, header=None) if ext in (".xlsx", ".xls") else pd.read_csv(path, header=None, sep=None, engine="python")
    rows = []
    for _, r in df.iterrows():
        lab = str(r.iloc[0]).strip()
        nums = [x for x in r.iloc[1:] if isinstance(x, (int, float)) and pd.notna(x)]
        if not nums:
            nums = [float(str(x).replace(".", "").replace(",", ".")) for x in r.iloc[1:] if re.fullmatch(r"-?[\d\.,]+", str(x).strip() or "x")]
        if lab and lab.lower() != "nan" and nums:
            rows.append(dict(wilayah_kategori=lab, turvar="(xlsx)", tahun=tahun, periode="(cek)", nilai=nums[-1]))
    return rows


report = []
by_code = {}
for path in sorted(glob.glob(os.path.join(IN, "*"))):
    m = re.match(r"([A-Za-z0-9]+)_(\d{4})\.(json|xlsx|xls|csv)$", os.path.basename(path))
    if not m:
        print("Lewati (nama tidak sesuai pola KODE_TAHUN.ext):", os.path.basename(path)); continue
    code, tahun = m.group(1), m.group(2)
    try:
        rows = read_table(path, tahun)
    except Exception as e:
        report.append([code, tahun, os.path.basename(path), 0, f"GAGAL: {e}"]); continue
    years_in = sorted({str(r["tahun"]) for r in rows})
    exp = EXPECT.get(code, ("?", None))[1]
    ncat = len({r["wilayah_kategori"] for r in rows})
    note = []
    if tahun not in years_in and rows and rows[0]["turvar"] != "(xlsx)":
        note.append(f"TAHUN DI FILE {years_in} != {tahun}")
    if exp and ncat < exp:
        note.append(f"kategori {ncat} < harapan {exp}")
    report.append([code, tahun, os.path.basename(path), len(rows), "; ".join(note) or "OK"])
    by_code.setdefault(code, []).extend(rows)

for code, rows in by_code.items():
    pd.DataFrame(rows).to_csv(os.path.join(OUT, f"{code}.csv"), index=False)
rep = pd.DataFrame(report, columns=["kode", "tahun", "file", "n_baris", "status"])
rep.to_csv(os.path.join(OUT, "_laporan_cek.csv"), index=False)
print(rep.to_string(index=False) if len(rep) else "Belum ada file di Raw_Dataset/manual/")
need = {"D03b", "D05", "D07", "D15", "D18", "D25"}
for c in sorted(need):
    have = sorted(set(rep[rep.kode == c].tahun)) if len(rep) else []
    print(f"{c}: tahun tersedia {have} -> {'LENGKAP' if {'2018','2025'} <= set(have) else 'KURANG (butuh 2018 & 2025)'}")
