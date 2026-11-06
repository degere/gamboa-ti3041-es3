import json
from pathlib import Path

# Lee el JSON original
with open('productos_original.json', 'r', encoding='utf-8') as f:
    productos = json.load(f)

fixture = []
for p in productos:
    fixture.append({
        "model": "Ferreteria.producto",
        "pk": p["id"],
        "fields": {
            "nombre": p["nombre"],
            "categoria": p["categoria"],
            "precio": p["precio"],
            "stock": p["stock"],
            "imagen": p["imagen"]
        }
    })

# Crea la carpeta fixtures si no existe
Path('Ferreteria/fixtures').mkdir(parents=True, exist_ok=True)

# Escribe la fixture
with open('Ferreteria/fixtures/productos.json', 'w', encoding='utf-8') as f:
    json.dump(fixture, f, ensure_ascii=False, indent=2)

print(f"Fixture generada con {len(fixture)} productos.")