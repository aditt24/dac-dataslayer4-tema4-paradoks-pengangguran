# -*- coding: utf-8 -*-
"""Redesain v8 dashboard Tableau DAC Tema 4, di atas v7c (DAC_Dashboard_Tema4_FINAL.twb).

Pemakaian: python redesign_tableau_v8.py <v7c.twb> <output.twb>
Basis = hasil redesign_tableau_v7.py yang sudah lolos cek di Tableau, jadi v7c tidak dibangun ulang.
Tidak mengubah data atau angka; menambah kartu "Cek provinsimu", Fokus kebijakan, grafik keputusan,
teks/tata letak baru, font Tableau, alias nama provinsi.
"""
import re
import sys
import uuid
import xml.etree.ElementTree as ET

SRC, OUT = sys.argv[1], sys.argv[2]
t = open(SRC, encoding='utf-8').read()
DS = 'federated.0dzsn910err68y1dlgf4w1omb1y9'      # Provinsi & KabKota
F = f'[{DS}]'
P_PROV = '[Parameters].[Parameter 0379056854634496]'
P_MODE = '[Parameters].[Parameter 0379056854757377]'
P_ACUAN = '[Parameters].[Parameter 0379056854831106]'
P_W = ['[Parameters].[Parameter 0379056855040004]', '[Parameters].[Parameter 0379056855146501]',
       '[Parameters].[Parameter 0379056855212038]', '[Parameters].[Parameter 0379056855277575]']
P_FOKUS_ID = 'Parameter 9400000000000099'
P_FOKUS = f'[Parameters].[{P_FOKUS_ID}]'

PAPER, CARD, INK, INK2, MUTED, AMBER = '#f3eee4', '#ffffff', '#14213d', '#4a5468', '#7c8494', '#f2a93b'
COBALT, COBALT_D, VERM, OXBLOOD, SAGE, GREY = '#2f5fa7', '#1d3f7a', '#e0603a', '#a12a1c', '#3f9363', '#d6cfc2'
F_BOLD, F_SEMI, F_BODY = 'Tableau Bold', 'Tableau Semibold', 'Tableau Book'
Q = '&quot;'


def rep(old, new, n=1):
    global t
    c = t.count(old)
    if n is None:
        assert c >= 1, ('tidak ditemukan', old[:120])
    else:
        assert c == n, (c, n, old[:160])
    t = t.replace(old, new)


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace("'", '&apos;').replace('"', '&quot;'))


def run(text, size=11, color=INK, font=F_BODY, bold=False):
    a = f" fontcolor='{color}' fontname='{font}' fontsize='{size}'"
    if bold:
        a = " bold='true'" + a
    return f"<run{a}>{esc(text)}</run>"


def frun(field, size=11, color=INK, font=F_BODY, bold=False):
    a = f" fontcolor='{color}' fontname='{font}' fontsize='{size}'"
    if bold:
        a = " bold='true'" + a
    return f"<run{a}><![CDATA[<{field}>]]></run>"


NL = '<run>Æ&#10;</run>'


def ft(*runs):
    return '<formatted-text>' + ''.join(runs) + '</formatted-text>'


def worksheet_block(name):
    m = re.search(r"<worksheet name='" + re.escape(name) + r"'>.*?</worksheet>", t, re.S)
    assert m, name
    return m


def set_ws(name, new):
    global t
    m = worksheet_block(name)
    t = t[:m.start()] + new + t[m.end():]


def set_title(name, *runs):
    w = worksheet_block(name).group(0)
    title = '<layout-options><title>' + ft(*runs) + '</title></layout-options>'
    if '<layout-options>' in w:
        w = re.sub(r'<layout-options>.*?</layout-options>', lambda _: title, w, count=1, flags=re.S)
    else:
        w = w.replace('<table>', title + '<table>', 1)
    set_ws(name, w)


def calc(cid, cap, formula, dtype='real', role='measure', typ='quantitative'):
    return (f"<column caption='{cap}' datatype='{dtype}' name='[{cid}]' role='{role}' type='{typ}'>"
            f"<calculation class='tableau' formula='{formula}' /></column>")


def ci(col, deriv, name, typ):
    return f"<column-instance column='[{col}]' derivation='{deriv}' name='[{name}]' pivot='key' type='{typ}' />"


def plain_window(name):
    return (f"<window class='worksheet' name='{name}'><cards><edge name='left'><strip size='160'><card type='pages' />"
            "<card type='filters' /><card type='marks' /></strip></edge><edge name='top'><strip size='2147483647'>"
            "<card type='columns' /></strip><strip size='2147483647'><card type='rows' /></strip><strip size='29'>"
            f"<card type='title' /></strip></edge></cards><simple-id uuid='{{{str(uuid.uuid4()).upper()}}}' /></window>")


NOLINES = ("<style-rule element='gridline'><format attr='line-visibility' value='off' /></style-rule>"
           f"<style-rule element='axis'><format attr='color' value='{INK2}' /></style-rule>"
           "<style-rule element='table-div'><format attr='line-visibility' scope='rows' value='off' />"
           "<format attr='line-visibility' scope='cols' value='off' /></style-rule>"
           "<style-rule element='worksheet'><format attr='display-field-labels' scope='rows' value='false' />"
           "<format attr='display-field-labels' scope='cols' value='false' /></style-rule>")
CLEAN = NOLINES + "<style-rule element='zeroline'><format attr='line-visibility' value='off' /></style-rule>"

# ================================================================ 0. font: Georgia -> font Tableau
t = t.replace("fontname='Georgia'", f"fontname='{F_BOLD}'")
t = t.replace("value='Georgia'", f"value='{F_BOLD}'")
assert 'Georgia' not in t

# ================================================================ 1. alias nama provinsi (nilai asli tetap)
NAMA = {}
for raw in ['ACEH', 'BALI', 'BANTEN', 'BENGKULU', 'DI YOGYAKARTA', 'DKI JAKARTA', 'GORONTALO', 'JAMBI', 'JAWA BARAT',
            'JAWA TENGAH', 'JAWA TIMUR', 'KALIMANTAN BARAT', 'KALIMANTAN SELATAN', 'KALIMANTAN TENGAH',
            'KALIMANTAN TIMUR', 'KALIMANTAN UTARA', 'KEP. BANGKA BELITUNG', 'KEP. RIAU', 'LAMPUNG', 'MALUKU',
            'MALUKU UTARA', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR', 'PAPUA', 'PAPUA BARAT', 'PAPUA BARAT DAYA',
            'PAPUA PEGUNUNGAN', 'PAPUA SELATAN', 'PAPUA TENGAH', 'RIAU', 'SULAWESI BARAT', 'SULAWESI SELATAN',
            'SULAWESI TENGAH', 'SULAWESI TENGGARA', 'SULAWESI UTARA', 'SUMATERA BARAT', 'SUMATERA SELATAN',
            'SUMATERA UTARA']:
    nice = raw.title()
    nice = (nice.replace('Dki ', 'DKI ').replace('Di Yogyakarta', 'DI Yogyakarta')
            .replace('Kep. ', 'Kepulauan '))
    NAMA[raw] = nice
