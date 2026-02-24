from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import current_user
from app.models import Product, CartItem, WishlistItem
from app import db

bp = Blueprint("products", __name__, url_prefix="/product")


@bp.route("/<product_id>")
def product_detail(product_id):
    product = Product.query.get(product_id)
    if not product:
        abort(404)

    related_products = (
        Product.query.filter(
            Product.category == product.category, Product.id != product_id
        )
        .limit(4)
        .all()
    )

    cart_count = 0
    in_wishlist = False
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
        in_wishlist = (
            WishlistItem.query.filter_by(
                user_id=current_user.id, product_id=product_id
            ).first()
            is not None
        )

    return render_template(
        "product_detail.html",
        product=product,
        related_products=related_products,
        cart_item_count=cart_count,
        in_wishlist=in_wishlist,
    )


@bp.route("/<product_id>/add_to_cart", methods=["POST"])
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        flash("Please sign in to add items to cart.", "warning")
        return redirect(url_for("auth.signin"))

    product = Product.query.get(product_id)
    if not product:
        abort(404)

    quantity = int(request.form.get("quantity", 1))

    cart_item = CartItem.query.filter_by(
        user_id=current_user.id, product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id, product_id=product_id, quantity=quantity
        )
        db.session.add(cart_item)

    db.session.commit()
    flash(f"{product.name} added to cart!", "success")
    return redirect(url_for("products.product_detail", product_id=product_id))


@bp.route("/<product_id>/add_to_wishlist", methods=["POST"])
def add_to_wishlist(product_id):
    if not current_user.is_authenticated:
        flash("Please sign in to add items to wishlist.", "warning")
        return redirect(url_for("auth.signin"))

    product = Product.query.get(product_id)
    if not product:
        abort(404)

    existing = WishlistItem.query.filter_by(
        user_id=current_user.id, product_id=product_id
    ).first()

    if existing:
        db.session.delete(existing)
        flash(f"{product.name} removed from wishlist!", "info")
    else:
        wishlist_item = WishlistItem(user_id=current_user.id, product_id=product_id)
        db.session.add(wishlist_item)
        flash(f"{product.name} added to wishlist!", "success")

    db.session.commit()
    return redirect(url_for("products.product_detail", product_id=product_id))
