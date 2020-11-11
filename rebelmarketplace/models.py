from rebelmarketplace import db

class Company(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address1 = db.Column(db.String(30), nullable=False)
    address2 = db.Column(db.String(30), nullable=True)
    address3 = db.Column(db.String(30), nullable=True)
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