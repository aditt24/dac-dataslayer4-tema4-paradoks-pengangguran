# -*- coding: utf-8 -*-
"""Redesain v7 dashboard Tableau DAC Tema 4 (edit XML .twb, diverifikasi di Tableau).

Pemakaian: python redesign_tableau_v7.py <input.twb> <output.twb>
Tidak mengubah data, definisi indikator, maupun hasil analisis; hanya
gaya, teks, tata letak, dan dua tampilan baru dari kolom t3 yang sudah ada.
"""
import re
import sys
import uuid
import xml.etree.ElementTree as ET

SRC, OUT = sys.argv[1], sys.argv[2]
t = open(SRC, encoding='utf-8').read()
DS = 'federated.0dzsn910err68y1dlgf4w1omb1y9'      # Provinsi & KabKota
DST1 = 'federated.0t1aunm074zhqx179uzcf086kdei'    # Jenjang Tren
P_PROV = '[Parameters].[Parameter 0379056854634496]'
P_MODE = '[Parameters].[Parameter 0379056854757377]'

# ---------------------------------------------------------------- tokens
PAPER = '#f3eee4'     # latar halaman
CARD = '#ffffff'      # kartu grafik
INK = '#14213d'       # teks utama, band judul
INK2 = '#4a5468'      # teks sekunder
MUTED = '#7c8494'     # catatan
AMBER = '#f2a93b'     # kicker / sorotan
COBALT = '#2f5fa7'    # pengangguran (TPT)
COBALT_D = '#1d3f7a'
COBALT_M = '#6f93c8'
VERM = '#e0603a'      # kerja tidak layak / informal
OXBLOOD = '#a12a1c'   # rentan ganda
SAGE = '#3f9363'      # relatif layak
GREY = '#d6cfc2'      # pembanding netral
F_HEAD = 'Georgia'
F_BODY = 'Tableau Book'
F_SEMI = 'Tableau Semibold'


def rep(old, new, n=1, s=None):
    """Ganti tepat n kemunculan (n=None: semua, minimal 1)."""
    global t
    src = t if s is None else s
    c = src.count(old)
    if n is None:
        assert c >= 1, ('tidak ditemukan', old[:120])
    else:
        assert c == n, (c, n, old[:160])
    out = src.replace(old, new)
    if s is None:
        t = out
    return out


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace("'", '&apos;').replace('"', '&quot;'))


def run(text, size=11, color=INK, font=F_BODY, bold=False, align=None):
    a = f" fontcolor='{color}' fontname='{font}' fontsize='{size}'"
    if bold:
        a = " bold='true'" + a
    if align is not None:
        a += f" fontalignment='{align}'"
    return f"<run{a}>{esc(text)}</run>"


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
    m = worksheet_block(name)
    w = m.group(0)
    title = '<layout-options><title>' + ft(*runs) + '</title></layout-options>'
    if '<layout-options>' in w:
        w = re.sub(r'<layout-options>.*?</layout-options>', lambda _: title, w, count=1, flags=re.S)
    else:
        w = w.replace('<table>', title + '<table>', 1)
    set_ws(name, w)


def add_table_style(name, rules):
    """Tambahkan style-rule ke <style> level tabel (sebelum <panes>)."""
    m = worksheet_block(name)
    w = m.group(0)
    i = w.index('<panes>')
    head = w[:i]
    if head.rstrip().endswith('<style />'):
        j = head.rstrip().rfind('<style />')
        head = head[:j] + '<style>' + rules + '</style>' + head[j + len('<style />'):]
    else:
        j = head.rfind('</style>')
        assert j > 0, name
        head = head[:j] + rules + head[j:]
    set_ws(name, head + w[i:])


CLEAN = ("<style-rule element='gridline'><format attr='line-visibility' value='off' /></style-rule>"
         "<style-rule element='zeroline'><format attr='line-visibility' value='off' /></style-rule>"
         f"<style-rule element='axis'><format attr='color' value='{INK2}' /></style-rule>"
         "<style-rule element='table-div'><format attr='line-visibility' scope='rows' value='off' />"
         "<format attr='line-visibility' scope='cols' value='off' /></style-rule>")

# ---------------------------------------------------------------- 1. parameter default
rep("value='&quot;PAPUA TENGAH&quot;'>", "value='&quot;Indonesia&quot;'>", None)
rep("formula='&quot;PAPUA TENGAH&quot;' />", "formula='&quot;Indonesia&quot;' />", None)


# ---------------------------------------------------------------- 1b. label kontrol yang manusiawi
for old, new in (('W TPT', 'Bobot TPT'), ('W NEET', 'Bobot NEET'), ('W Setengah', 'Bobot setengah pengangguran'),
                 ('W Informal', 'Bobot informal'), ('Mode Peta', 'Lihat peringkat menurut'),
                 ('Pembanding Jejak', 'Acuan pembanding')):
    rep(f"caption='{old}' datatype=", f"caption='{new}' datatype=", None)
rep("&quot; kab/kota persisten ganda se-Indonesia (2017–2025). Gulir tabel untuk melihat semua.&quot;",
    "&quot; kab/kota bertahan di atas dua acuan&quot;", None)
rep("&quot; kab/kota persisten ganda di &quot; + [Parameters].[Parameter 0379056854634496] + &quot;.&quot;",
    "&quot; kab/kota di &quot; + [Parameters].[Parameter 0379056854634496] + &quot; di atas dua acuan, 2017–2025&quot;", None)

rep("&quot;Klik provinsi di peta untuk melihat posisinya.&quot;", "&quot;Klik provinsi di peta, kuadran, atau garis peringkat.&quot;", None)

# ---------------------------------------------------------------- 2. palet semantik
def recolor_encoding(field_frag, mapping):
    global t
    pat = re.compile(r"<encoding attr='color' field='" + re.escape(field_frag) + r"' type='palette'>.*?</encoding>", re.S)
    ms = list(pat.finditer(t))
    assert ms, field_frag
    for m in reversed(ms):
        blk = m.group(0)
        for old, new in mapping.items():
            blk = blk.replace(f"<map to='{old}'>", f"<map to='{new}'>")
        t = t[:m.start()] + blk + t[m.end():]


def set_bucket_colors(field_frag, colors):
    """colors: {bucket_label: hex}; ganti warna per bucket di palet yang ada."""
    global t
    pat = re.compile(r"(<encoding attr='color' field='" + re.escape(field_frag) + r"' type='palette'>)(.*?)(</encoding>)", re.S)
    ms = list(pat.finditer(t))
    assert ms, field_frag
    for m in reversed(ms):
        body = ''.join(f"<map to='{c}'><bucket>&quot;{esc(b)}&quot;</bucket></map>" for b, c in colors.items())
        t = t[:m.start()] + m.group(1) + body + m.group(3) + t[m.end():]


QUAD = {'Antrean Kerja Formal': COBALT, 'Relatif Layak': SAGE,
        'Rentan Ganda': OXBLOOD, 'Rentan Tersembunyi': VERM}
set_bucket_colors('[none:kuadran:nk]', QUAD)
set_bucket_colors('[attr:kuadran:nk]', QUAD)
set_bucket_colors('[none:indikator_label:nk]', {'Pengangguran terbuka (TPT)': COBALT,
                                               'Informal non-pertanian': VERM})
set_bucket_colors('[none:Calculation_0379056859357227:nk]', {'SMK': COBALT_D, 'SMA': COBALT_M,
                                                             'Jenjang lain': GREY})
set_bucket_colors('[none:Calculation_0379056860176440:nk]', {'Di atas acuan': COBALT_D,
                                                             'Di bawah acuan': '#d4deec',
                                                             'Tidak ada data': '#efe9de'})
recolor_encoding('[none:Calculation_0379056883658815:nk]', {'#111111': INK})

# palet baru di datasource Provinsi (sebelum palet kuadran) dan Jenjang Tren
MAPCLS = {}
for lab, cols in (('TPT', ['#1d3f7a', '#2f5fa7', '#6f93c8', '#b4c6e0', '#e3e9f1']),
                  ('KTL', ['#8e1b10', '#c7401f', '#e47b57', '#f1b8a0', '#f7e2d8'])):
    for b, c in zip(['01-05', '06-10', '11-19', '20-29', '30-38'], cols):
        MAPCLS[f'{lab} {b}'] = c
new_pal = "<encoding attr='color' field='[none:Calculation_9100000000000001:nk]' type='palette'>" + ''.join(
    f"<map to='{c}'><bucket>&quot;{b}&quot;</bucket></map>" for b, c in MAPCLS.items()) + '</encoding>'
LERENG = dict(QUAD)
LERENG['Lainnya'] = '#ddd6ca'
new_pal += "<encoding attr='color' field='[none:Calculation_9100000000000002:nk]' type='palette'>" + ''.join(
    f"<map to='{c}'><bucket>&quot;{esc(b)}&quot;</bucket></map>" for b, c in LERENG.items()) + '</encoding>'
k = t.index("<encoding attr='color' field='[none:kuadran:nk]' type='palette'>")
t = t[:k] + new_pal + t[k:]
k = t.index("<encoding attr='color' field='[none:indikator_label:nk]' type='palette'>")
t = t[:k] + ("<encoding attr='color' field='[none:Calculation_1046185747062785:nk]' type='palette'>"
             f"<map to='#cfc6b6'><bucket>&quot;2015&quot;</bucket></map>"
             f"<map to='{VERM}'><bucket>&quot;2025&quot;</bucket></map></encoding>") + t[k:]

# ---------------------------------------------------------------- 3. kalkulasi baru
KEY = ['NUSA TENGGARA BARAT', 'SULAWESI BARAT', 'NUSA TENGGARA TIMUR', 'DKI JAKARTA',
       'KEP. RIAU', 'BANTEN', 'ACEH', 'MALUKU']
