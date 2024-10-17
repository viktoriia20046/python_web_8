import json
import os
from mongoengine import Document, StringField, ReferenceField, ListField, connect
from dotenv import load_dotenv

# Завантажуємо змінні з .env файлу
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
    author = ReferenceField(Author, reverse_delete_rule='CASCADE')
    quote_text = StringField(required=True)
    tags = ListField(StringField())

# Завантаження авторів з файлу authors.json
def load_authors():
    with open('authors.json', 'r') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(
                fullname=author_data['fullname'],
                born_date=author_data.get('born_date', ''),
                born_location=author_data.get('born_location', ''),
                description=author_data.get('description', '')
            )
            author.save()
    print("Автори успішно завантажені.")

# Завантаження цитат з файлу quotes.json
def load_quotes():
    with open('quotes.json', 'r') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                quote = Quote(
                    author=author,
                    quote_text=quote_data['quote'],
                    tags=quote_data.get('tags', [])
                )
                quote.save()
    print("Цитати успішно завантажені.")

# Функція для пошуку цитат
def search_quotes():
    author_name = input("Введіть ім'я автора: ").strip()
    author = Author.objects(fullname=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        if quotes:
            for quote in quotes:
                print(f"Цитата: {quote.quote_text}")
                print(f"Теги: {', '.join(quote.tags)}")
        else:
            print(f"Цитати для автора {author_name} не знайдені.")
    else:
        print(f"Автор {author_name} не знайдений.")

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
            print("До побачення!")
            break
        else:
            print("Неправильний вибір, спробуйте ще раз.")

if __name__ == '__main__':
    main_menu()