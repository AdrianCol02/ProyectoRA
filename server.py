from flask import Flask, jsonify, request
from products import products


app = Flask (__name__)

@app.route("/ping")
def ping():
    return jsonify({"message": "HOLA!"})

@app.route(methods=['GET'])
def addDatoGet():
    return jsonify({"products": products, "message": "product’s list"})


@app.route ('/products', methods=['POST'])
def addDatoPost():
    new_product = {
        "name" : request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(new_product)
    print (request.json)
    return jsonify ({"message": "Product Added Succesfully", "products": products})

"""
@app.route('/products/<string:product_name>', methods=['PUT'])
def addProductFichero():
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(new_product)
    print(request.json)
    with open('products2.py', 'w') as file:
        file.write(str(new_product))

    return jsonify({"message": "Product Added Succesfully", "products": products})



@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    productFound = [product for product in products if product ['name'] == product_name]
    if (len(productFound) > 0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        return jsonify ({
            "message": "Product Updated",
            "product": productFound[0]
        })
    return jsonify({"message": "Product Not Found"})


@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productsFound =[product for product in products if product['name'] == product_name]
    if (len(productsFound)> 0):
        products.remove(productsFound[0])
        return jsonify ({
            "message": "Product Deleted",
            "products": products
        })
    return jsonify ({"message": "Product Not found"})
"""

app.run (debug=True, port=4000)
