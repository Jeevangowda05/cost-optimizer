from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from cloud_optimizer.request_utils import extract_float, extract_payload
from cloud_optimizer.response_utils import error_response, success_response

from .logic import generate_rightsizing_recommendations
from .models import Recommendation


@login_required
@require_POST
def recommendations_view(request):
    try:
        payload = extract_payload(request)
        cpu = extract_float(payload.get('cpu'), 'cpu')
        memory = extract_float(payload.get('memory'), 'memory')
        current_cost = extract_float(payload.get('current_cost', 0), 'current_cost')
    except ValueError:
        return error_response(status=400)

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
