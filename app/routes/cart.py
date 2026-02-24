from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import current_user
from app.models import CartItem, Product, Order, OrderItem
from app import db
import uuid

bp = Blueprint("cart", __name__, url_prefix="/cart")


@bp.route("/")
def view_cart():
    if not current_user.is_authenticated:
        flash("Please sign in to view your cart.", "warning")
        return redirect(url_for("auth.signin"))

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal = sum(
        item.product.price * item.quantity for item in cart_items if item.product
    )

    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    return render_template(
        "cart.html",
        cart_items=cart_items,
        subtotal=subtotal,
        cart_item_count=cart_count,
    )


@bp.route("/update/<item_id>", methods=["POST"])
def update_cart(item_id):
    if not current_user.is_authenticated:
        flash("Please sign in to update your cart.", "warning")
        return redirect(url_for("auth.signin"))

    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not cart_item:
        abort(404)

    quantity = int(request.form.get("quantity", 1))
    if quantity <= 0:
        db.session.delete(cart_item)
        flash("Item removed from cart.", "info")
    else:
        cart_item.quantity = quantity
        flash("Cart updated.", "success")

    db.session.commit()
    return redirect(url_for("cart.view_cart"))


@bp.route("/remove/<item_id>")
def remove_from_cart(item_id):
    if not current_user.is_authenticated:
        flash("Please sign in to remove items from cart.", "warning")
        return redirect(url_for("auth.signin"))

    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Item removed from cart.", "success")

    return redirect(url_for("cart.view_cart"))


@bp.route("/checkout")
def checkout():
    if not current_user.is_authenticated:
        flash("Please sign in to checkout.", "warning")
        return redirect(url_for("auth.signin"))

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("main.home"))

    subtotal = sum(
        item.product.price * item.quantity for item in cart_items if item.product
    )

    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    return render_template(
        "checkout.html",
        cart_items=cart_items,
        subtotal=subtotal,
        cart_item_count=cart_count,
    )


@bp.route("/place_order", methods=["POST"])
def place_order():
    if not current_user.is_authenticated:
        flash("Please sign in to place an order.", "warning")
        return redirect(url_for("auth.signin"))

    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("main.home"))

    total_price = sum(
        item.product.price * item.quantity for item in cart_items if item.product
    )

    order = Order(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        total_price=total_price,
        status="processing",
    )
    db.session.add(order)

    for item in cart_items:
        if item.product:
            order_item = OrderItem(
                id=str(uuid.uuid4()),
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price * item.quantity,
            )
            db.session.add(order_item)

    for item in cart_items:
        db.session.delete(item)

    db.session.commit()
    flash("Order placed successfully!", "success")
    return redirect(url_for("main.orders"))
