from django.utils.timezone import now
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Bookings
from .serializers import BookingsSerializer, BookingsPatchSerializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAdminUser
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from django.core.mail import send_mail
import os

class BookingsViewSet(viewsets.ModelViewSet):
    queryset = Bookings.objects.all()

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == 'update':
            return BookingsPatchSerializer
        return BookingsSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @method_decorator(ratelimit(key='ip', rate='5/m', method='GET', block=False))
    def retrieve(self, request, pk=None):

        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return Response(
                {"error": "Too many requests. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        try:
            user = get_object_or_404(Bookings, pk=pk)
            serializer = BookingsSerializer(user)
            return Response(serializer.data)
        except Http404:
            return Response(
                {'error': "The requested booking does not exist."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except :
            return Response(
                {'errors': "unexpected error please try later :{"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=False))
    def create(self, request, *args, **kwargs):

        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return Response(
                {"error": "Too many requests. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            username=serializer.validated_data['username']
            space_type=serializer.validated_data['space_id'].type
            start_time=serializer.validated_data['start_time']
            end_time=serializer.validated_data['end_time']
            booking_status='Pending'
            to_email = serializer.validated_data['user_email']
            created_at=now()

            subject="Booking Pending - Your Reservation Details"
            message = mail_create_booking_content(username,space_type,start_time,end_time,created_at,booking_status)
            from_email=os.getenv('EMAIL_HOST_USER')
            send_booking_status_email(subject,from_email,to_email,message)

            self.perform_create(serializer)
            
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError as e:
            return Response(
                {'errors': e.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except :
            return Response(
                {'errors': "unexpected error please try later :{"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
        )
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            username=instance.username
            space_type=instance.space_id.type
            start_time=instance.start_time
            end_time=instance.end_time
            booking_status=instance.status
            to_email = instance.user_email
            created_at=now()

            subject=f"Booking {booking_status} - Your Reservation Details"
            message = mail_create_booking_content(username,space_type,start_time,end_time,created_at,booking_status)
            from_email=os.getenv('EMAIL_HOST_USER')
            send_booking_status_email(subject,from_email,to_email,message)
            
            return Response(serializer.data)
        except serializers.ValidationError as e:
            return Response(
                {'errors': e.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except :
            return Response(
                {'errors': "unexpected error please try later :{"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response(
            {'error': 'Deletion is not permitted'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Update is not permitted'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    

def send_booking_status_email(subject, from_email, to_email, message) :
    send_mail(
        subject,
        message,
        from_email,
        [to_email]
    )

def mail_create_booking_content(username, space_type, start_time, end_time, created_at, status) :
    return f"""
Dear {username},
Your booking has been successfully created and confirmed.
Booking Details:

Date of Booking: {created_at}
Booking Status: {status}

Your Reservation Specifics:

Space type: {space_type}
Start time: {start_time}
End time: {end_time}

What to Expect Next:

You will receive an update on your booking state with email, so please follow along :)

Thank you for choosing Soil workspace. We look forward to serving you!
Best regards,
Soil
"""
