from django.contrib.auth.decorators import login_required
import json

from django.views.decorators.http import require_POST

from cloud_optimizer.response_utils import error_response, success_response

from .logic import generate_rightsizing_recommendations
from .models import Recommendation


@login_required
@require_POST
def recommendations_view(request):
    try:
        payload = _extract_payload(request)
        cpu = _extract_float(payload.get('cpu'), 'cpu')
        memory = _extract_float(payload.get('memory'), 'memory')
        current_cost = _extract_float(payload.get('current_cost', 0), 'current_cost')
    except ValueError as exc:
        return error_response(str(exc), status=400)

    recommendations = generate_rightsizing_recommendations(cpu, memory, current_cost)

    for recommendation in recommendations:
        potential_savings = recommendation['potential_savings']
        Recommendation.objects.create(
            user=request.user,
            resource_name=recommendation['type'],
            current_cost=current_cost,
            optimized_cost=max(current_cost - potential_savings, 0),
            savings_percent=(potential_savings / current_cost * 100) if current_cost else 0,
            recommendation_text=recommendation['description'],
        )

    return success_response({'recommendations': recommendations})


def _extract_float(value, field_name):
    if value in (None, ''):
        raise ValueError(f'{field_name} is required.')
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f'{field_name} must be a number.') from exc
    if parsed < 0:
        raise ValueError(f'{field_name} must be non-negative.')
    return parsed


def _extract_payload(request):
    if request.content_type and 'application/json' in request.content_type:
        try:
            return json.loads(request.body.decode('utf-8') or '{}')
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError('Invalid JSON payload.') from exc
    return request.POST
