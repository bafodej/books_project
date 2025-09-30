import sqlite3
import os

def check_database():
    """Vérifier le contenu de books_database.db"""
    db_file = 'books_database.db'
    
    print("=== VÉRIFICATION BASE DE DONNÉES BOOKS SCRAPER ===")
    
    if not os.path.exists(db_file):
        print(f"❌ Le fichier {db_file} n'existe pas !")
        return
    
    # Taille du fichier
    size_kb = os.path.getsize(db_file) / 1024
    print(f"📁 Taille du fichier: {size_kb:.1f} KB")
    
    try:
        # Connexion à la base [web:204]
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Découvrir les tables [web:203]
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tables trouvées: {[table[0] for table in tables]}")
        
        if not tables:
            print("❌ Aucune table trouvée dans la base !")
            return
        
        # Vérifier la structure de la table books
        cursor.execute("PRAGMA table_info(books)")
        columns = cursor.fetchall()
        print(f"\n🏗️  Structure de la table 'books':")
        for col in columns:
            print(f"   • {col[1]} ({col[2]})")
        
        # Compter les livres
        cursor.execute("SELECT COUNT(*) FROM books")
        count = cursor.fetchone()[0]
        print(f"\n📚 Nombre total de livres: {count}")
        
        if count == 0:
            print("⚠️  Aucun livre trouvé. Relancez: scrapy crawl books")
            conn.close()
            return
        
        # Échantillon de livres [web:205]
        cursor.execute("SELECT title, price, category FROM books LIMIT 5")
        books = cursor.fetchall()
        print(f"\n📖 Échantillon de 5 livres:")
        for i, book in enumerate(books, 1):
            title = book[0][:35] + "..." if len(book[0]) > 35 else book[0]
            print(f"   {i}. {title}")
            print(f"      Prix: £{book[1]} | Catégorie: {book[2]}")
        
        # Top catégories
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM books 
            WHERE category IS NOT NULL 
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 5
        """)
        categories = cursor.fetchall()
        print(f"\n🏷️  Top 5 catégories:")
        for i, cat in enumerate(categories, 1):
            print(f"   {i}. {cat[0]}: {cat[1]} livres")
        
        # Statistiques de prix
        cursor.execute("SELECT MIN(price), AVG(price), MAX(price) FROM books")
        prix_stats = cursor.fetchone()
        print(f"\n💰 Statistiques prix:")
        print(f"   • Prix minimum: £{prix_stats[0]:.2f}")
        print(f"   • Prix moyen: £{prix_stats[1]:.2f}")
        print(f"   • Prix maximum: £{prix_stats[2]:.2f}")
        
        # Répartition des notes
        cursor.execute("SELECT rating, COUNT(*) FROM books GROUP BY rating ORDER BY rating DESC")
        ratings = cursor.fetchall()
        print(f"\n⭐ Répartition des notes:")
        for rating, count in ratings:
            if rating == 0:
                print(f"   • Sans note: {count} livres")
            else:
                print(f"   • {rating} étoiles: {count} livres")
        
        conn.close()
        print(f"\n✅ Base de données analysée avec succès !")
        print(f"🎯 Prêt pour l'étape suivante: API FastAPI")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_database()
