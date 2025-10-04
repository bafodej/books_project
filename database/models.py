from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    
    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)
    
    # Données essentielles (correspondant à votre scraper)
    title = Column(String(500), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    upc = Column(String(50), unique=True, index=True)  # Identifiant unique livre
    stock = Column(Integer, default=0)  # Plus précis qu'availability
    rating = Column(Integer, default=0)  # 0-5 étoiles
    
    # Métadonnées
    category = Column(String(100), index=True)
    description = Column(Text)  # Peut être long
    image_url = Column(String(500))
    url = Column(String(500), unique=True)  # URL source
    
    # Timestamps automatiques
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())

    
    # Index composés pour les requêtes analytiques
    __table_args__ = (
        Index('idx_category_price', 'category', 'price'),
        Index('idx_rating_price', 'rating', 'price'),
    )
    
    def __repr__(self):
        return f"<Book(title='{self.title}', price={self.price})>"

