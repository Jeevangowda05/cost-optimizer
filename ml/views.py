import csv
import json
from io import StringIO

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import CloudDataset


@login_required
def predict_view(request):
    return JsonResponse({'message': 'ML prediction endpoint placeholder for Day 3.'})


@login_required
@require_POST
def upload_dataset_view(request):
    try:
        records = _extract_records(request)
    except ValueError as exc:
        return JsonResponse({'error': str(exc)}, status=400)

    if not records:
        return JsonResponse({'error': 'No dataset records provided.'}, status=400)

    dataset_rows = []
    for record in records:
        try:
            dataset_rows.append(
                CloudDataset(
                    user=request.user,
                    cpu=float(record['cpu']),
                    memory=float(record['memory']),
                    cost=float(record['cost']),
                    tag=str(record['tag']).strip(),
                    cloud=str(record['cloud']).strip(),
                )
            )
        except (KeyError, TypeError, ValueError):
            return JsonResponse(
                {'error': 'Invalid dataset format. Required fields: cpu, memory, cost, tag, cloud.'},
                status=400,
            )

    with transaction.atomic():
        CloudDataset.objects.bulk_create(dataset_rows)

    return JsonResponse({'message': 'Dataset uploaded successfully.', 'count': len(dataset_rows)}, status=201)


def _extract_records(request):
    if request.content_type and 'application/json' in request.content_type:
        try:
            payload = json.loads(request.body.decode('utf-8') or '{}')
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError('Invalid JSON payload.') from exc

        if isinstance(payload, dict):
            records = payload.get('records')
        else:
            records = payload
        if not isinstance(records, list):
            raise ValueError('JSON payload must be a list or include a records list.')
        return records

    dataset_file = request.FILES.get('dataset')
    if not dataset_file:
        raise ValueError('Upload a dataset file or send JSON payload.')

    try:
        decoded_data = dataset_file.read().decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError('Dataset file must be UTF-8 encoded.') from exc

    if dataset_file.name.lower().endswith('.json'):
        try:
            records = json.loads(decoded_data)
        except json.JSONDecodeError as exc:
            raise ValueError('Invalid JSON file.') from exc
        if not isinstance(records, list):
            raise ValueError('JSON dataset file must contain a list of records.')
        return records

    if dataset_file.name.lower().endswith('.csv'):
        reader = csv.DictReader(StringIO(decoded_data))
        return list(reader)

    raise ValueError('Unsupported file format. Use CSV or JSON.')