ALIAS = '<aliases>' + ''.join(f"<alias key='&quot;{k}&quot;' value='{v}' />" for k, v in NAMA.items()) + '</aliases>'
# kolom wilayah di definisi datasource Provinsi & KabKota (bukan di dependensi worksheet)
ds_start = t.index(f"<datasource caption='Provinsi &amp; KabKota' inline='true' name='{DS}'")
ds_end = t.index('</datasource>', ds_start)
blk = t[ds_start:ds_end]
old = "<column datatype='string' name='[wilayah]' role='dimension' type='nominal' />"
assert blk.count(old) == 1, blk.count(old)
blk = blk.replace(old, "<column datatype='string' name='[wilayah]' role='dimension' type='nominal'>" + ALIAS + '</column>')
t = t[:ds_start] + blk + t[ds_end:]

# ================================================================ 2. parameter Fokus kebijakan
FOKUS = ['Seimbang', 'Kurangi pengangguran', 'Perbaiki mutu kerja', 'Anak muda (NEET)', 'Atur sendiri']
BOBOT = {'Seimbang': (0.25, 0.25, 0.25, 0.25), 'Kurangi pengangguran': (0.4, 0.4, 0.1, 0.1),
         'Perbaiki mutu kerja': (0.1, 0.1, 0.4, 0.4), 'Anak muda (NEET)': (0.2, 0.6, 0.1, 0.1)}
P_FOKUS_DEF = (f"<column caption='Fokus kebijakan' datatype='string' name='[{P_FOKUS_ID}]' param-domain-type='list' "
               f"role='measure' type='nominal' value='{Q}Seimbang{Q}'><calculation class='tableau' formula='{Q}Seimbang{Q}' />"
               '<members>' + ''.join(f"<member value='{Q}{esc(f)}{Q}' />" for f in FOKUS) + '</members></column>')
k = t.index("<datasource hasconnection='false' inline='true' name='Parameters' version='18.1'>")
k = t.index('<column ', k)          # sesudah <aliases enabled='yes' />
t = t[:k] + P_FOKUS_DEF + t[k:]


def wexpr(i):
    cases = ' '.join(f'WHEN {Q}{esc(f)}{Q} THEN {BOBOT[f][i]}' for f in BOBOT)
    return f'(CASE {P_FOKUS} {cases} ELSE {P_W[i]} END)'


def patch_formula(cid):
    global t
    pat = re.compile(r"(<column caption='[^']*' datatype='real' name='\[" + cid + r"\]'[^>]*>\s*<calculation class='tableau' formula=')([^']*)(')")
    ms = list(pat.finditer(t))
    assert ms, cid
    for m in reversed(ms):
        f = m.group(2)
        for i in range(4):
            assert P_W[i] in f, (cid, i)
            f = f.replace(P_W[i], wexpr(i))
        t = t[:m.start(2)] + f + t[m.end(2):]
    return len(ms)


patch_formula('Calculation_0379056855822353')   # Total Bobot
patch_formula('Calculation_0379056855859218')   # Skor Dinamis
for ws in ('H2-G Penimbang', 'H2-G Pesan Bobot'):
    w = worksheet_block(ws).group(0)
    w = w.replace("<datasource-dependencies datasource='Parameters'>", "<datasource-dependencies datasource='Parameters'>" + P_FOKUS_DEF, 1)
    set_ws(ws, w)
rep(f"THEN {Q}Isi minimal satu bobot untuk melihat ranking.{Q}", f"THEN {Q}Atur sendiri: isi minimal satu bobot.{Q}", None)

# ================================================================ 3. kalkulasi kartu & keputusan
C_PK, C_FK = 'Calculation_9400000000000001', 'Calculation_9400000000000002'
C_MED = ['Calculation_9400000000000003', 'Calculation_9400000000000004', 'Calculation_9400000000000005', 'Calculation_9400000000000006']
C_YAKIN, C_STABIL, C_REKOM = 'Calculation_9400000000000007', 'Calculation_9400000000000008', 'Calculation_9400000000000009'
C_D = ['Calculation_9400000000000011', 'Calculation_9400000000000012', 'Calculation_9400000000000013', 'Calculation_9400000000000014']
C_TIPE, C_SOROT, C_AKSI = 'Calculation_9400000000000021', 'Calculation_9400000000000022', 'Calculation_9400000000000023'
Z = ['z_tpt', 'z_neet', 'z_tsp', 'z_informal']
DNAME = ['TPT', 'NEET', 'Setengah pengangguran', 'Informal']

C_RT, C_RK = 'Calculation_9400000000000031', 'Calculation_9400000000000032'
D_RT = calc(C_RT, 'Teks Peringkat TPT', 'STR(INT([rank_tpt]))', 'string', 'dimension', 'nominal')
D_RK = calc(C_RK, 'Teks Peringkat KTL', 'STR(INT([rank_ktl]))', 'string', 'dimension', 'nominal')
D_PK = calc(C_PK, 'Provinsi Kartu', f'IF {P_PROV} = {Q}Indonesia{Q} THEN {Q}NUSA TENGGARA BARAT{Q} ELSE {P_PROV} END', 'string', 'dimension', 'nominal')
D_FK = calc(C_FK, 'Filter Kartu', f'[wilayah] = [{C_PK}]', 'boolean', 'dimension', 'nominal')
D_MED = [calc(C_MED[i], f'Median {DNAME[i]}', f'{{ FIXED : MEDIAN([{Z[i]}]) }}') for i in range(4)]
D_YAKIN = calc(C_YAKIN, 'Keyakinan',
               f'IF [prob_top10] = 0 THEN {Q}Tidak pernah 10 besar prioritas{Q} '
               f'ELSE {Q}10 besar di {Q} + STR(INT(ROUND([prob_top10]*100))) + {Q}% skenario bobot{Q} END',
               'string', 'dimension', 'nominal')
D_STABIL = calc(C_STABIL, 'Stabil',
                f'IF [kuadran_stabil_3batas] THEN {Q}tipe stabil{Q} ELSE {Q}tipe bisa berubah{Q} END',
                'string', 'dimension', 'nominal')
REKOM = [('Rentan Ganda', 'Padat karya formal dan program NEET'),
         ('Rentan Tersembunyi', 'Formalisasi usaha mikro, hilirisasi'),
         ('Antrean Kerja Formal', 'Percepat penyerapan kerja formal'),
         ('Relatif Layak', 'Pertahankan, pantau mutu kerja')]
D_REKOM = calc(C_REKOM, 'Rekomendasi', 'CASE [kuadran] ' + ' '.join(f'WHEN {Q}{a}{Q} THEN {Q}{b}{Q}' for a, b in REKOM[:3])
               + f' ELSE {Q}{REKOM[3][1]}{Q} END', 'string', 'dimension', 'nominal')
