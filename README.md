# Amazon Clone

A full-featured e-commerce web application built with Flask that replicates core Amazon shopping functionality.

## Features

### Core Functionality
- **Product Catalog** - Browse 80+ products across 25+ categories
- **Shopping Cart** - Add/remove items, quantity management
- **User Authentication** - Sign in/sign out with session management
- **Product Search** - Search products across the catalog
- **Wishlist** - Save products for later
- **Order History** - Track past orders

### Multi-Language Support
- English (US)
- Spanish (Mexico)
- French (Canada)
- German (Germany)
- Japanese (Japan)

### Multi-Currency Support
- USD ($)
- INR (₹)
- EUR (€)
- JPY (¥)
- GBP (£)

## Categories

| Category | Description |
|----------|-------------|
| Laptops | Gaming, Business, Professional laptops |
| Watches | Analog, Digital, Luxury watches |
| Smartwatches | Fitness trackers, Smart wearables |
| Monitors | Gaming, Office monitors |
| Headphones | Wireless, Wired, ANC headphones |
| Smartphones | Latest smartphones |
| Gaming Components | CPUs, GPUs, Motherboards, RAM, SSDs |
| Gaming Peripherals | Keyboards, Mice, Headsets |
| Gaming Furniture | Gaming chairs, Desks |
| Fashion | Clothing, Footwear, Accessories |
| Home & Living | Furniture, Decor, Bedding |
| Kitchenware | Appliances, Cookware |
| Beauty & Personal Care | Skincare, Makeup |
| And more... | |

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS (via CDN)
- **Database**: In-memory (easily upgradable to SQLite/PostgreSQL)
- **Dependencies**: Flask, Jinja2, Werkzeug

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Himadryy/Amazon_Clone.git
cd Amazon_Clone
```

2. Create virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask jinja2 werkzeug
```

4. Run the application:
```bash
python amazon.py
```

5. Open your browser and visit:
```
http://127.0.0.1:5000
```

## Project Structure

```
Amazon_Clone/
├── amazon.py           # Main application (all-in-one)
├── static/             # Static assets (logos)
├── amazon_clone.db     # SQLite database (if used)
├── venv/               # Virtual environment
└── __pycache__/       # Python cache
```

## Usage

### Default Login
- Email: `user@example.com`
- Password: `password`

### Key Routes
| Route | Description |
|-------|-------------|
| `/` | Home page with products |
| `/search?query=<term>` | Search products |
| `/product/<id>` | Product details |
| `/cart` | Shopping cart |
| `/wishlist` | User wishlist |
| `/signin` | User login |
| `/orders` | Order history |

## Customization

### Adding Products
Edit the `products_list` in `amazon.py`:
```python
Product(
    "Product Name",
    99.99,
    "Description",
    "Category",
    ["image_url1", "image_url2"],
    rating=4.5,
    reviews=100,
    features=["Feature 1", "Feature 2"],
    specs={"Key": "Value"}
)
```

### Adding Languages
Add entries to the `TRANSLATIONS` dictionary in `amazon.py`.

## Screenshots

![Amazon Clone Screenshot](Screenshot%202025-11-23%20at%2012.47.24%20PM.png)

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
