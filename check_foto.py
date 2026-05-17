import json, re

with open('drive_links.json', encoding='utf-8') as f:
    drive = json.load(f)
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

# Cerca fotoPan e fotoPart nel drive
foto_codes = set()
for r in data:
    if r['fotoPan'] and r['fotoPan'] != '0': foto_codes.add(r['fotoPan'])
    if r['fotoPart'] and r['fotoPart'] != '0': foto_codes.add(r['fotoPart'])

drive_keys = set(k for k in drive.keys() if not k.startswith('_'))

# Match esatto
exact = foto_codes & drive_keys
print(f'Match esatto fotoPan/fotoPart in Drive: {len(exact)}/{len(foto_codes)}')
print('Esempi match:', list(exact)[:10])

# Esempio PdR: fotoPan=9282
sample_foto = ['9282', '9283', '0599C', '0585C', '0213', '0214']
for f in sample_foto:
    found = f in drive
    # cerca anche con prefisso 100_
    found2 = f'100_{f}' in drive
    print(f'  "{f}" in drive: {found} | "100_{f}": {found2}')

# Mostra chiavi Drive che sembrano codici foto (4-5 cifre con eventuale lettera)
foto_like = [k for k in drive_keys if re.match(r'^[0-9]{3,5}[A-Z]?$', k)]
print(f'\nChiavi Drive simili a codici foto (3-5 cifre): {len(foto_like)}')
print('Esempi:', foto_like[:20])

# Anche con 100_ prefix
foto_100 = [k for k in drive_keys if re.match(r'^100_[0-9]+$', k)]
print(f'\nChiavi Drive tipo "100_NNNN": {len(foto_100)}')
print('Esempi:', foto_100[:10])
