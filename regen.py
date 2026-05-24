import xlrd, json, os, re

wb = xlrd.open_workbook('DatiPdRBP e MP uniti.xls')
sh = wb.sheets()[0]

# Colonne (0-based): K=10, L=11, M=12, N=13, V=21, W=22, Z=25
def val(r, c):
    v = sh.cell_value(r, c)
    if isinstance(v, float) and v == int(v):
        v = int(v)
    return str(v).strip()

def normalizza_zona(raw):
    """Estrae il nome zona da valori come '[5] - SelciLama' → 'SelciLama'"""
    cleaned = re.sub(r'^\[\d+\]\s*-\s*', '', raw).strip()
    # Rimuove anche eventuale prefisso numerico tipo "5_" o "5 "
    cleaned = re.sub(r'^\d+[_\s]+', '', cleaned).strip()
    return cleaned

records = []
for r in range(1, sh.nrows):
    pdr = val(r, 25)
    if not pdr or pdr in ('0', ''):
        continue
    zona_raw = val(r, 10)  # Colonna K
    records.append({
        'pdr':      pdr,
        'zona':     normalizza_zona(zona_raw),
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
