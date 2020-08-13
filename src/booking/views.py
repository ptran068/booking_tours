from .models import Book
from .serializers import BookingSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from middlewares.permissions import IsOwner, IsOwnerOrPostOnly
from rest_framework.permissions import IsAuthenticated
from tours.models import Tours
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPostOnly]

    def perform_create(self, serializer):
        tour_id = self.request.query_params.get('tour_id')
        serializer.save(created_by=self.request.user, tours_id=tour_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        start_date = request.data.get('start_date')
        tour_id = request.query_params.get('tour_id')
        tour = Tours.objects.filter(id=tour_id).first()
        books = Book.objects.filter(start_date=start_date).filter(tours_id=tour_id).filter(status=0)
        if len(books) < tour.limit_booking:
            serializer.is_valid(raise_exception=True)
            try:
                self.perform_create(serializer)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        tour_id = self.request.query_params.get('tour_id')
        if tour_id is not None:
            return self.queryset.filter(created_by=self.request.user, tours_id=tour_id)
        return self.queryset.filter(created_by=self.request.user)


class BookDetail(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
