import os
from flask_admin import Admin
from models import db, User, Planets, Characters, Favorites
from flask_admin.contrib.sqla import ModelView

class CustomCharactersModelView(ModelView):
    column_list = ['id', 'name', 'height', 'mass', 'hair_color', 'skin_color', 'eyes_color', 'birth_year', 'gender', 'homeworld']

class CustomPlanetsModelView(ModelView):
    column_list = ['id', 'name', 'orbital_period', 'rotation_period', 'diameter', 'gravity', 'climate', 'terrain', 'surface_water', 'population']

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(CustomPlanetsModelView(Planets, db.session))
    admin.add_view(CustomCharactersModelView(Characters, db.session))
    # admin.add_view(ModelView(StarShips, db.session))
    admin.add_view(ModelView(Favorites, db.session))
    

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))