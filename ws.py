from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_marshmallow import Marshmallow

ws = Flask(__name__)

# let the program know to refer to this base directory
basedir = os.path.abspath(os.path.dirname(__file__))
# Init data base
ws.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db_new.sqlite')
# disable SQL modification tacking system to save system resources
ws.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init data base
db = SQLAlchemy(ws)
# Init Marshmallow to handle data
ma = Marshmallow(ws)


# Building our data base for putting and pulling data
class Product(db.Model):
    # assign fields
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(200))
    total = db.Column(db.String(200))
    available = db.Column(db.String(100))
    used = db.Column(db.String(200))
    percentage = db.Column(db.Float)

    # define init to get data from user and put into the database
    def __init__(self, client_name, total, available, used, percentage):
        self.client_name = client_name
        self.total = total
        self.available = available
        self.used = used
        self.percentage = percentage


# define what we want to see in our database
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'client_name', 'total', 'available', 'used', 'percentage')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

"""
define POST req, upload chunks of data from 
the user to our database, the data is in json format and
structured as a list of dicts.
note: we can also post single dict data
"""


@ws.route('/api/CpuMemory', methods=['POST'])
def cpu_memory_post():
    data = request.get_json()

    # check if data is single dict
    if isinstance(data, dict):
        new_product = Product(data['client_name'], data['total'],
                              data['available'], data['used'],
                              data['percentage'])

        db.session.add(new_product)
        db.session.commit()

        # 201 - created
        return {"status": 201}
    # if data in a list of dict
    for n in data:
        new_product = Product(n['client_name'], n['total'],
                              n['available'], n['used'],
                              n['percentage'])

        db.session.add(new_product)
        db.session.commit()

    # 201 - created
    return {"status": 201}


"""
define PUT req, can upload single dict data.
checking if user_id already in data, if so return a message. 
"""


@ws.route('/api/CpuMemory/single/<int:user_id>', methods=['PUT'])
def cpu_memory_put(user_id):
    # extracting the data to json serializable
    client_name = request.json['client_name']
    total = request.json['total']
    available = request.json['available']
    used = request.json['used']
    percentage = request.json['percentage']

    # checking if id already exists
    data = Product.query.filter_by(id=user_id).first()
    if data:
        return {"message": "Cpu data id already exist..."}

    new_product = Product(client_name, total,
                          available, used, percentage)

    db.session.add(new_product)
    db.session.commit()

    # 201 - created
    return {"status": 201}


"""
define GET req, we can pull the data corresponding 
to the id and display it
"""


@ws.route('/api/CpuMemory/<int:user_id>', methods=['GET'])
def cpu_memory_get(user_id):
    data = Product.query.filter_by(id=user_id).first()

    if not data:
        # 404 - User id not found
        return {"status": 404}

    # getting the data requested
    cpu_data = {}
    cpu_data['client_name'] = data.client_name
    cpu_data['id'] = data.id
    cpu_data['total'] = data.total
    cpu_data['available'] = data.available
    cpu_data['used'] = data.used
    cpu_data['percentage'] = data.percentage

    return {"message": 200, "data": cpu_data}


"""
define DELETE req, lets us delete the data
corresponding to the user id that was inputted
"""


@ws.route('/api/CpuMemory/del/<int:user_id>', methods=['DELETE'])
def cpu_memory_del(user_id):
    data = Product.query.filter_by(id=user_id).first()

    try:
        db.session.delete(data)
        db.session.commit()

        # 200 - ok
        return {"message": "data deleted", "status": 200}

    except:
        # 404 - User id not found
        return {"status": 404}


"""
define PATCH req, lets us update data corresponding 
to the user id that was inputted
"""


@ws.route('/api/CpuMemory/update/<int:user_id>', methods=['PATCH'])
def cpu_memory_patch(user_id):
    # if user id in data base
    data = Product.query.filter_by(id=user_id).first()
    if data:
        # Taking the data and making it json serializable
        client_name = request.json['client_name']
        total = request.json['total']
        available = request.json['available']
        used = request.json['used']
        percentage = request.json['percentage']

        # our desired data to update
        update_dict = {"client_name": client_name, "total": total,
                       "available": available, "used": used,
                       "percentage": percentage}

        # finding our data corresponding to the id and updating it
        Product.query.filter_by(id=user_id).update(update_dict)
        db.session.commit()

        # 200 - ok
        return {"message": "updated",
                "status": 200}

    # 404 - User id not found
    return {"message": "User id not found",
            "status": 404}


if __name__ == '__main__':
    ws.run(debug=True)
