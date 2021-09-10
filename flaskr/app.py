from flaskr import create_app
from flask_restful import Api
from flaskr.modelos.modelos import db
from flaskr.vistas.vistas import VistaCancionesUsuario, VistaCancion, VistaSignIn, VistaAlbum, VistaAlbumesUsuario, VistaCancionesAlbum, VistaLogIn, VistaAlbumesCanciones, VistaRecursoCompartido, VistaRecursosCompartidos, VistaUsuarios, VistaUsuario, VistaAlbumes, VistaAlbumUsuariosCompartidos, VistaCancionUsuariosCompartidos
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)

api = Api(app)
api.add_resource(VistaCancionesUsuario, '/usuario/<int:id_usuario>/canciones')
api.add_resource(VistaCancion, '/cancion/<int:id_cancion>')
api.add_resource(VistaAlbumesCanciones, '/cancion/<int:id_cancion>/albumes')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/logIn')
api.add_resource(VistaAlbumesUsuario, '/usuario/<int:id_usuario>/albumes')
api.add_resource(VistaAlbum, '/album/<int:id_album>')
api.add_resource(VistaCancionesAlbum, '/album/<int:id_album>/canciones')
api.add_resource(VistaRecursosCompartidos, '/recurso/compartido')
api.add_resource(VistaAlbumUsuariosCompartidos, '/recurso/compartido/<int:id_album>/usuario')
api.add_resource(VistaCancionUsuariosCompartidos, '/recurso/cancion/<int:id_cancion>/usuario')
api.add_resource(VistaRecursoCompartido, '/recurso/compartido/<int:id_recurso_compartido>')
api.add_resource(VistaUsuarios, '/usuarios')
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>')
api.add_resource(VistaAlbumes, '/albumes')

jwt = JWTManager(app)
