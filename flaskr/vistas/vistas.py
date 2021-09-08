from flask import request
from flaskr.modelos.modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema, RecursoCompartido, RecursoCompartidoSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
album_schema = AlbumSchema()
recurso_compartido_schema = RecursoCompartidoSchema()


class VistaCanciones(Resource):

    def post(self):
        nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
        db.session.add(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

    def get(self):
        return [cancion_schema.dump(ca) for ca in Cancion.query.all()]

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
            return "El usuario no existe", 400
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}

class VistaAlbumesUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre',409

        return album_schema.dump(nuevo_album)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [album_schema.dump(al) for al in usuario.albumes]

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

    def post(self):

        usuario_destino = request.json["usuario_destino"]
        usuario_origen_id = request.json["usuario_origen_id"]
        tipo_recurso = request.json["tipo_recurso"]
        id_recurso = request.json["id_recurso"]

        if usuario_destino == None or usuario_origen_id == None:
            return "Error. El usuario destinatario o de origen no puede ser vacio", 400

        if type(usuario_destino) != str:
            return "Error. El usuario destinatario debe ser un texto", 400

        if type(usuario_origen_id) != int:
            return "Error. El id de usuario origen debe ser un numero", 400

        usuario_o = Usuario.query.filter(Usuario.id == usuario_origen_id).first()
        if usuario_o is None:
            return "El usuario destino no existe", 400

        if tipo_recurso == None:
            return "Error. El tipo de recurso no puede ser vacio", 400

        if tipo_recurso != "ALBUM" and tipo_recurso != "CANCION":
            return "Error. El tipo de recurso debe ser ALBUM o CANCION", 400

        if id_recurso == None:
            return "Error. El id de recurso no puede ser vacio", 400

        usuarios_destinos = usuario_destino.split(',')
        for ud in usuarios_destinos:
            usuario_d = Usuario.query.filter(Usuario.nombre == ud).first()
            if usuario_d is None:
                return "El usuario destino " + Usuario.nombre + " no existe", 400

            recurso_compartido = RecursoCompartido(
                tipo_recurso= tipo_recurso,
                usuario_origen_id=usuario_origen_id,
                usuario_destino_id=usuario_d.id,
            )
            if tipo_recurso == "ALBUM":
                recurso_compartido.album_id = id_recurso
            else:
                recurso_compartido.cancion_id = id_recurso

        try:
            db.session.commit()
            db.session.add(recurso_compartido)
            return "Recurso compartido correctamente"
        except IntegrityError:
            db.session.rollback()
            return "Error", 400

class VistaRecursoCompartido(Resource):

    def get(self, id_recurso_compartido):
        return recurso_compartido_schema.dump(RecursoCompartido.query.get_or_404(id_recurso_compartido))

    def delete(self, id_recurso_compartido):
        recurso_compartido = RecursoCompartido.query.get_or_404(id_recurso_compartido)
        db.session.delete(recurso_compartido)
        db.session.commit()
        return '',204
