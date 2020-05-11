from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Example route
# @app.route('/', methods=['GET'])
# def get():
#   return jsonify({ "msg": "Hello"})

# Init db
db = SQLAlchemy(app)

# Init Marshmellow
ma = Marshmallow(app)


class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty


class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')
    

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Create Product
@app.route('/product', methods=['POST'])
def add_product():
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']
  
  new_product = Product(name, description, price, qty)
  
  db.session.add(new_product)
  db.session.commit()
  
  return product_schema.jsonify(new_product)

# Get Products
@app.route('/products', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result)

# Get Single Product
@app.route('/products/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)
 
# Update Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)
  
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']
  
  product.name = name
  product.description = description
  product.price = price
  product.qty = qty
  
  db.session.commit()
  
  return product_schema.jsonify(product)


# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()
  
  return product_schema.jsonify(product)
# Run server
if __name__ == '__main__':
  app.run(debug=True)

