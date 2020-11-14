from flask import render_template, url_for, request, flash, redirect, abort
from rebelmarketplace import app, db, bcyrpt
from rebelmarketplace.forms import RegistrationForm, LoginForm, ProductForm, UpdateAccountForm, BuyForm, UpdateProductForm
from rebelmarketplace.models import Company, Product
from flask_login import login_user, current_user, logout_user, login_required
import os
from PIL import Image

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html", title="About")

@app.route("/contact/")
def contact():
    return render_template("contact.html", title="Contact")

@app.route("/product/<int:product_id>/")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product.html", title=product.name, product=product)

def save_image(form_image):
    image_fn = form_image.filename
    image_path = os.path.join(app.root_path, "static/product_pics", image_fn)

    output_size = (125, 125)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    
    return image_fn



@app.route("/product/new/", methods=["GET", "POST"])
@login_required
def new_product(): 
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data,
                    price=form.price.data, quantity=form.quantity.data, company=current_user)
        
        if form.image.data:
            image_file = save_image(form.image.data)
            product.image = image_file
            
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully", "success")
        return redirect(url_for("account"))
    return render_template("create_product.html", title="New Product", form=form)   

@app.route("/product/<int:product_id>/update/", methods=["GET", "POST"])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.company != current_user:
        abort(403)
    form = UpdateProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        if form.image.data:
            product.image = save_image(form.image.data)
        db.session.commit()
        flash("Your product has been updated", "success")
        return redirect(url_for("product", product_id=product.id))
    elif request.method == "GET":        
            form.name.data = product.name
            form.description.data = product.description
            form.price.data = product.price
            form.quantity.data = product.quantity   

    return render_template("Update_product.html", title="Update Product", form=form, product=product)   

@app.route("/product/<int:product_id>/delete/", methods=["POST"])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.company != current_user:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash("Your product has been deleted", "success")
    return redirect(url_for("company", company_id=current_user.id))


@app.route("/catalogue/")
def catalogue():
    products = Product.query.all()
    
    return render_template("catalogue.html", products=products)

@app.route("/company/<int:company_id>")
def company(company_id):
    company = Company.query.get_or_404(company_id)
    products = company.products
    return render_template("company.html", products=products, company=company)

@app.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcyrpt.generate_password_hash(form.password.data).decode("utf-8")
        company = Company(name=form.name.data, email=form.email.data, 
                        password=hashed_password, address1=form.address1.data, 
                        address2=form.address2.data, county=form.county.data, 
                        eircode=form.eircode.data)
        db.session.add(company)
        db.session.commit()
        flash("Your account has been created! You can now log in!", "success") # this isnt working
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(email=form.email.data).first()
        if company and bcyrpt.check_password_hash(company.password, form.password.data):
            login_user(company, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Login successful!", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "error")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account/", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    products = current_user.products
    if form.validate_on_submit():
        current_user.description = form.description.data
        current_user.thank_you_msg= form.thank_you_msg.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":        
            form.name.data = current_user.name
            form.email.data = current_user.email
            form.description.data = current_user.description
            form.thank_you_msg.data = current_user.thank_you_msg
            form.address1.data = current_user.address1
            form.address2.data = current_user.address2
            form.address3.data = current_user.address3
            form.county.data = current_user.county
            form.eircode.data = current_user.eircode
    return render_template("account.html", title="Account", products=products, form=form)

@app.route("/buy/<int:product_id>/", methods=["GET", "POST"])
def buy(product_id):
    form = BuyForm()
    product = Product.query.get(product_id)
    if form.validate_on_submit():
        if product.quantity > 0:
            product.quantity -= 1
        db.session.commit()
    
        company = product.company
        return render_template("thanks.html", title="Thanks", company=company)

    return render_template("buy.html", product=product, form=form)



