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


class BookResponse(BookBase):
    """Schéma pour les réponses API"""
    id: int
    scraped_at: datetime
    
    class Config:
        from_attributes = True  # Pour la compatibilité SQLAlchemy


class BookSearch(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

