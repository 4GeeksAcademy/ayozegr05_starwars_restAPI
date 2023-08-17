from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref="user")
    # users_favorite_planets = db.relationship('Planets', secondary = favorites)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(120), unique=True, nullable=False)
    price  = db.Column(db.Integer)

    def __repr__(self):
        return '<Product %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            # do not serialize the password, its a security breach
        }
    

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(60), unique=True, nullable=False)
    rotation_period = db.Column(db.String(50))
    orbital_period = db.Column(db.String(50))
    diameter = db.Column(db.String(50))
    climate = db.Column(db.String(50))
    gravity = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.String(50))
    population = db.Column(db.String(50))
   
    def __repr__(self):
        return '<Planets %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population ": self.population ,
            # do not serialize the password, its a security breach
        }

    
class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(60), unique=True, nullable=False)
    height  = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    eyes_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(10))
    gender = db.Column(db.String(50))
    homeworld = db.Column(db.String(50))
    

    def __repr__(self):
        return '<Characters %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eyes_color": self.eyes_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    element_id = db.Column(db.Integer)  # ID del personaje o planeta favorito
    element_type = db.Column(db.String(50))  # "character" o "planet"
    element_name = db.Column(db.String(50))  # Nombre del elemento favorito
  
    def __repr__(self):
        return '<Favorites %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "element_id": self.element_id,
            "element_type": self.element_type, 
            "element_name": self.element_name,
            # do not serialize the password, its a security breach
        }

    