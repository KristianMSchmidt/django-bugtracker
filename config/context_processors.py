"""
context processors can be used when some extra context is needed in all templates - ie.g. in _base.thml
Note that this processor is not really needed, as I can get access to notifications via user
Unsolved issue: how to paginate notifications, when base.html has no view-function? auto-paginate in template? Or can I paginate here somehow?
"""
from notifications.models import Notification

def get_notifications_to_context(request):
    context = {}
    if request.user.is_authenticated:
        context = {
            'notifications':Notification.objects.filter(recipient=request.user)[:20],
            'num_unseen_notifications': Notification.objects.filter(recipient=request.user, unseen=True).count()
        }
    return context
    