key_in = ', '.join(f'&quot;{k}&quot;' for k in KEY)
CALC_WARNA = ("<column caption='Warna Peta' datatype='string' name='[Calculation_9100000000000001]' role='dimension' type='nominal'>"
              "<calculation class='tableau' formula='IF " + P_MODE + " = &quot;Pengangguran (TPT)&quot; THEN &quot;TPT &quot; ELSE &quot;KTL &quot; END + "
              "(IF [Calculation_0379056855457801] &lt;= 5 THEN &quot;01-05&quot; ELSEIF [Calculation_0379056855457801] &lt;= 10 THEN &quot;06-10&quot; "
              "ELSEIF [Calculation_0379056855457801] &lt;= 19 THEN &quot;11-19&quot; ELSEIF [Calculation_0379056855457801] &lt;= 29 THEN &quot;20-29&quot; ELSE &quot;30-38&quot; END)' /></column>")
CALC_LERENG = ("<column caption='Warna Lereng' datatype='string' name='[Calculation_9100000000000002]' role='dimension' type='nominal'>"
               "<calculation class='tableau' formula='IF [wilayah] IN (" + key_in + ") OR [wilayah] = " + P_PROV + " THEN [kuadran] ELSE &quot;Lainnya&quot; END' /></column>")
CALC_LABEL = ("<column caption='Label Lereng' datatype='string' name='[Calculation_9100000000000003]' role='dimension' type='nominal'>"
              "<calculation class='tableau' formula='IF [wilayah] IN (" + key_in + ") OR [wilayah] = " + P_PROV + " THEN [Calculation_0379056855416840] END' /></column>")
SINGKATAN_DEF = re.search(r"<column caption='Singkatan'[^>]*>\s*<calculation[^>]*/>\s*</column>", t).group(0)
RANKPETA_DEF = re.search(r"<column caption='Rank Peta'[^>]*>\s*<calculation[^>]*/>\s*</column>", t).group(0)
k = t.index("<column caption='Singkatan'")
MN_ALIAS = ("<column datatype='string' name='[:Measure Names]' role='dimension' type='nominal'><aliases>"
            f"<alias key='&quot;[{DS}].[sum:rank_tpt:qk]&quot;' value='TPT' />"
            f"<alias key='&quot;[{DS}].[sum:rank_ktl:qk]&quot;' value='Kerja tidak layak' />"
            '</aliases></column>')
assert "name='[:Measure Names]'" not in t[:k]
t = t[:k] + MN_ALIAS + CALC_WARNA + CALC_LERENG + CALC_LABEL + t[k:]


# column-instance level datasource: syarat agar palet dipakai Tableau
CI = lambda c: f"<column-instance column='[{c}]' derivation='None' name='[none:{c}:nk]' pivot='key' type='nominal' />"
k = t.index("<column-instance column='[Calculation_0379056883658815]'")
t = t[:k] + CI('Calculation_9100000000000001') + CI('Calculation_9100000000000002') + t[k:]
k = t.index("<column-instance column='[Calculation_0379056859357227]'")
t = t[:k] + CI('Calculation_1046185747062785') + t[k:]

# ---------------------------------------------------------------- 4. peta: warna ganda TPT biru / KTL merah bata
m = worksheet_block('H2-E Peta Berbalik')
w = m.group(0)
w = w.replace(f"<datasource-dependencies datasource='{DS}'>",
              f"<datasource-dependencies datasource='{DS}'>" + CALC_WARNA +
              "<column-instance column='[Calculation_9100000000000001]' derivation='None' name='[none:Calculation_9100000000000001:nk]' pivot='key' type='nominal' />", 1)
c0 = w.count(f"<color column='[{DS}].[sum:Calculation_0379056855457801:qk]' />")
assert c0 == 1, c0
w = w.replace(f"<color column='[{DS}].[sum:Calculation_0379056855457801:qk]' />",
              f"<color column='[{DS}].[none:Calculation_9100000000000001:nk]' />")
# label tile: putih di kelas gelap tetap (rank<=19)
i = w.index("<style-rule element='mark'>")
w = w[:i] + "<style-rule element='mark'>" + new_pal.split('</encoding>')[0].replace("field='[none:Calculation_9100000000000001", f"field='[{DS}].[none:Calculation_9100000000000001") + '</encoding></style-rule>' + w[i:]
set_ws('H2-E Peta Berbalik', w)
set_title('H2-E Peta Berbalik',
          run('①  ', 15, VERM, F_HEAD, True), run('Satu provinsi, dua peringkat', 15, INK, F_HEAD, True), NL,
          run('Angka = peringkat dari 38 (1 = paling rentan). Biru = menurut TPT, merah bata = menurut kerja tidak layak. Makin gelap, makin rentan.', 9, INK2))

# ---------------------------------------------------------------- 5. slope chart peringkat (baru)
SLOPE_NAME = 'H2-S Lereng Peringkat'
LERENG_WS = f"<encoding attr='color' field='[{DS}].[none:Calculation_9100000000000002:nk]' type='palette'>" + ''.join(
    f"<map to='{c}'><bucket>&quot;{esc(b)}&quot;</bucket></map>" for b, c in LERENG.items()) + '</encoding>'
slope = f"""<worksheet name='{SLOPE_NAME}'>
      <layout-options><title>{ft(run('Peringkat berbalik', 13, INK, F_HEAD, True), NL, run('TPT (kiri) → kerja tidak layak (kanan). Atas = paling rentan.', 9, INK2))}</title></layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='Provinsi &amp; KabKota' name='{DS}' />
            <datasource name='Parameters' />
          </datasources>
          <datasource-dependencies datasource='Parameters'>
            <column caption='Pilih Provinsi' datatype='string' name='[Parameter 0379056854634496]' param-domain-type='list' role='measure' type='nominal' value='&quot;Indonesia&quot;'>
              <calculation class='tableau' formula='&quot;Indonesia&quot;' />
            </column>
          </datasource-dependencies>
          <datasource-dependencies datasource='{DS}'>
            {SINGKATAN_DEF}
            {CALC_LERENG}
            {CALC_LABEL}
            <column datatype='string' name='[kuadran]' role='dimension' type='nominal' />
            <column caption='Peringkat TPT' datatype='real' name='[rank_tpt]' role='measure' type='quantitative' />
            <column caption='Peringkat KTL' datatype='real' name='[rank_ktl]' role='measure' type='quantitative' />
            <column datatype='string' name='[wilayah]' role='dimension' type='nominal' />
            <column-instance column='[Calculation_9100000000000002]' derivation='None' name='[none:Calculation_9100000000000002:nk]' pivot='key' type='nominal' />
            <column-instance column='[Calculation_9100000000000003]' derivation='None' name='[none:Calculation_9100000000000003:nk]' pivot='key' type='nominal' />
            <column-instance column='[wilayah]' derivation='None' name='[none:wilayah:nk]' pivot='key' type='nominal' />
            <column-instance column='[kuadran]' derivation='None' name='[none:kuadran:nk]' pivot='key' type='nominal' />
            <column-instance column='[rank_tpt]' derivation='Sum' name='[sum:rank_tpt:qk]' pivot='key' type='quantitative' />
            <column-instance column='[rank_ktl]' derivation='Sum' name='[sum:rank_ktl:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <filter class='categorical' column='[{DS}].[:Measure Names]'>
            <groupfilter function='union' user:op='manual'>
              <groupfilter function='member' level='[:Measure Names]' member='&quot;[{DS}].[sum:rank_tpt:qk]&quot;' />
              <groupfilter function='member' level='[:Measure Names]' member='&quot;[{DS}].[sum:rank_ktl:qk]&quot;' />
            </groupfilter>
          </filter>
          <manual-sort column='[{DS}].[:Measure Names]' direction='ASC'>
            <dictionary>
              <bucket>&quot;[{DS}].[sum:rank_tpt:qk]&quot;</bucket>
              <bucket>&quot;[{DS}].[sum:rank_ktl:qk]&quot;</bucket>
            </dictionary>
          </manual-sort>
          <slices>
            <column>[{DS}].[:Measure Names]</column>
          </slices>
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='axis'>
            <encoding attr='space' class='0' field='[{DS}].[Multiple Values]' field-type='quantitative' max='39' min='0' range-type='fixed' reverse='true' scope='rows' type='space' />
            <format attr='display' class='0' field='[{DS}].[Multiple Values]' scope='rows' value='false' />
          </style-rule>
          <style-rule element='cell'>
            <format attr='text-format' field='[{DS}].[Multiple Values]' value='#,##0' />
          </style-rule>
          <style-rule element='mark'>{LERENG_WS}</style-rule>
          {CLEAN}
          <style-rule element='tooltip'><format attr='background-color' value='#ffffff' /></style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Line' />
            <encodings>
              <color column='[{DS}].[none:Calculation_9100000000000002:nk]' />
              <lod column='[{DS}].[none:wilayah:nk]' />
              <text column='[{DS}].[none:Calculation_9100000000000003:nk]' />
              <lod column='[{DS}].[none:kuadran:nk]' />
            </encodings>
            <customized-tooltip>
              <formatted-text>
                <run bold='true'><![CDATA[<[{DS}].[none:wilayah:nk]>]]></run>
                <run>Æ&#10;</run>
                <run><![CDATA[Peringkat TPT <SUM(Peringkat TPT)> → kerja tidak layak <SUM(Peringkat KTL)> (dari 38; 1 = paling rentan)]]></run>
                <run>Æ&#10;</run>
                <run><![CDATA[Tipe: <[{DS}].[none:kuadran:nk]>. Sumber: BPS, Sakernas Agustus 2025.]]></run>
              </formatted-text>
            </customized-tooltip>
            <style>
              <style-rule element='mark'>
                <format attr='mark-labels-show' value='true' />
                <format attr='mark-labels-cull' value='true' />
                <format attr='size' value='1.2' />
              </style-rule>
            </style>
          </pane>
        </panes>
        <rows>[{DS}].[Multiple Values]</rows>
        <cols>[{DS}].[:Measure Names]</cols>
      </table>
      <simple-id uuid='{{{str(uuid.uuid4()).upper()}}}' />
    </worksheet>"""
