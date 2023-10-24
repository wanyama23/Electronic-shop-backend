from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
# from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import MetaData


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
# class User(db.Model, UserMixin):
class User(db.Model):
    __tablename__ = "user"    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String)
    password = db.Column(db.String(60), nullable=False)
    address = db.relationship("Location", backref="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cart = db.relationship('Cart', backref='user', lazy=True)

    def add_to_cart(self,product_id):
        item_to_add = Cart(product_id=product_id, user_id=self.id)
        db.session.add(item_to_add)
        db.session.commit()
        flash('Your item has been added to your cart!', 'success')

    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}', '{self.email}','{self.id}')"



class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Products('{self.name}', '{self.price}')"

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="cart")
    quantity = db.Column(db.Integer, nullable=False, default=1)


    def __repr__(self):
        return f"Cart('Product id:{self.product_id}','id: {self.id}','User id:{self.user_id}'')"