D_D = [calc(C_D[i], DNAME[i], f'ROUND(100 * (AVG([{Z[i]}]) - AVG([{C_MED[i]}])), 0)') for i in range(4)]
D_TIPE = calc(C_TIPE, 'Tipe Kartu', f'{{ FIXED : MAX(IF [{C_FK}] THEN [kuadran] END) }}', 'string', 'dimension', 'nominal')
D_SOROT = calc(C_SOROT, 'Sorot Tipe', f'[kuadran] = [{C_TIPE}]', 'boolean', 'dimension', 'nominal')
AKSI = [('Rentan Ganda', 'Padat karya, NEET'), ('Rentan Tersembunyi', 'Formalisasi usaha mikro'),
        ('Antrean Kerja Formal', 'Serap ke kerja formal'), ('Relatif Layak', 'Jaga mutu kerja')]
D_AKSI = calc(C_AKSI, 'Aksi Tipe', 'CASE [kuadran] ' + ' '.join(f'WHEN {Q}{a}{Q} THEN {Q}{b}{Q}' for a, b in AKSI[:3])
              + f' ELSE {Q}{AKSI[3][1]}{Q} END', 'string', 'dimension', 'nominal')
C_WK, C_CONTOH = 'Calculation_9400000000000024', 'Calculation_9400000000000025'
D_WK = calc(C_WK, 'Warna Keputusan', f'IF [{C_SOROT}] THEN [kuadran] ELSE {Q}Lain{Q} END', 'string', 'dimension', 'nominal')
D_CONTOH = calc(C_CONTOH, 'Catatan Contoh', f'IF {P_PROV} = {Q}Indonesia{Q} THEN {Q}(contoh){Q} ELSE {Q}{Q} END', 'string', 'dimension', 'nominal')
ALL_NEW = D_WK + D_CONTOH + D_RT + D_RK + D_PK + D_FK + ''.join(D_MED) + D_YAKIN + D_STABIL + D_REKOM + ''.join(D_D) + D_TIPE + D_SOROT + D_AKSI
k = t.index("<column caption='Singkatan' datatype='string' name='[Calculation_0379056855416840]'")
t = t[:k] + ALL_NEW + t[k:]

# palet: Sorot Tipe (bool) dan Measure Names kartu penyebab
k = t.index("<column-instance column='[Calculation_0379056883658815]'")
t = t[:k] + ci(C_SOROT, 'None', f'none:{C_SOROT}:nk', 'nominal') + ci(C_WK, 'None', f'none:{C_WK}:nk', 'nominal') + t[k:]
PAL = (f"<encoding attr='color' field='[none:{C_SOROT}:nk]' type='palette'>"
       f"<map to='{VERM}'><bucket>true</bucket></map><map to='#ddd6ca'><bucket>false</bucket></map></encoding>")
QUADC = {'Antrean Kerja Formal': COBALT, 'Relatif Layak': SAGE, 'Rentan Ganda': OXBLOOD, 'Rentan Tersembunyi': VERM, 'Lain': '#e4ded3'}
PAL_WK = (f"<encoding attr='color' field='[none:{C_WK}:nk]' type='palette'>" + ''.join(
    f"<map to='{c}'><bucket>&quot;{b}&quot;</bucket></map>" for b, c in QUADC.items()) + '</encoding>')
PAL = PAL + PAL_WK
k = t.index("<encoding attr='color' field='[none:kuadran:nk]' type='palette'>")
t = t[:k] + PAL + t[k:]
# alias Measure Names tetap (caption kalkulasi sudah nama tampil)

# ================================================================ 4. worksheet baru
P_PROV_DEP = ("<datasource-dependencies datasource='Parameters'>"
              "<column caption='Pilih Provinsi' datatype='string' name='[Parameter 0379056854634496]' param-domain-type='list' "
              f"role='measure' type='nominal' value='{Q}Indonesia{Q}'><calculation class='tableau' formula='{Q}Indonesia{Q}' /></column>"
              '</datasource-dependencies>')
RAW = ("<column datatype='string' name='[wilayah]' role='dimension' type='nominal' />"
       "<column datatype='string' name='[kuadran]' role='dimension' type='nominal' />"
       "<column caption='Peringkat TPT' datatype='real' name='[rank_tpt]' role='measure' type='quantitative' />"
       "<column caption='Peringkat KTL' datatype='real' name='[rank_ktl]' role='measure' type='quantitative' />"
       "<column datatype='real' name='[prob_top10]' role='measure' type='quantitative' />"
       "<column datatype='boolean' name='[kuadran_stabil_3batas]' role='dimension' type='nominal' />"
       + ''.join(f"<column datatype='real' name='[{z}]' role='measure' type='quantitative' />" for z in Z))
FILTER_KARTU = (f"<filter class='categorical' column='{F}.[none:{C_FK}:nk]'>"
                f"<groupfilter function='member' level='[none:{C_FK}:nk]' member='true' user:ui-domain='database' "
                "user:ui-enumeration='inclusive' user:ui-marker='enumerate' /></filter>")


def ws_xml(name, title_runs, deps, view_extra, style, pane, rows='', cols='', with_param=True):
    ttl = f"<layout-options><title>{ft(*title_runs)}</title></layout-options>" if title_runs else ''
    dss = f"<datasource caption='Provinsi &amp; KabKota' name='{DS}' />" + ("<datasource name='Parameters' />" if with_param else '')
    return (f"<worksheet name='{name}'>{ttl}<table><view><datasources>{dss}</datasources>"
            f"<datasource-dependencies datasource='{DS}'>{deps}</datasource-dependencies>"
            + (P_PROV_DEP if with_param else '') +
            f"{view_extra}<aggregation value='true' /></view><style>{style}</style><panes>{pane}</panes>"
            + (f'<rows>{rows}</rows>' if rows else '<rows />') + (f'<cols>{cols}</cols>' if cols else '<cols />')
            + f"</table><simple-id uuid='{{{str(uuid.uuid4()).upper()}}}' /></worksheet>")


CI_FK = ci(C_FK, 'None', f'none:{C_FK}:nk', 'nominal')
BASE_DEPS = D_PK + D_FK + RAW + CI_FK
SLICE_FK = FILTER_KARTU + f"<slices><column>{F}.[none:{C_FK}:nk]</column></slices>"

# ---- K1 peringkat
K1, K2, K3, KR = 'H2-K1 Peringkat', 'H2-K2 Penyebab', 'H2-K3 Diagnosis', 'H2-R Keputusan'
k1_deps = BASE_DEPS + D_RT + D_RK + D_CONTOH + ci(C_CONTOH, 'None', f'none:{C_CONTOH}:nk', 'nominal') + ci('wilayah', 'None', 'none:wilayah:nk', 'nominal') \
    + ci(C_RT, 'None', f'none:{C_RT}:nk', 'nominal') + ci(C_RK, 'None', f'none:{C_RK}:nk', 'nominal')
k1_pane = ("<pane selection-relaxation-option='selection-relaxation-allow'><view><breakdown value='auto' /></view>"
           "<mark class='Text' /><encodings>"
           f"<text column='{F}.[none:wilayah:nk]' /><text column='{F}.[none:{C_RT}:nk]' /><text column='{F}.[none:{C_RK}:nk]' /><text column='{F}.[none:{C_CONTOH}:nk]' />"
           "</encodings><style><style-rule element='mark'><format attr='mark-labels-show' value='false' />"
           "</style-rule></style></pane>")
