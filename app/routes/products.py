from flask import render_template, Blueprint, redirect, url_for, request
from app.models import db, Business, Product
from flask_login import login_required, current_user

products_bp = Blueprint("products", __name__)

@products_bp.route("/products")
@login_required
def products():
    all_products = Product.query.filter_by(business_id=current_user.id).all()
    return render_template("products/list.html", products=all_products)

@products_bp.route("/products/new", methods=["GET","POST"])
@login_required
def add_product():
    if request.method == "POST":
        business_id = current_user.id
        name = request.form["name"]
        description = request.form["description"]
        base_price = request.form["base_price"]
        photo_url = request.form["photo_url"]

        product = Product(business_id=business_id, name=name, description=description, base_price=base_price, photo_url=photo_url)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("products.products"))
    else:
        return render_template("products/new.html")