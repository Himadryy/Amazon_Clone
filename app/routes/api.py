from flask import Blueprint, jsonify, request
from app.models import Product, User, Order
from app import db
from flask_login import current_user

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/products", methods=["GET"])
def get_products():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    category = request.args.get("category")

    query = Product.query
    if category:
        query = query.filter_by(category=category)

    products = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(
        {
            "products": [p.to_dict() for p in products.items],
            "total": products.total,
            "page": products.page,
            "pages": products.pages,
        }
    )


@bp.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product.to_dict())


@bp.route("/products/search", methods=["GET"])
def search_products():
    query = request.args.get("q", "")
    products = Product.query.filter(Product.name.ilike(f"%{query}%")).limit(20).all()

    return jsonify(
        {
            "products": [p.to_dict() for p in products],
            "count": len(products),
        }
    )


@bp.route("/categories", methods=["GET"])
def get_categories():
    categories = db.session.query(Product.category).distinct().all()
    return jsonify(
        {
            "categories": [c[0] for c in categories],
        }
    )


@bp.route("/cart", methods=["GET"])
def get_cart():
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401

    from app.models import CartItem

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    return jsonify(
        {
            "items": [
                {
                    "id": item.id,
                    "product": item.product.to_dict() if item.product else None,
                    "quantity": item.quantity,
                }
                for item in cart_items
            ],
        }
    )


@bp.route("/orders", methods=["GET"])
def get_orders():
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401

    orders = (
        Order.query.filter_by(user_id=current_user.id)
        .order_by(Order.order_date.desc())
        .all()
    )

    return jsonify(
        {
            "orders": [
                {
                    "id": order.id,
                    "total_price": order.total_price,
                    "status": order.status,
                    "order_date": order.order_date.isoformat(),
                    "items": [
                        {
                            "product_id": item.product_id,
                            "quantity": item.quantity,
                            "price": item.price,
                        }
                        for item in order.items
                    ],
                }
                for order in orders
            ],
        }
    )


@bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"})
