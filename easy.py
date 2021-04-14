"""
Convenience script that loads most used models into django shell and predefines some constants. 
Usage: 
$docker-compose exec web python manage.py shell
$from easy import *
"""
from tickets.models import Ticket
from projects.models import Project
from django.contrib.auth import get_user_model
import json

User = get_user_model()
users = User.objects.all()
u0 = users[0]
tickets = Ticket.objects.all()
t0=tickets[0]
projects = Project.objects.all()
p0=projects[0]
print("Models:  Tickets, Projects, User imported")
print("tickets, projects, users defined")
print("t0, p0, u0 defined")

def create_projects():
    with open('projects/projects.json') as f:
        projects_json = json.load(f)

    for project in projects_json:
        project = Project(
                title=project['title'], description=project['description'], created_by_id=12)
        try:
            project.save()
            print("Saved project: " + str(project))
        except:
            print("Could not save project: " + str(project))

