from django.http import JsonResponse


def success_response(payload=None, status=200, message=None):
    payload = payload or {}
    body = {'success': True, 'data': payload}
    if message:
        body['message'] = message
    body.update(payload)
    return JsonResponse(body, status=status)


def error_response(status=400, error=None, code=None):
    messages = {
        400: 'Invalid request.',
        404: 'Resource not found.',
        405: 'Method not allowed.',
        500: 'Internal server error.',
        503: 'Service unavailable.',
    }
    error_message = error or messages.get(status, 'Request failed.')
    error_code = code or {
        400: 'invalid_request',
        404: 'not_found',
        405: 'method_not_allowed',
        500: 'internal_error',
        503: 'service_unavailable',
    }.get(status, 'request_failed')
    return JsonResponse({'success': False, 'error': error_message, 'code': error_code}, status=status)
