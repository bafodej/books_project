from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

class BookBase(BaseModel):
    """Schéma de base pour les livres"""
    title: str = Field(..., min_length=1, max_length=500)
    price: float = Field(..., gt=0)
    upc: Optional[str] = Field(None, max_length=50)
    stock: int = Field(default=0, ge=0)
    rating: int = Field(default=0, ge=0, le=5)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    url: Optional[HttpUrl] = None

class BookCreate(BookBase):
    """Schéma pour la création de livres"""
    pass

class BookUpdate(BaseModel):
    """Schéma pour la mise à jour de livres"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    rating: Optional[int] = Field(None, ge=0, le=5)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None

class BookResponse(BookBase):
    """Schéma pour les réponses API"""
    id: int
    scraped_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Pour la compatibilité SQLAlchemy

class BookAnalytics(BaseModel):
    """Schéma pour les données analytiques"""
    category: str
    avg_price: float
    book_count: int
    min_price: float
    max_price: float

class ScrapingSessionResponse(BaseModel):
    """Schéma pour les sessions de scraping"""
    id: int
    started_at: datetime
    finished_at: Optional[datetime] = None
    books_scraped: int
    errors_count: int
    status: str
    
    class Config:
        from_attributes = True
