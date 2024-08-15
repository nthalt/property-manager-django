import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from properties.models import Property, PropertyImage, Location, Amenity
from dotenv import load_dotenv
import psycopg2


class Command(BaseCommand):
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
            amenities_string = str(hotel[6])
            amenities_list = re.findall(r'"(.*?)"|(\w+)', amenities_string)
            amenities_list = [item[0] if item[0] else item[1]
                              for item in amenities_list]

            for amenity_name in amenities_list:
                amenity_name = amenity_name.strip()
                if amenity_name:  # Check if amenity_name is not empty
                    amenity, _ = Amenity.objects.get_or_create(
                        name=amenity_name)
                    property.amenities.add(amenity)

            # Find the original image
            original_image_name = os.path.basename(hotel[8])
            scrapy_image_path = os.path.join(
                settings.BASE_DIR, '..', 'scrapy', 'hotel_scraper', original_image_name)

            if os.path.exists(scrapy_image_path):
                # Clean the filename after finding the image
                cleaned_image_name = clean_filename(original_image_name)

                # Save the image with the cleaned name
                with open(scrapy_image_path, 'rb') as f:
                    django_image = PropertyImage(property=property)
                    django_image.image.save(cleaned_image_name, File(f))
                    django_image.save()

        scrapy_cur.close()
        scrapy_conn.close()

        self.stdout.write(self.style.SUCCESS(
            'Successfully migrated data from Scrapy to Django'))
