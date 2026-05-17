import json, re

with open('drive_links.json', encoding='utf-8') as f:
    drive = json.load(f)
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

foto_pan = set(r['fotoPan'] for r in data if r['fotoPan'] and r['fotoPan'] != '0')
foto_part = set(r['fotoPart'] for r in data if r['fotoPart'] and r['fotoPart'] != '0')
all_foto = foto_pan | foto_part

# Match con prefisso 100_
match_100 = [f for f in all_foto if f'100_{f}' in drive]
print(f'Match con prefisso 100_: {len(match_100)}/{len(all_foto)}')

# Quelli che NON matchano
no_match = [f for f in all_foto if f'100_{f}' not in drive]
print(f'Non trovati: {len(no_match)}')
print('Esempi non trovati:', no_match[:20])

# Pattern dei non trovati
con_lettera = [f for f in no_match if re.search(r'[A-Z]', f)]
print(f'\nNon trovati con lettera (es. C, E): {len(con_lettera)}')
print('Esempi:', con_lettera[:15])

solo_num = [f for f in no_match if not re.search(r'[A-Z]', f)]
print(f'Non trovati solo numerici: {len(solo_num)}')
print('Esempi:', solo_num[:15])
