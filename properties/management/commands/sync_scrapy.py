"""
fetches hotel information from database of 
scrapy project and stores data in a new postgres database.
"""
import os
import re
import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import IntegrityError
from dotenv import load_dotenv
from properties.models import Property, PropertyImage, Location, Amenity


class Command(BaseCommand):
    """
    fetches data from scrapy project database and stores in a new postgres database
    """
    help = 'Migrate data from Scrapy database to Django database'

    def handle(self, *args, **options):
        load_dotenv()
        # Connect to Scrapy database
        scrapy_conn = psycopg2.connect(
            dbname=os.getenv('SCRAPY_DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        scrapy_cur = scrapy_conn.cursor()

        # Fetch data from Scrapy database
        scrapy_cur.execute("SELECT * FROM hotels")
        hotels = scrapy_cur.fetchall()

        def clean_filename(filename):
            # Remove invalid characters and convert to lowercase
            filename, ext = os.path.splitext(filename)
            filename = re.sub(r'[^a-zA-Z0-9]', '_', filename).lower()
            return f"{filename}{ext}"

        for hotel in hotels:
            # Handle Location (with duplicate check based on name, latitude, and longitude)
            location_name = hotel[3]
            latitude = hotel[4] if hotel[4] else None
            longitude = hotel[5] if hotel[5] else None

            location, created = Location.objects.get_or_create(
                name=location_name,
                latitude=latitude,
                longitude=longitude,
                defaults={'type': 'city'}
            )

            # Handle Property
            property, created = Property.objects.get_or_create(
                title=hotel[1],
                defaults={'description': ''}
            )

            if created:
                property.locations.add(location)

            # Handle Amenities (with duplicate check)
            amenities_string = hotel[6]
            for amenity_name in amenities_string:
                if amenity_name:
                    try:
                        amenity, _ = Amenity.objects.get_or_create(
                            name=amenity_name)
                        property.amenities.add(amenity)
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(
                            f"Duplicate amenity found: {amenity_name}"))

            # Handle Images
            original_image_name = os.path.basename(hotel[8])
            scrapy_image_path = os.path.join(
                settings.BASE_DIR, '..', 'scrapy', 'hotel_scraper', 'images', original_image_name)

            if os.path.exists(scrapy_image_path):
                cleaned_image_name = clean_filename(original_image_name)
                existing_images = PropertyImage.objects.filter(
                    property=property)

                if not existing_images.exists():
                    with open(scrapy_image_path, 'rb') as f:
                        django_image = PropertyImage(property=property)
                        django_image.image.save(
                            cleaned_image_name, ContentFile(f.read()), save=True)
                    print(f"Saved new image: {cleaned_image_name}")
                else:
                    print(
                        f"Image already exists for property: {property.title}")
            else:
                print(f"Image file not found: {scrapy_image_path}")

        scrapy_cur.close()
        scrapy_conn.close()

        self.stdout.write(self.style.SUCCESS(
            'Successfully migrated data from Scrapy to Django'))
