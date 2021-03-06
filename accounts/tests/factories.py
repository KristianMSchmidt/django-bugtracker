# $ docker-compose exec web python manage.py test accounts.tests.factories

import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'john%s' % n)
    email = 'JohnDoe@example.com'
    password = factory.PostGenerationMethodCall('set_password',
                                                'defaultpassword')
