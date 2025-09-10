# Flux DocMorris — Starter

Ce dépôt génère automatiquement un flux **CSV** (séparateur `;`) et **XML** conforme aux colonnes suivantes :

```
EAN13;NC;LABORATOIRE;MARQUE;NOM DU PRODUIT;TVA;PRIX;STOCK;ID PROMOFARMA;CATEGORIE;CATEGORIE2;CATEGORIE3;FORMAT;POIDS;URL IMAGE;DESCRIPTION
```

## Structure
```
data/catalog.csv                # Votre catalogue (UTF-8 ; séparateur ;)
scripts/generate_feed.py        # Générateur du flux
docs/docmorris.csv              # Sortie publiée (CSV)
docs/docmorris.xml              # Sortie publiée (XML)
```

## Utilisation locale
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas openpyxl
export CATALOG_PATH="data/catalog.csv"   # ou data/catalog.xlsx
python scripts/generate_feed.py
```

## Publication via GitHub Pages
Activez **GitHub Pages** sur la branche `main` et le dossier `/docs`.  
L'URL publique sera :
- `https://<votre-user>.github.io/<repo>/docmorris.csv`
- `https://<votre-user>.github.io/<repo>/docmorris.xml`

## Mise à jour quotidienne (GitHub Actions)
Un workflow (voir `.github/workflows/feed.yml`) régénère et **commit** les fichiers tous les jours.