k1_style = CLEAN
# isi kartu di judul sheet (sel teks Tableau memotong baris berhuruf besar)
K1_XML = ws_xml(K1, [run('Cek provinsimu', 14, INK, F_SEMI, True), NL,
                     frun(f'{F}.[none:wilayah:nk]', 15, INK, F_BOLD, True), run('   ', 9, INK2), frun(f'{F}.[none:{C_CONTOH}:nk]', 9, MUTED), NL,
                     run('Peringkat TPT  ', 10, INK2), frun(f'{F}.[none:{C_RT}:nk]', 22, COBALT, F_BOLD, True),
                     run('   →   ', 14, INK2), run('kerja tidak layak  ', 10, INK2),
                     frun(f'{F}.[none:{C_RK}:nk]', 22, VERM, F_BOLD, True)],
                k1_deps, SLICE_FK, k1_style, k1_pane)

# ---- K2 penyebab: selisih dari median 38 provinsi (Measure Names)
k2_deps = BASE_DEPS + ''.join(D_MED) + ''.join(D_D) + ''.join(
    ci(C_D[i], 'User', f'usr:{C_D[i]}:qk', 'quantitative') for i in range(4))
MN = ''.join(f"<groupfilter function='member' level='[:Measure Names]' member='&quot;{F}.[usr:{c}:qk]&quot;' />" for c in C_D)
k2_view = (SLICE_FK.replace('</slices>', f'<column>{F}.[:Measure Names]</column></slices>')
           + f"<filter class='categorical' column='{F}.[:Measure Names]'><groupfilter function='union' user:op='manual'>{MN}</groupfilter></filter>"
           + f"<manual-sort column='{F}.[:Measure Names]' direction='ASC'><dictionary>"
           + ''.join(f'<bucket>&quot;{F}.[usr:{c}:qk]&quot;</bucket>' for c in C_D) + '</dictionary></manual-sort>')
# pindahkan filter MN sebelum slices
k2_view = (FILTER_KARTU
           + f"<filter class='categorical' column='{F}.[:Measure Names]'><groupfilter function='union' user:op='manual'>{MN}</groupfilter></filter>"
           + f"<manual-sort column='{F}.[:Measure Names]' direction='ASC'><dictionary>"
           + ''.join(f'<bucket>&quot;{F}.[usr:{c}:qk]&quot;</bucket>' for c in C_D) + '</dictionary></manual-sort>'
           + f"<slices><column>{F}.[none:{C_FK}:nk]</column><column>{F}.[:Measure Names]</column></slices>")
MN_PAL = (f"<encoding attr='color' field='{F}.[:Measure Names]' type='palette'>"
          + ''.join(f"<map to='{col}'><bucket>&quot;{F}.[usr:{c}:qk]&quot;</bucket></map>"
                    for c, col in zip(C_D, [COBALT, COBALT, VERM, VERM])) + '</encoding>')
k2_style = (f"<style-rule element='axis'><encoding attr='space' class='0' field='{F}.[Multiple Values]' field-type='quantitative' "
            "max='90' min='-90' range-type='fixed' scope='cols' type='space' />"
            f"<format attr='display' class='0' field='{F}.[Multiple Values]' scope='cols' value='false' /></style-rule>"
            "<style-rule element='cell'>" + ''.join(f"<format attr='text-format' field='{F}.[usr:{c}:qk]' value='+#,##0;-#,##0;0' />" for c in C_D) + "</style-rule>"
            f"<style-rule element='header'><format attr='width' field='{F}.[:Measure Names]' value='215' /></style-rule>"
            f"<style-rule element='label'><format attr='font-size' value='10' /><format attr='color' value='{INK}' /></style-rule>"
            f"<style-rule element='mark'>{MN_PAL}</style-rule>"
            + NOLINES + f"<style-rule element='zeroline'><format attr='stroke-size' value='2' /><format attr='color' value='{INK}' /></style-rule>")
k2_pane = ("<pane selection-relaxation-option='selection-relaxation-allow'><view><breakdown value='auto' /></view>"
           "<mark class='Bar' /><encodings>"
           f"<text column='{F}.[Multiple Values]' />"
           "</encodings><customized-tooltip>" + ft(
               run('Selisih skor provinsi ini dari median 38 provinsi (skala 0–100). Positif = lebih rentan.', 10, INK)) +
           "</customized-tooltip><style><style-rule element='mark'><format attr='mark-labels-show' value='true' />"
           "<format attr='size' value='0.6' /><format attr='mark-color' value='{INK2}' /></style-rule></style></pane>")
K2_XML = ws_xml(K2, [run('Penyebabnya', 12, INK, F_SEMI, True), run('   selisih dari median 38 provinsi; kanan = lebih rentan', 9, INK2)],
                k2_deps, k2_view, k2_style, k2_pane, rows=f'{F}.[:Measure Names]', cols=f'{F}.[Multiple Values]')

# ---- K3 diagnosis
k3_deps = BASE_DEPS + D_YAKIN + D_STABIL + D_REKOM + ''.join(
    ci(c, 'None', f'none:{c}:nk', 'nominal') for c in (C_YAKIN, C_STABIL, C_REKOM)) + ci('kuadran', 'None', 'none:kuadran:nk', 'nominal')
k3_pane = ("<pane selection-relaxation-option='selection-relaxation-allow'><view><breakdown value='auto' /></view>"
           "<mark class='Text' /><encodings>"
           f"<text column='{F}.[none:kuadran:nk]' /><text column='{F}.[none:{C_REKOM}:nk]' />"
           f"<text column='{F}.[none:{C_YAKIN}:nk]' /><text column='{F}.[none:{C_STABIL}:nk]' />"
           "</encodings><customized-label>" + ft(
               run('Tipe: ', 12, INK2, F_SEMI), frun(f'{F}.[none:kuadran:nk]', 15, OXBLOOD, F_BOLD, True), NL,
               run('Usulan tim: ', 10, INK2), frun(f'{F}.[none:{C_REKOM}:nk]', 10, INK, F_SEMI), NL,
               frun(f'{F}.[none:{C_YAKIN}:nk]', 9, INK2), run(' · ', 9, INK2), frun(f'{F}.[none:{C_STABIL}:nk]', 9, INK2)) +
           "</customized-label><style><style-rule element='mark'><format attr='mark-labels-show' value='true' />"
           "<format attr='mark-labels-cull' value='false' /></style-rule></style></pane>")
K3_XML = ws_xml(K3, None, k3_deps, SLICE_FK, CLEAN, k3_pane)

