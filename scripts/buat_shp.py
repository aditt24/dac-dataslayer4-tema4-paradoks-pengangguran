"""
Membuat shapefile (SHP) dari batas wilayah geoBoundaries IDN ADM2 (sumber asli: BPS via WFP/OCHA, CC BY 3.0 IGO).
Output: Spatial/
  - IDN_kabkota_2020/            : seluruh kab/kota Indonesia (519 poligon)
  - JATENG_kabkota_analisis/     : 35 kab/kota Jawa Tengah + atribut hasil analisis (TPT, LISA, dll.)
  - JATENG_kabkota.geojson       : versi GeoJSON (untuk Power BI Azure Map / konversi TopoJSON di mapshaper.org)
"""
import os, re, json
import pandas as pd
import shapefile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "Raw_Dataset", "spasial_non_bps", "geoBoundaries-IDN-ADM2_simplified.geojson")
OUT = os.path.join(BASE, "Spatial"); os.makedirs(OUT, exist_ok=True)
PRJ = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
gj = json.load(open(SRC, encoding="utf-8"))


def parts_of(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return [ring for poly in polys for ring in poly]


def write(path, feats, fields, rowfn):
    w = shapefile.Writer(path, shapeType=shapefile.POLYGON)
    for name, typ, size, dec in fields:
        w.field(name, typ, size=size, decimal=dec)
    for ft in feats:
        w.poly(parts_of(ft["geometry"]))
        w.record(*rowfn(ft))
    w.close()
    open(path + ".prj", "w").write(PRJ)


# 1) Seluruh Indonesia
os.makedirs(os.path.join(OUT, "IDN_kabkota_2020"), exist_ok=True)
write(os.path.join(OUT, "IDN_kabkota_2020", "IDN_kabkota_2020"), gj["features"],
      [("nama", "C", 60, 0), ("shapeID", "C", 40, 0)],
      lambda ft: [ft["properties"]["shapeName"], ft["properties"]["shapeID"]])

# 2) Jawa Tengah + atribut analisis
sp = pd.read_csv(os.path.join(BASE, "Processed_Dataset", "v5", "F_jateng_kabkota_spasial.csv"))
sp["key"] = sp.iloc[:, 0].astype(str).str.upper().str.strip()
attr = sp.set_index("key")


def key_of(name):
    return re.sub(r"\s+", " ", name.upper().replace("KABUPATEN ", "")).strip()


jt = []
for ft in gj["features"]:
    k = key_of(ft["properties"]["shapeName"])
    if k in attr.index:
        ring = parts_of(ft["geometry"])[0]
        cx = sum(p[0] for p in ring) / len(ring); cy = sum(p[1] for p in ring) / len(ring)
        if 108.5 <= cx <= 111.8 and -8.4 <= cy <= -5.8:
            jt.append(ft)
print("Jateng poligon:", len(jt))


def g(k, c, d=None):
    try:
        v = attr.loc[k, c]
        return d if pd.isna(v) else v
    except KeyError:
        return d


cols = [("nama", "C", 40, 0), ("tpt25", "N", 8, 2), ("tpt_dasar", "N", 8, 2), ("tpt_mngh", "N", 8, 2), ("tpt_tinggi", "N", 8, 2),
        ("rls", "N", 8, 2), ("peng_kap", "N", 12, 0), ("lisa_tpt", "C", 24, 0), ("lisa_mngh", "C", 24, 0)]
os.makedirs(os.path.join(OUT, "JATENG_kabkota_analisis"), exist_ok=True)
write(os.path.join(OUT, "JATENG_kabkota_analisis", "JATENG_kabkota_analisis"), jt, cols,
      lambda ft: [key_of(ft["properties"]["shapeName"]).title()] + [g(key_of(ft["properties"]["shapeName"]), c, 0) for c in ["tpt25", "dasar", "menengah", "tinggi", "rls", "peng_kap"]]
      + [g(key_of(ft["properties"]["shapeName"]), c, "") for c in ["lisa_tpt25", "lisa_menengah"]])
fc = {"type": "FeatureCollection", "features": []}
for ft in jt:
    k = key_of(ft["properties"]["shapeName"])
    props = {"nama": k.title()}
    for c in ["tpt25", "dasar", "menengah", "tinggi", "rls", "peng_kap", "lisa_tpt25", "lisa_menengah"]:
        v = g(k, c, None)
        props[c] = (None if v is None else (float(v) if not isinstance(v, str) else v))
    fc["features"].append({"type": "Feature", "properties": props, "geometry": ft["geometry"]})
json.dump(fc, open(os.path.join(OUT, "JATENG_kabkota.geojson"), "w", encoding="utf-8"), ensure_ascii=False)
print("Selesai:", os.listdir(OUT))
