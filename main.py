from dotenv import load_dotenv
from mongoengine import connect
import os

# Завантажуємо змінні з .env файлу
load_dotenv()

# Тепер можна отримати URI MongoDB
mongo_uri = os.getenv('MONGODB_URI')
connect('mydatabase', host=mongo_uri)