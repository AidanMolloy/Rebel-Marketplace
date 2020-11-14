from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError, NumberRange
from rebelmarketplace.models import Company
from rebelmarketplace.counties import counties 

class RegistrationForm(FlaskForm):

    name = StringField('Business Name *', 
                        validators=[DataRequired(),Length(min=2, max=30)])
    email = StringField('Email *', 
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password *", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password *", validators=[DataRequired(), EqualTo('password')])
    address1 = StringField('Address *', 
                        validators=[DataRequired(),Length(min=2, max=30)])
    address2 = StringField("Address line 2", validators=[Optional(), Length(min=2, max=30)])                        
    address3 = StringField("Address line 3", validators=[Optional(), Length(min=2, max=30)])                        
    county = SelectField('County *', 
                        choices=counties,
                        validators=[DataRequired()])
    # could check for valid eircode or even use the eircode to query for addess?
    # maybe even check from eircode then ask user is this the address and let them adjust accordingly
    eircode = StringField('Eircode *', 
                        validators=[DataRequired(),Length(min=2, max=30)])
    thank_you_msg = TextAreaField("Thank you message")
    

    submit = SubmitField('Register Now')

    def validate_email(self, email):
        company = Company.query.filter_by(email=email.data).first()
        if company:
            raise ValidationError("An account already exists for that email")

    def validate_eircode(self, eircode):
        company = Company.query.filter_by(eircode=eircode.data).first()
        if company:
            raise ValidationError("Another company is already using this Eircode")



class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    
    remember = BooleanField("Remember me") # cookie stuff ngl dont really know anything about this 
    submit = SubmitField("Login")  


class ProductForm(FlaskForm):
    name = StringField('Product Name *', validators=[DataRequired()])
    description = TextAreaField("Product Description *", validators=[DataRequired()])
    price = IntegerField('Price € *', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity *', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField("Product Image ", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Create Product")  

class UpdateAccountForm(FlaskForm):
    thank_you_msg = TextAreaField("Thank you message")
    description = TextAreaField("Company description")

    submit = SubmitField("Update account")

class BuyForm(FlaskForm):
    card_number = StringField("Card Number *", validators=[DataRequired()])
    expiration_date = StringField("Expiration Date MM/YY *", validators=[DataRequired()])
    cvv = StringField("CVV *", validators=[DataRequired()])

    submit = SubmitField("Place Order")