# Amazon-like Store - Django E-commerce Application

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

A modern e-commerce web application built with Django that provides an Amazon-style product browsing and management experience.

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Application Architecture](#application-architecture)
- [Configuration](#configuration)
- [Development](#development)
- [Production Deployment](#production-deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

- **Product Catalog**: Browse products with images, descriptions, and pricing
- **Admin Interface**: Easy product management through Django admin
- **Responsive Design**: Amazon-inspired UI with clean, professional styling
- **Product Management**: Add, edit, and manage product inventory
- **Database Integration**: SQLite database for product storage
- **Image Support**: Product image uploads and display

## Screenshots

### Main Store Interface
The customer-facing product catalog with a clean, Amazon-inspired design:

![Main Store Page](https://github.com/user-attachments/assets/4cb85538-8dd5-47a3-82e5-441ebcfdab83)

*Store interface displaying products in a responsive grid layout with pricing and stock information*

### Django Admin Dashboard
Powerful admin interface for managing products, users, and store settings:

> 📸 **Note:** Screenshots of the admin dashboard and product management forms are available in the `/tmp/playwright-mcp-output/` directory after running the application. Upload these to GitHub Issues/PR attachments and replace these placeholder URLs:
> - `admin-dashboard.png` - Django admin interface
> - `admin-add-product.png` - Product creation form

<!--
Placeholder for admin dashboard screenshot:
![Admin Dashboard](URL_TO_BE_REPLACED)
*Django admin dashboard showing product management capabilities*

Placeholder for product form screenshot:
![Add Product Form](URL_TO_BE_REPLACED)
*Product creation form with fields for name, description, price, stock, and image upload*
-->

## Technologies Used

### Backend
- **🐍 Python 3.8+** - Programming language
- **🌐 Django 5.1.6** - Web framework
- **🗄️ SQLite** - Database (development)
- **📷 Pillow** - Image processing

### Frontend  
- **🎨 HTML5 & CSS3** - Structure and styling
- **📱 Responsive Design** - Mobile-friendly layout
- **🎯 Amazon-inspired UI** - Professional e-commerce styling

### Development Tools
- **🔧 Django Admin** - Content management interface
- **🗃️ Django Migrations** - Database schema management
- **🧪 Django Testing Framework** - Built-in testing capabilities

## Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)

## Installation

Follow these steps to get the Amazon-like Store running on your local machine:

### 📥 1. Clone the Repository
```bash
git clone https://github.com/Data-Science-Intech/sonar-to-copilot-try.git
cd sonar-to-copilot-try
```

### 📦 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Django==5.1.6 Pillow
```

### 🗄️ 3. Set Up Database
Apply database migrations to create the necessary tables:
```bash
python manage.py migrate
```

### 👤 4. Create Admin User
**Option A: Interactive setup**
```bash
python manage.py createsuperuser
```

**Option B: Quick setup with default credentials**
```bash
python manage.py shell < set_admin_password.py
```
This creates an admin user with:
- **Username:** `admin`
- **Password:** `admin@123`

> ⚠️ **Security Note:** Change the default admin password in production environments

## Usage

### 🚀 Running the Development Server

1. **Start the Django development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application**
   - 🛍️ **Main store:** http://127.0.0.1:8000/
   - ⚙️ **Admin panel:** http://127.0.0.1:8000/admin/

### 📝 Managing Products

#### Adding Products via Admin Panel

1. Navigate to the admin panel at http://127.0.0.1:8000/admin/
2. Log in with your admin credentials
3. Click on **"Products"** under the **"STORE"** section
4. Click **"Add Product"** to create new products
5. Fill in product details:
   - **Name:** Product title
   - **Description:** Detailed product description
   - **Price:** Product price in dollars
   - **Stock quantity:** Available inventory count
   - **Product image:** Upload product image (optional)

#### Product Display Features

- ✅ **Grid Layout:** Products displayed in responsive card layout
- 💰 **Pricing:** Clear price display with currency formatting
- 📦 **Stock Levels:** Real-time inventory tracking
- 🖼️ **Images:** Support for product images with fallback placeholders
- 📱 **Responsive:** Optimized for desktop and mobile viewing

### 🎯 Quick Start Guide

1. **Install and setup** (see Installation section above)
2. **Start the server:** `python manage.py runserver`
3. **Add products:** Visit admin panel and create some products
4. **Browse store:** Visit main page to see your products
5. **Customize:** Modify templates and styles as needed

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

## Application Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   Web Browser   │    │   Web Browser   │
│   (Customer)    │    │   (Admin)       │    │   (Developer)   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │ HTTP Requests        │ HTTP Requests        │ Management
          │                      │                      │ Commands
          ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Django Web Server                            │
│                   (python manage.py runserver)                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      URL Router                                 │
│  ┌─────────────────┐              ┌─────────────────┐           │
│  │    Store App    │              │   Admin Panel   │           │
│  │   /store/       │              │    /admin/      │           │
│  └─────────────────┘              └─────────────────┘           │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Views Layer                              │
│  ┌─────────────────┐              ┌─────────────────┐           │
│  │ product_list()  │              │ Django Admin    │           │
│  │    Views        │              │    Interface    │           │
│  └─────────────────┘              └─────────────────┘           │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Models Layer                              │
│                 ┌─────────────────┐                             │
│                 │ Product Model   │                             │
│                 │ - name          │                             │
│                 │ - description   │                             │
│                 │ - price         │                             │
│                 │ - image         │                             │
│                 │ - stock         │                             │
│                 └─────────────────┘                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SQLite Database                             │
│                      (db.sqlite3)                              │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components:

- **🌐 Frontend:** Amazon-inspired responsive web interface
- **⚙️ Backend:** Django framework with MVT (Model-View-Template) architecture  
- **🗄️ Database:** SQLite for development (easily replaceable with PostgreSQL/MySQL)
- **👨‍💼 Admin:** Built-in Django admin interface for content management
- **📱 Templates:** Responsive HTML templates with CSS styling

## Configuration

### 🗄️ Database Configuration

The application uses **SQLite** by default for easy setup and development:

- **Database file:** `db.sqlite3` (included in repository)
- **Pre-configured with:** Admin user setup and Product model migrations
- **Contains:** Sample data and database schema

### ⚙️ Application Settings

Key configuration files:

**📁 `try_cursor/settings.py`** - Main Django configuration:
- Database configuration (SQLite)
- Static files handling 
- Installed apps including the `store` app
- Debug mode (enabled for development)
- Security settings

### 📁 Media File Handling

Product images are stored in:
- **Upload directory:** `products/` 
- **Development:** Files stored locally
- **Production note:** Configure proper media file handling for deployment

### 🔧 Environment Variables

For production deployment, consider setting:
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

> 💡 **Tip:** Use environment variables for sensitive configuration in production

## Development

### 🛠️ Adding New Features

**1. Create Models** (`store/models.py`)
```bash
# Add your model classes here
```

**2. Generate and Apply Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**3. Create Views** (`store/views.py`)
```bash
# Add your view functions here
```

**4. Configure URLs** (`store/urls.py`)
```bash
# Add URL patterns for your views
```

**5. Design Templates** (`store/templates/store/`)
```bash
# Create HTML templates for your views
```

### 🧪 Testing

Run the Django test suite:
```bash
python manage.py test
```

### 🔧 Development Tools

**Useful Django Commands:**
```bash
# Create superuser
python manage.py createsuperuser

# Check for issues
python manage.py check

# Collect static files
python manage.py collectstatic

# Open Django shell
python manage.py shell

# Show migrations
python manage.py showmigrations
```

### 📝 Code Style

- Follow **PEP 8** Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep views simple and logic in models when possible

## Production Deployment

### 🚀 Production Checklist

**Security & Configuration:**
- [ ] Set `DEBUG = False` in settings
- [ ] Configure secure `SECRET_KEY`
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Use environment variables for sensitive data

**Database:**
- [ ] Migrate from SQLite to PostgreSQL/MySQL
- [ ] Configure database connection pooling
- [ ] Set up database backups

**Static & Media Files:**
- [ ] Configure static file serving (Nginx/Apache)
- [ ] Set up media file handling and storage
- [ ] Consider CDN for static assets

**Application Server:**
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Configure proper logging
- [ ] Set up process monitoring

**Infrastructure:**
- [ ] Configure reverse proxy (Nginx)
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall and security groups
- [ ] Set up monitoring and alerting

### 🐳 Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "try_cursor.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### ☁️ Cloud Deployment

**Popular platforms:**
- **Heroku:** Easy deployment with git push
- **AWS Elastic Beanstalk:** Managed Django hosting
- **DigitalOcean App Platform:** Simple container deployment
- **Railway:** Modern deployment platform

## Contributing

We welcome contributions! Please follow these steps:

### 🤝 How to Contribute

1. **🍴 Fork the repository**
2. **🌿 Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **💻 Make your changes**
4. **✅ Test your changes**
   ```bash
   python manage.py test
   ```
5. **📝 Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **📤 Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **🔄 Submit a pull request**

### 📋 Development Guidelines

- Follow PEP 8 coding standards
- Add tests for new features
- Update documentation as needed
- Keep commit messages clear and descriptive

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.