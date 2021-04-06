"""
docker-compose exec web python manage.py shell
from easy import *
"""
from tickets.models import Ticket
from projects.models import Project
from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()
tickets = Ticket.objects.all()
projects = Project.objects.all()
print("Models:  Tickets, Projects, User imported")

print("tickets, projects, users also defined")
