import os
from app import create_app, db
from app.models import User, Product
import uuid

app = create_app(os.environ.get("FLASK_ENV", "development"))


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Product": Product}


def init_db():
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email="user@example.com").first():
            user = User(
                id=str(uuid.uuid4()),
                email="user@example.com",
                name="Test User",
            )
            user.set_password("password")
            db.session.add(user)

        if Product.query.count() == 0:
            products = [
                Product(
                    id=str(uuid.uuid4()),
                    name="HP Victus 15-fb3004AX",
                    price=599.99,
                    description="A powerful gaming laptop for entry-level gamers.",
                    category="Laptops",
                    image_urls="https://placehold.co/600x400/1a1a1a/ffffff?text=Victus+1",
                    rating=4.5,
                    reviews=120,
                    features="AMD Ryzen 5 8645HS|NVIDIA RTX 2050|16GB DDR5|512GB SSD|144Hz Display",
                    specs="Brand: HP|Screen: 15.6 inches|CPU: AMD Ryzen 5|RAM: 16GB",
                ),
                Product(
                    id=str(uuid.uuid4()),
                    name="Apple MacBook Air M2",
                    price=1199.00,
                    description="The incredibly capable laptop that lets you work, play or create anywhere.",
                    category="Laptops",
                    image_urls="https://placehold.co/600x400/e0e0e0/000000?text=MacBook+Air",
                    rating=4.9,
                    reviews=1500,
                    features="M2 Chip|13.6-inch Retina|8GB RAM|256GB SSD|18hr Battery",
                    specs="Brand: Apple|Screen: 13.6 inches|CPU: Apple M2|RAM: 8GB",
                ),
                Product(
                    id=str(uuid.uuid4()),
                    name="Casio MRW-200H",
                    price=45.00,
                    description="A robust analog watch with 100m water resistance.",
                    category="Watches",
                    image_urls="https://placehold.co/600x400/111111/ffffff?text=Casio+Sport",
                    rating=4.6,
                    reviews=15000,
                    features="100M Water Resistance|Bi-directional bezel|Day-date display|Luminous hands",
                    specs="Brand: Casio|Movement: Quartz|Water Resistance: 100m",
                ),
                Product(
                    id=str(uuid.uuid4()),
                    name="Samsung Galaxy S24 Ultra",
                    price=1299.00,
                    description="The ultimate smartphone with AI features.",
                    category="Smartphones",
                    image_urls="https://placehold.co/600x400/222222/ffffff?text=Galaxy+S24",
                    rating=4.8,
                    reviews=2500,
                    features="Snapdragon 8 Gen 3|200MP Camera|12GB RAM|256GB Storage|S Pen",
                    specs="Brand: Samsung|Screen: 6.8 inches|CPU: Snapdragon 8 Gen 3|RAM: 12GB",
                ),
                Product(
                    id=str(uuid.uuid4()),
                    name="Sony WH-1000XM5",
                    price=349.00,
                    description="Industry-leading noise cancellation headphones.",
                    category="Headphones",
                    image_urls="https://placehold.co/600x400/333333/ffffff?text=Sony+XM5",
                    rating=4.9,
                    reviews=8000,
                    features="30hr Battery|HD Noise Cancelling|Touch Controls|Multipoint Connection",
                    specs="Brand: Sony|Type: Over-ear|Connectivity: Bluetooth 5.2",
                ),
            ]
            db.session.add_all(products)

        db.session.commit()
        print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=3000)
