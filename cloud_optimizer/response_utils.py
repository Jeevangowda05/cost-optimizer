from django.http import JsonResponse


def success_response(payload, status=200):
    body = {'success': True}
    body.update(payload)
    return JsonResponse(body, status=status)


def error_response(status=400):
    messages = {
        400: 'Invalid request.',
        500: 'Internal server error.',
        503: 'Service unavailable.',
    }
    return JsonResponse({'success': False, 'error': messages.get(status, 'Request failed.')}, status=status)
