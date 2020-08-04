from .models import Categories
from .serializers import CategoriSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from middlewares.authentication import AuthenticationJWT

class CategoryList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        categories = Categories.objects.all()
        serializer = CategoriSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostCategoryList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AuthenticationJWT]

    def post(self, request, format=None):
        serializer = CategoriSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

