from flask import render_template, url_for, request, flash, redirect, abort
from rebelmarketplace import app, db, bcyrpt
from rebelmarketplace.forms import RegistrationForm, LoginForm, ProductForm
from rebelmarketplace.models import Company, Product
from flask_login import login_user, current_user, logout_user, login_required


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

@app.route("/product/new/", methods=["GET", "POST"])
@login_required
def new_product(): 
    form = ProductForm()
    if form.validate_on_submit():
        post = Product(name=form.name.data, description=form.description.data,
                    price=form.price.data, quantity=form.quantity.data, company=current_user)
        db.session.add(post)
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
    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        db.session.commit()
        flash("Your product has been updated", "success")
        return redirect(url_for("product", product_id=product.id))
    elif request.method == "GET":        
            form.name.data = product.name
            form.description.data = product.description
            form.price.data = product.price
            form.quantity.data = product.quantity
    return render_template("create_product.html", title="Update Product", form=form)   

@app.route("/product/<int:product_id>/delete/", methods=["POST"])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.company != current_user:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash("Your product has been deleted")
    return redirect(url_for("company", company_id=current_user.id))


@app.route("/catalog/")
def catalog():
    products = Product.query.all()
    
    return render_template("catalog.html", products=products)

@app.route("/company/<int:company_id>")
def company(company_id):
    company = Company.query.get_or_404(company_id)
    products = company.products
    return render_template("company.html", products=products)

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

@app.route("/account/")
@login_required
def account():
    products = current_user.products
    return render_template("account.html", title="Your Account", products=products)

@app.route("/buy/<int:product_id>/", methods=["POST"])
def buy(product_id):
    product = Product.query.get(product_id)
    if product.quantity > 0:
        product.quantity -= 1
    db.session.commit()
    
    company = product.company
    return render_template("thanks.html", title="Thanks", company=company)

