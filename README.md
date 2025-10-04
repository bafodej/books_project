# Books Scraper & REST API 📚

Un projet complet de scraping et d'API REST pour analyser une collection de 1000 livres provenant de [books.toscrape.com](http://books.toscrape.com).

## ✨ Fonctionnalités

- 🕷️ **Scraper Scrapy** - Extraction de 1000 livres avec métadonnées complètes
- 🗄️ **Base de données SQLite** avec SQLAlchemy ORM
- 🚀 **API REST FastAPI** avec architecture clean
- 📊 **Recherche avancée** - Filtrage par titre, catégorie, prix
- 📖 **Documentation automatique** Swagger/OpenAPI
- 🏗️ **Architecture modulaire** - Séparation des couches

## 🛠️ Technologies

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Scraping**: Scrapy
- **Base de données**: SQLite
- **Documentation**: Swagger UI, ReDoc


## 🚀 Installation & Lancement

### 1. Cloner le projet


### 2. Créer l'environnement virtuel


### 3. Installer les dépendances


### 4. Lancer l'API


L'API sera accessible à : http://localhost:8000

## 📚 Documentation API

Une fois l'API lancée, accédez à :
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/books` | Liste paginée des livres |
| `GET` | `/books/{id}` | Détails d'un livre |
| `POST` | `/books/search` | Recherche avec filtres |
| `GET` | `/books/categories/list` | Liste des catégories |


## 🕷️ Utilisation du scraper

Pour re-scraper les données :

cd books_scraper
scrapy crawl books


## 📊 Données collectées

Chaque livre contient :
- **Titre** et **description**
- **Prix** et **stock disponible**
- **Note** (1-5 étoiles)
- **Catégorie** et **UPC**
- **URLs** image et produit
- **Date de scraping**

## 🧪 Tests

Tester l'API avec curl
curl http://localhost:8000/books?limit=5

Ou directement dans Swagger UI
http://localhost:8000/docs

## 🚢 Architecture

Le projet suit une **Clean Architecture** :
- **API Layer** (`api/`) - Routes et contrôleurs
- **Service Layer** (`services/`) - Logique métier
- **Data Layer** (`database/`) - Modèles et accès données
- **Infrastructure** (`books_scraper/`) - Collecte de données

## 📈 Données

La base contient **1000 livres** répartis sur **50 catégories**, avec :
- Prix moyen : ~35€
- Gamme complète de ratings (1-5 étoiles)
- Stock et disponibilité
- Métadonnées complètes


---

⭐ **N'hésitez pas à donner une étoile si ce projet vous a été utile !**



