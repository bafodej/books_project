"""
Script de migration pour créer/mettre à jour la structure de la base de données
"""
import sqlite3
import os
from datetime import datetime

def backup_existing_database():
    """Créer une sauvegarde de la base existante"""
    if os.path.exists('books_database.db'):
        backup_name = f'books_database_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        try:
            os.system(f'copy books_database.db {backup_name}')  # Windows
            print(f"Sauvegarde créée: {backup_name}")
        except:
            print("Pas de sauvegarde nécessaire")

def create_or_migrate_database():
    """Créer la table ou migrer si elle existe"""
    backup_existing_database()
    
    connection = sqlite3.connect('books_database.db')
    cursor = connection.cursor()
    
    # Vérifier si la table existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("Table books n'existe pas, création en cours...")
        # Créer la table complète
        create_books_table = """
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            rating INTEGER DEFAULT 0,
            category TEXT,
            description TEXT,
            upc TEXT UNIQUE,
            image_url TEXT,
            url TEXT UNIQUE,
            scraped_at TIMESTAMP,
            updated_at TIMESTAMP,
            UNIQUE(title, price)
        )
        """
        cursor.execute(create_books_table)
        print("Table books créée avec succès")
    else:
        print("Table books existe déjà")
        # Ajouter la colonne updated_at si elle n'existe pas
        try:
            cursor.execute("ALTER TABLE books ADD COLUMN updated_at TIMESTAMP")
            print("Colonne updated_at ajoutée")
        except sqlite3.OperationalError:
            print("Colonne updated_at existe déjà")
    
    # Créer les index pour optimiser les requêtes
    try:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_category_price ON books(category, price)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rating_price ON books(rating, price)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON books(title)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_upc ON books(upc)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_url ON books(url)")
        print("Index créés avec succès")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création des index: {e}")
    
    connection.commit()
    connection.close()
    print("Migration/Création terminée !")

if __name__ == "__main__":
    create_or_migrate_database()

