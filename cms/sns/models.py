from django.db import models
from django.contrib.postgres.fields import DateRangeField
from filer.fields.image import FilerImageField
from filer.fields.folder import FilerFolderField

class PackageType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Package(models.Model):
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE, related_name='packages')
    name = models.CharField(max_length=100)
    description = models.TextField()
    def get_absolute_url(self):
        return reverse('package_detail', args=[str(self.id)])
    
    # Image and media-related fields
    cover_photo = FilerImageField(on_delete=models.SET_NULL, null=True, blank=True, related_name='package_cover')
    icon = models.ImageField(upload_to='package_icons/', null=True, blank=True)
    icon_label = models.CharField(max_length=50, blank=True)
    
    # Folder fields
    image_folder = FilerFolderField(on_delete=models.SET_NULL, null=True, blank=True, related_name='package_image_folders')
    video_folder = FilerFolderField(on_delete=models.SET_NULL, null=True, blank=True, related_name='package_video_folders')
    media_folder = FilerFolderField(on_delete=models.SET_NULL, null=True, blank=True, related_name='package_media_folders')
    
    # Text fields related to the package
    content = models.TextField()
    exclusions = models.TextField()
    notes = models.TextField()
    promotions = models.TextField()
    honeymoon_offer = models.TextField()

    def __str__(self):
        return self.name

class RoomCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Room(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    category = models.ForeignKey(RoomCategory, on_delete=models.SET_NULL, null=True, related_name='rooms')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField()
    extended_price = models.DecimalField(max_digits=10, decimal_places=2)
    valid_period = DateRangeField()

    def __str__(self):
        return f"{self.package.name} - {self.name}"