from flask import Flask,  render_template, url_for, request, flash
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "0748d28ecb03830a0acae6d1886c55ed"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

# c1 = Company(name="t", email="t", password="t", address1="t", address2="t", county="t", eircode="t")

class Company(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address1 = db.Column(db.String(30), nullable=False)
    address2 = db.Column(db.String(30), nullable=False)
    county = db.Column(db.String(30), nullable=False)
    eircode = db.Column(db.String(30), unique=True, nullable=False)

    products = db.relationship("Product", backref="company", lazy=True)

    def __repr__(self):
        return "Company('{}', '{}', '{}', '{}')".format(self.name, 
                                                    self.email,
                                                    self.county,
                                                    self.eircode
                                                )

class Product(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False) # come back to min values
    quantity = db.Column(db.Integer, nullable=False) # come back to min values
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    
    def __repr__(self):
        return "Product('{}'. '{}'. '{}'. '{}')".format(self.name, 
                                                    self.description,
                                                    self.price,
                                                    self.quantity,
                                                    self.company
                                                )

 
products = [
    {
        "id": 0,
        "name": "Sample product 1",
        "company": "Sample Company 1",
        "price": 20,
    },
    {
        "id": 1,
        "name": "Sample product 2",
        "company": "Sample Company 2",
        "price": 69,
    },
    {
        "id": 2,
        "name": "Sample product 3",
        "company": "Sample Company 3",
        "price": 420,
    },
    {
        "id": 3,
        "name": "Sample product 4",
        "company": "Sample Company 4",
        "price": 50,
    },
    {
        "id": 4,
        "name": "Sample product 5",
        "company": "Sample Company 5",
        "price": 20,
    },
    {
        "id": 5,
        "name": "Sample product 6",
        "company": "Sample Company 6",
        "price": 69,
    },
    {
        "id": 6,
        "name": "Sample product 7",
        "company": "Sample Company 7",
        "price": 420,
    },
    {
        "id": 7,
        "name": "Sample product 8",
        "company": "Sample Company 8",
        "price": 50,
    }
]

  

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html", title="About")

@app.route("/contact/")
def contact():
    return render_template("contact.html", title="Contact")

@app.route("/product/<int:pid>")
def product(pid):
    return render_template("products.html", product=products[pid])

@app.route("/catalog/")
def catalog():
    return render_template("catalog.html", products=products)

@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return "Account created for %s!" % (form.company.data)

    return render_template("register.html", title="Register", form=form)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)

if __name__ == "__main__":
    app.run(debug=True)
