"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Product, Characters, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [user.serialize() for user in users]
    response = {
        "status": "ok",
        "users": user_list
    }
    return jsonify(response)


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_single(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize()), 200
    

@app.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    
    if user:
        favorites_list = [favorite.serialize() for favorite in user.favorites]
        response = {
            "status": "ok",
            "favorites": favorites_list
        }
        return jsonify(response)
    else:
        return "Usuario no encontrado", 404
    
@app.route('/users/<int:user_id>/favorites/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    
    if user and planet:
        # Verificar si ya existe un favorito con la combinación user_id y id_planet
        existing_favorite = Favorites.query.filter_by(user_id=user_id, element_id=planet_id).first()

        if existing_favorite:
            return "Planet is already in favorites", 400

    
        new_favorite = Favorites(user_id=user_id, element_id=planet_id, element_type='Planet', element_name=planet.name)
        db.session.add(new_favorite)
        db.session.commit()
        return "Planet added to favorites successfully", 201
    else:
        return "User or planet not found", 404
    

@app.route('/users/<int:user_id>/favorites/planet/<int:planet_id>', methods = ['DELETE'])
def remove_planet_favorite(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    
    if user and planet:
        favorite_to_remove = Favorites.query.filter_by(user_id=user_id, element_id=planet_id, element_type='Planet').first()
        if favorite_to_remove:
            db.session.delete(favorite_to_remove)
            db.session.commit()
            return "Planet removed from favorites successfully", 200
        else:
            return "Planet is not in user's favorites", 404
    else:
        return "User or planet not found", 404


@app.route('/users/<int:user_id>/favorites/people/<int:id_character>', methods=['POST'])
def add_people_favorites(user_id, id_character):
    user = User.query.get(user_id)
    person = Characters.query.get(id_character)

    if user and person:
        # Verificar si ya existe un favorito con la combinación user_id y id_character
        existing_favorite = Favorites.query.filter_by(user_id=user_id, element_id=id_character).first()

        if existing_favorite:
            return "Character is already in favorites", 400

        new_person_favorite = Favorites(user_id=user_id, element_type="Character", element_id=id_character, element_name=person.name)
        db.session.add(new_person_favorite)
        db.session.commit()
        return "Character added successfully", 200
    else:
        return "User or character not found", 404
    
@app.route('/users/<int:user_id>/favorites/people/<int:id_character>', methods=['DELETE'])
def delete_planet_favorite(user_id, id_character):
    favorite = Favorites.query.filter_by(user_id=user_id, element_id=id_character, element_type='Character').first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return "Person removed from favorites successfully", 200
    else:
        return "Person not found in user's favorites", 404
    

# @app.route("/products", methods = ["GET"])
# def get_product ():
#     # products = Product.query.filter_by(name = "producto").all() #seklect * from table where name = "product"
#     products = Product.query.all() # select * from table
#     product_list = list(map(lambda obj : obj.serialize(), products))          # FORMA 1 de SERIALIZAR
#     response = {
#         "status": "ok",
#         "products" : product_list
#     }
#     return jsonify(response)


# @app.route("/products", methods = ["GET"])
# def get_product ():
#     # products = Product.query.filter_by(name = "producto").all() #seklect * from table where name = "product"
#     products = Product.query.all() # select * from table
    
#     product_list = []                                                         # FORMA 2 DE SERIALIZAR
#     for product in products:
#         product_list.append(product.serialize())

#     response = {
#         "status": "ok",
#         "products" : product_list
#     }
#     return jsonify(response)


@app.route("/products", methods = ["GET"])
def get_product ():
    # products = Product.query.filter_by(name = "producto").all() #seklect * from table where name = "product"
    products = Product.query.all()                                         # select * from table
    
    product_list = [product.serialize() for product in products ]          #  FORMA 3 DE SERIALIZAR.....cOMPREHENSION DE LISTAS

    response = {
        "status": "ok",
        "products" : product_list
    }
    return jsonify(response)


@app.route("/product/<int:id_product>", methods=["GET"])
def get_product_single(id_product):
    product = Product.query.get(id_product)
    return jsonify(product.serialize()), 200


@app.route("/newproduct", methods=["POST"])
def new_product ():
    body = json.loads(request.data)
    print(body )
    new_product = Product(name = body["name"], price = body["price"])
    db.session.add(new_product)
    db.session.commit()
    return jsonify("msj"), 200

@app.route("/people", methods = ["GET"])
def get_people ():
    # products = Product.query.filter_by(name = "producto").all() #seklect * from table where name = "product"
    characters = Characters.query.all()                                         # select * from table
    
    people_list = [person.serialize() for person in characters ]          #  FORMA 3 DE SERIALIZAR.....cOMPREHENSION DE LISTAS

    response = {
        "status": "ok",
        "people" : people_list
    }
    return jsonify(response)

@app.route("/people/<int:id_character>", methods=["GET"])
def get_person_single(id_character):
    person = Characters.query.get(id_character)
    if person:
        return jsonify(person.serialize()), 200
    else:
         return "Person not found", 404

@app.route("/people", methods=["POST"])
def new_person ():
    body = json.loads(request.data)
    print(body )
    new_person = Characters(name = body["name"], mass = body["mass"], height = body["height"], skin_color = body["skin_color"], hair_color = body["hair_color"], eyes_color = body["eyes_color"], birth_year = body["birth_year"], gender = body["gender"], homeworld = body["homeworld"])
    db.session.add(new_person)
    db.session.commit()
    return jsonify("msj"), 200


#Aqui borras personajes segun sus indices que ya tratas como una lista a la base de datos. No es común.
@app.route('/people/<int:id_character>', methods=['DELETE'])
def delete_people(id_character):
    print("This is the position to delete: ", id_character)
    
    # Obtén todos los personajes
    characters = Characters.query.all()
    
    if 0 <= id_character < len(characters):
        character_to_delete = characters[id_character]
        db.session.delete(character_to_delete)
        db.session.commit()
        return 'Person deleted successfully', 200
    else:
        return "Person not found", 400

# #Aqui accedes comunmente a la base de datos y borras el registro directamente. Los indices no varían
# @app.route('/people/<int:id_character>', methods=['DELETE'])
# def delete_person(id_character):
#     print("This is the ID to delete: ", id_character)
    
#     person = Characters.query.get(id_character)
    
#     if person:
#         db.session.delete(person)
#         db.session.commit()
#         return 'Person deleted successfully', 200
#     else:
#         return 'Person not found', 404

# #Aqui modificas los personajes en base a su indice....
# @app.route('/people/<int:id_character>', methods=['PUT'])
# def update_person(id_character):
#     updated_data = json.loads(request.data)
    
#     # Obtén todos los personajes
#     characters = Characters.query.all()
    
#     if 0 <= id_character < len(characters):
#         person_to_update = characters[id_character]
        
#         # Actualiza los campos con los nuevos datos
#         if 'name' in updated_data:
#             person_to_update.name = updated_data['name']
#         if 'mass' in updated_data:
#             person_to_update.mass = updated_data['mass']
#         if 'height' in updated_data:
#             person_to_update.height = updated_data['height']
#         # ... y así sucesivamente para otros campos que quieras actualizar
        
#         db.session.commit()
#         return "Personaje actualizado correctamente", 200
#     else:
#         return "Personaje no encontrado", 404

#AQUI TAMBIEN
@app.route('/people/<int:id_character>', methods=['PUT'])
def update_person(id_character):
    updated_data = json.loads(request.data)
    
    person = Characters.query.get(id_character)
    
    if person:
        # Actualiza los campos con los nuevos datos
        if 'name' in updated_data:
            person.name = updated_data['name']
        if 'mass' in updated_data:
            person.mass = updated_data['mass']
        if 'height' in updated_data:
            person.height = updated_data['height']
        if 'skin_color' in updated_data:
            person.skin_color = updated_data['skin_color']
        if 'hair_color' in updated_data:
            person.hair_color = updated_data['hair_color']
        if 'eyes_color' in updated_data:
            person.eyes_color = updated_data['eyes_color']
        if 'birth_year' in updated_data:
            person.birth_year = updated_data['birth_year']
        if 'gender' in updated_data:
            person.gender = updated_data['gender']
        if 'homeworld' in updated_data:
            person.homeworld = updated_data['homeworld']
        
        db.session.commit()
        return "Personaje actualizado correctamente", 200
    else:
        return "Personaje no encontrado", 404

@app.route("/planets", methods = ["GET"])
def get_planets ():
    # products = Product.query.filter_by(name = "producto").all() #seklect * from table where name = "product"
    planets = Planets.query.all()                                         # select * from table
    
    planets_list = [planet.serialize() for planet in planets ]          #  FORMA 3 DE SERIALIZAR.....cOMPREHENSION DE LISTAS

    response = {
        "status": "ok",
        "people" : planets_list
    }
    return jsonify(response)


@app.route("/planet/<int:id_planet>", methods=["GET"])
def get_planet_single(id_planet):
    planet = Planets.query.get(id_planet)
    if planet:
        return jsonify(planet.serialize()), 200
    else:
        return "Planet not found", 404


@app.route("/planets", methods=["POST"])
def new_planet ():
    body = json.loads(request.data)
    print(body )
    new_planet = Planets(name = body["name"], rotation_period = body["rotation_period"], orbital_period = body["orbital_period"], diameter = body["diameter"], climate = body["climate"], gravity = body["gravity"], terrain = body["terrain"], surface_water = body["surface_water"], population = body["population"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify("msj"), 200

#Aqui borramos en base a la id (pk), que la he hecho visible en el archivo admin.
@app.route('/planet/<int:id_planet>', methods=['DELETE'])
def delete_planet(id_planet):
    print("This is the ID to delete: ", id_planet)
    
    planet = Planets.query.get(id_planet)
    
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return 'Planet deleted successfully', 200
    else:
        return 'Planet not found', 404

@app.route('/planet/<int:id_planet>', methods=['PUT'])
def update_planet(id_planet):
    updated_data = json.loads(request.data)
    
    planet = Planets.query.get(id_planet)
    
    if planet:
        if 'name' in updated_data:
            planet.name = updated_data['name']
        if 'orbital_period' in updated_data:
            planet.orbital_period = updated_data['orbital_period']
        if 'rotation_period' in updated_data:
            planet.rotation_period = updated_data['rotation_period']
        if 'diameter' in updated_data:
            planet.diameter = updated_data['diameter']
        if 'gravity' in updated_data:
            planet.gravity = updated_data['gravity']
        if 'climate' in updated_data:
            planet.climate = updated_data['climate']
        if 'terrain' in updated_data:
            planet.terrain = updated_data['terrain']
        if 'surface_water' in updated_data:
            planet.surface_water = updated_data['surface_water']
        if 'population' in updated_data:
            planet.population = updated_data['population']
        
        db.session.commit()
        return "Planet updated successfully", 200
    else:
        return "Planet not found", 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)






