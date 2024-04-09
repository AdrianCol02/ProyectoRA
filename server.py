from flask import Flask, jsonify, request


app = Flask (__name__)


@app.route("/ping")
def ping():
    return jsonify({"message": "HOLA!"})


@app.route('/get', methods=['GET'])
def addDatoGet():
    # Código para cuando llega un get
    # return jsonify({"products": products, "message": "product’s list"})
    return jsonify ({"message": "DatoGet recibido"})


@app.route ('/post', methods=['POST'])
def addDatoPost():
    # Código para cuando llega un post
    new_dato = {
        "name" : request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    XXXXXXX.append(new_dato)
    print (request.json)
    return jsonify ({"message": "DatoPost recibido"})


# Rutas para servir archivos estáticos y listarlos
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/users')
def users():
    return app.send_static_file('users.html')

@app.route('/logs')
def logs():
    return jsonify(os.listdir('public/logs'))

# Para servir los archivos estáticos
@app.route('/logs/<path:filename>')
def serve_logs(filename):
    return app.send_static_file(os.path.join('logs', filename))

# Manejador para errores 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

# Manejador para errores 500
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

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
