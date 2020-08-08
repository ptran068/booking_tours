from .models import Tours
from .serializers import ToursSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from middlewares.authentication import AuthenticationJWT
from middlewares.permission import MyUserPermissions
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from rest_framework import filters
from files.models import File

class ToursList(APIView):
    permission_classes = [AllowAny]
    serializer_class = ToursSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'address']

    def get(self, request, format=None):
        tours = Tours.objects.all().order_by('created_at')
        pagesize = int(settings.PAGESIZE)
        page_total = round(Tours.objects.all().count() / pagesize + 0.5)
        paginator = Paginator(tours, pagesize)
        page = request.GET.get("page", "1").isdigit() and int(request.GET.get("page", "1")) or 1
        try:
            paginated_querySet = paginator.page(page)
        except EmptyPage:
            paginated_querySet = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(paginated_querySet, many=True)
        content = {
            "page": page,
            "pagetotal": page_total,
            "listtours": serializer.data,
        }
        return Response(content)

class PostToursList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AuthenticationJWT]

    def post(self, request, format=None):
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