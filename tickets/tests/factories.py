import factory
from projects.tests.factories import ProjectFactory
from accounts.tests.factories import UserFactory
from ..models import Ticket


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    title = factory.Sequence(lambda n: f'test ticket title{n}')
    description = 'test description'
    project = factory.SubFactory(ProjectFactory)
    submitter = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)
    developer = factory.SubFactory(UserFactory)
    status = Ticket.Status.IN_PROGRESS
    priority = Ticket.Priority.LOW
    type = Ticket.Type.BUG
