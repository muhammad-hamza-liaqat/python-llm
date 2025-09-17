# Django Project README

## Table of Contents
- [Project Description](#project-description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Project Description
This is a complete Python Django project template designed to serve as a starting point for web applications. It includes Django's built-in authentication system, admin interface, and basic URL routing. The project follows Django best practices and is structured for scalability.

Key features:
- LLM Model Training
- Admin panel for data management

## Requirements
- Python 3.8 or higher
- Django 4.2 or higher
- PostgreSQL (recommended) or SQLite for development
- Redis (optional, for caching)

## Installation
1. **Clone the Repository**
   ```bash
   git clone git@github.com:muhammad-hamza-liaqat/python-llm.git
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   `requirements.txt` file is laready available, with all the packages used in this project
   ```
   Django>=4.2.0
   ```

   Then install:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to include your settings:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3  # Or PostgreSQL URL
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

## Usage
1. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

3. **Run the Development Server**
   See [Running the Application](#running-the-application) section.

4. **Access the Admin Panel**
   Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

## Configuration
### Database
- For development, SQLite is used by default.
- For production, configure PostgreSQL in `settings.py`:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': os.environ.get('DB_NAME'),
          'USER': os.environ.get('DB_USER'),
          'PASSWORD': os.environ.get('DB_PASSWORD'),
          'HOST': os.environ.get('DB_HOST'),
          'PORT': os.environ.get('DB_PORT'),
      }
  }
  ```

### Static Files
Collect static files for production:
```bash
python manage.py collectstatic
```

### Logging
Django logging is configured in `settings.py`. Logs are output to console by default. For production, adjust to file-based logging.

## Running the Application
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

To run on a specific host/port:
```bash
python manage.py runserver 0.0.0.0:8000
```

## Testing
Run the test suite:
```bash
python manage.py test
```

To run tests for a specific app:
```bash
python manage.py test myapp
```

Ensure tests pass before committing changes.

## Deployment
1. **Prepare for Production**
   - Set `DEBUG = False` in `settings.py`.
   - Configure `ALLOWED_HOSTS`.
   - Run `python manage.py collectstatic`.

2. **Deploy with Gunicorn and Nginx**
   Install Gunicorn:
   ```bash
   pip install gunicorn
   ```
   Run with Gunicorn:
   ```bash
   gunicorn yourproject.wsgi:application --bind 0.0.0.0:8000
   ```

3. **Use a Platform like Heroku, DigitalOcean, or AWS**
   - For Heroku: Create a `Procfile` with `web: gunicorn yourproject.wsgi`.
   - Set environment variables via the platform's dashboard.

4. **Database**
   - Migrate the database on the server: `python manage.py migrate`.

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/new-feature`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Open a Pull Request.

Please ensure code follows PEP 8 style guidelines and includes tests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For questions or issues, open a GitHub issue or contact the maintainer.

Last updated: September 17, 2025