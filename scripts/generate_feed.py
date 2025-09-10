#!/usr/bin/env python3
import os, sys, pandas as pd, xml.etree.ElementTree as ET, json
from datetime import datetime

REQUIRED_COLUMNS = [
    "EAN13","NC","LABORATOIRE","MARQUE","NOM DU PRODUIT","TVA","PRIX","STOCK",
    "ID PROMOFARMA","CATEGORIE","CATEGORIE2","CATEGORIE3","FORMAT","POIDS",
    "URL IMAGE","DESCRIPTION"
]

ALIAS_MAP = {
    "EAN":"EAN13",
    "EAN_13":"EAN13",
    "BRAND":"MARQUE",
    "NOM_PRODUIT":"NOM DU PRODUIT",
    "NAME":"NOM DU PRODUIT",
    "VAT":"TVA",
    "PRICE":"PRIX",
    "STOCK_QTY":"STOCK",
    "CATEGORY":"CATEGORIE",
    "CATEGORY1":"CATEGORIE",
    "CATEGORY2":"CATEGORIE2",
    "CATEGORY3":"CATEGORIE3",
    "WEIGHT":"POIDS",
    "IMAGE_URL":"URL IMAGE",
    "DESCRIPTION_LONGUE":"DESCRIPTION",
}

def normalize_headers(df):
    mapping = {}
    for col in df.columns:
        key = col.strip()
        up = key.upper()
        mapping[col] = ALIAS_MAP.get(up, key)
    df = df.rename(columns=mapping)
    return df

def ensure_columns(df):
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df = df[REQUIRED_COLUMNS]
    return df

def to_semicolon_csv(df, path):
    df.to_csv(path, index=False, sep=";", encoding="utf-8")

def to_xml(df, path):
    root = ET.Element("products")
    for _, row in df.iterrows():
        p = ET.SubElement(root, "product")
        for col in REQUIRED_COLUMNS:
            el = ET.SubElement(p, col.replace(" ", "_").replace("/", "_"))
            val = row[col]
            if pd.isna(val):
                val = ""
            el.text = str(val)
    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)

def main():
    catalog_path = os.getenv("CATALOG_PATH", "data/catalog.csv")
    out_dir = os.getenv("OUT_DIR", "docs")
    os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(catalog_path):
        alt = "data/catalog.xlsx"
        if os.path.exists(alt):
            df = pd.read_excel(alt)
        else:
            raise SystemExit(f"Catalog not found: {catalog_path} (or {alt}).")
    else:
        if catalog_path.lower().endswith(".xlsx"):
            df = pd.read_excel(catalog_path)
        else:
            df = pd.read_csv(catalog_path, sep=";", encoding="utf-8")

    df = normalize_headers(df)
    df = ensure_columns(df)

    for col in ["TVA","PRIX","STOCK","POIDS"]:
        if col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            except Exception:
                pass

    csv_path = os.path.join(out_dir, "docmorris.csv")
    xml_path = os.path.join(out_dir, "docmorris.xml")
    to_semicolon_csv(df, csv_path)
    to_xml(df, xml_path)

    with open(os.path.join(out_dir, "health.json"), "w", encoding="utf-8") as f:
        json.dump({"generated_at": datetime.utcnow().isoformat() + "Z", "rows": int(len(df))}, f, ensure_ascii=False)

    print(f"Wrote: {csv_path} and {xml_path} (rows={len(df)})")

if __name__ == "__main__":
    main()
