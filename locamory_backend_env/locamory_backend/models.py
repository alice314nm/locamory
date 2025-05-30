from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


'''
    The model for memory that stores:
    - title
    - description
    - date (when the event happened for user)
    - latitude
    - longitude
'''
class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    title = models.CharField(max_length=60)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        default=0.0,
        help_text="Latitude coordinate"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=0.0,
        help_text="Longitude coordinate"
    )
    
    def __str__(self):
        return self.title

    

'''
    The model for Images:
    - memory (the memory id in the DB)
    - image (the image itself)
'''
class MemoryImage(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='memory_images/')