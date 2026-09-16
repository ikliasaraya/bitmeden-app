from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Product, db, Listing, ListingType
from datetime import datetime


listings_bp = Blueprint("listings", __name__)

@listings_bp.route("/listings")
@login_required
def listings():
    all_listings = Listing.query.join(Product).filter(Product.business_id == current_user.id).all()
    return render_template("listings/list.html", listings=all_listings)

@listings_bp.route("/listings/new", methods=["GET","POST"])
@login_required
def add_listings():
    if request.method == "POST":
        product_id = request.form["product_id"]
        listing_type = request.form["type"]
        discounted_price = request.form["discounted_price"]
        quantity_available = request.form["quantity_available"]
        start_time = datetime.strptime(request.form["start_time"], "%Y-%m-%dT%H:%M")
        end_time = datetime.strptime(request.form["end_time"], "%Y-%m-%dT%H:%M")
    
        listing = Listing(
            product_id = product_id,
            type = ListingType(listing_type),
            discounted_price = discounted_price,
            quantity_available = quantity_available,
            start_time = start_time,
            end_time = end_time)

        db.session.add(listing)
        db.session.commit()
        return redirect(url_for("listings.listings"))
    else: 
        my_products = Product.query.filter_by(business_id=current_user.id).all()
        return render_template("listings/new.html", products = my_products)