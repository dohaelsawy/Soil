from rest_framework import serializers
from .models import Space

class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = '__all__'
        
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Space name cannot be empty.")
        
        existing_space = Space.objects.filter(name__iexact=value)
        if self.instance:
            existing_space = existing_space.exclude(pk=self.instance.pk)
        
        if existing_space.exists():
            raise serializers.ValidationError("A space with this name already exists.")
        
        return value
    
    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError("Capacity must be at least 1.")
        return value
    
    def validate_price_per_hour(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value