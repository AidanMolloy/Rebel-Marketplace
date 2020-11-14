from rebelmarketplace import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(company_id):
    return Company.query.get(int(company_id))

class Company(db.Model, UserMixin):
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address1 = db.Column(db.String(30), nullable=False)
    address2 = db.Column(db.String(30), nullable=True)
    address3 = db.Column(db.String(30), nullable=True)
    county = db.Column(db.String(30), nullable=False)
    eircode = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True, default="")
    thank_you_msg = db.Column(db.Text, nullable=True, default="Thank you")
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
    price = db.Column(db.Numeric(scale=2, asdecimal=True), nullable=False) # come back to min values
    quantity = db.Column(db.Integer, nullable=False) # come back to min values
    image = db.Column(db.String(20), nullable=False, default="default.png")
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    
    def __repr__(self):
        return "Product('{}'. '{}'. '{}'. '{}')".format(self.name, 
                                                    self.description,
                                                    self.price,
                                                    self.quantity,
                                                    self.company
                                                )

# db.drop_all()
# db.create_all()