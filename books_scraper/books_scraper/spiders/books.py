import scrapy
from books_scraper.items import BookScraperItem
import re
from datetime import datetime

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        # Extraire tous les livres de la page d'accueil
        books = response.css('article.product_pod')
        
        for book in books:
            # URL du livre pour la page détail
            relative_url = book.css('h3 a::attr(href)').get()
            if relative_url:
                book_url = response.urljoin(relative_url)
                yield scrapy.Request(book_url, callback=self.parse_book_detail)
        
        # Pagination automatique
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book_detail(self, response):
        item = BookScraperItem()
        
        # Données de base
        item['url'] = response.url
        item['title'] = response.css('h1::text').get()
        item['scraped_at'] = datetime.now()
        
        # Prix - nettoyer le format £51.77
        price_text = response.css('p.price_color::text').get()
        item['price'] = self.clean_price(price_text)
        
        # Stock - extraire le nombre depuis "In stock (22 available)"
        stock_text = response.css('p.instock.availability::text').getall()
        item['stock'] = self.extract_stock(' '.join(stock_text))
        
        # Rating - extraire depuis "star-rating Three" -> 3
        rating_class = response.css('p.star-rating::attr(class)').get()
        item['rating'] = self.extract_rating(rating_class)
        
        # Catégorie depuis breadcrumb - 3ème élément
        breadcrumb_items = response.css('ul.breadcrumb li')
        if len(breadcrumb_items) >= 3:
            item['category'] = breadcrumb_items[2].css('a::text').get()
        
        # Description - paragraphe après le header "Product Description"
        item['description'] = response.css('#product_description ~ p::text').get()
        
        # UPC depuis le tableau
        item['upc'] = response.css('table tr:first-child td::text').get()
        
        # Image URL - construire l'URL complète
        image_relative = response.css('#product_gallery img::attr(src)').get()
        item['image_url'] = response.urljoin(image_relative) if image_relative else None
        
        yield item

    def clean_price(self, price_text):
        """Nettoie le prix: £51.77 -> 51.77"""
        if price_text:
            return float(re.sub(r'[£,]', '', price_text))
        return None
    
    def extract_stock(self, stock_text):
        """Extrait le stock: 'In stock (22 available)' -> 22"""
        if stock_text and 'In stock' in stock_text:
            # Chercher les nombres dans le texte
            numbers = re.findall(r'\((\d+) available\)', stock_text)
            return int(numbers[0]) if numbers else 1  # défaut: 1 si disponible
        return 0
    
    def extract_rating(self, rating_class):
        """Convertit rating: 'star-rating Three' -> 3"""
        if rating_class:
            ratings = {
                'One': 1, 'Two': 2, 'Three': 3, 
                'Four': 4, 'Five': 5
            }
            for word, number in ratings.items():
                if word in rating_class:
                    return number
        return 0 
