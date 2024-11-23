from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.utils import secure_filename
import os
from ..models.models import User, Product
from .. import db
from ..config import Config

CATEGORIES = ["T-shirts", "Jeans", "Jackets", "Shoes", "Accessories"]
admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin_dashboard', methods=['GET'])
@admin.route('/admin_dashboard/search/<search>')
@admin.route('/admin_dashboard/filter/<category>')
@login_required
@admin_required
def admin_dashboard(category='ALL', search=''):
    if search:
        search_query = request.args.get("product_name")
        products = Product.query.filter(Product.title.like(f'%{search_query}%')).all()
    else:
        if category == 'ALL':
            products = Product.query.all()
        else:
            products = Product.query.filter_by(category=category).all()
    
    return render_template('admin/admin_dashboard.html', 
                         products=products, 
                         categories=CATEGORIES)

@admin.route('/create_product', methods=['GET', 'POST'])
@login_required
@admin_required
def create_product():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        price = request.form.get('price')
        image = request.files.get('image')
        
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            image_path = f"assets/product_images/{filename}"
            
            product = Product(
                title=title,
                category=category,
                price=float(price),
                image_path=image_path
            )
            
            db.session.add(product)
            db.session.commit()
            
            flash("Product added successfully!", category='success')
            return redirect(url_for('admin.admin_dashboard'))
            
    return render_template('admin/create_product.html')

@admin.route('/delete_product/<int:product_id>')
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Delete the image file
    if product.image_path:
        image_path = os.path.join(Config.UPLOAD_FOLDER, os.path.basename(product.image_path))
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    
    flash("Product deleted successfully!", category='success')
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/add_admin', methods=['GET', 'POST'])
@login_required
@admin_required
def add_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if current_user.check_password(password):
            user = User.query.filter_by(email=email).first()
            if user:
                user.user_type = 'Admin'
                db.session.commit()
                flash(f"Successfully made {email} an admin!", category='success')
            else:
                flash("Email does not exist!", category='error')
        else:
            flash("Incorrect password!", category='error')
            
        return redirect(url_for('admin.admin_dashboard'))
        
    return render_template('admin/add_admin.html')
