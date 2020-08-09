from .models import Book
from .serializers import BookingSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from middlewares.permissions import IsOwner, IsOwnerOrPostOnly
from rest_framework.permissions import IsAuthenticated


class BookList(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPostOnly]

    def perform_create(self, serializer):
        tour_id = self.request.query_params.get('tour_id')
        serializer.save(created_by=self.request.user, tours_id=tour_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user)


class BookDetail(generics.RetrieveUpdateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user)
