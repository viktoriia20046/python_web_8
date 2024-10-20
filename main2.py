import json
import os
from mongoengine import Document, StringField, ReferenceField, ListField, connect
from dotenv import load_dotenv
from producer import producer
from consumer import consumer

# Завантажуємо зміни з .env файлу
load_dotenv()

# Отримуємо URI MongoDB з файлу .env
mongo_uri = os.getenv('MONGODB_URI')

# Підключення до MongoDB
connect('mydatabase', host=mongo_uri)

# Модель для авторів
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

# Модель для цитат
class Quote(Document):
    author = ReferenceField(Author, required=True)
    text = StringField(required=True)
    tags = ListField(StringField())  # Додаємо теги

# Завантаження авторів з JSON файлу
def load_authors():
    with open('authors.json', 'r') as file:
        authors_data = json.load(file)

        for item in authors_data:
            author = Author(
                fullname=item['fullname'],
                born_date=item['born_date'],
                born_location=item['born_location'],
                description=item['description']
            )
            author.save()
    print("Автори успішно завантажені.")

# Завантаження цитат з JSON файлу
def load_quotes():
    with open('quotes.json', 'r') as file:
        quotes_data = json.load(file)

        for item in quotes_data:
            author_name = item['author']
            quote_text = item['quote']
            tags = item.get('tags', [])  # Отримуємо теги з цитати, якщо є

            author = Author.objects(fullname=author_name).first()
            if author:
                quote = Quote(author=author, text=quote_text, tags=tags)
                quote.save()
            else:
                print(f"Автор не знайдений: {author_name}")
    print("Цитати успішно завантажені.")

# Функція для пошуку цитат
def search_quotes():
    search = input("Введіть ім'я автора або тег для пошуку: ").strip()

    if search.startswith('tag:'):
        tag = search.split(':')[1]
        quotes = Quote.objects(tags=tag)
    else:
        quotes = Quote.objects(author__fullname=search)
    
    if quotes:
        for quote in quotes:
            print(f"{quote.author.fullname}: {quote.text}")
    else:
        print(f"Цитати для '{search}' не знайдені.")

# Головне меню
def main_menu():
    while True:
        print("1. Завантажити авторів та цитати")
        print("2. Шукати цитати")
        print("3. Вийти")
        choice = input("Оберіть опцію: ").strip()

        if choice == '1':
            load_authors()
            load_quotes()
        elif choice == '2':
            search_quotes()
        elif choice == '3':
            break
        else:
            print("Невірна опція, спробуйте ще раз.")

if __name__ == "__main__":
    main_menu()