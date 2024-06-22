import json
from django.core.management import BaseCommand
from django.db import connection
from main.models import Client, Message, Sending
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE main_message RESTART IDENTITY CASCADE;')
            cursor.execute('TRUNCATE TABLE main_sending RESTART IDENTITY CASCADE;')
            cursor.execute('TRUNCATE TABLE main_client RESTART IDENTITY CASCADE;')

        Client.objects.all().delete()
        Message.objects.all().delete()
        Sending.objects.all().delete()

        with open('data.json', 'r') as f:
            data = json.load(f)

        clients_to_create = []
        messages_to_create = []

        for item in data:
            if item["model"] == "main.client":
                name, email, owner = item['fields']['name'], item['fields']['email'], item['fields']['owner']
                clients_to_create.append(Client(name=name, email=email, owner=User.objects.get(pk=owner)))
            elif item["model"] == "main.message":
                theme, text, owner = item['fields']['theme'], item['fields']['text'], item['fields']['owner']
                messages_to_create.append(Message(theme=theme, text=text, owner=User.objects.get(pk=owner)))

        Client.objects.bulk_create(clients_to_create)
        Message.objects.bulk_create(messages_to_create)

        for item in data:
            if item["model"] == "main.sending":
                message = Message.objects.get(pk=item['fields']['message'])
                owner = User.objects.get(pk=item['fields']['owner'])
                s = Sending(message=message, owner=owner)
                s.save()
                s.clients.set(item['fields']['clients'])