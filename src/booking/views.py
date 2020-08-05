from .models import Book
from .serializers import BookingSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from middlewares.permissions import IsOwner, IsOwnerOrPostOnly


class BookList(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsOwnerOrPostOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user)


class BookDetail(generics.RetrieveUpdateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Book.objects.filter(created_by=self.request.user)

