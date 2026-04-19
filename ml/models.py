from django.conf import settings
from django.db import models


class PredictionModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='predictions',
        null=True,
        blank=True,
    )
    input_data = models.JSONField(default=dict)
    prediction_result = models.JSONField(default=dict)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Prediction {self.id}'