# ---- Keputusan: jumlah provinsi per tipe, tipe provinsi kartu disorot
kr_deps = BASE_DEPS + D_TIPE + D_SOROT + D_WK + D_AKSI + ci('kuadran', 'None', 'none:kuadran:nk', 'nominal') + ci(C_WK, 'None', f'none:{C_WK}:nk', 'nominal') \
    + ci(C_SOROT, 'None', f'none:{C_SOROT}:nk', 'nominal') + ci(C_AKSI, 'Attribute', f'attr:{C_AKSI}:nk', 'nominal') \
    + ci('wilayah', 'CountD', 'ctd:wilayah:qk', 'quantitative')
kr_view = (f"<manual-sort column='{F}.[none:kuadran:nk]' direction='ASC'><dictionary>"
           + ''.join(f'<bucket>&quot;{a}&quot;</bucket>' for a, _ in AKSI) + '</dictionary></manual-sort>')
kr_style = (f"<style-rule element='axis'><encoding attr='space' class='0' field='{F}.[ctd:wilayah:qk]' field-type='quantitative' "
            "max='52' min='0' range-type='fixed' scope='cols' type='space' />"
            f"<format attr='display' class='0' field='{F}.[ctd:wilayah:qk]' scope='cols' value='false' /></style-rule>"
            f"<style-rule element='header'><format attr='width' field='{F}.[none:kuadran:nk]' value='165' /></style-rule>"
            f"<style-rule element='header'><format attr='font-size' value='10' /><format attr='color' value='{INK}' /></style-rule>"
            f"<style-rule element='label'><format attr='font-size' value='10' /><format attr='color' value='{INK}' /></style-rule>"
            f"<style-rule element='mark'>{PAL.replace(f'field={chr(39)}[none:', f'field={chr(39)}{F}.[none:')}</style-rule>" + CLEAN)
kr_pane = ("<pane selection-relaxation-option='selection-relaxation-allow'><view><breakdown value='auto' /></view>"
           "<mark class='Bar' /><encodings>"
           f"<color column='{F}.[none:{C_WK}:nk]' /><text column='{F}.[ctd:wilayah:qk]' /><text column='{F}.[attr:{C_AKSI}:nk]' />"
           "</encodings><customized-tooltip>" + ft(
               frun(f'{F}.[none:kuadran:nk]', 10, INK, F_SEMI, True), run(': ', 10, INK), frun(f'{F}.[ctd:wilayah:qk]', 10, INK),
               run(' provinsi. Usulan (tafsiran tim): ', 10, INK), frun(f'{F}.[attr:{C_AKSI}:nk]', 10, INK)) +
           "</customized-tooltip><customized-label>" + ft(
               frun(f'{F}.[ctd:wilayah:qk]', 13, INK, F_BOLD, True), run('  ·  ', 9, MUTED), frun(f'{F}.[attr:{C_AKSI}:nk]', 10, INK2)) +
           "</customized-label><style><style-rule element='mark'><format attr='mark-labels-show' value='true' />"
           "<format attr='mark-labels-cull' value='false' /><format attr='size' value='0.62' /></style-rule></style></pane>")
KR_XML = ws_xml(KR, None, kr_deps, kr_view, kr_style, kr_pane, rows=f'{F}.[none:kuadran:nk]', cols=f'{F}.[ctd:wilayah:qk]')

k = t.index("<worksheet name='H2-Narasi'>")
t = t[:k] + K1_XML + K2_XML + K3_XML + KR_XML + t[k:]
k = t.index("<window class='worksheet' name='H2-Narasi'>")
t = t[:k] + ''.join(plain_window(n) for n in (K1, K2, K3, KR)) + t[k:]

# aksi klik provinsi: kartu & keputusan tidak mengubah parameter
t = t.replace("<exclude-sheet name='H2-Narasi' />",
              "<exclude-sheet name='H2-Narasi' />" + ''.join(f"<exclude-sheet name='{n}' />" for n in (K1, K2, K3, KR)), 1)
# label kuadran: Papua Tengah (peringkat 1) ikut dilabeli
rep(f"{Q}ACEH{Q}, {Q}MALUKU{Q}) OR [wilayah] = {P_PROV} THEN [Calculation_0379056855416840]",
    f"{Q}ACEH{Q}, {Q}MALUKU{Q}, {Q}PAPUA TENGAH{Q}) OR [wilayah] = {P_PROV} THEN [Calculation_0379056855416840]", None)
# petunjuk narasi
rep(f"{Q}Klik provinsi di peta, kuadran, atau garis peringkat.{Q}", f"{Q}Klik provinsi di peta, kuadran, atau daftar prioritas.{Q}", None)

# ================================================================ 5. teks judul (kalimat biasa, font Tableau)
S_TPT, S_INF = 'H1-S TPT Satu Dekade', 'H1-S Informal Satu Dekade'
M_PETA, M_HIST = 'H2-K Peta KabKota', 'H2-K Sebaran Tahun'
set_title(S_TPT, run('Pengangguran turun', 14, INK, F_SEMI, True), NL, run('TPT 2015 dan 2025, % angkatan kerja', 10, INK2))
set_title(S_INF, run('Kerja informal naik', 14, INK, F_SEMI, True), NL, run('Informal 2015 dan 2025, % pekerja nonpertanian', 10, INK2))
set_title('H1-B Tren TPT', run('Pengangguran SMK tertinggi sejak 2015', 14, INK, F_SEMI, True), NL,
          run('TPT per jenjang, 2015–2025 (%). ', 10, INK2), run('SMK', 10, COBALT_D, F_SEMI), run(' dan ', 10, INK2),
          run('SMA', 10, '#6f93c8', F_SEMI), run(' disorot; SMK naik 3,2 poin saat COVID.', 10, INK2))
set_title('H2-E Peta Berbalik', run('Peringkat 38 provinsi', 14, INK, F_SEMI, True), NL,
          run('1 = paling rentan. Biru: menurut TPT. Merah bata: menurut kerja tidak layak.', 10, INK2))
set_title('H2-F Kuadran', run('Empat tipe masalah kerja', 14, INK, F_SEMI, True), NL,
          run('Skor 0–100. Garis putus = median 38 provinsi; klasifikasi relatif.', 10, INK2))
set_title('H2-G Penimbang', run('Provinsi yang didahulukan', 14, INK, F_SEMI, True), NL,
          run('8 teratas · ● bobot pilihan · pita = 1.000 skenario · ★ stabil di 10 besar', 9, INK2))
for name, lab in (('H1-KPI TPT', 'TPT nasional, 2025'), ('H1-KPI SMK', 'TPT lulusan SMK, 2025'),
                  ('H1-KPI Informal PT', 'Informal lulusan perguruan tinggi, 2015 → 2025'), ('H1-KPI NEET', 'NEET usia 15–24, 2025')):
    set_title(name, run(lab, 10, INK2, F_SEMI))
    w = worksheet_block(name).group(0)
    w = w.replace("fontsize='26'", "fontsize='30'").replace("fontsize='19'", "fontsize='26'")
    w = w.replace('*0.00&quot;%&quot;', '*0.0&quot;%&quot;')
    set_ws(name, w)

# ================================================================ 6. tata letak
X = lambda px: int(round(px / 1900 * 100000))
Y = lambda px: int(round(px / 1100 * 100000))
zid = [200]


