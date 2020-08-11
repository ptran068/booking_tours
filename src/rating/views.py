from django.http import Http404
from .models import Rating
from rest_framework.response import Response
from .serializers import RatingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from middlewares.authentication import AuthenticationJWT
from rest_framework.views import APIView
from rest_framework import status

class RatingList(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, format=True):
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostRating(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AuthenticationJWT]
    ratings = Rating.objects.all()

    def post(self, request, format=True):
        serializer = RatingSerializer(data=request.data)
        tour_id_id = self.request.query_params.get('tour_id')
        if serializer.is_valid():
            serializer.save(user_id=request.user, tour_id_id=tour_id_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PutRating(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AuthenticationJWT]

    def get_object(self, pk):
        try:
            return Rating.objects.get(pk=pk)
        except Rating.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        rating = self.get_object(pk)
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
