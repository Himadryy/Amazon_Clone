from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import current_user
from app.models import Product, CartItem
from app import db
from flask import current_app

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    products = Product.query.limit(20).all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]

    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()

    return render_template(
        "home.html",
        products=products,
        categories=categories,
        cart_item_count=cart_count,
    )


@bp.route("/category/<category_name>")
def category(category_name):
    products = Product.query.filter_by(category=category_name).all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]

    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()

    return render_template(
        "category.html",
        products=products,
        category_name=category_name,
        categories=categories,
        cart_item_count=cart_count,
    )


@bp.route("/search")
def search():
    query = request.args.get("query", "")
    products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()

    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]

    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()

    return render_template(
        "search.html",
        products=products,
        query=query,
        categories=categories,
        cart_item_count=cart_count,
    )


@bp.route("/set_locale", methods=["POST"])
def set_locale():
    session["language"] = request.form.get("language", "en_US")
    session["currency"] = request.form.get("currency", "USD")
    flash("Your language and currency preferences have been updated.", "success")
    return redirect(request.referrer or url_for("main.home"))


@bp.route("/wishlist")
def wishlist():
    if not current_user.is_authenticated:
        flash("Please sign in to view your wishlist.", "warning")
        return redirect(url_for("auth.signin"))

    from app.models import WishlistItem

    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    products = [item.product for item in wishlist_items if item.product]

    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]

    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()

    return render_template(
        "wishlist.html",
        products=products,
        categories=categories,
        cart_item_count=cart_count,
    )


@bp.route("/orders")
def orders():
    if not current_user.is_authenticated:
        flash("Please sign in to view your orders.", "warning")
        return redirect(url_for("auth.signin"))

    from app.models import Order

    user_orders = (
        Order.query.filter_by(user_id=current_user.id)
        .order_by(Order.order_date.desc())
        .all()
    )

    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]

    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()

    return render_template(
        "orders.html",
        orders=user_orders,
        categories=categories,
        cart_item_count=cart_count,
    )


@bp.route("/recommendations")
def recommendations():
    if not current_user.is_authenticated:
        flash("Please sign in to view recommendations.", "warning")
        return redirect(url_for("auth.signin"))

    products = Product.query.limit(10).all()

    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]

    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()

    return render_template(
        "recommendations.html",
        products=products,
        categories=categories,
        cart_item_count=cart_count,
    )
