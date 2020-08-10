from rest_framework import viewsets
from .models import Rating
from .serializers import RatingSerializer
from rest_framework.permissions import IsAuthenticated
from middlewares.authentication import AuthenticationJWT


class RatingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AuthenticationJWT]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
