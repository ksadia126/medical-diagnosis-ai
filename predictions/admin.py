"""
Admin configuration for predictions app.
"""
from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    """
    Admin interface for viewing and managing predictions.
    """
    list_display = ['id', 'user', 'disease_type', 'prediction_result', 'created_at']
    list_filter = ['disease_type', 'created_at', 'prediction_result']
    search_fields = ['user__username', 'prediction_result']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Prediction Info', {
            'fields': ('disease_type', 'prediction_result', 'confidence_score')
        }),
        ('User Info', {
            'fields': ('user',)
        }),
        ('Technical Data', {
            'fields': ('input_data', 'created_at'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )
    
    def has_add_permission(self, request):
        """Don't allow manual creation of predictions through admin."""
        return False
