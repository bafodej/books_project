import sqlite3
from database.models import Book

# Connexion à la base
conn = sqlite3.connect('books_database.db')
cursor = conn.cursor()

# Statistiques générales
print("=== STATISTIQUES GÉNÉRALES ===")
cursor.execute("SELECT COUNT(*) FROM books")
total = cursor.fetchone()[0]
print(f"Total de livres: {total}")

cursor.execute("SELECT AVG(price) FROM books")
avg_price = cursor.fetchone()[0]
print(f"Prix moyen: {avg_price:.2f}€")

cursor.execute("SELECT COUNT(DISTINCT category) FROM books WHERE category IS NOT NULL")
categories = cursor.fetchone()[0]
print(f"Nombre de catégories: {categories}")

print("\n=== ÉCHANTILLON DE DONNÉES ===")
cursor.execute("SELECT title, price, category FROM books LIMIT 5")
for row in cursor.fetchall():
    print(f"- {row[0][:50]}... | {row[1]}€ | {row[2]}")

print("\n=== TOP CATÉGORIES ===")
cursor.execute("""
SELECT category, COUNT(*) as count, AVG(price) as avg_price 
FROM books 
WHERE category IS NOT NULL 
GROUP BY category 
ORDER BY count DESC 
LIMIT 5
""")
for row in cursor.fetchall():
    print(f"- {row[0]}: {row[1]} livres (prix moyen: {row[2]:.2f}€)")

conn.close()
