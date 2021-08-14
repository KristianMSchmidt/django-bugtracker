import factory

from projects.models import Project
from django.test import Client
from accounts.tests.factories import UserFactory


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    title = 'test project title'
    description = 'test description'
    created_by = factory.SubFactory(UserFactory)