def nid():
    zid[0] += 1
    return zid[0]


def zstyle(bg=None, margin=0, pad=0):
    s = ("<zone-style><format attr='border-color' value='#000000' /><format attr='border-style' value='none' />"
         "<format attr='border-width' value='0' />" + f"<format attr='margin' value='{margin}' />")
    if pad:
        s += f"<format attr='padding' value='{pad}' />"
    if bg:
        s += f"<format attr='background-color' value='{bg}' />"
    return s + '</zone-style>'


def zone(x, y, w, h, inner='', **attrs):
    a = {'h': str(Y(h)), 'id': str(nid()), 'w': str(X(w)), 'x': str(X(x)), 'y': str(Y(y))}
    a.update({k.replace('_', '-'): v for k, v in attrs.items()})
    s = ' '.join(f"{k}='{a[k]}'" for k in sorted(a))
    return f"<zone {s}>{inner}</zone>"


def zsheet(name, x, y, w, h, bg=CARD, title=True, pad=8):
    kw = {} if title else {'show_title': 'false'}
    return zone(x, y, w, h, zstyle(bg, 0, pad), name=name, **kw)


def ztext(x, y, w, h, runs, bg=None, pad=10):
    return zone(x, y, w, h, ft(*runs) + zstyle(bg, 0, pad), forceUpdate='true', type_v2='text')


def zblank(x, y, w, h, bg):
    return zone(x, y, w, h, zstyle(bg), type_v2='empty')


def zparam(param, mode, x, y, w, h, bg=CARD):
    return zone(x, y, w, h, zstyle(bg, 0, 4), mode=mode, param=param, type_v2='paramctrl')


def zbutton(target_uuid, caption, x, y, w, h, bg, fg='#ffffff'):
    inner = (f"<button action='tabdoc:goto-sheet window-id=&quot;{target_uuid}&quot;' button-type='text'>"
             f"<button-visual-state><caption>{esc(caption)}</caption>"
             f"<button-caption-font-style fontcolor='{fg}' fontname='{F_SEMI}' fontsize='12' />"
             f"<format attr='background-color' value='{bg}' /></button-visual-state></button>")
    return zone(x, y, w, h, inner, type_v2='dashboard-object')


def window_uuid(name):
    m = re.search(r"<window class='dashboard'[^>]*name='" + re.escape(name) + r"'>.*?<simple-id uuid='([^']+)' />\s*</window>", t, re.S)
    return m.group(1)


H1, H2 = 'Hal 1 - Dua Wajah', 'Hal 2 - Provinsi ke KabKota'
U1, U2 = window_uuid(H1), window_uuid(H2)
WM = "<zone h='100000' id='{}' is-scaled='1' param='Image/New_Watermark.png' type-v2='bitmap' w='100000' x='0' y='0' />"


def band(kicker, headline, deck):
    return ztext(44, 44, 1530, 118, [run(kicker, 9, AMBER, F_SEMI), NL, run(headline, 24, '#ffffff', F_BOLD, True), NL,
                                     run(deck, 11, '#cdd5e3', F_BODY)], bg=INK, pad=6)


TINT_B, TINT_R, TINT_N = '#edf2f9', '#fcefe9', '#f1efea'


def kartu_angka(x, angka, warna, ket1, ket2=None):
    runs = [run(angka, 34, warna, F_BOLD, True), NL, run(ket1, 11, INK, F_SEMI)]
    if ket2:
        runs += [NL, run(ket2, 10, INK2)]
    tint = TINT_B if warna == COBALT else TINT_R
    return [ztext(x, 698, 258, 294, runs, bg=tint, pad=18), zblank(x, 698, 5, 294, warna)]


FOOT1 = ('Sumber: BPS, Sakernas Agustus 2015–2025 (diolah). TPT = pengangguran terbuka ÷ angkatan kerja. Informal nonpertanian = pekerja '
         'nonpertanian berstatus berusaha sendiri, dibantu buruh tidak tetap, pekerja bebas, atau pekerja keluarga ÷ seluruh pekerja nonpertanian. '
         '≤SD = tamat SD ke bawah. NEET = penduduk 15–24 tahun yang tidak sekolah, tidak bekerja, dan tidak ikut pelatihan.')
KX = [44, 498, 953, 1408]
z1 = [zblank(0, 0, 1900, 1100, PAPER), WM.format(5),
      band('Bab 1 dari 2  ·  Pendidikan dan pasar kerja Indonesia, 2015–2025',
           'Pengangguran turun, kerja informal naik',
           'Berlaku di enam jenjang pendidikan, 2015–2025.'),
      zbutton(U2, 'Bab 2: provinsi  →', 1588, 106, 262, 42, VERM)]
for x, ws, col in zip(KX, ['H1-KPI TPT', 'H1-KPI SMK', 'H1-KPI Informal PT', 'H1-KPI NEET'], [COBALT, COBALT, VERM, INK2]):
    z1.append(zsheet(ws, x, 172, 442, 104, pad=12))
    z1.append(zblank(x, 172, 5, 104, col))
for x, ws in zip(KX, ['H1-P Spark TPT', 'H1-P Spark SMK', None, 'H1-P Spark NEET']):
    if ws:
        z1.append(zsheet(ws, x + 12, 212, 150, 56, title=False, pad=0))
z1 += [ztext(44, 288, 900, 80, [run('Lulusan ≤SD jarang menganggur, paling banyak informal', 14, INK, F_SEMI, True), NL,
                                 run('2025. Kiri: ', 10, INK2), run('TPT, % angkatan kerja', 10, COBALT, F_SEMI),
                                 run('. Kanan: ', 10, INK2), run('informal, % pekerja nonpertanian', 10, VERM, F_SEMI),
                                 run('.', 10, INK2)], bg=CARD, pad=12),
       zsheet('H1-C Cermin TPT', 44, 368, 360, 320, title=False, pad=10),
       zsheet('H1-C Cermin Informal', 404, 368, 540, 320, title=False, pad=10),
       zsheet(S_TPT, 954, 288, 442, 400, pad=12),
       zsheet(S_INF, 1406, 288, 444, 400, pad=12),
       zsheet('H1-B Tren TPT', 44, 698, 1000, 294, pad=12),
       ztext(44, 1000, 1806, 52, [run(FOOT1, 8, MUTED)], pad=4)]
z1 += kartu_angka(1054, '68,4%', VERM, 'pekerja nonpertanian ≤SD berstatus informal', 'padahal pengangguran ≤SD hanya 2,3%')
z1 += kartu_angka(1323, '6 dari 6', VERM, 'jenjang pendidikan: informal naik sejak 2015', 'lulusan PT 8,2% → 16,6%')
z1 += kartu_angka(1592, '8,6%', COBALT, 'pengangguran lulusan SMK, 2025', 'tertinggi di antara jenjang, 11 tahun berturut-turut')

