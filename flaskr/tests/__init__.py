import flask
from flaskr.modelos.modelos import Usuario
import unittest
from flask import Flask

from app import db

class BaseTestClass(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_test_app('testing')
        # self.client = flask.app.test_client()

        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.init_app(self.app)
            db.create_all()
            # BaseTestClass.create_user('usuario1', '123456')
            # BaseTestClass.create_user('usuario2', '123456')


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()

    @staticmethod
    def create_user(name, contrasena):
        user =  Usuario(name, contrasena)
        db.session.add(user)
        db.session.commit()
        return user

    def login(self, name, contrasena):
        return self.client.post('/login', data=dict(
            nombre=name,
            contrasena=contrasena
        ), follow_redirects=True)



def create_test_app(config_name):
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial_canciones_test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY']='frase-secreta-2'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app
