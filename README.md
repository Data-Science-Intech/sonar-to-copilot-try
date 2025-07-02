# Amazon-like Store - Django E-commerce Application

A modern e-commerce web application built with Django that provides an Amazon-style product browsing and management experience.

## Features

- **Product Catalog**: Browse products with images, descriptions, and pricing
- **Admin Interface**: Easy product management through Django admin
- **Responsive Design**: Amazon-inspired UI with clean, professional styling
- **Product Management**: Add, edit, and manage product inventory
- **Database Integration**: SQLite database for product storage
- **Image Support**: Product image uploads and display

## Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Data-Science-Intech/sonar-to-copilot-try.git
   cd sonar-to-copilot-try
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install Django==5.1.6 Pillow
   ```

3. **Apply database migrations** (if needed)
   ```bash
   python manage.py migrate
   ```

4. **Set up admin user** (optional, for admin panel access)
   ```bash
   python manage.py createsuperuser
   ```
   
   Or use the provided script to set up admin user with default credentials:
   ```bash
   python manage.py shell < set_admin_password.py
   ```
   This creates an admin user with:
   - Username: `admin`
   - Password: `admin@123`

## Usage

### Running the Development Server

1. **Start the Django development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application**
   - Main store: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

### Adding Products

1. Navigate to the admin panel at http://127.0.0.1:8000/admin/
2. Log in with your admin credentials
3. Click on "Products" under the "STORE" section
4. Click "Add Product" to create new products
5. Fill in product details:
   - Name
   - Description
   - Price
   - Stock quantity
   - Product image (optional)

### Viewing Products

- Visit the main page at http://127.0.0.1:8000/ to see all products
- Products are displayed in a grid layout with images, names, descriptions, and prices
- Stock levels are shown for each product

## Project Structure

```
sonar-to-copilot-try/
├── manage.py              # Django management script
├── db.sqlite3            # SQLite database file
├── set_admin_password.py # Script to set admin password
├── try_cursor/           # Main Django project directory
│   ├── __init__.py
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   ├── wsgi.py          # WSGI application
│   └── asgi.py          # ASGI application
└── store/               # Store Django app
    ├── __init__.py
    ├── admin.py         # Admin interface configuration
    ├── apps.py          # App configuration
    ├── models.py        # Product model definition
    ├── views.py         # View functions
    ├── urls.py          # App URL patterns
    ├── tests.py         # Test cases
    ├── migrations/      # Database migrations
    └── templates/       # HTML templates
        └── store/
            └── product_list.html  # Main product listing page
```

## Configuration

### Database

The application uses SQLite by default. The database file (`db.sqlite3`) is included and pre-configured with:
- Admin user setup
- Product model migrations
- Sample data (if any)

### Settings

Key settings are located in `try_cursor/settings.py`:
- Database configuration
- Static files handling
- Installed apps including the `store` app
- Debug mode (enabled for development)

### Media Files

Product images are uploaded to the `products/` directory. Make sure your deployment environment has proper media file handling configured for production use.

## Development

### Adding New Features

1. Create new models in `store/models.py`
2. Create and apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Add views in `store/views.py`
4. Configure URLs in `store/urls.py`
5. Create templates in `store/templates/store/`

### Testing

Run the Django test suite:
```bash
python manage.py test
```

## Production Deployment

For production deployment, consider:

1. Set `DEBUG = False` in settings
2. Configure a production database (PostgreSQL, MySQL)
3. Set up proper static file serving
4. Configure media file handling
5. Use a production WSGI server like Gunicorn
6. Set up proper security settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.