FOOT2 = ('Sumber: BPS (Sakernas Agustus 2025; TPT kab/kota 2017–2025; Susenas Maret). Skor "tidak bekerja" = TPT + NEET; skor "kerja tidak layak" = '
         'informal + setengah pengangguran (min–maks, 0–100). TPT dan kerja tidak layak hanya berkorelasi lemah antarprovinsi (ρ = −0,30; p = 0,066). '
         'Kerja tidak layak lebih terkait urbanisasi (ρ parsial −0,67) daripada lama sekolah (−0,14; tidak signifikan). '
         'Papua pemekaran memakai data provinsi induk sebelum 2024 (estimasi). Batas kab/kota: geoBoundaries ADM2, hanya geometri.')
z2 = [zblank(0, 0, 1900, 1100, PAPER), WM.format(3),
      band('Bab 2 dari 2  ·  38 provinsi dan 514 kabupaten/kota, 2025',
           'Pengangguran rendah belum tentu kerja layak',
           'NTB peringkat 34 menurut TPT, tetapi peringkat 2 menurut kerja tidak layak.'),
      zbutton(U1, '←  Bab 1', 1588, 106, 262, 42, INK),
      zsheet('H2-E Peta Berbalik', 44, 172, 836, 364, pad=12),
      zsheet('H2-Narasi', 44, 536, 600, 56, bg=CARD, title=False, pad=8),
      zparam(P_MODE, 'compact', 644, 536, 236, 56),
      zsheet(K1, 890, 172, 470, 140, pad=12),
      zparam(P_PROV, 'compact', 1150, 176, 204, 40),
      zsheet(K2, 890, 312, 470, 162, pad=12),
      zsheet(K3, 890, 474, 470, 118, title=False, pad=12),
      zblank(890, 172, 5, 420, INK),
      zsheet('H2-F Kuadran', 1370, 172, 480, 420, pad=10),
      zsheet('H2-G Penimbang', 44, 602, 680, 306, pad=10),
      zparam(P_FOKUS, 'compact', 44, 908, 680, 30),
      zparam(P_W[0], 'slider', 44, 938, 340, 30),
      zparam(P_W[1], 'slider', 384, 938, 340, 30),
      zparam(P_W[2], 'slider', 44, 966, 340, 30),
      zparam(P_W[3], 'slider', 384, 966, 340, 30),
      zsheet('H2-G Pesan Bobot', 64, 730, 640, 40, bg=None, title=False, pad=0),
      zsheet(M_PETA, 734, 602, 668, 258, pad=6),
      zsheet(M_HIST, 734, 860, 480, 132, pad=6),
      zparam(P_ACUAN, 'compact', 1214, 860, 188, 132),
      ztext(1412, 602, 438, 50, [run('Langkah per tipe masalah', 14, INK, F_SEMI, True), NL,
                                 run('Jumlah provinsi per tipe; tipe provinsi terpilih disorot.', 9, INK2)], bg=CARD, pad=10),
      zsheet(KR, 1412, 652, 438, 236, title=False, pad=8),
      ztext(1412, 888, 438, 104, [run('135', 24, COBALT_D, F_BOLD, True), run('  kab/kota selalu di atas median sejenis', 10, INK, F_SEMI), NL,
                                 run('Tiap tahun 2017–2025: perlu program jangka panjang.', 9, INK2)], bg=TINT_B, pad=12),
      zblank(1412, 888, 5, 104, COBALT_D),
      ztext(44, 1000, 1806, 52, [run(FOOT2, 8, MUTED)], pad=4)]


def rebuild(dname, zones):
    global t
    m = re.search(r"(<dashboard enable-sort-zone-taborder='true' name='" + re.escape(dname) + r"'>)(.*?)(<simple-id uuid='[^']+' />\s*</dashboard>)", t, re.S)
    body = m.group(2)
    size = re.search(r"<size [^>]*/>", body).group(0)
    t = t[:m.start()] + m.group(1) + '<style />' + size + '<zones>' + ''.join(zones) + '</zones>' + m.group(3) + t[m.end():]


rebuild(H1, z1)
rebuild(H2, z2)


def set_viewpoints(dname, sheets):
    global t
    m = re.search(r"(<window class='dashboard'[^>]*name='" + re.escape(dname) + r"'>)\s*<viewpoints>.*?</viewpoints>", t, re.S)
    vp = '<viewpoints>' + ''.join(f"<viewpoint name='{s}'><zoom type='entire-view' /></viewpoint>" for s in sheets) + '</viewpoints>'
    t = t[:m.start()] + m.group(1) + vp + t[m.end():]


set_viewpoints(H1, ['H1-C Cermin TPT', 'H1-C Cermin Informal', 'H1-P Spark TPT', 'H1-P Spark SMK', 'H1-P Spark NEET', 'H1-B Tren TPT',
                    S_TPT, S_INF, 'H1-KPI Informal PT', 'H1-KPI NEET', 'H1-KPI SMK', 'H1-KPI TPT'])
set_viewpoints(H2, ['H2-E Peta Berbalik', 'H2-F Kuadran', 'H2-G Penimbang', 'H2-G Pesan Bobot', M_PETA, M_HIST, 'H2-Narasi',
                    K1, K2, K3, KR])

# ---- tambahan v8b
# palet Measure Names kartu penyebab di level datasource
k = t.index("<encoding attr='color' field='[none:kuadran:nk]' type='palette'>")
t = t[:k] + ("<encoding attr='color' field='[:Measure Names]' type='palette'>" + ''.join(
    f"<map to='{col}'><bucket>&quot;{F}.[usr:{c}:qk]&quot;</bucket></map>" for c, col in zip(C_D, [COBALT, COBALT, VERM, VERM]))
    + '</encoding>') + t[k:]
# format default nilai Jenjang Tren: 1 desimal di semua label
DST1 = 'federated.0t1aunm074zhqx179uzcf086kdei'
a = t.index(f"<datasource caption='Jenjang Tren' inline='true' name='{DST1}'")
b = t.index('</datasource>', a)
blk = t[a:b]
old = "<column caption='Nilai' datatype='real' name='[nilai]' role='measure' type='quantitative' />"
assert blk.count(old) == 1
blk = blk.replace(old, "<column caption='Nilai' datatype='real' default-format='n#,##0.0' name='[nilai]' role='measure' type='quantitative' />")
t = t[:a] + blk + t[b:]
t = t.replace("value='#,##0.0'", "value='*0.0'").replace("value='#,##0.0&quot;%&quot;'", "value='*0.0&quot;%&quot;'")
rep(f"{Q}+3,19 saat COVID{Q}", f"{Q}+3,2 poin saat COVID{Q}", None)
# judul peta kab/kota tanpa nomor
rep(f"<run bold='true' fontcolor='{VERM}' fontname='{F_BOLD}' fontsize='14'>④  </run>", '', None)
rep(f"{Q}④ Contoh NTB", f"{Q}Contoh NTB", None)
# caption kontrol ringkas
for old, new in (('Bobot TPT', 'TPT'), ('Bobot NEET', 'NEET'), ('Bobot setengah pengangguran', 'Setengah'),
                 ('Bobot informal', 'Informal'), ('Fokus kebijakan', 'Fokus')):
    rep(f"caption='{old}' datatype=", f"caption='{new}' datatype=", None)

