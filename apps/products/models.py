from apps import db_sql

# from dbConfig.db import db

db = db_sql


class Category(db.Model):
    """ Product Category model"""
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id',ondelete='SET NULL'))
    category_name = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"category_name :'{self.category_name}')"


class Product(db.Model):
    """ Product model"""
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id',ondelete='SET NULL'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id',ondelete='SET NULL'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    product_name = db.Column(db.String(255), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    sold_quantity = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    rating = db.relationship('Rating', backref='rating_person', lazy=True)

    def __repr__(self):
        return f"product name :'{self.product_name}')"

    def format(self):
        "Product formating"
        return {
            'id': self.id,
            'category_id': self.category_id,
            'product_name': self.product_name,
            'brand': self.brand,
            'price': self.price,
        }


class Rating(db.Model):
    """ Product Rating model"""
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id', ondelete='SET NULL'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='SET NULL'))
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"rating :'{self.review}')"
