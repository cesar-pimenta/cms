from django.http import JsonResponse
from django.views import View


class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({
            'status': 'healthy',
            'version': '1.0.0',
        })
