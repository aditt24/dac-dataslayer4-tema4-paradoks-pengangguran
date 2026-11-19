"""
Ambil data multi-tahun dari WebAPI BPS (webapi.bps.go.id) untuk semua tabel inti DAC.

Cara pakai (PowerShell):
    $env:BPS_KEY = "<key dari webapi.bps.go.id/developer>"
    python scripts/ambil_panel_bps.py

Output: Raw_Dataset/bps_webapi/<nama>.csv (format panjang) + Raw_Dataset/bps_webapi/<nama>_raw_<tahun>.json (respon asli API, bukti sumber).
Key dibaca dari environment variable BPS_KEY dan tidak disimpan ke file.
"""
import os, json, csv, time, urllib.request

KEY = os.environ.get("BPS_KEY")
if not KEY:
    raise SystemExit("Set dulu environment variable BPS_KEY (daftar gratis di https://webapi.bps.go.id/developer/).")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "Raw_Dataset", "bps_webapi")
os.makedirs(OUT, exist_ok=True)

# nama file: (var_id, tahun_awal, tahun_akhir)  -- var_id dari halaman tabel BPS (listTahun)
VARS = {
    "D05_tpt_provinsi": (543, 2015, 2026),
    "D06_tpak_provinsi": (2396, 2021, 2026),
    "D03b_setengah_pengangguran_provinsi": (1181, 2015, 2025),
    "D07_informal_provinsi": (2153, 2018, 2025),
    "D08_informal_nonpertanian_provinsi": (1162, 2015, 2024),
    "D10_formal_provinsi": (1168, 2015, 2025),
    "D11_upah_per_jam_provinsi": (1172, 2015, 2025),
    "D15_neet_provinsi": (1186, 2015, 2025),
    "D18_rls_provinsi": (1429, 2015, 2025),
    "D01_tpt_pendidikan": (1179, 2015, 2025),
    "D02_informal_pendidikan": (2157, 2018, 2023),
    "D02b_informal_nonpertanian_pendidikan": (1166, 2015, 2025),
    "D03_setengah_pengangguran_pendidikan": (1184, 2015, 2025),
    "D04_tpt_umur": (1180, 2015, 2025),
    "D04b_tpt_jenis_kelamin": (1177, 2015, 2025),
    "D16_neet_jenis_kelamin": (2655, 2020, 2025),
    "D14_bekerja_sektor_pendidikan": (1971, 2018, 2025),
    "K01_tpt_jk_kabkota": (2824, 2017, 2025),
    "D25_kemiskinan_provinsi": (192, 2015, 2026),
    "D06b_angkatan_kerja_provinsi": (2394, 2021, 2026),
    # BPS Provinsi Jawa Tengah (domain 3300)
    "J03_tpt_kabkota_pendidikan_jateng": (1864, 2019, 2023, "3300"),
}


def call(var, th, domain="0000"):
    url = f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/{domain}/var/{var}/th/{th}/key/{KEY}"
    req = urllib.request.Request(url, headers={"User-Agent": "dac-research-script"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def decode(js, var):
    vv = {str(v["val"]): v["label"] for v in js.get("vervar", [])}
    tv = {str(v["val"]): v["label"] for v in js.get("turvar", [])}
    tt = {str(v["val"]): v["label"] for v in js.get("tahun", [])}
    th = {str(v["val"]): v["label"] for v in js.get("turtahun", [])}
    rows = []
    for k, val in (js.get("datacontent") or {}).items():
        for vc in sorted(vv, key=len, reverse=True):
            if not k.startswith(vc):
                continue
            r = k[len(vc):]
            if not r.startswith(str(var)):
                continue
            r = r[len(str(var)):]
            done = False
            for tc in sorted(tv, key=len, reverse=True):
                if not r.startswith(tc):
                    continue
                r2 = r[len(tc):]
                for yc in tt:
                    if r2.startswith(yc) and r2[len(yc):] in th:
                        rows.append([vv[vc], tv[tc], tt[yc], th[r2[len(yc):]], val])
                        done = True
                        break
                if done:
                    break
            if done:
                break
    return rows


for name, spec in VARS.items():
    var, y0, y1 = spec[:3]; domain = spec[3] if len(spec) > 3 else "0000"
    allrows = []
    for year in range(y0, y1 + 1):
        th_id = year - 1900
        try:
            js = call(var, th_id, domain)
        except Exception as e:
            print("GAGAL", name, year, e)
            continue
        if js.get("status") != "OK" or js.get("data-availability") == "list-not-available":
            print("kosong", name, year, js.get("message", js.get("data-availability")))
            continue
        with open(os.path.join(OUT, f"{name}_raw_{year}.json"), "w", encoding="utf-8") as f:
            json.dump(js, f, ensure_ascii=False)
        rows = decode(js, var)
        allrows += rows
        print(name, year, len(rows), "baris")
        time.sleep(0.4)
    with open(os.path.join(OUT, f"{name}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["wilayah_kategori", "turvar", "tahun", "periode", "nilai"])
        w.writerows(allrows)
print("Selesai. Cek folder", OUT)