k = t.index("<worksheet name='H2-Narasi'>")
t = t[:k] + slope + t[k:]
slope_win = f"""<window class='worksheet' name='{SLOPE_NAME}'>
      <cards>
        <edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /><card type='measures' /></strip></edge>
        <edge name='top'><strip size='2147483647'><card type='columns' /></strip><strip size='2147483647'><card type='rows' /></strip><strip size='29'><card type='title' /></strip></edge>
      </cards>
      <simple-id uuid='{{{str(uuid.uuid4()).upper()}}}' />
    </window>"""
k = t.index("<window class='worksheet' name='H2-Narasi'>")
t = t[:k] + slope_win + t[k:]

# ---------------------------------------------------------------- 6. judul & gaya worksheet lain
set_title('H1-A Dumbbell',
          run('Paling jarang menganggur, paling sering informal', 15, INK, F_HEAD, True), NL,
          run('●', 11, COBALT, F_BODY, True), run(' TPT (% angkatan kerja)    ', 9, INK2),
          run('●', 11, VERM, F_BODY, True), run(' Informal (% pekerja nonpertanian)    · 2025 · penyebut berbeda', 9, INK2))
set_title('H1-B Tren TPT',
          run('TPT lulusan SMK tertinggi sebelas tahun berturut-turut', 15, INK, F_HEAD, True), NL,
          run('TPT menurut jenjang, 2015–2025 (%). ', 9, INK2), run('SMK', 9, COBALT_D, F_SEMI),
          run(' dan ', 9, INK2), run('SMA', 9, COBALT_M, F_SEMI), run(' disorot. Saat COVID (2019→2020) TPT SMK naik paling tajam: +3,19 poin.', 9, INK2))
set_title('H1-D COVID Bar',
          run('COVID: TPT SMK naik paling tajam', 13, INK, F_HEAD, True), NL,
          run('Perubahan TPT 2019→2020, poin persen. SMK +3,19.', 9, INK2))
set_title('H1-F Informal 2015 vs 2025',
          run('Sepuluh tahun: informal naik di keenam jenjang', 13, INK, F_HEAD, True), NL,
          run('% informal di antara pekerja nonpertanian.  ', 9, INK2),
          run('■', 10, '#bdb3a1', F_BODY, True), run(' 2015   ', 9, INK2),
          run('■', 10, VERM, F_BODY, True), run(' 2025', 9, INK2))
for name, lab, col in (('H1-KPI TPT', 'TPT nasional, 2025', COBALT), ('H1-KPI SMK', 'TPT lulusan SMK, 2025', COBALT),
                       ('H1-KPI Informal PT', 'Informal lulusan PT', VERM),
                       ('H1-KPI NEET', 'NEET usia 15–24, 2025', INK2)):
    set_title(name, run(lab.upper(), 8, INK2, F_SEMI))
    w = worksheet_block(name).group(0)
    w = re.sub(r"<run bold='true' fontsize='20'>", f"<run fontcolor='{col}' fontname='{F_HEAD}' fontsize='26'>", w)
    set_ws(name, w)
set_title('H2-F Kuadran',
          run('②  ', 15, VERM, F_HEAD, True), run('Empat tipe kerentanan', 15, INK, F_HEAD, True), NL,
          run('Skor 0–100 (min–maks). Garis = median 38 provinsi: klasifikasi relatif, bukan kategori resmi.', 9, INK2))
set_title('H2-G Penimbang',
          run('③  ', 14, VERM, F_HEAD, True), run('Priority Lab: siapa yang tetap di atas?', 14, INK, F_HEAD, True), NL,
          run('● bobotmu · pita = rentang 90% dari 1.000 skenario bobot · ★ 10 besar di ≥90% skenario', 8, INK2))
set_title('H2-I KPI KabKota',
          run('④  ', 14, VERM, F_HEAD, True),
          f"<run bold='true' fontcolor='{INK}' fontname='{F_HEAD}' fontsize='11'><![CDATA[<[{DS}].[usr:Calculation_0379056860061750:nk]>]]></run>", NL,
          run('■', 10, COBALT_D, F_BODY, True), run(' di atas acuan   ', 8, INK2), run('■', 10, '#d4deec', F_BODY, True),
          run(' di bawah acuan   ', 8, INK2), run('■', 10, '#efe9de', F_BODY, True), run(' tidak ada data', 8, INK2))
# KPI kab/kota: buang awalan '⑤ Jejak kab/kota • ' dari calc (nomor kini dari judul)
rep("formula='&quot;⑤ Jejak kab/kota • &quot; + (IF", "formula='(IF", None)
# narasi provinsi: font
w = worksheet_block('H2-Narasi').group(0)
w = w.replace("<run fontalignment='0' fontsize='12'>", f"<run fontalignment='0' fontcolor='{INK}' fontname='{F_SEMI}' fontsize='11'>")
set_ws('H2-Narasi', w)

for name in ('H1-A Dumbbell', 'H1-B Tren TPT', 'H1-D COVID Bar', 'H1-F Informal 2015 vs 2025',
             'H2-F Kuadran', 'H2-G Penimbang', 'H2-E Peta Berbalik'):
    add_table_style(name, CLEAN)
# warna bar COVID
w = worksheet_block('H1-D COVID Bar').group(0)
if "<mark class='Automatic' />" in w and 'mark-color' not in w:
    i = w.index('</pane>')
    pane = w[:i]
    if '<style>' in pane[pane.rfind('<pane'):]:
        pane = pane.replace("<style-rule element='mark'>", f"<style-rule element='mark'><format attr='mark-color' value='{COBALT_M}' />", 1)
    else:
        pane = pane + f"<style><style-rule element='mark'><format attr='mark-color' value='{COBALT_M}' /></style-rule></style>"
    w = pane + w[i:]
    set_ws('H1-D COVID Bar', w)


# ---------------------------------------------------------------- 6b. perbaikan QA putaran 4
NOFL = "<style-rule element='worksheet'><format attr='display-field-labels' scope='rows' value='false' /><format attr='display-field-labels' scope='cols' value='false' /></style-rule>"
for name in ('H1-A Dumbbell', 'H1-D COVID Bar', 'H1-F Informal 2015 vs 2025', 'H2-G Penimbang'):
    add_table_style(name, NOFL)
# caption peringkat (header slope chart + tooltip)
rep("<column datatype='real' name='[rank_tpt]'", "<column caption='Peringkat TPT' datatype='real' name='[rank_tpt]'", None)
rep("<column datatype='real' name='[rank_ktl]'", "<column caption='Peringkat KTL' datatype='real' name='[rank_ktl]'", None)
# KPI informal PT: font angka
w = worksheet_block('H1-KPI Informal PT').group(0)
w = w.replace("<run bold='true' fontsize='14'>", f"<run fontcolor='{VERM}' fontname='{F_HEAD}' fontsize='19'>")
set_ws('H1-KPI Informal PT', w)
# informal 2015 vs 2025 -> dot plot satu baris per jenjang
w = worksheet_block('H1-F Informal 2015 vs 2025').group(0)
w = w.replace(f"<rows>([{DST1}].[none:jenjang:nk] / [{DST1}].[none:Calculation_1046185747062785:nk])</rows>", f"<rows>[{DST1}].[none:jenjang:nk]</rows>")
w = w.replace("<mark class='Automatic' />", "<mark class='Circle' />", 1)
w = w.replace("</encodings>\n          </pane>", "</encodings><style><style-rule element='mark'><format attr='size' value='2.2' /></style-rule></style>\n          </pane>", 1)
assert "format attr='size' value='2.2'" in w
set_ws('H1-F Informal 2015 vs 2025', w)
# Priority Lab: 10 provinsi, judul sumbu
w = worksheet_block('H2-G Penimbang').group(0)
w = w.replace("<min>1</min>\n            <max>15</max>", "<min>1</min>\n            <max>10</max>")
assert '<max>10</max>' in w
set_ws('H2-G Penimbang', w)
add_table_style('H2-G Penimbang', f"<style-rule element='axis'><format attr='title' class='0' field='[{DS}].[usr:Calculation_0379056856055829:qk:1]' scope='cols' value='Peringkat dengan bobotmu (1 = paling rentan)' /></style-rule>")
# Kuadran: judul sumbu ringkas
rep("value='Dimensi &quot;tidak bekerja&quot; (skor 0–100)&#9;'", "value='Tidak bekerja: TPT + NEET (0–100)'", None)
rep("value='Dimensi &quot;kerja tidak layak&quot; (skor 0–100)&#9;'", "value='Kerja tidak layak (0–100)'", None)
# peta tile: rentang sumbu rapat + tile lebih besar
w = worksheet_block('H2-E Peta Berbalik').group(0)
w = w.replace("max='7' min='-2' range-type='fixed' reverse='true' scope='rows'", "max='7.0' min='-1.0' range-type='fixed' reverse='true' scope='rows'")
w = w.replace("fold='true' max='7' min='-2' range-type='fixed'", "fold='true' max='7.0' min='-1.0' range-type='fixed'")
w = w.replace("max='17' min='-6' range-type='fixed' scope='cols'", "max='16.0' min='-1.0' range-type='fixed' scope='cols'")
w = w.replace("<format attr='size' value='3.922652006149292' />", "<format attr='size' value='4.6' />")
w = w.replace("<format attr='size' value='3.5248618125915527' />", "<format attr='size' value='4.2' />")
assert "max='16.0'" in w and "value='4.6'" in w
set_ws('H2-E Peta Berbalik', w)


