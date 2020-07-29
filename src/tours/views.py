from .models import Tours
from .serializers import ToursSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from middlewares.authentication import AuthenticationJWT

# Create your views here.

class ToursList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        snippets = Tours.objects.all()
        serializer = ToursSerializer(snippets, many=True)
        return Response(serializer.data)

class PostToursList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AuthenticationJWT]

    def post(self, request, format=None):
        serializer = ToursSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(createdBy=request.user)
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
        snippet = self.get_object(pk)
        serializer = ToursSerializer(snippet)
        return Response(serializer.data)

class EditToursListDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AuthenticationJWT]

    def get_object(self, pk):
        try:
            return Tours.objects.get(pk=pk)
        except Tours.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ToursSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
