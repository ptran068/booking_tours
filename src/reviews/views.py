from rest_framework.generics import get_object_or_404
from files.models import File
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from middlewares.permissions import IsOwner
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['PUT'])
def like_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.like.filter(id=request.user.id).exists():
        review.like.remove(request.user)
    else:
        review.like.add(request.user)
    serializer = ReviewSerializer(review)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]

        if self.action in ['update', 'destroy']:
            return [IsOwner()]

        if self.action in ('create',):
            return [IsAuthenticated()]

    def retrieve(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(Review, pk=pk)
        obj.views += 1
        obj.save(update_fields=['views'])
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        images_id = self.request.data.get('images')
        images = []
        for image_id in images_id:
            image = File.objects.filter(id=image_id).first()
            if image is not None:
                images.append(image)

        serializer.save(created_by=self.request.user, images=images)

    def get_queryset(self):
        tours_id = self.request.query_params.get('tours_id')
        return Review.objects.all().filter(tours_id=tours_id)
