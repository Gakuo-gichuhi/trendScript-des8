from datetime import date
from .models import DailyVisitor

class VisitorCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ignore admin pages
        if not request.path.startswith("/admin"):
            today = date.today()
            obj, created = DailyVisitor.objects.get_or_create(date=today)
            obj.count += 1
            obj.save()

        return self.get_response(request)
