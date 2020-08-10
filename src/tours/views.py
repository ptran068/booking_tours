from .models import Tours
from .serializers import ToursSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from middlewares.authentication import AuthenticationJWT
from middlewares.permission import MyUserPermissions
from rest_framework import filters
from files.models import File
from rest_framework.generics import ListAPIView

class ToursList(ListAPIView):
    queryset = Tours.objects.all().order_by('created_at')
    permission_classes = [AllowAny]
    serializer_class = ToursSerializer
    filterset_fields = ['title']
    ordering_fields = ['-created_at']


class PostToursList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AuthenticationJWT]

    def post(self, request, format=None):
        images_id = request.data.get('images')
        images = []
        for image_id in images_id:
            image = File.objects.filter(id=image_id).first()
            if image is not None:
                images.append(image)
        serializer = ToursSerializer(data=request.data)
        images_id = request.data.get('images')
        images = []
        for image_id in images_id:
            image = File.objects.filter(id=image_id).first()
            if image is not None:
                images.append(image)
        if serializer.is_valid():
            serializer.save(created_by=request.user, images=images)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ToursListDetail(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Tours.objects.get(pk=pk)
        except Tours.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tour = self.get_object(pk)
        tour.views +=1
        tour.save()
        serializer = ToursSerializer(tour)
        return Response(serializer.data)

class EditOrDeleteToursDetail(APIView):
    permission_classes = [MyUserPermissions]
    authentication_classes = [AuthenticationJWT]

    def get_object(self, pk):
        try:
            return Tours.objects.get(pk=pk)
        except Tours.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        tour = self.get_object(pk)
        serializer = ToursSerializer(tour, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tour = self.get_object(pk)
        tour.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)