from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from ..models.models import Product
from .. import db

products = Blueprint('products', __name__)

CATEGORIES = ["T-shirts", "Jeans", "Jackets", "Shoes", "Accessories"]

@products.route('/')
def index():
    return redirect(url_for('products.home_page'))

@products.route('/home_page')
@products.route('/home_page/search/<search>')
@products.route('/home_page/filter/<category>')
@login_required
def home_page(category='ALL', search=''):
    if search:
        search_query = request.args.get("product_name")
        products_list = Product.query.filter(Product.title.like(f'%{search_query}%')).all()
    else:
        if category == 'ALL':
            products_list = Product.query.all()
        else:
            products_list = Product.query.filter_by(category=category).all()
            
    return render_template('products/home_page.html', 
                         products=products_list, 
                         categories=CATEGORIES)