# ---------------------------------------------------------------- 6c. v7b: slope ganda Bab 1 + peta kab/kota Bab 2
import os as _os
TAHUN_BANDING_DEF = re.search(r"<column caption='Tahun Banding'[^>]*>\s*<calculation[^>]*/>\s*</column>", t).group(0)
JENJANG_TAMPIL_DEF = re.search(r"<column caption='Jenjang Tampil'[^>]*>\s*<calculation[^>]*/>\s*</column>", t).group(0)


def slope_sheet(name, indikator, head, sub, color):
    fid = f'[{DST1}]'
    return f"""<worksheet name='{name}'>
      <layout-options><title>{ft(run(head, 14, INK, F_HEAD, True), NL, run(sub, 9, INK2))}</title></layout-options>
      <table>
        <view>
          <datasources><datasource caption='Jenjang Tren' name='{DST1}' /></datasources>
          <datasource-dependencies datasource='{DST1}'>
            {JENJANG_TAMPIL_DEF}
            {TAHUN_BANDING_DEF}
            <column caption='Indikator' datatype='string' name='[indikator]' role='dimension' type='nominal' />
            <column caption='Jenjang' datatype='string' name='[jenjang]' role='dimension' type='nominal' />
            <column caption='Nilai' datatype='real' name='[nilai]' role='measure' type='quantitative' />
            <column caption='Tahun' datatype='integer' name='[tahun]' role='measure' type='quantitative' />
            <column-instance column='[Calculation_0379056859291690]' derivation='None' name='[none:Calculation_0379056859291690:nk]' pivot='key' type='nominal' />
            <column-instance column='[Calculation_1046185747062785]' derivation='None' name='[none:Calculation_1046185747062785:nk]' pivot='key' type='nominal' />
            <column-instance column='[indikator]' derivation='None' name='[none:indikator:nk]' pivot='key' type='nominal' />
            <column-instance column='[nilai]' derivation='Sum' name='[sum:nilai:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <filter class='categorical' column='{fid}.[none:indikator:nk]'>
            <groupfilter function='member' level='[none:indikator:nk]' member='&quot;{indikator}&quot;' user:ui-domain='database' user:ui-enumeration='inclusive' user:ui-marker='enumerate' />
          </filter>
          <filter class='categorical' column='{fid}.[none:Calculation_1046185747062785:nk]'>
            <groupfilter function='union' user:ui-domain='database' user:ui-enumeration='inclusive' user:ui-marker='enumerate'>
              <groupfilter function='member' level='[none:Calculation_1046185747062785:nk]' member='&quot;2015&quot;' />
              <groupfilter function='member' level='[none:Calculation_1046185747062785:nk]' member='&quot;2025&quot;' />
            </groupfilter>
          </filter>
          <slices>
            <column>{fid}.[none:indikator:nk]</column>
            <column>{fid}.[none:Calculation_1046185747062785:nk]</column>
          </slices>
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='axis'>
            <format attr='display' class='0' field='{fid}.[sum:nilai:qk]' scope='rows' value='false' />
          </style-rule>
          <style-rule element='cell'>
            <format attr='text-format' field='{fid}.[sum:nilai:qk]' value='#,##0.0' />
          </style-rule>
          <style-rule element='label'>
            <format attr='text-format' field='{fid}.[sum:nilai:qk]' value='#,##0.0' />
          </style-rule>
          <style-rule element='mark'><format attr='mark-color' value='{color}' /></style-rule>
          {CLEAN}
          <style-rule element='worksheet'><format attr='display-field-labels' scope='cols' value='false' /></style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Line' />
            <encodings>
              <lod column='{fid}.[none:Calculation_0379056859291690:nk]' />
              <text column='{fid}.[none:Calculation_0379056859291690:nk]' />
              <text column='{fid}.[sum:nilai:qk]' />
            </encodings>
            <customized-tooltip>
              <formatted-text>
                <run bold='true'><![CDATA[<{fid}.[none:Calculation_0379056859291690:nk]> <{fid}.[none:Calculation_1046185747062785:nk]>: <{fid}.[sum:nilai:qk]>%]]></run>
                <run>Æ&#10;</run>
                <run>Sumber: BPS, Sakernas Agustus 2015 dan 2025.</run>
              </formatted-text>
            </customized-tooltip>
            <customized-label>
              <formatted-text>
                <run fontcolor='{INK2}' fontsize='8'>&lt;{fid}.[none:Calculation_0379056859291690:nk]&gt; </run>
                <run bold='true' fontcolor='{color}' fontsize='9'>&lt;{fid}.[sum:nilai:qk]&gt;</run>
              </formatted-text>
            </customized-label>
            <style>
              <style-rule element='mark'>
                <format attr='mark-labels-show' value='true' />
                <format attr='mark-labels-cull' value='true' />
                <format attr='mark-labels-mode' value='line-ends' />
                <format attr='size' value='1.6' />
                <format attr='mark-color' value='{color}' />
              </style-rule>
            </style>
          </pane>
        </panes>
        <rows>{fid}.[sum:nilai:qk]</rows>
        <cols>{fid}.[none:Calculation_1046185747062785:nk]</cols>
      </table>
      <simple-id uuid='{{{str(uuid.uuid4()).upper()}}}' />
    </worksheet>"""


def plain_window(name):
    return (f"<window class='worksheet' name='{name}'><cards><edge name='left'><strip size='160'><card type='pages' />"
            "<card type='filters' /><card type='marks' /></strip></edge><edge name='top'><strip size='2147483647'>"
            "<card type='columns' /></strip><strip size='2147483647'><card type='rows' /></strip><strip size='29'>"
            f"<card type='title' /></strip></edge></cards><simple-id uuid='{{{str(uuid.uuid4()).upper()}}}' /></window>")


S_TPT, S_INF = 'H1-S TPT Satu Dekade', 'H1-S Informal Satu Dekade'
k = t.index("<worksheet name='H2-Narasi'>")
t = t[:k] + slope_sheet(S_TPT, 'tpt', 'TPT turun di keenam jenjang ↘', '2015 → 2025 · % angkatan kerja', COBALT) \
    + slope_sheet(S_INF, 'informal_nonag', 'Informal naik di keenam jenjang ↗', '2015 → 2025 · % pekerja nonpertanian', VERM) + t[k:]
k = t.index("<window class='worksheet' name='H2-Narasi'>")
t = t[:k] + plain_window(S_TPT) + plain_window(S_INF) + t[k:]

# ---- sumber data spasial kab/kota (geometri geoBoundaries + angka BPS t5)
GEO = 'federated.1yt21t90rlniyk11nec891sgkv9c'
tpl = open(_os.environ['TPL_TWB'], encoding='utf-8').read()
geo_ds = re.search(r"<datasource caption='IDN_kabkota_persistensi_v7'.*?</datasource>", tpl, re.S).group(0)
P_ACUAN = '[Parameters].[Parameter 0379056854831106]'
G1 = ("<column caption='Tahun di atas acuan' datatype='integer' name='[Calculation_9200000000000001]' role='measure' type='quantitative'>"
      f"<calculation class='tableau' formula='IF {P_ACUAN} = &quot;Nasional&quot; THEN [thn_atas_nas] ELSE [thn_atas_sej] END' /></column>")
G2 = ("<column caption='Kelas Jejak' datatype='string' name='[Calculation_9200000000000002]' role='dimension' type='nominal'>"
      "<calculation class='tableau' formula='IF [Calculation_9200000000000001] = 9 THEN &quot;9 dari 9 tahun&quot; "
      "ELSEIF [Calculation_9200000000000001] &gt;= 7 THEN &quot;7-8 tahun&quot; ELSEIF [Calculation_9200000000000001] &gt;= 4 THEN &quot;4-6 tahun&quot; "
      "ELSEIF [Calculation_9200000000000001] &gt;= 1 THEN &quot;1-3 tahun&quot; ELSE &quot;Tidak pernah&quot; END' /></column>")
G3 = ("<column caption='Sesuai Provinsi' datatype='boolean' name='[Calculation_9200000000000003]' role='dimension' type='nominal'>"
      f"<calculation class='tableau' formula='{P_PROV} = &quot;Indonesia&quot; OR [prov_kab] = {P_PROV}' /></column>")
G4 = ("<column caption='Judul Jejak' datatype='string' name='[Calculation_9200000000000004]' role='dimension' type='nominal'>"
      "<calculation class='tableau' formula='STR({ FIXED : SUM(IF [Calculation_9200000000000003] AND [Calculation_9200000000000001] = 9 THEN 1 ELSE 0 END) }) "
      f"+ &quot; kab/kota di atas &quot; + (IF {P_ACUAN} = &quot;Nasional&quot; THEN &quot;TPT nasional&quot; ELSE &quot;median kab/kota sejenis&quot; END) "
      f"+ &quot; pada 9 dari 9 tahun&quot; + (IF {P_PROV} = &quot;Indonesia&quot; THEN &quot;&quot; ELSE &quot; · &quot; + {P_PROV} END)' /></column>")
JEJAK = {'9 dari 9 tahun': '#1d3f7a', '7-8 tahun': '#2f5fa7', '4-6 tahun': '#6f93c8', '1-3 tahun': '#b9cae2', 'Tidak pernah': '#e9e3d7'}
geo_pal = ("<style><style-rule element='mark'><encoding attr='color' field='[none:Calculation_9200000000000002:nk]' type='palette'>"
           + ''.join(f"<map to='{c}'><bucket>&quot;{b}&quot;</bucket></map>" for b, c in JEJAK.items()) + '</encoding></style-rule></style>')
