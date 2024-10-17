import json
import re
import pika
import redis
from mongoengine import Document, StringField, connect, ReferenceField, ListField
from dotenv import load_dotenv
import os

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
    author = ReferenceField(Author)
    quote = StringField()

# Завантаження авторів з файлу authors.json
def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(**author_data)
            author.save()
        print("Автори успішно завантажені.")

# Пошук цитат за ім'ям автора
def search_quotes():
    command = input("Enter command (name:author_name or exit): ").strip()
    if command.startswith("name:"):
        author_name = command.split(":")[1].strip()
        try:
            author = Author.objects(fullname=author_name).first()
            if author:
                quotes = Quote.objects(author=author)
                for quote in quotes:
                    print(f"Цитата: {quote.quote}")
            else:
                print("Автор не знайдений.")
        except Exception as e:
            print(f"Сталася помилка: {str(e)}")
    elif command == "exit":
        return
    else:
        print("Невірна команда.")

# Головне меню
def main_menu():
    while True:
        print("1. Load authors and quotes")
        print("2. Search quotes")
        print("3. Produce contacts")
        print("4. Consume emails")
        print("5. Consume SMS")
        
        choice = input("Choose an option: ").strip()

        if choice == '1':
            load_authors()
        elif choice == '2':
            search_quotes()
        elif choice == '3':
            print("Функція недоступна")
        elif choice == '4':
            print("Функція недоступна")
        elif choice == '5':
            print("Функція недоступна")
        else:
            print("Невірний вибір. Спробуйте знову.")

if __name__ == "__main__":
    main_menu()