from django.http import JsonResponse


def predict_view(request):
    return JsonResponse({'message': 'ML prediction endpoint placeholder for Day 3.'})