cols_add = (G1 + G2 + G3 + G4 + "<column caption='Nama kab/kota' datatype='string' name='[nama_kab]' role='dimension' type='nominal' />"
            + "<column-instance column='[Calculation_9200000000000002]' derivation='None' name='[none:Calculation_9200000000000002:nk]' pivot='key' type='nominal' />")
i = geo_ds.index('<layout ')
geo_ds = geo_ds[:i] + cols_add + geo_ds[i:]
j = geo_ds.index('/>', geo_ds.index('<layout ')) + 2
geo_ds = geo_ds[:j] + geo_pal + geo_ds[j:]
k = t.index('\n  </datasources>')
t = t[:k] + '\n    ' + geo_ds + t[k:]

GD = f'[{GEO}]'
GEO_DEPS = (f"<datasource-dependencies datasource='Parameters'>"
            "<column caption='Pilih Provinsi' datatype='string' name='[Parameter 0379056854634496]' param-domain-type='list' role='measure' type='nominal' value='&quot;Indonesia&quot;'><calculation class='tableau' formula='&quot;Indonesia&quot;' /></column>"
            "<column caption='Acuan pembanding' datatype='string' name='[Parameter 0379056854831106]' param-domain-type='list' role='measure' type='nominal' value='&quot;Sesama kota/kabupaten&quot;'><calculation class='tableau' formula='&quot;Sesama kota/kabupaten&quot;' /></column>"
            "</datasource-dependencies>"
            f"<datasource-dependencies datasource='{GEO}'>{G1}{G2}{G3}{G4}"
            "<column datatype='spatial' name='[Geometry]' role='measure' type='nominal' />"
            "<column caption='Kode' datatype='string' name='[kode]' role='dimension' type='nominal' />"
            "<column caption='Nama kab/kota' datatype='string' name='[nama_kab]' role='dimension' type='nominal' />"
            "<column caption='Provinsi' datatype='string' name='[prov_kab]' role='dimension' type='nominal' />"
            "<column caption='Thn Atas Nas' datatype='integer' name='[thn_atas_nas]' role='measure' type='quantitative' />"
            "<column caption='Thn Atas Sej' datatype='integer' name='[thn_atas_sej]' role='measure' type='quantitative' />"
            "<column caption='Rata TPT 2017-2025' datatype='real' name='[rata_tpt_kab]' role='measure' type='quantitative' />"
            "<column-instance column='[Geometry]' derivation='Collect' name='[clct:Geometry:nk]' pivot='key' type='nominal' />"
            "<column-instance column='[kode]' derivation='None' name='[none:kode:nk]' pivot='key' type='nominal' />"
            "<column-instance column='[nama_kab]' derivation='None' name='[none:nama_kab:nk]' pivot='key' type='nominal' />"
            "<column-instance column='[prov_kab]' derivation='None' name='[none:prov_kab:nk]' pivot='key' type='nominal' />"
            "<column-instance column='[nama_kab]' derivation='Attribute' name='[attr:nama_kab:nk]' pivot='key' type='nominal' />"
            "<column-instance column='[prov_kab]' derivation='Attribute' name='[attr:prov_kab:nk]' pivot='key' type='nominal' />"
            "<column-instance column='[kode]' derivation='Count' name='[cnt:kode:qk]' pivot='key' type='quantitative' />"
            "<column-instance column='[rata_tpt_kab]' derivation='Sum' name='[sum:rata_tpt_kab:qk]' pivot='key' type='quantitative' />"
            "<column-instance column='[Calculation_9200000000000001]' derivation='Sum' name='[sum:Calculation_9200000000000001:qk]' pivot='key' type='quantitative' />"
            "<column-instance column='[Calculation_9200000000000001]' derivation='None' name='[none:Calculation_9200000000000001:ok]' pivot='key' type='ordinal' />"
            "<column-instance column='[Calculation_9200000000000002]' derivation='None' name='[none:Calculation_9200000000000002:nk]' pivot='key' type='nominal' />"
            "<column-instance column='[Calculation_9200000000000003]' derivation='None' name='[none:Calculation_9200000000000003:nk]' pivot='key' type='nominal' />"
            "<column-instance column='[Calculation_9200000000000004]' derivation='None' name='[none:Calculation_9200000000000004:nk]' pivot='key' type='nominal' />"
            "</datasource-dependencies>"
            f"<filter class='categorical' column='{GD}.[none:Calculation_9200000000000003:nk]'>"
            "<groupfilter function='member' level='[none:Calculation_9200000000000003:nk]' member='true' user:ui-domain='database' user:ui-enumeration='inclusive' user:ui-marker='enumerate' /></filter>"
            f"<slices><column>{GD}.[none:Calculation_9200000000000003:nk]</column></slices>")
GEO_PAL_WS = (f"<style-rule element='mark'><encoding attr='color' field='{GD}.[none:Calculation_9200000000000002:nk]' type='palette'>"
              + ''.join(f"<map to='{c}'><bucket>&quot;{b}&quot;</bucket></map>" for b, c in JEJAK.items()) + '</encoding></style-rule>')
M_PETA, M_HIST = 'H2-K Peta KabKota', 'H2-K Sebaran Tahun'
peta = f"""<worksheet name='{M_PETA}'>
      <layout-options><title>{ft(run('④  ', 14, VERM, F_HEAD, True), f"<run bold='true' fontcolor='{INK}' fontname='{F_HEAD}' fontsize='12'><![CDATA[<{GD}.[none:Calculation_9200000000000004:nk]>]]></run>", NL, run('Warna = jumlah tahun TPT kab/kota di atas acuan, 2017–2025 · klik provinsi untuk memperbesar', 8, INK2))}</title></layout-options>
      <table>
        <view>
          <datasources><datasource caption='IDN_kabkota_persistensi_v7' name='{GEO}' /><datasource name='Parameters' /></datasources>
          <mapsources><mapsource name='Tableau' /></mapsources>
          {GEO_DEPS}
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='map'><format attr='washout' value='1' /></style-rule>
          {GEO_PAL_WS}
          <style-rule element='cell'><format attr='text-format' field='{GD}.[sum:rata_tpt_kab:qk]' value='#,##0.00' /></style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Automatic' />
            <encodings>
              <lod column='{GD}.[clct:Geometry:nk]' />
              <lod column='{GD}.[none:kode:nk]' />
              <color column='{GD}.[none:Calculation_9200000000000002:nk]' />
              <tooltip column='{GD}.[attr:nama_kab:nk]' />
              <tooltip column='{GD}.[attr:prov_kab:nk]' />
              <tooltip column='{GD}.[sum:Calculation_9200000000000001:qk]' />
              <tooltip column='{GD}.[sum:rata_tpt_kab:qk]' />
              <lod column='{GD}.[none:Calculation_9200000000000004:nk]' />
              <geometry column='{GD}.[clct:Geometry:nk]' />
            </encodings>
            <customized-tooltip>
              <formatted-text>
                <run bold='true'><![CDATA[<{GD}.[attr:nama_kab:nk]>, <{GD}.[attr:prov_kab:nk]>]]></run>
                <run>Æ&#10;</run>
                <run><![CDATA[TPT di atas acuan pada <SUM(Tahun di atas acuan)> dari 9 tahun (2017–2025); rata-rata TPT <SUM(Rata TPT 2017-2025)>%]]></run>
                <run>Æ&#10;</run>
                <run>Angka: BPS (TPT kab/kota). Batas wilayah: geoBoundaries, hanya geometri.</run>
              </formatted-text>
            </customized-tooltip>
            <style><style-rule element='mark'><format attr='mark-color' value='#e9e3d7' /></style-rule></style>
          </pane>
        </panes>
        <rows>{GD}.[Latitude (generated)]</rows>
        <cols>{GD}.[Longitude (generated)]</cols>
      </table>
      <simple-id uuid='{{{str(uuid.uuid4()).upper()}}}' />
    </worksheet>"""
hist = f"""<worksheet name='{M_HIST}'>
      <layout-options><title>{ft(run('Sebaran berbentuk U: kab/kota jarang berpindah kelas  ', 10, INK, F_SEMI), run('jumlah kab/kota per tahun di atas acuan (0–9) · batang = legenda peta', 8, INK2))}</title></layout-options>
      <table>
        <view>
          <datasources><datasource caption='IDN_kabkota_persistensi_v7' name='{GEO}' /><datasource name='Parameters' /></datasources>
          {GEO_DEPS}
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='axis'><format attr='display' class='0' field='{GD}.[cnt:kode:qk]' scope='rows' value='false' /></style-rule>
          {GEO_PAL_WS}
          {CLEAN}
          <style-rule element='worksheet'><format attr='display-field-labels' scope='cols' value='false' /></style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
            <encodings>
              <color column='{GD}.[none:Calculation_9200000000000002:nk]' />
              <text column='{GD}.[cnt:kode:qk]' />
            </encodings>
            <customized-tooltip><formatted-text><run><![CDATA[<{GD}.[cnt:kode:qk]> kab/kota: TPT di atas acuan pada <{GD}.[none:Calculation_9200000000000001:ok]> dari 9 tahun]]></run></formatted-text></customized-tooltip>
            <style><style-rule element='mark'><format attr='mark-labels-show' value='true' /><format attr='size' value='0.9' /></style-rule></style>
          </pane>
        </panes>
        <rows>{GD}.[cnt:kode:qk]</rows>
        <cols>{GD}.[none:Calculation_9200000000000001:ok]</cols>
      </table>
      <simple-id uuid='{{{str(uuid.uuid4()).upper()}}}' />
    </worksheet>"""
