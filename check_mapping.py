import json

with open('drive_links.json', encoding='utf-8') as f:
    drive = json.load(f)
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

# Cerca il PdR di esempio
target = '11714030030013'
rec = next((r for r in data if r['pdr'] == target), None)
print('Record PdR', target, ':', rec)

# Controlla se la chiave Scheda fabbricato-{fab} esiste
if rec:
    key = f'Scheda fabbricato-{rec["fab"]}'
    print(f'\nChiave cercata: "{key}"')
    print(f'Trovata in drive_links: {key in drive}')
    if key in drive:
        print(f'ID Drive: {drive[key]}')

# Conta quante Scheda fabbricato esistono in drive
schede = {k: v for k, v in drive.items() if k.startswith('Scheda fabbricato')}
print(f'\nTotale "Scheda fabbricato" in Drive: {len(schede)}')
print('Esempi:', list(schede.keys())[:10])

# Conta quanti fab unici ci sono in data.json
fabs = set(r['fab'] for r in data if r['fab'] and r['fab'] not in ('0', ''))
print(f'\nCFabbricato unici in data.json: {len(fabs)}')

# Quanti matchano con Scheda fabbricato in drive
match = sum(1 for f in fabs if f'Scheda fabbricato-{f}' in drive)
print(f'Match fab -> Scheda fabbricato: {match}/{len(fabs)}')

# Anche CPresa: cerca Scheda presa_singola
presa_key = 'Scheda presa_singola'
print(f'\n"Scheda presa_singola" in Drive: {presa_key in drive}')
if presa_key in drive:
    print(f'ID: {drive[presa_key]}')
