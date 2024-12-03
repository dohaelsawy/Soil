from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Space
from .serializers import SpaceSerializer

class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer

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

    def update(self, request, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=partial
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
        
    def destroy(self) :
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Space deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


    @action(detail=False, methods=['GET'])
    def available_spaces(self):
        available_spaces = Space.objects.filter(availability=True)
        serializer = self.get_serializer(available_spaces, many=True)
        return Response(serializer.data)