k = t.index("<worksheet name='H2-Narasi'>")
t = t[:k] + peta + hist + t[k:]
k = t.index("<window class='worksheet' name='H2-Narasi'>")
t = t[:k] + plain_window(M_PETA) + plain_window(M_HIST) + t[k:]
# aksi klik provinsi: kecualikan sheet yang tidak punya field wilayah
t = t.replace("<exclude-sheet name='H2-Narasi' />", f"<exclude-sheet name='H2-Narasi' /><exclude-sheet name='{M_PETA}' /><exclude-sheet name='{M_HIST}' />", 1)


# ---------------------------------------------------------------- 6d. v7c: Bab 1 lebih hidup (sparkline KPI, cermin terbalik, anotasi COVID)
DSN = 'federated.0zr6ror1g7j0xl15tunfk0v2ypxt'   # NEET Nasional


def calc(cid, cap, formula, dtype='real', role='measure', typ='quantitative'):
    return (f"<column caption='{cap}' datatype='{dtype}' name='[{cid}]' role='{role}' type='{typ}'>"
            f"<calculation class='tableau' formula='{formula}' /></column>")


Q = '&quot;'
C1 = calc('Calculation_9300000000000001', 'Spark TPT SMK', f'SUM(IF [indikator] = {Q}tpt{Q} AND [jenjang] = {Q}SMK{Q} THEN [nilai] END)')
C2 = calc('Calculation_9300000000000002', 'Spark Informal PT', f'SUM(IF [indikator] = {Q}informal_nonag{Q} AND [jenjang] = {Q}Universitas{Q} THEN [nilai] END)')
C3 = calc('Calculation_9300000000000003', 'Warna Cermin TPT', f'IF [jenjang] = {Q}SD{Q} OR [jenjang] = {Q}SMK{Q} THEN {Q}TPT sorot{Q} ELSE {Q}TPT lain{Q} END', 'string', 'dimension', 'nominal')
C4 = calc('Calculation_9300000000000004', 'Warna Cermin INF', f'IF [jenjang] = {Q}SD{Q} OR [jenjang] = {Q}SMK{Q} THEN {Q}INF sorot{Q} ELSE {Q}INF lain{Q} END', 'string', 'dimension', 'nominal')
C5 = calc('Calculation_9300000000000005', 'Label Tren', f'IF ([tahun] = 2015 OR [tahun] = 2025) AND ([jenjang] = {Q}SMK{Q} OR [jenjang] = {Q}SMA{Q} OR [jenjang] = {Q}SD{Q}) THEN (IF [jenjang] = {Q}SD{Q} THEN {Q}≤SD{Q} ELSE [jenjang] END) ELSEIF [jenjang] = {Q}SMK{Q} AND [tahun] = 2020 THEN {Q}+3,19 saat COVID{Q} END', 'string', 'dimension', 'nominal')
C6 = calc('Calculation_9300000000000006', 'Spark TPT Nasional', 'AVG([tpt_nasional])')
C7 = calc('Calculation_9300000000000007', 'Spark NEET', f'SUM(IF [wilayah_kategori] = {Q}INDONESIA{Q} AND [periode] = {Q}Tahun{Q} THEN [nilai] END)')
CI3 = "<column-instance column='[Calculation_9300000000000003]' derivation='None' name='[none:Calculation_9300000000000003:nk]' pivot='key' type='nominal' />"
CI4 = "<column-instance column='[Calculation_9300000000000004]' derivation='None' name='[none:Calculation_9300000000000004:nk]' pivot='key' type='nominal' />"
k = t.index("<column caption='Sorot Jenjang'")
t = t[:k] + C1 + C2 + C3 + C4 + C5 + t[k:]
k = t.index("<column-instance column='[Calculation_0379056859357227]'")
t = t[:k] + CI3 + CI4 + t[k:]
CERMIN_PAL = {'TPT sorot': COBALT, 'TPT lain': '#b4c6e0', 'INF sorot': VERM, 'INF lain': '#f3c2ad'}
k = t.index("<encoding attr='color' field='[none:indikator_label:nk]' type='palette'>")
t = t[:k] + "<encoding attr='color' field='[none:Calculation_9300000000000003:nk]' type='palette'>" + ''.join(
    f"<map to='{CERMIN_PAL[b]}'><bucket>&quot;{b}&quot;</bucket></map>" for b in ('TPT sorot', 'TPT lain')) + '</encoding>' \
    + "<encoding attr='color' field='[none:Calculation_9300000000000004:nk]' type='palette'>" + ''.join(
    f"<map to='{CERMIN_PAL[b]}'><bucket>&quot;{b}&quot;</bucket></map>" for b in ('INF sorot', 'INF lain')) + '</encoding>' + t[k:]
k = t.index("<column caption='Singkatan'")
t = t[:k] + C6 + t[k:]
k = t.index("<column caption='KPI NEET'")
t = t[:k] + C7 + t[k:]

T1RAW = ("<column caption='Indikator' datatype='string' name='[indikator]' role='dimension' type='nominal' />"
         "<column caption='Jenjang' datatype='string' name='[jenjang]' role='dimension' type='nominal' />"
         "<column caption='Nilai' datatype='real' name='[nilai]' role='measure' type='quantitative' />"
         "<column caption='Tahun' datatype='integer' name='[tahun]' role='measure' type='quantitative' />"
         "<column caption='Urut Jenjang' datatype='integer' name='[urut_jenjang]' role='measure' type='quantitative' />")


def spark(name, ds, cap, deps, cid, color):
    f = f'[{ds}]'
    return f"""<worksheet name='{name}'>
      <table>
        <view>
          <datasources><datasource caption='{cap}' name='{ds}' /></datasources>
          <datasource-dependencies datasource='{ds}'>{deps}
            <column-instance column='[tahun]' derivation='None' name='[none:tahun:qk]' pivot='key' type='quantitative' />
            <column-instance column='[{cid}]' derivation='User' name='[usr:{cid}:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='axis'>
            <format attr='display' class='0' field='{f}.[usr:{cid}:qk]' scope='rows' value='false' />
            <format attr='display' class='0' field='{f}.[none:tahun:qk]' scope='cols' value='false' />
            <encoding attr='space' class='0' field='{f}.[usr:{cid}:qk]' field-type='quantitative' fold='true' scope='rows' type='space' />
          </style-rule>
          <style-rule element='cell'><format attr='text-format' field='{f}.[usr:{cid}:qk]' value='#,##0.0' /></style-rule>
          {CLEAN}
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Line' />
            <encodings><text column='{f}.[usr:{cid}:qk]' /></encodings>
            <customized-tooltip><formatted-text><run><![CDATA[<{f}.[none:tahun:qk]>: <{f}.[usr:{cid}:qk]>%]]></run></formatted-text></customized-tooltip>
            <customized-label><formatted-text><run fontcolor='{INK2}' fontsize='7'>&lt;{f}.[usr:{cid}:qk]&gt;</run></formatted-text></customized-label>
            <style>
              <style-rule element='mark'>
                <format attr='mark-color' value='{color}' />
                <format attr='size' value='1.2' />
                <format attr='mark-labels-show' value='false' />
              </style-rule>
            </style>
          </pane>
        </panes>
        <rows>{f}.[usr:{cid}:qk]</rows>
        <cols>{f}.[none:tahun:qk]</cols>
      </table>
      <simple-id uuid='{{{str(uuid.uuid4()).upper()}}}' />
    </worksheet>"""


SP = [('H1-P Spark TPT', DS, 'Provinsi &amp; KabKota', C6 + "<column caption='Tahun' datatype='integer' name='[tahun]' role='measure' type='quantitative' /><column caption='Tpt Nasional' datatype='real' name='[tpt_nasional]' role='dimension' type='ordinal' />", 'Calculation_9300000000000006', COBALT),
      ('H1-P Spark SMK', DST1, 'Jenjang Tren', C1 + T1RAW, 'Calculation_9300000000000001', COBALT),
      ('H1-P Spark PT', DST1, 'Jenjang Tren', C2 + T1RAW, 'Calculation_9300000000000002', VERM),
      ('H1-P Spark NEET', DSN, 'NEET Nasional', C7 + "<column caption='Nilai' datatype='real' name='[nilai]' role='dimension' type='ordinal' /><column caption='Periode' datatype='string' name='[periode]' role='dimension' type='nominal' /><column caption='Tahun' datatype='integer' name='[tahun]' role='measure' type='quantitative' /><column caption='Wilayah Kategori' datatype='string' name='[wilayah_kategori]' role='dimension' type='nominal' />", 'Calculation_9300000000000007', INK2)]


