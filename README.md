# Property-Manager-Django

This is a django property manager application which fetches hotel informations from a Scrapy project database and stores the data into Django postgres database. Django admin can apply CRUD operations on the data. The admin panel provides the property, location, amenity, propertyImage models for visualizing and managing data.
For anyone interested, the Scrapy project can be found here [https://github.com/nthalt/scrapy](https://github.com/nthalt/scrapy). You need to run the scrapy project once for this project to run smoothly.

<!-- - [Description](#description) -->

- [Requirements](#requirements)
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Important Notes](#important-notes)
- [Database Schema](#database-schema)
  - [properties_property](#properties_property)
  - [properties_location](#properties_location)
  - [properties_amenity](#properties_amenity)
  - [properties_propertyimage](#properties_propertyimage)
- [Contributing](#contributing)

## Requirements

- Python 3 or higher
- PostgreSQL
- Django
- Run the scrapy project from here [https://github.com/nthalt/scrapy](https://github.com/nthalt/scrapy)

<!-- ## Description

Django application to store property information using django admin. -->

## Features

1. Uses Django Model(s) and migrations
2. Uses Django admin with proper authentication
3. Enables CRUD operations for all the models maintaining relationship from
   Django admin panel
4. Provides a Django CLI application to migrate all the data from
   Scrapy project database to Django
5. Uses postgres database
6. Uses Django ORM

## Setup and Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/nthalt/property-manager-django.git
   cd property-manager-django
   ```

   Make sure the django project and scrapy project are under the same parent directory. Please maintain the following directory structure otherwise scrapy data might not be fetched properly.

   ```bash
   .
   ├── scrapy/
   └── property-manager-django/
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate # On Windows use: venv\Scripts\activate
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a file named .env in the project root and add your PostgreSQL database connection details. Use .env.example as a reference.**

   ```bash
   cp .env.example .env
   ```

5. **Make sure Postgresql database engine is installed and running**

6. **Create the database for Django to store data**

   ```bash
   CREATE DATABASE your_django_db_name
   ```

<!-- 7. **Create the migration files**

   ```bash
   python manage.py makemigrations
   ``` -->

7.  **Apply the migrations to the database**

    ```bash
    python manage.py migrate
    ```

8.  **Migrate data from scrapy database**

    ```bash
    python manage.py sync_scrapy
    ```

9.  **Create an admin user**

    ```bash
    python manage.py createsuperuser
    ```

    Set your desired `Username`,`Email address` and`Password`.

10. **Start the django development server**

    ```bash
    python manage.py runserver
    ```

    The application can be viewed here : [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

### Important Notes:

- Please follow the directory structure mentioned in [Setup and Installation](#setup-and-installation). Scrapy and Django project should be under the same parent directory.
- Ensure that the database is created `CREATE DATABASE your_django_db_name`
- Ensure that you have activated the virtual environment before running the `pip install -r requirements.txt` command. This ensures that all dependencies are installed within the virtual environment and do not affect the global Python environment.

## Database Schema

### Properties

The database schema consists of the following main tables:

#### properties_property

| Column      | Type                     | Constraints                 |
| ----------- | ------------------------ | --------------------------- |
| property_id | integer                  | Primary Key, Auto-increment |
| title       | character varying(255)   | Not Null, Unique            |
| description | text                     |                             |
| create_date | timestamp with time zone | Not Null                    |
| update_date | timestamp with time zone | Not Null                    |

#### properties_amenity

| Column | Type                   | Constraints                 |
| ------ | ---------------------- | --------------------------- |
| id     | bigint                 | Primary Key, Auto-increment |
| name   | character varying(255) | Not Null, Unique            |

#### properties_location

| Column    | Type                   | Constraints                 |
| --------- | ---------------------- | --------------------------- |
| id        | bigint                 | Primary Key, Auto-increment |
| name      | character varying(255) | Not Null                    |
| type      | character varying(100) | Not Null                    |
| latitude  | double precision       |                             |
| longitude | double precision       |                             |

#### properties_propertyimage

| Column      | Type                   | Constraints                 |
| ----------- | ---------------------- | --------------------------- |
| id          | bigint                 | Primary Key, Auto-increment |
| image       | character varying(100) | Not Null                    |
| property_id | integer                | Not Null, Foreign Key       |

### Relationships

- A Property can have multiple PropertyImages (One-to-Many)
- Properties and Locations have a Many-to-Many relationship
- Properties and Amenities have a Many-to-Many relationship

### Indexing

- Unique constraints are in place for property titles and amenity names
- A composite unique index is created on location name, latitude, and longitude
- Foreign key relationships are established between the tables

### Auto-managed Fields

- `create_date` and `update_date` in the `properties_property` table are automatically managed timestamp fields

<!--
   a. property_id
   b. title
   c. description
   d. images (One to many)
   e. location (many to many)
      i. name
      ii. type (country, state, city)
      iii. latitude
      iv. longitude
   f. amenities (many to many)
      i. name
   g. create_date (datetime, auto insert)
   h. update_date (datetime, auto update)
-->

<details>
<summary>

## Contributing

</summary>

We welcome contributions to this project. To ensure a smooth collaboration, please follow these guidelines:

1. **Fork the Repository**: Start by forking the repository on GitHub.

2. **Clone the Repository**: Clone your forked repository to your local machine using:

   ```bash
   git clone https://github.com/username/property-manager-django.git
   ```

3. **Create a Branch**: Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature-or-bugfix-description
   ```

4. **Make Changes**: Implement your changes in the codebase. Ensure your code adheres to the project's coding standards and includes appropriate tests.

5. **Commit Changes**: Commit your changes with a clear and descriptive commit message:

   ```bash
   git add .
   git commit -m "Description of the feature or bug fix"
   ```

6. **Push to GitHub**: Push your branch to your forked repository on GitHub:

   ```bash
   git push origin feature-or-bugfix-description
   ```

7. **Create a Pull Request**: Go to the original repository on GitHub and create a pull request. Provide a clear and detailed description of your changes.

8. **Review Process**: Wait for the project maintainers to review your pull request. Be prepared to make any necessary changes based on feedback.

Thank you for your contributions! Your help is greatly appreciated.

</details>
