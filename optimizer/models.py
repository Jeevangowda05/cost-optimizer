from django.conf import settings
from django.db import models


class Recommendation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recommendations',
        null=True,
        blank=True,
    )
    resource_name = models.CharField(max_length=255)
    current_cost = models.DecimalField(max_digits=10, decimal_places=2)
    optimized_cost = models.DecimalField(max_digits=10, decimal_places=2)
    savings_percent = models.DecimalField(max_digits=5, decimal_places=2)
    recommendation_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.resource_name} - {self.savings_percent}% savings'