def cermin(name, indikator, cdef, cid, left):
    f = f'[{DST1}]'
    rev = " reverse='true'" if left else ''
    hdr = (f"<style-rule element='header'><format attr='width' field='{f}.[none:Calculation_0379056859291690:nk]' value='{0 if left else 92}' /></style-rule>")
    return f"""<worksheet name='{name}'>
      <table>
        <view>
          <datasources><datasource caption='Jenjang Tren' name='{DST1}' /></datasources>
          <datasource-dependencies datasource='{DST1}'>
            {JENJANG_TAMPIL_DEF}{TAHUN_BANDING_DEF}{cdef}{T1RAW}
            <column-instance column='[Calculation_0379056859291690]' derivation='None' name='[none:Calculation_0379056859291690:nk]' pivot='key' type='nominal' />
            <column-instance column='[Calculation_1046185747062785]' derivation='None' name='[none:Calculation_1046185747062785:nk]' pivot='key' type='nominal' />
            <column-instance column='[{cid}]' derivation='None' name='[none:{cid}:nk]' pivot='key' type='nominal' />
            <column-instance column='[indikator]' derivation='None' name='[none:indikator:nk]' pivot='key' type='nominal' />
            <column-instance column='[nilai]' derivation='Sum' name='[sum:nilai:qk]' pivot='key' type='quantitative' />
            <column-instance column='[urut_jenjang]' derivation='Sum' name='[sum:urut_jenjang:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <filter class='categorical' column='{f}.[none:indikator:nk]'>
            <groupfilter function='member' level='[none:indikator:nk]' member='&quot;{indikator}&quot;' user:ui-domain='database' user:ui-enumeration='inclusive' user:ui-marker='enumerate' />
          </filter>
          <filter class='categorical' column='{f}.[none:Calculation_1046185747062785:nk]'>
            <groupfilter function='member' level='[none:Calculation_1046185747062785:nk]' member='&quot;2025&quot;' user:ui-domain='database' user:ui-enumeration='inclusive' user:ui-marker='enumerate' />
          </filter>
          <computed-sort column='{f}.[none:Calculation_0379056859291690:nk]' direction='ASC' using='{f}.[sum:urut_jenjang:qk]' />
          <slices>
            <column>{f}.[none:indikator:nk]</column>
            <column>{f}.[none:Calculation_1046185747062785:nk]</column>
          </slices>
          <aggregation value='true' />
        </view>
        <style>
          <style-rule element='axis'>
            <encoding attr='space' class='0' field='{f}.[sum:nilai:qk]' field-type='quantitative'{rev} scope='cols' type='space' />
            <format attr='display' class='0' field='{f}.[sum:nilai:qk]' scope='cols' value='false' />
          </style-rule>
          <style-rule element='cell'><format attr='text-format' field='{f}.[sum:nilai:qk]' value='#,##0.0&quot;%&quot;' /></style-rule>
          {hdr}
          {CLEAN}
          <style-rule element='worksheet'><format attr='display-field-labels' scope='rows' value='false' /></style-rule>
        </style>
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
            <encodings>
              <color column='{f}.[none:{cid}:nk]' />
              <text column='{f}.[sum:nilai:qk]' />
            </encodings>
            <customized-tooltip><formatted-text><run><![CDATA[<{f}.[none:Calculation_0379056859291690:nk]>, 2025: <{f}.[sum:nilai:qk]>]]></run><run>Æ&#10;</run><run>Sumber: BPS, Sakernas Agustus 2025.</run></formatted-text></customized-tooltip>
            <style>
              <style-rule element='mark'>
                <format attr='mark-labels-show' value='true' />
                <format attr='size' value='0.62' />
              </style-rule>
            </style>
          </pane>
        </panes>
        <rows>{f}.[none:Calculation_0379056859291690:nk]</rows>
        <cols>{f}.[sum:nilai:qk]</cols>
      </table>
      <simple-id uuid='{{{str(uuid.uuid4()).upper()}}}' />
    </worksheet>"""


CM_L, CM_R = 'H1-C Cermin TPT', 'H1-C Cermin Informal'
blocks = ''.join(spark(*a) for a in SP) + cermin(CM_L, 'tpt', C3, 'Calculation_9300000000000003', True) \
    + cermin(CM_R, 'informal_nonag', C4, 'Calculation_9300000000000004', False)
k = t.index("<worksheet name='H2-Narasi'>")
t = t[:k] + blocks + t[k:]
k = t.index("<window class='worksheet' name='H2-Narasi'>")
t = t[:k] + ''.join(plain_window(n) for n in [a[0] for a in SP] + [CM_L, CM_R]) + t[k:]

# tren: anotasi COVID di titik SMK 2020 + ujung garis
w = worksheet_block('H1-B Tren TPT').group(0)
w = w.replace(f"<datasource-dependencies datasource='{DST1}'>", f"<datasource-dependencies datasource='{DST1}'>" + C5 +
              "<column-instance column='[Calculation_9300000000000005]' derivation='Attribute' name='[attr:Calculation_9300000000000005:nk]' pivot='key' type='nominal' />", 1)
assert w.count(f"<text column='[{DST1}].[none:LabelJenjangSorotan:nk]' />") == 1
w = w.replace(f"<text column='[{DST1}].[none:LabelJenjangSorotan:nk]' />", f"<text column='[{DST1}].[attr:Calculation_9300000000000005:nk]' />")
w = w.replace("<format attr='mark-labels-mode' value='line-ends' />", "<format attr='mark-labels-mode' value='all' />")
w = w.replace("<format attr='mark-labels-cull' value='true' />", "<format attr='mark-labels-cull' value='false' />")
set_ws('H1-B Tren TPT', w)
set_title('H1-B Tren TPT',
          run('③  ', 14, VERM, F_HEAD, True), run('Kasus SMK: TPT tertinggi sebelas tahun, paling terpukul COVID', 14, INK, F_HEAD, True), NL,
          run('TPT menurut jenjang 2015–2025 (%). ', 9, INK2), run('SMK', 9, COBALT_D, F_SEMI), run(' dan ', 9, INK2),
          run('SMA', 9, COBALT_M, F_SEMI), run(' disorot. Tapi pekerja SMK justru lebih formal daripada SMA (informal 35,8% vs 43,8%).', 9, INK2))
set_title(S_TPT, run('②  ', 12, VERM, F_HEAD, True), run('TPT turun di keenam jenjang ↘', 12, INK, F_HEAD, True), NL,
          run('2015 → 2025 · % angkatan kerja', 9, INK2))
set_title(S_INF, run('Informal naik di keenam jenjang ↗', 12, INK, F_HEAD, True), NL,
          run('2015 → 2025 · % pekerja nonpertanian', 9, INK2))

# Bab 2 kuadran: label hanya provinsi kunci + terpilih
w = worksheet_block('H2-F Kuadran').group(0)
if CALC_LABEL not in w:
    w = w.replace(f"<datasource-dependencies datasource='{DS}'>", f"<datasource-dependencies datasource='{DS}'>" + CALC_LABEL +
                  "<column-instance column='[Calculation_9100000000000003]' derivation='None' name='[none:Calculation_9100000000000003:nk]' pivot='key' type='nominal' />", 1)
assert w.count(f"<text column='[{DS}].[none:Calculation_0379056855416840:nk]' />") == 1
w = w.replace(f"<text column='[{DS}].[none:Calculation_0379056855416840:nk]' />", f"<text column='[{DS}].[none:Calculation_9100000000000003:nk]' />")
set_ws('H2-F Kuadran', w)

# ---------------------------------------------------------------- 7. tata letak dashboard
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
    return ztext(44, 44, 1530, 118, [
        run(kicker, 9, AMBER, F_SEMI), NL,
        run(headline, 24, '#ffffff', F_HEAD, True), NL,
        run(deck, 12, '#cdd5e3', F_BODY)], bg=INK, pad=8)


FOOT1 = ('Sumber: BPS, Sakernas Agustus 2015–2025 (diolah). TPT = pengangguran terbuka ÷ angkatan kerja. Informal nonpertanian = pekerja '
         'nonpertanian berstatus berusaha sendiri, dibantu buruh tidak tetap, pekerja bebas, atau pekerja keluarga ÷ seluruh pekerja nonpertanian. '
         '≤SD = tamat SD ke bawah. NEET = penduduk 15–24 tahun yang tidak sekolah, tidak bekerja, dan tidak ikut pelatihan.')
z1 = [zblank(0, 0, 1900, 1100, PAPER), WM.format(5),
      band('BAB 1 / 2  ·  PENDIDIKAN DAN PASAR KERJA INDONESIA, 2015–2025',
           'Pengangguran turun. Kerja layak tidak ikut naik.',
           'Sejak 2015 TPT turun di keenam jenjang pendidikan, tetapi porsi pekerja informal justru naik di keenam jenjang.'),
      zbutton(U2, 'Bab 2: peta provinsi  →', 1588, 106, 262, 42, VERM),
      # KPI
      zsheet('H1-KPI TPT', 44, 172, 232, 104, pad=10),
      zsheet('H1-KPI SMK', 284, 172, 232, 104, pad=10),
      zsheet('H1-KPI Informal PT', 524, 172, 232, 104, pad=10),
      zsheet('H1-KPI NEET', 764, 172, 232, 104, pad=10),
      zsheet('H1-P Spark TPT', 52, 214, 84, 50, title=False, pad=0),
      zsheet('H1-P Spark SMK', 292, 214, 84, 50, title=False, pad=0),
      zsheet('H1-P Spark NEET', 772, 214, 84, 50, title=False, pad=0),
      ztext(1006, 172, 844, 104, [
          run('ALUR HALAMAN INI', 8, INK2, F_SEMI), NL,
          run('①', 11, VERM, F_HEAD, True), run(' Potret 2025   ', 10, INK, F_SEMI), run('→   ', 10, INK2),
          run('②', 11, VERM, F_HEAD, True), run(' Satu dekade   ', 10, INK, F_SEMI), run('→   ', 10, INK2),
          run('③', 11, VERM, F_HEAD, True), run(' Kasus SMK   ', 10, INK, F_SEMI), run('→   ', 10, INK2),
          run('Bab 2: di mana paradoksnya paling kuat?', 10, INK, F_SEMI), NL,
          run('●', 10, COBALT, F_BODY, True), run(' biru = TPT, % angkatan kerja    ', 9, INK2),
          run('●', 10, VERM, F_BODY, True), run(' merah bata = informal, % pekerja nonpertanian (penyebut berbeda)', 9, INK2)],
          bg='#e9e2d4', pad=10),
      # baris utama
      ztext(44, 288, 952, 86, [
          run('①  ', 15, VERM, F_HEAD, True), run('Cermin terbalik: paling jarang menganggur, paling sering informal', 14, INK, F_HEAD, True), NL,
          run('2025 · ', 9, INK2), run('◀ TPT, % angkatan kerja', 9, COBALT, F_SEMI), run('      jenjang      ', 9, INK2),
          run('informal, % pekerja nonpertanian ▶', 9, VERM, F_SEMI), run('   · dua skala terpisah karena penyebutnya berbeda', 9, INK2)], bg=CARD, pad=12),
      zsheet(CM_L, 44, 374, 380, 330, title=False, pad=10),
      zsheet(CM_R, 424, 374, 572, 330, title=False, pad=10),
      zsheet(S_TPT, 1006, 288, 417, 416, pad=12),
      zsheet(S_INF, 1433, 288, 417, 416, pad=12),
      # baris bawah
      zsheet('H1-B Tren TPT', 44, 716, 1222, 276, pad=12),
      ztext(1276, 716, 574, 276, [
          run('JADI', 9, AMBER, F_SEMI), NL,
          run('Bekerja belum tentu bekerja layak.', 16, '#ffffff', F_HEAD, True), NL,
          run('①', 11, AMBER, F_HEAD, True), run(' Lulusan ≤SD hampir tak menganggur (2,3%), tetapi 68,4% pekerjanya informal.', 10, '#ffffff'), NL,
          run('②', 11, AMBER, F_HEAD, True), run(' Dalam sepuluh tahun TPT turun di semua jenjang, informal naik di semua jenjang; lulusan PT 8,2% → 16,6%.', 10, '#ffffff'), NL,
          run('③', 11, AMBER, F_HEAD, True), run(' SMK paling banyak menganggur, tetapi pekerjanya lebih formal dari SMA.', 10, '#ffffff'), NL,
          run('TPT saja tidak cukup untuk menilai mutu kerja. Bab 2 menguji ini di 38 provinsi dan 514 kab/kota →', 10, '#cdd5e3', F_HEAD)],
          bg=INK, pad=16),
      ztext(44, 1000, 1806, 52, [run(FOOT1, 8, MUTED)], pad=4),
      ]

