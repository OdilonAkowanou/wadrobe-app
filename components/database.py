# components/database.py
import sqlite3
import os

DB_PATH = "data/wardrobe.db"

def init_db():
    """Crée la base de données au démarrage"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vetements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            categorie TEXT,
            couleur TEXT,
            style TEXT,
            image_path TEXT,
            date_ajout TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def ajouter_vetement(nom, categorie, couleur, style, image_path):
    """Ajoute un vêtement dans la base"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vetements (nom, categorie, couleur, style, image_path)
        VALUES (?, ?, ?, ?, ?)
    """, (nom, categorie, couleur, style, image_path))
    conn.commit()
    conn.close()

def get_tous_vetements():
    """Récupère tous les vêtements"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vetements")
    vetements = cursor.fetchall()
    conn.close()
    return vetements

def supprimer_vetement(vetement_id):
    """Supprime un vêtement par son ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vetements WHERE id = ?", (vetement_id,))
    conn.commit()
    conn.close()