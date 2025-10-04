from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database.models import Book
from api.dependencies import get_database
from services.book_service import BookService
from database.schemas import BookResponse, BookSearch

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
async def get_books(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(20, ge=1, le=100, description="Nombre d'éléments à retourner"),
    db: Session = Depends(get_database)
):
    """Récupérer une liste paginée de livres"""
    service = BookService(db)
    books = service.get_books(skip=skip, limit=limit)
    return books

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db: Session = Depends(get_database)
):
    """Récupérer un livre par son ID"""
    service = BookService(db)
    book = service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return book

@router.post("/search", response_model=List[BookResponse])
async def search_books(
    search: BookSearch,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_database)
):
    """Rechercher des livres selon des critères"""
    service = BookService(db)
    return service.search_books(search, skip=skip, limit=limit)

@router.get("/categories/list")
async def get_categories(db: Session = Depends(get_database)):
    """Récupérer toutes les catégories disponibles"""
    service = BookService(db)
    return {"categories": service.get_categories()}