# locale Indonesia (koma desimal) + animasi 0,5 detik: sama dengan yang disimpan Tableau lewat menu
t = t.replace('<workbook ', "<workbook locale='id_ID' ", 1) if "<workbook locale=" not in t else t
if "<style-rule element='animation'>" not in t:
    t = t.replace('  <datasources>', "  <style><style-rule element='animation'><format attr='animation-duration' value='0.5' /></style-rule></style>\n  <datasources>", 1)

import re as _re
t = _re.sub(r"(name='\[Calculation_0379056855900179\]'[^>]*>\s*<calculation class='tableau' formula=')[^']*(')",
            lambda m: m.group(1) + f'{Q}Klik provinsi di peta, kuadran, atau daftar prioritas, atau pilih lewat menu kartu.{Q}' + m.group(2), t)
rep("caption='Pilih Provinsi' datatype=", "caption='Provinsi' datatype=", None)
for one, a, b, col in (("<run fontalignment='0'>Rentan Tersembunyi</run>", 'Rentan', 'Tersembunyi', VERM),
                       ('<run>Relatif Layak</run>', 'Relatif', 'Layak', SAGE),
                       ('<run>Rentan Ganda</run>', 'Rentan', 'Ganda', OXBLOOD),
                       ('<run>Antrean Kerja Formal</run>', 'Antrean', 'Kerja Formal', COBALT)):
    rep(one, run(a, 9, col, F_SEMI) + NL + run(b, 9, col, F_SEMI), None)
# KPI angka: format bawaan field (ikut locale) + tanda % sebagai teks
for cid in ('Calculation_0379056860336187', 'Calculation_0379056859422764', 'Calculation_0379056859787314'):
    t = _re.sub(r"(<column caption='[^']*' datatype='real' )(name='\[" + cid + r"\]')", r"\1default-format='n#,##0.0' \2", t)
    t = _re.sub(r"<format attr='text-format' field='\[[^\]]+\]\.\[usr:" + cid + r":qk\]' value='[^']*' />", '', t)
for ws in ('H1-KPI TPT', 'H1-KPI SMK', 'H1-KPI NEET'):
    w = worksheet_block(ws).group(0)
    i = w.index('</customized-label>')
    j = w.rfind('</run>', 0, i) + len('</run>')
    m = _re.search(r"<run fontcolor='([^']*)' fontname='([^']*)' fontsize='([^']*)'>&gt;</run>", w)
    w = w[:j] + f"<run fontcolor='{m.group(1)}' fontname='{m.group(2)}' fontsize='{m.group(3)}'>%</run>" + w[j:]
    set_ws(ws, w)
KPI_TXT = {'H1-KPI TPT': 'Calculation_0379056860336187', 'H1-KPI SMK': 'Calculation_0379056859422764',
           'H1-KPI NEET': 'Calculation_0379056859787314'}
for n, (ws, cid) in enumerate(KPI_TXT.items()):
    # angka bulat + digit desimal terpisah, disambung koma di label (format kustom Tableau abaikan locale)
    c_int, c_dec = f'Calculation_94000000000001{n}1', f'Calculation_94000000000001{n}2'
    cdef = (calc(c_int, f'Bulat {ws[7:]}', f'INT(ROUND([{cid}], 1))', 'integer')
            + calc(c_dec, f'Desimal {ws[7:]}', f'INT(ROUND([{cid}] * 10, 0)) % 10', 'integer'))
    w = worksheet_block(ws).group(0)
    dsm = _re.search(r"<datasource-dependencies datasource='([^']+)'>", w)
    dsn = dsm.group(1)
    w = w.replace(dsm.group(0), dsm.group(0) + cdef + ci(c_int, 'User', f'usr:{c_int}:qk', 'quantitative')
                  + ci(c_dec, 'User', f'usr:{c_dec}:qk', 'quantitative'), 1)
    col = {'H1-KPI TPT': COBALT, 'H1-KPI SMK': COBALT, 'H1-KPI NEET': INK2}[ws]
    w = w.replace(f"<text column='[{dsn}].[usr:{cid}:qk]' />",
                  f"<text column='[{dsn}].[usr:{c_int}:qk]' /><text column='[{dsn}].[usr:{c_dec}:qk]' />")
    lbl = ('<customized-label>' + ft(frun(f'[{dsn}].[usr:{c_int}:qk]', 30, col, F_BOLD), run(',', 30, col, F_BOLD),
                                     frun(f'[{dsn}].[usr:{c_dec}:qk]', 30, col, F_BOLD), run('%', 30, col, F_BOLD))
           + '</customized-label>')
    w = _re.sub(r'<customized-label>.*?</customized-label>', lambda _: lbl, w, count=1, flags=_re.S)
    w = w.replace("<format attr='mark-labels-cull' value='true' />", "<format attr='mark-labels-cull' value='false' />")
    set_ws(ws, w)
    a = t.index(f"name='{dsn}'")
    k = t.index('<column ', t.index('</connection>', a))
    t = t[:k] + cdef + t[k:]
w = worksheet_block('H2-F Kuadran').group(0)
w = w.replace("text-width-delta='-18'", "text-width-delta='20'")
set_ws('H2-F Kuadran', w)
# ---- perapian akhir: tile tidak bertumpuk, Priority Lab 8 baris, tren 2015–2025, kuadran tanpa label median
w = worksheet_block('H2-E Peta Berbalik').group(0)
assert "<format attr='size' value='4.6' />" in w and "<format attr='size' value='4.2' />" in w
w = w.replace("<format attr='size' value='4.6' />", "<format attr='size' value='4.3' />").replace("<format attr='size' value='4.2' />", "<format attr='size' value='3.9' />")
pass  # rentang x tetap -1..16 (tile tepi tidak terpotong)
w = w.replace("<format attr='font-size' value='7' />", "<format attr='font-size' value='6' />")
set_ws('H2-E Peta Berbalik', w)
w = worksheet_block('H2-G Penimbang').group(0)
w = w.replace("<max>10</max>", "<max>8</max>", 1)
assert '<max>8</max>' in w
set_ws('H2-G Penimbang', w)
DST1 = 'federated.0t1aunm074zhqx179uzcf086kdei'
# (sumbu tren dibiarkan otomatis: rentang tetap memunculkan ikon pin)
rep(f" ELSEIF [jenjang] = {Q}SMK{Q} AND [tahun] = 2020 THEN {Q}+3,2 poin saat COVID{Q}", '', None)
w = worksheet_block('H2-F Kuadran').group(0)
w = w.replace("id='refline0' label-type='automatic'", "id='refline0' label-type='none'").replace("id='refline1' label-type='automatic'", "id='refline1' label-type='none'")
set_ws('H2-F Kuadran', w)
t = t.replace("<workbook locale='id_ID' ", '<workbook ', 1)
t = t.replace(" original-version='18.1'", " locale='id_ID' original-version='18.1'", 1)
open(OUT, 'w', encoding='utf-8').write(t)
ET.parse(OUT)
print('OK', len(t))
