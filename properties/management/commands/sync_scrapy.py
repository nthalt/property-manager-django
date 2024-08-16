"""
fetches hotel information from database of 
scrapy project and stores data in a new postgres database.
"""
import os
import re
import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
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
            # Create or get Location
            location, _ = Location.objects.get_or_create(
                name=hotel[3],
                type='city',
                latitude=hotel[4],
                longitude=hotel[5]
            )

            # Create or get Property
            property, created = Property.objects.get_or_create(
                title=hotel[1],
                # Default description if creating new
                defaults={'description': ''}
            )

            if created:
                property.locations.add(location)

            # Parse and handle Amenities
            amenities_string = (hotel[6])
            # print(f"Raw amenities string: {amenities_string}")
            for amenity_name in amenities_string:
                if amenity_name:  # Check if amenity_name is not empty
                    amenity, _ = Amenity.objects.get_or_create(
                        name=amenity_name)
                    # print(amenity)
                    property.amenities.add(amenity)

            # Find the original image
            original_image_name = os.path.basename(hotel[8])
            # print(f"hotel [8] path: {hotel[8]}")
            # print(f"base dir: {settings.BASE_DIR}")
            scrapy_image_path = os.path.join(
                settings.BASE_DIR, '..', 'scrapy', 'hotel_scraper', 'images', original_image_name)
            # print(f"scrapy image path: {scrapy_image_path}")
            if os.path.exists(scrapy_image_path):
                # Clean the filename after finding the image
                cleaned_image_name = clean_filename(original_image_name)
                # print(f"cleaned image name: {cleaned_image_name}")

                existing_images = PropertyImage.objects.filter(
                    property=property)

                if not existing_images.exists():
                    # Save the image with the cleaned name
                    with open(scrapy_image_path, 'rb') as f:
                        django_image = PropertyImage(property=property)
                        django_image.image.save(
                            cleaned_image_name, ContentFile(f.read()), save=True)
                    print(f"Saved new image: {cleaned_image_name}")
                    # with open(scrapy_image_path, 'rb') as f:
                    #     django_image = PropertyImage(property=property)
                    #     django_image.image.save(cleaned_image_name, File(f))
                    #     django_image.save()
                else:
                    print(
                        f"Image already exists for property: {property.title}")
            else:
                print(f"Image file not found: {scrapy_image_path}")

        scrapy_cur.close()
        scrapy_conn.close()

        self.stdout.write(self.style.SUCCESS(
            'Successfully migrated data from Scrapy to Django'))
