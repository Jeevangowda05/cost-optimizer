from django.http import JsonResponse


def success_response(payload, status=200):
    body = {'success': True}
    body.update(payload)
    return JsonResponse(body, status=status)


def error_response(message, status=400):
    return JsonResponse({'success': False, 'error': message}, status=status)
