from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from middlewares.permissions import IsOwnerOrReadOnly


class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        review_id = self.request.query_params.get("review_id")
        return Comment.objects.filter(review_id=review_id)


class CommentDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(created_by=self.request.user)

