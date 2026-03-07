"""
Database models for predictions app.
"""
from django.db import models
from django.contrib.auth.models import User


class Prediction(models.Model):
    """
    Stores prediction history for each user.
    """
    DISEASE_CHOICES = [
        ('heart', 'Heart Disease'),
        ('lung', 'Lung Cancer'),
        ('diabetes', 'Diabetes'),
        ('parkinsons', 'Parkinsons Disease'),
        ('thyroid', 'Thyroid Disorder'),
    ]
    
    # User who made the prediction (nullable for anonymous predictions)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='predictions'
    )
    
    # Type of disease predicted
    disease_type = models.CharField(max_length=20, choices=DISEASE_CHOICES)
    
    # Store the input data as JSON
    input_data = models.JSONField(help_text="Input features used for prediction")
    
    # Prediction result
    prediction_result = models.CharField(max_length=100)
    
    # Confidence score (if available from model)
    confidence_score = models.FloatField(null=True, blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']  # Most recent first
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['disease_type']),
        ]
    
    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f"{user_str} - {self.get_disease_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"