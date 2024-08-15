# Setup and Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/nthalt/django-project.git
   cd django-project
   ```

2. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**:

   ```bash
   source venv/bin/activate # On Windows use: venv\Scripts\activate
   ```

4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Make sure Postgresql database engine is installed and running.**

6. **Create the database**

   ```bash
   CREATE DATABASE your_db_name
   ```

7. **Create the migration files**

   ```bash
   python manage.py makemigrations
   ```

8. **Apply the migrations to the database**

   ```bash
   python manage.py migrate
   ```

9. **Migrate data from scrapy database**
   ```bash
   python manage.py sync_scrapy
   ```

### Important Notes:

- Ensure that you have activated the virtual environment before running the `pip install -r requirements.txt` command. This ensures that all dependencies are installed within the virtual environment and do not affect the global Python environment.
