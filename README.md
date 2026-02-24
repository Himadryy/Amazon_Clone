# Amazon Clone

A production-ready e-commerce web application built with Flask that replicates core Amazon shopping functionality. This project demonstrates professional software engineering practices suitable for portfolio demonstration and resume showcasing.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey?style=flat&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red?style=flat)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat&logo=docker)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-blue?style=flat&logo=github)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

## Features

### Core Functionality
- **Product Catalog** - Browse products across multiple categories
- **Shopping Cart** - Add/remove items, quantity management
- **User Authentication** - Secure sign in/sign up with Flask-Login
- **Product Search** - Search products across the catalog
- **Wishlist** - Save products for later
- **Order History** - Track past orders
- **REST API** - Full API endpoints for frontend integration

### Multi-Language Support
- English (US)
- Spanish (Mexico)
- French (Canada)
- German (Germany)
- Japanese (Japan)

### Multi-Currency Support
- USD ($), INR (₹), EUR (€), JPY (¥), GBP (£)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask 3.0 (Python 3.11+) |
| Database | SQLAlchemy 2.0 + SQLite |
| Authentication | Flask-Login |
| Frontend | HTML5, Tailwind CSS |
| Testing | pytest + coverage |
| Containerization | Docker |
| CI/CD | GitHub Actions |

## Project Structure

```
Amazon_Clone/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py             # SQLAlchemy ORM models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py           # Home, search, categories
│   │   ├── products.py       # Product details, wishlist
│   │   ├── cart.py           # Cart, checkout, orders
│   │   ├── auth.py           # Authentication routes
│   │   └── api.py            # REST API endpoints
│   ├── templates/            # Jinja2 templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── signin.html
│   │   ├── signup.html
│   │   └── ...
│   └── utils/
│       └── translations.py    # i18n translations
├── config.py                 # Configuration management
├── run.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Local development setup
├── pytest.ini               # Test configuration
├── tests/
│   └── test_routes.py       # Unit tests
├── .github/workflows/
│   └── ci.yml               # CI/CD pipeline
└── README.md
```

## Quick Start

### Option 1: Local Development

```bash
# Clone repository
git clone https://github.com/Himadryy/Amazon_Clone.git
cd Amazon_Clone

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py

# Open browser
http://127.0.0.1:5000
```

### Option 2: Docker

```bash
# Build and run with Docker
docker-compose up --build

# Or build manually
docker build -t amazon-clone .
docker run -p 5000:5000 amazon-clone
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | List all products (paginated) |
| GET | `/api/products/<id>` | Get product details |
| GET | `/api/products/search?q=<query>` | Search products |
| GET | `/api/categories` | List all categories |
| GET | `/api/cart` | Get user's cart |
| GET | `/api/orders` | Get user's orders |
| GET | `/api/health` | Health check |

## Testing

```bash
# Run tests with coverage
pytest tests/ -v --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment | `development` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `DATABASE_URL` | Database URI | `sqlite:///amazon_clone.db` |

## Default Login

- **Email:** `user@example.com`
- **Password:** `password`

## Key Routes

| Route | Description |
|-------|-------------|
| `/` | Home page with products |
| `/category/<name>` | Products by category |
| `/search?q=<query>` | Search products |
| `/product/<id>` | Product details |
| `/cart` | Shopping cart |
| `/auth/signin` | User login |
| `/auth/signup` | User registration |
| `/orders` | Order history |
| `/wishlist` | User wishlist |

## Professional Highlights

This project demonstrates:

- ✅ **Modular Architecture** - Clean separation of concerns with Flask blueprints
- ✅ **ORM Pattern** - SQLAlchemy for database operations
- ✅ **Authentication** - Secure user sessions with Flask-Login
- ✅ **RESTful API** - JSON endpoints for frontend integration
- ✅ **Containerization** - Docker for consistent deployment
- ✅ **Testing** - Unit tests with pytest
- ✅ **CI/CD** - GitHub Actions for automated testing
- ✅ **i18n** - Multi-language support
- ✅ **Configuration Management** - Environment-based settings

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for **educational purposes only**. It is not affiliated with, endorsed by, or connected to Amazon.com or any of its affiliates. All product names, logos, and brands are property of their respective owners.

## Author

- **Himadryy** - [GitHub](https://github.com/Himadryy)

## Acknowledgments

- Inspired by Amazon's e-commerce functionality
- Built with Flask web framework
- UI styled with Tailwind CSS
- Architecture inspired by Flask best practices
