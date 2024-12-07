from rest_framework import serializers
from .models import Bookings
from django.contrib.auth.models import User
from spaces.models import Space


class BookingsSerializer(serializers.ModelSerializer):

    space_id = serializers.PrimaryKeyRelatedField(
        queryset=Space.objects.all(), 
        write_only=True
    )

    class Meta:
        model = Bookings
        fields = ['username', 'user_email', 'space_id', 'start_time', 'end_time','status']
        extra_kwargs = {
            'status': {'read_only': True}
        }

    def validate(self, data):

        space = data['space_id']

        if not space.is_available:
            raise serializers.ValidationError({
                'space_id': "This space is currently not available for booking."
            })

        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time")

        overlapping_bookings = Bookings.objects.filter(
            space_id=space,
            status__in=['pending', 'confirmed'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time']
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This time slot is already booked")
        

        return data

    def create(self, validated_data):

        email = validated_data['user_email']
        username = validated_data['username']

        User.objects.get_or_create(
            username=username,
            email=email,
        )

        booking=Bookings.objects.create(
            username=username,
            user_email=email,
            space_id=validated_data['space_id'],
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time'],
            status='pending'
        )

        return booking


class BookingsPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ['status']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance