"""GeoJSON kab/kota (geometri geoBoundaries, disederhanakan) + atribut persistensi TPT dari BPS (t5_kabkota_jejak).
Keluaran: Spatial/IDN_kabkota_persistensi_v7.geojson untuk peta kab/kota di dashboard v7."""
import json
import sys
sys.setrecursionlimit(100000)
import pandas as pd


def rdp(pts, eps):
    """Ramer-Douglas-Peucker untuk satu ring."""
    if len(pts) < 4:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    n = (dx * dx + dy * dy) ** 0.5 or 1e-12
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return rdp(pts[:idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]


def ring(r, eps=0.003):
    """Ring tertutup: pecah dua agar RDP tidak runtuh (titik awal = titik akhir)."""
    pts = [(round(x, 4), round(y, 4)) for x, y in r]
    if len(pts) < 8:
        return [list(p) for p in pts]
    m = len(pts) // 2
    out = rdp(pts[:m + 1], eps)[:-1] + rdp(pts[m:], eps)
    if len(out) < 4:
        out = pts
    return [list(p) for p in out]


def simp(geom):
    if geom['type'] == 'Polygon':
        return {'type': 'Polygon', 'coordinates': [ring(r) for r in geom['coordinates']]}
    return {'type': 'MultiPolygon', 'coordinates': [[ring(r) for r in poly] for poly in geom['coordinates']]}


g = json.load(open('Spatial/IDN_kabkota_kode_bps.geojson', encoding='utf-8'))
j = pd.read_csv('Processed_Dataset/tableau/t5_kabkota_jejak.csv', dtype={'kode': str}).set_index('kode')
feats, miss = [], []
for f in g['features']:
    k = str(f['properties']['kode'])
    if k not in j.index:
        miss.append(k)
        continue
    r = j.loc[k]
    feats.append({'type': 'Feature', 'geometry': simp(f['geometry']), 'properties': {
        'kode': k, 'nama_kab': r['nama'], 'prov_kab': r['nama_prov'], 'kota': bool(r['is_kota']),
        'thn_atas_nas': int(r['tahun_atas_nasional']), 'thn_atas_sej': int(r['tahun_atas_sejenis']),
        'n_tahun': int(r['n_tahun']), 'rata_tpt_kab': float(r['rata_tpt']), 'ganda': bool(r['persisten_ganda'])}})
out = {'type': 'FeatureCollection', 'features': feats}
json.dump(out, open('Spatial/IDN_kabkota_persistensi_v7.geojson', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(feats), 'fitur; tanpa pasangan:', miss)
