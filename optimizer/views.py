from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def recommendations_view(request):
    return JsonResponse({'message': 'Optimizer endpoint placeholder for Day 4+.'})
