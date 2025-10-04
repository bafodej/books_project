from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import corrigé
from api.routes.books import router as books_router

app = FastAPI(
    title="Books Reader API",
    description="API REST pour consulter une collection de 1000 livres scrapés",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion corrigée
app.include_router(books_router)

@app.get("/")
async def root():
    return {
        "message": "Books Reader API",
        "docs": "/docs",
        "total_books": "1000 scraped books",
        "endpoints": {
            "GET /books": "List books (paginated)",
            "GET /books/{id}": "Get book by ID", 
            "POST /books/search": "Search books",
            "GET /books/categories/list": "Get all categories"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}


