from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Space
from .serializers import SpaceSerializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAdminUser
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


    def retrieve(self, request, pk=None):
        try:
            user = get_object_or_404(Space, pk=pk)
            serializer = SpaceSerializer(user)
            return Response(serializer.data)
        except Http404:
            return Response(
                {'error': "The requested Space does not exist."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request):
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
            partial=True
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
        
    def destroy(self,request, pk=None) :
        try:
            instance = self.get_object()
            instance.delete()
            return Response(
                {"message": "Space deleted successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "The requested Space does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )



    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="type", 
                type=OpenApiTypes.STR, 
                description="Filter spaces by type (e.g., 'meeting_room')"
            ),
            OpenApiParameter(
                name="min_capacity", 
                type=OpenApiTypes.INT, 
                description="Filter spaces with a minimum capacity"
            ),
            OpenApiParameter(
                name="max_price", 
                type=OpenApiTypes.FLOAT, 
                description="Filter spaces within a maximum price range"
            ),
        ],
        responses={200: SpaceSerializer(many=True)},
    )

    @method_decorator(ratelimit(key='ip', rate='5/m', method='GET', block=False))
    def list(self, request, *args, **kwargs):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return Response(
                {"error": "Too many requests. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        space_type = request.query_params.get('type', None)
        min_capacity = request.query_params.get('min_capacity', None)
        max_price = request.query_params.get('max_price', None)


        queryset = Space.objects.filter(is_available=True)

        if space_type:
            queryset = queryset.filter(type=space_type)
        if min_capacity:
            queryset = queryset.filter(capacity__gte=min_capacity)
        if max_price:
            queryset = queryset.filter(price_per_hour__lte=max_price)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Update is not permitted'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
