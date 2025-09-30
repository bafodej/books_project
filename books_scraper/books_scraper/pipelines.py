# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import json
import hashlib
from datetime import datetime

class ValidationPipeline:
    """Validation des champs obligatoires"""
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get('title') or not adapter.get('price'):
            raise DropItem(f"Missing required fields: {item}")
        return item

class CleaningPipeline:
    """Nettoyage et formatage des données"""
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Nettoyer la description
        if adapter.get('description'):
            desc = adapter['description'].strip()
            # Limiter la longueur pour la base
            adapter['description'] = desc[:1000] + "..." if len(desc) > 1000 else desc
        
        # Convertir les tags en string JSON
        if adapter.get('tags'):
            adapter['tags'] = json.dumps(adapter['tags'])
        
        return item

class SQLitePipeline:
    """Stockage en base SQLite"""
    def __init__(self):
        # Créer la base de données
        self.connection = sqlite3.connect('books_database.db')
        self.cursor = self.connection.cursor()
        self.create_table()
    
    def create_table(self):
        """Créer la table des livres"""
        create_books_table = """
        CREATE TABLE IF NOT EXISTS books (
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
            UNIQUE(title, price) -- Éviter les doublons
        )
        """
        self.cursor.execute(create_books_table)
        self.connection.commit()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Insérer les données
        insert_sql = """
        INSERT OR IGNORE INTO books (
            title, price, stock, rating, category, 
            description, upc, image_url, url, scraped_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            self.cursor.execute(insert_sql, (
                adapter.get('title'),
                adapter.get('price'),
                adapter.get('stock', 0),
                adapter.get('rating', 0),
                adapter.get('category'),
                adapter.get('description'),
                adapter.get('upc'),
                adapter.get('image_url'),
                adapter.get('url'),
                adapter.get('scraped_at')
            ))
            self.connection.commit()
            spider.logger.info(f"Item saved: {adapter.get('title')}")
        except sqlite3.Error as e:
            spider.logger.error(f"Database error: {e}")
            raise DropItem(f"Database error: {e}")
        
        return item
    
    def close_spider(self, spider):
        """Fermer la connexion"""
        self.connection.close()
        spider.logger.info("Database connection closed")

class AdvancedDuplicatesPipeline:
    def __init__(self):
        self.items_seen = set()
        self.similarity_threshold = 0.9
    
    def process_item(self, item, spider):
        # Déduplication par hash de contenu
        content_hash = hashlib.sha256(
            f"{item.get('title', '')}{item.get('upc', '')}".encode()
        ).hexdigest()
        
        if content_hash in self.items_seen:
            raise DropItem(f"Duplicate detected: {item.get('title')}")
        self.items_seen.add(content_hash)
        return item
