from sqlalchemy.orm import Session
from database.models import Book
from database.schemas import BookSearch
from typing import List, Optional

class BookService:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_books(self, skip: int = 0, limit: int = 20) -> List[Book]:
        """Récupérer une liste paginée de livres"""
        return self.db.query(Book).offset(skip).limit(limit).all()
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Récupérer un livre par son ID"""
        return self.db.query(Book).filter(Book.id == book_id).first()
    
    def search_books(self, search: BookSearch, skip: int = 0, limit: int = 20) -> List[Book]:
        """Rechercher des livres selon des critères"""
        query = self.db.query(Book)
        
        if search.query:
            query = query.filter(Book.title.contains(search.query))
        if search.category:
            query = query.filter(Book.category == search.category)
        if search.min_price:
            query = query.filter(Book.price >= search.min_price)
        if search.max_price:
            query = query.filter(Book.price <= search.max_price)
            
        return query.offset(skip).limit(limit).all()
    
    def get_categories(self) -> List[str]:
        """Récupérer toutes les catégories disponibles"""
        return [cat[0] for cat in self.db.query(Book.category).distinct().filter(Book.category.isnot(None)).all()]


