# analyse_sql.py
from database.database import get_db
from sqlalchemy import text, func
from database.models import Book

def analyse_prix_moyens():
    """Analyse des prix moyens par catégorie"""
    db = next(get_db())
    query = """
    SELECT 
        category,
        AVG(price) as prix_moyen,
        COUNT(*) as nombre_livres,
        MIN(price) as prix_min,
        MAX(price) as prix_max
    FROM books 
    WHERE category IS NOT NULL
    GROUP BY category
    ORDER BY prix_moyen DESC
    """
    return db.execute(text(query)).fetchall()

def top_categories():
    """Top 10 des catégories avec le plus de livres"""
    db = next(get_db())
    query = """
    SELECT 
        category,
        COUNT(*) as nombre_livres,
        AVG(price) as prix_moyen
    FROM books 
    WHERE category IS NOT NULL
    GROUP BY category
    ORDER BY nombre_livres DESC
    LIMIT 10
    """
    return db.execute(text(query)).fetchall()

def analyse_ratings():
    """Analyse des notes par catégorie"""
    db = next(get_db())
    query = """
    SELECT 
        category,
        AVG(rating) as note_moyenne,
        COUNT(CASE WHEN rating = 5 THEN 1 END) as livres_5_etoiles
    FROM books 
    WHERE category IS NOT NULL AND rating > 0
    GROUP BY category
    ORDER BY note_moyenne DESC
    """
    return db.execute(text(query)).fetchall()

def livres_en_rupture():
    """Livres en rupture de stock par catégorie"""
    db = next(get_db())
    query = """
    SELECT 
        category,
        COUNT(*) as livres_rupture,
        AVG(price) as prix_moyen_rupture
    FROM books 
    WHERE stock = 0 AND category IS NOT NULL
    GROUP BY category
    ORDER BY livres_rupture DESC
    """
    return db.execute(text(query)).fetchall()

if __name__ == "__main__":
    print("=== ANALYSE DES PRIX MOYENS ===")
    for row in analyse_prix_moyens():
        print(f"{row.category}: {row.prix_moyen:.2f}€ ({row.nombre_livres} livres)")
    
    print("\n=== TOP CATEGORIES ===")
    for row in top_categories():
        print(f"{row.category}: {row.nombre_livres} livres (prix moyen: {row.prix_moyen:.2f}€)")
