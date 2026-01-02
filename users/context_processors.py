from .models import Notification

def notifications_count(request):
    count = 0
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()
    return {'notifications_count': count}
