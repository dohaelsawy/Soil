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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
        )
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response(serializer.data)
        except serializers.ValidationError as e:
            return Response(
                {'errors': e.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def destroy(self, request, *args, **kwargs):
        return Response(
            {'error': 'Deletion is not permitted'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )