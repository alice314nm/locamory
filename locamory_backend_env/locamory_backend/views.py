from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Memory, MemoryImage
from .serializers import MemorySerializer, MemoryImageSerializer

class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['date']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'title']
    ordering = ['-date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Memory.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def upload_images(self, request, pk=None):
        memory = self.get_object()
        images = request.FILES.getlist('images')
        for image in images:
            MemoryImage.objects.create(memory=memory, image=image)
        return Response({'status': 'images uploaded'}, status=status.HTTP_201_CREATED)

        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = float(request.query_params.get('radius', 10))  # default 10 km

        if not lat or not lng:
            return Response({'error': 'Missing lat or lng'}, status=status.HTTP_400_BAD_REQUEST)

        lat, lng = float(lat), float(lng)

        def haversine(lat1, lon1, lat2, lon2):
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * asin(sqrt(a))
            return 6371 * c  # Earth radius in km

        nearby_memories = [
            m for m in self.get_queryset()
            if haversine(lat, lng, float(m.latitude), float(m.longitude)) <= radius
        ]

        serializer = self.get_serializer(nearby_memories, many=True)
        return Response(serializer.data)

class MemoryImageViewSet(viewsets.ModelViewSet):
    serializer_class = MemoryImageSerializer

    def get_queryset(self):
        queryset = MemoryImage.objects.all()
        memory_id = self.request.query_params.get('memory_id')
        if memory_id:
            queryset = queryset.filter(memory_id=memory_id)
        return queryset
