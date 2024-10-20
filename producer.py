import pika
import json

def producer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Створюємо чергу
    channel.queue_declare(queue='email_queue')

    # Генеруємо фейкові дані для контактів
    contacts = [
        {'name': 'John Doe', 'email': 'john@example.com'},
        {'name': 'Jane Doe', 'email': 'jane@example.com'}
    ]

    # Надсилаємо кожен контакт у чергу
    for contact in contacts:
        channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(contact))
        print(f"Надіслано контакт: {contact['name']}")

    connection.close()