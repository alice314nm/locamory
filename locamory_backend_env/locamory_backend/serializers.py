from rest_framework import serializers
from .models import Memory, MemoryImage

class MemoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryImage
        fields = ('id', 'image')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url
        return representation

class MemorySerializer(serializers.ModelSerializer):
    images = MemoryImageSerializer(many=True, read_only=True)
    location = serializers.SerializerMethodField()
    
    class Meta:
        model = Memory
        fields = ('id', 'title', 'description', 'date', 'latitude', 'longitude', 'location', 'images')
        read_only_fields = ('id',)
    
    def get_location(self, obj):
        return {
            'latitude': float(obj.latitude),
            'longitude': float(obj.longitude)
        }
    
    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES

        memory = Memory.objects.create(user=request.user, **validated_data)

        for image_data in images_data.getlist('images'):
            MemoryImage.objects.create(memory=memory, image=image_data)

        return memory
