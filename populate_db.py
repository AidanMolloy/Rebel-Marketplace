import requests
from rebelmarketplace import bcyrpt
from rebelmarketplace.models import *
from random import randint

URL = "https://fakestoreapi.com/products"

products = requests.get(URL).json()

company_names = {
    "men clothing": "Gentlemens' Garments",
    "jewelery": "Ballincollig Bling",
    "electronics": "ComputerWorld",
    "women clothing": "Pennyz"            
}

company_details = {
    "Gentlemens' Garments": {
        "email": "gg@gmail.com",
        "password": "ggarments",
        "address1":"12 Clothes Street",
        "county": "Galway",
        "eircode": "T12 V21X"
    },
    "Ballincollig Bling": {
        "email": "bb@gmail.com",
        "password": "bbling",
        "address1":"69 Gold Square",
        "county": "Cork",
        "eircode": "P31 420J"
    },
    "ComputerWorld": {
        "email": "cw@gmail.com",
        "password": "cworld",
        "address1":"2 Binary Tree",
        "county": "Dublin",
        "eircode": "G13 FV7P"
    },
    "Pennyz": {
        "email": "p@gmail.com",
        "password": "gurl",
        "address1": "18 Fashion Lane",
        "county": "Kerry",
        "eircode": "D45 P9XC"
    }
}

db.drop_all()
db.create_all()

for k, v in company_details.items():
    name = k
    email = v["email"]
    password = v["password"]
    address1 = v["address1"]
    county = v["county"]
    eircode = v["eircode"]
    hashed_password = bcyrpt.generate_password_hash(password).decode("utf-8")
    
    company = Company(name=name, email=email, 
                    password=hashed_password, address1=address1, 
                    county=county, eircode=eircode)

    db.session.add(company)
    for p in products:
        company_key = p["category"]
        if company_names[company_key] == name:
            pname = p["title"]
            desc = p["description"]
            price = p["price"] # come back and round later
            quantity = randint(5, 50)
            image = p["image"]
        
            product = Product(name=pname, description=desc, image=image,
                        price=price, quantity=quantity, company=company)
            db.session.add(product)

db.session.commit()
    

        



    








