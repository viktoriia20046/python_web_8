import pika
import json

def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Споживаємо повідомлення з черги
    channel.queue_declare(queue='email_queue')

    def callback(ch, method, properties, body):
        contact = json.loads(body)
        print(f"Отримано контакт: {contact['name']} - {contact['email']}")

    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

    print('Очікування повідомлень...')
    channel.start_consuming()