from flask import request
from sqlalchemy.orm import query
from flaskr.modelos.modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema, RecursoCompartido, RecursoCompartidoSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
album_schema = AlbumSchema()
recurso_compartido_schema = RecursoCompartidoSchema()


class VistaCancionesUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.canciones.append(nueva_cancion)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene una cancion con dicho nombre',409

        return cancion_schema.dump(nueva_cancion)

    # @jwt_required()

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        propios = []

        for c in usuario.canciones:
            propios.append(c)

        # compartidos = []
        for c in usuario.compartidos:
            if c.cancion_id != None :
                cc = Cancion.query.filter(Cancion.id == c.cancion_id).first()
                nueva_cancion = Cancion(titulo=cc.titulo, minutos=cc.titulo, segundos=cc.titulo, interprete=cc.titulo, propia='False')
                #cc.propia = 'False'
                propios.append(nueva_cancion)

        return [cancion_schema.dump(ca) for ca in propios]

class VistaCancion(Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))

    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get("titulo",cancion.titulo)
        cancion.minutos = request.json.get("minutos",cancion.minutos)
        cancion.segundos = request.json.get("segundos",cancion.segundos)
        cancion.interprete = request.json.get("interprete",cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)

    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return '',204

class VistaAlbumesCanciones(Resource):
    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        return [album_schema.dump(al) for al in cancion.albumes]

class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity = nuevo_usuario.id)
        return {"mensaje":"usuario creado exitosamente", "token":token_de_acceso}


    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204

class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe.", 400
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}

class VistaAlbumesUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"], propio=1)
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre',409

        return album_schema.dump(nuevo_album)

    # @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        propios = []
        for a in usuario.albumes:
            propios.append(a)

        for c in usuario.compartidos:
            if c.album_id != None :
                ac = Album.query.filter(Album.id == c.album_id).first()
                nuevo_album = Album(titulo=ac.titulo, anio=ac.anio, descripcion=ac.descripcion, medio=ac.medio, propio=0)
                #ac.propio = 0
                propios.append(nuevo_album)

        return [album_schema.dump(al) for al in propios]

class VistaUsuario(Resource):
    def get(self, id_usuario):
        return usuario_schema.dump(Usuario.query.get_or_404(id_usuario))
class VistaCancionesAlbum(Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)

        if "id_cancion" in request.json.keys():

            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea',404
        else:
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]

class VistaAlbum(Resource):

    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))

    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get("titulo",album.titulo)
        album.anio = request.json.get("anio", album.anio)
        album.descripcion = request.json.get("descripcion", album.descripcion)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)

    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '',204

class VistaUsuarios(Resource):

    def get(self):
        return [usuario_schema.dump(u) for u in Usuario.query.all()]

class VistaAlbumes(Resource):

    def get(self):
        return [album_schema.dump(a) for a in Album.query.all()]

class VistaRecursosCompartidos(Resource):

    def get(self):
        return [recurso_compartido_schema.dump(rc) for rc in RecursoCompartido.query.all()]

    # @jwt_required()
    def post(self):

        usuario_destino = request.json["usuario_destino"]
        usuario_origen_id = request.json["usuario_origen_id"]
        tipo_recurso = request.json["tipo_recurso"]
        id_recurso = request.json["id_recurso"]

        if usuario_destino == None or usuario_origen_id == None:
            db.session.rollback()
            return "Error. El usuario destinatario o de origen no puede ser vacio", 400

        if type(usuario_destino) != str:
            db.session.rollback()
            return "Error. El usuario destinatario debe ser un texto", 400

        if type(usuario_origen_id) != int:
            db.session.rollback()
            return "Error. El id de usuario origen debe ser un numero", 400

        usuario_o = Usuario.query.filter(Usuario.id == usuario_origen_id).first()
        if usuario_o is None:
            db.session.rollback()
            return "El usuario origen no existe", 400

        if tipo_recurso == None:
            db.session.rollback()
            return "Error. El tipo de recurso no puede ser vacio", 400

        if tipo_recurso != "ALBUM" and tipo_recurso != "CANCION":
            db.session.rollback()
            return "Error. El tipo de recurso debe ser ALBUM o CANCION", 400

        if id_recurso == None:
            db.session.rollback()
            return "Error. El id de recurso no puede ser vacio", 400

        usuarios_destinos = usuario_destino.split(',')
        print(usuarios_destinos)
        for ud in usuarios_destinos:
            usuario_d = Usuario.query.filter(Usuario.nombre == ud).first()
            if usuario_d is None:
                if tipo_recurso == "ALBUM":
                    db.session.rollback()
                    return 'No se puede compartir el álbum porque una o más personas no se encuentran registradas en Ionic.', 400
                else:
                    db.session.rollback()
                    return 'No se puede compartir la canción porque una o más personas no se encuentran registradas en Ionic.', 400

            recurso_compartido = RecursoCompartido(
                tipo_recurso= tipo_recurso,
                usuario_origen_id=usuario_origen_id,
                usuario_destino_id=usuario_d.id,
            )
            if tipo_recurso == "ALBUM":
                recurso_compartido.album_id = id_recurso
            else:
                recurso_compartido.cancion_id = id_recurso

            db.session.add(recurso_compartido)

        db.session.commit()
        return recurso_compartido_schema.dump(recurso_compartido)


class VistaRecursoCompartido(Resource):

    def get(self, id_recurso_compartido):
        return recurso_compartido_schema.dump(RecursoCompartido.query.get_or_404(id_recurso_compartido))

    def delete(self, id_recurso_compartido):
        recurso_compartido = RecursoCompartido.query.get_or_404(id_recurso_compartido)
        db.session.delete(recurso_compartido)
        db.session.commit()
        return '',204
class VistaAlbumUsuariosCompartidos(Resource):

    def get(self, id_album):
        recurso_compartido = RecursoCompartido.query.filter(RecursoCompartido.album_id == id_album).group_by(RecursoCompartido.usuario_destino_id).all()
        usuarios = []
        for rc in recurso_compartido:
            u = Usuario.query.filter(Usuario.id == rc.usuario_destino_id).first()
            usuarios.append(u)
        return [usuario_schema.dump(u) for u in usuarios]

class VistaCancionUsuariosCompartidos(Resource):

    def get(self, id_cancion):
        recurso_compartido = RecursoCompartido.query.filter(RecursoCompartido.cancion_id == id_cancion).group_by(RecursoCompartido.usuario_destino_id).all()
        usuarios = []
        for rc in recurso_compartido:
            u = Usuario.query.filter(Usuario.id == rc.usuario_destino_id).first()
            usuarios.append(u)
        return [usuario_schema.dump(u) for u in usuarios]
