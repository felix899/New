from django.core.management.base import BaseCommand
from sns.models import Package, Room, PackageType

class Command(BaseCommand):
    help = 'Investigate all Packages and their related objects'

    def get_folder_info(self, folder):
        if folder:
            return f"{folder.name} (ID: {folder.id})"
        return 'None'

    def handle(self, *args, **options):
        packages = Package.objects.all()

        for package in packages:
            self.stdout.write(self.style.SUCCESS(f"\nPackage: {package.name}"))
            self.stdout.write(f"Description: {package.description}")
            self.stdout.write(f"Package Type: {package.package_type.name}")

            # Image and media information
            self.stdout.write(f"Cover Photo: {'Yes' if package.cover_photo else 'No'}")
            self.stdout.write(f"Icon: {'Yes' if package.icon else 'No'}")
            self.stdout.write(f"Icon Label: {package.icon_label}")

            # Folder information with names and IDs
            self.stdout.write(f"Image Folder: {self.get_folder_info(package.image_folder)}")
            self.stdout.write(f"Video Folder: {self.get_folder_info(package.video_folder)}")
            self.stdout.write(f"Media Folder: {self.get_folder_info(package.media_folder)}")

            # Text fields
            self.stdout.write(f"Content: {package.content[:50]}...")  # First 50 characters
            self.stdout.write(f"Exclusions: {package.exclusions[:50]}...")
            self.stdout.write(f"Notes: {package.notes[:50]}...")
            self.stdout.write(f"Promotions: {package.promotions[:50]}...")
            self.stdout.write(f"Honeymoon Offer: {package.honeymoon_offer[:50]}...")

            # Related rooms
            rooms = package.rooms.all()
            self.stdout.write(f"\nRelated Rooms ({rooms.count()}):")
            for room in rooms:
                self.stdout.write(f"  - {room.name} (Category: {room.category.name if room.category else 'N/A'})")
                self.stdout.write(f"    Price: {room.price}, Extended Price: {room.extended_price}")
                self.stdout.write(f"    Valid Period: {room.valid_period}")
                self.stdout.write(f"    Notes: {room.notes[:50]}...")

            self.stdout.write("\n" + "-"*50)