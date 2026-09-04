import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

conn = sqlite3.connect(BASE_DIR / "produits.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produits(
    uid TEXT PRIMARY KEY,
    nom TEXT NOT NULL,
    prix INTEGER NOT NULL,
    categorie TEXT,
    stock INTEGER
)
""")

produits = [
    ("338FE7F7", "Livre de recette", 1500, "Livre", 100),
    ("83ED4110", "Planche cuisine", 3000, "Cuisine", 100),
    ("33373C10", "Livre de recette", 1500, "Livre", 100),
    ("C371E9F7", "Porte clé", 200, "accessoire", 100)
]
cursor.executemany(
    """
    INSERT OR REPLACE INTO produits
    VALUES (?, ?, ?, ?, ?)
    """,
    produits
)

conn.commit()
conn.close()

print("Base produits créée avec succès.")