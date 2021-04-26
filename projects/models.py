from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse 

class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=301, default="")
    
    # one-to-many relationship
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete = models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # we override the default related name, which is 'project_set'
    users = models.ManyToManyField(get_user_model(), related_name='projects', blank=True) 

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.id)])


"""
# override save method to notify users
def save(self, *args, **kw):
    # I think I should use a m2m-signal here... https://stackoverflow.com/questions/44155519/get-selected-values-of-manytomany-field-in-django-model-save-method
    # But using a signal will create the additional problem of getting request.user in the signal-function  
    pass

    if self.pk is not None:  # we are updating an existing project
        # notify newly enrolled users
        print()


        temp = vars(self)
        for item in temp:
            print(item, ':', temp[item])

        #print(self.users.all())

        orig = Project.objects.get(pk=self.pk)
        orig_user_set = orig.users.all()
        #print(orig.title)
        #print(orig.users.all())
        super(Project, self).save(*args, **kw)

        current = Project.objects.get(pk=self.pk)
        print(current.title)
        print(current.users.all())

        current_user_set = current.users.all()

        newly_disenrolled_users = orig_user_set.difference(current_user_set)
        newly_enrolled_users = current_user_set.difference(orig_user_set)
        
        #print(orig_user_set)
        #print(current_user_set)   
        #print(newly_enrolled_users)
        #print(newly_disenrolled_users)
    if self.pk is not None:  # we are creating a new projet
        # notify enrolled users
        pass
    """
