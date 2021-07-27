from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse

class NotificationsSeen(View, LoginRequiredMixin):

    def post(self, request):




        for ntf in self.request.user.notification_set.all().filter(unseen=True):
            ntf.unseen = False
            ntf.save()

        return JsonResponse({'succes': True})
