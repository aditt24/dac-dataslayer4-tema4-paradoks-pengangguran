"""Kemas .twb hasil edit + folder Data/Image dari twbx basis menjadi .twbx baru.
Pemakaian: python pack_twbx.py <twb> <folder_ekstrak_basis> <out.twbx> <nama_twb_dalam_zip>"""
import zipfile, os, sys
twb, base, out, inner = sys.argv[1:5]
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(twb, inner)
    for root, _, fs in os.walk(base):
        for f in fs:
            fp = os.path.join(root, f)
            if fp.endswith('.twb'):
                continue
            z.write(fp, os.path.relpath(fp, base).replace(os.sep, '/'))
print('packed', out, os.path.getsize(out))
