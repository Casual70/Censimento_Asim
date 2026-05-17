import xlrd, json, os

wb = xlrd.open_workbook('DatiPdRBP e MP uniti.xls')
sh = wb.sheets()[0]

# Colonne (0-based): L=11, M=12, N=13, V=21, W=22, Z=25
def val(r, c):
    v = sh.cell_value(r, c)
    if isinstance(v, float) and v == int(v):
        v = int(v)
    return str(v).strip()

records = []
for r in range(1, sh.nrows):
    pdr = val(r, 25)
    if not pdr or pdr in ('0', ''):
        continue
    records.append({
        'pdr':      pdr,
        'via':      val(r, 11),
        'fab':      val(r, 12),
        'presa':    val(r, 13),
        'fotoPan':  val(r, 21),
        'fotoPart': val(r, 22),
    })

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, separators=(',', ':'))

size_kb = os.path.getsize('data.json') / 1024
print(f'Record: {len(records)}, Dimensione: {size_kb:.1f} KB')
print('Esempio:', json.dumps(records[1], ensure_ascii=False))