FOOT2 = ('Sumber: BPS (Sakernas Agustus 2025; TPT kab/kota 2017–2025; Susenas Maret). Skor "tidak bekerja" = TPT + NEET; skor "kerja tidak layak" = '
         'informal + setengah pengangguran (min–maks, 0–100). TPT dan kerja tidak layak hanya berkorelasi lemah antarprovinsi (ρ = −0,30; p = 0,066). '
         'Persisten ganda = TPT di atas acuan nasional dan median kab/kota sejenis setiap tahun. Empat provinsi Papua pemekaran memakai data provinsi induk sebelum 2024 (estimasi). '
         'Batas kab/kota: geoBoundaries IDN ADM2 (CC BY 3.0 IGO), hanya geometri.')
z2 = [zblank(0, 0, 1900, 1100, PAPER), WM.format(3),
      band('BAB 2 / 2  ·  38 PROVINSI → 514 KABUPATEN/KOTA, 2025',
           'Peringkat berbalik saat mutu kerja ikut dihitung.',
           'NTB peringkat 34 dari 38 menurut TPT, tetapi peringkat 2 menurut kerja tidak layak. DKI Jakarta sebaliknya: 7 → 38.'),
      zbutton(U1, '←  Bab 1', 1588, 106, 262, 42, INK),
      # peta + kontrol
      zsheet('H2-E Peta Berbalik', 44, 172, 836, 380, pad=12),
      zsheet('H2-Narasi', 44, 552, 600, 56, bg=CARD, title=False, pad=8),
      zparam(P_MODE, 'compact', 644, 552, 236, 56),
      zsheet(SLOPE_NAME, 890, 172, 330, 436, pad=10),
      zsheet('H2-F Kuadran', 1230, 172, 620, 436, pad=12),
      # baris bawah
      zsheet('H2-G Penimbang', 44, 618, 600, 280, pad=10),
      zparam('[Parameters].[Parameter 0379056855040004]', 'slider', 44, 898, 300, 47),
      zparam('[Parameters].[Parameter 0379056855146501]', 'slider', 344, 898, 300, 47),
      zparam('[Parameters].[Parameter 0379056855212038]', 'slider', 44, 945, 300, 47),
      zparam('[Parameters].[Parameter 0379056855277575]', 'slider', 344, 945, 300, 47),
      zsheet('H2-G Pesan Bobot', 64, 760, 560, 40, bg=None, title=False, pad=0),
      zsheet(M_PETA, 654, 618, 748, 248, pad=6),
      zsheet(M_HIST, 654, 866, 560, 126, pad=6),
      zparam('[Parameters].[Parameter 0379056854831106]', 'compact', 1214, 866, 188, 126),
      ztext(1412, 618, 438, 374, [
          run('KESIMPULAN', 9, AMBER, F_SEMI), NL,
          run('TPT rendah bukan jaminan kerja layak.', 15, '#ffffff', F_HEAD, True), NL,
          run('Rentan Ganda', 10, '#f0a08f', F_SEMI), run(' · Aceh, Maluku, Malut → padat karya formal, program NEET.', 10, '#ffffff'), NL,
          run('Rentan Tersembunyi', 10, '#f0a08f', F_SEMI), run(' · NTB, Sulbar, NTT → formalisasi usaha mikro, hilirisasi pertanian.', 10, '#ffffff'), NL,
          run('Antrean Kerja Formal', 10, '#9db7e0', F_SEMI), run(' · DKI, Kepri, Banten → percepat penyerapan kerja formal.', 10, '#ffffff'), NL,
          run('135 kab/kota', 10, '#9db7e0', F_SEMI), run(' selalu di atas median sejenis (66 juga di atas TPT nasional) → program jangka panjang.', 10, '#ffffff'), NL,
          run('Kerja tidak layak lebih terkait urbanisasi (ρ parsial −0,67) daripada lama sekolah (−0,14; tidak signifikan).', 9, '#cdd5e3')],
          bg=INK, pad=16),
      ztext(44, 1000, 1806, 52, [run(FOOT2, 8, MUTED)], pad=4),
      ]


def rebuild(dname, zones):
    global t
    m = re.search(r"(<dashboard enable-sort-zone-taborder='true' name='" + re.escape(dname) + r"'>)(.*?)(<simple-id uuid='[^']+' />\s*</dashboard>)", t, re.S)
    body = m.group(2)
    size = re.search(r"<size [^>]*/>", body).group(0)
    new = (m.group(1) + '<style />'
           + size + '<zones>' + ''.join(zones) + '</zones>' + m.group(3))
    t = t[:m.start()] + new + t[m.end():]


rebuild(H1, z1)
rebuild(H2, z2)

# ---------------------------------------------------------------- 8. viewpoint dashboard (entire view, tanpa seleksi lama)
def set_viewpoints(dname, sheets):
    global t
    m = re.search(r"(<window class='dashboard'[^>]*name='" + re.escape(dname) + r"'>)\s*<viewpoints>.*?</viewpoints>", t, re.S)
    vp = '<viewpoints>' + ''.join(
        f"<viewpoint name='{s}'>" + ("<zoom type='entire-view' />" if s != 'H2-I Jejak KabKota' else '') + '</viewpoint>'
        for s in sheets) + '</viewpoints>'
    t = t[:m.start()] + m.group(1) + vp + t[m.end():]


set_viewpoints(H1, [CM_L, CM_R, 'H1-P Spark TPT', 'H1-P Spark SMK', 'H1-P Spark NEET', 'H1-B Tren TPT', S_TPT, S_INF,
                    'H1-KPI Informal PT', 'H1-KPI NEET', 'H1-KPI SMK', 'H1-KPI TPT'])
set_viewpoints(H2, ['H2-E Peta Berbalik', 'H2-F Kuadran', 'H2-G Penimbang', 'H2-G Pesan Bobot',
                    M_PETA, M_HIST, 'H2-Narasi', SLOPE_NAME])

# ---------------------------------------------------------------- 9. buang worksheet yang dikeluarkan dari cerita
DROP = ['H1-A Dumbbell', 'H1-P Spark PT', 'H1-C Heatmap Sektor', 'H1-E Donut SMK Sektor', 'H1-D COVID Bar', 'H1-F Informal 2015 vs 2025', 'H2-I Jejak KabKota', 'H2-I KPI KabKota', 'H2-E Teks Cerita', 'H2-H Dumbbell Pembanding',
        'H2-H Mini Tile', 'H2-H Pesan Pembanding', 'H2-E Peta Geo']
for n in DROP:
    t = re.sub(r"<worksheet name='" + re.escape(n) + r"'>.*?</worksheet>\s*", '', t, count=1, flags=re.S)
    t = re.sub(r"<window class='worksheet'[^>]*name='" + re.escape(n) + r"'>.*?</window>\s*", '', t, count=1, flags=re.S)
    t = re.sub(r"<thumbnail [^>]*name='" + re.escape(n) + r"'[^>]*>.*?</thumbnail>\s*", '', t, count=1, flags=re.S)
    t = re.sub(r"\s*<exclude-sheet name='" + re.escape(n) + r"' />", '', t)
    assert f"name='{n}'" not in t, n

# buka langsung di Bab 1
t = t.replace("<window class='dashboard' maximized='true' name='Hal 2 - Provinsi ke KabKota'>", "<window class='dashboard' name='Hal 2 - Provinsi ke KabKota'>")
t = t.replace("<window class='dashboard' name='Hal 1 - Dua Wajah'>", "<window class='dashboard' maximized='true' name='Hal 1 - Dua Wajah'>")
open(OUT, 'w', encoding='utf-8').write(t)
ET.parse(OUT)
print('OK', len(t))
