from flaskr.tests import BaseTestClass
import unittest
import json
from app import app, db
from flask import request

ROUTE_POST = '/recurso/compartido'
class RecursosCompartidosTestCase(BaseTestClass):

    def test_usuario_destinatario_vacio(self):
        with app.test_client() as client:
            result = client.post(
                ROUTE_POST,
                data=json.dumps(dict(
                    usuario_origen_id=2,
                    usuario_destino=None,
                    id_recurso= 3,
                    tipo_recurso="ALBUM"
                )),
                content_type='application/json'
            )
            self.assertEqual(
                result.data,
                b'"Error. El usuario destinatario o de origen no puede ser vacio"\n'
            )

    def test_usuario_origen_vacio(self):
        with app.test_client() as client:
            result = client.post(
                ROUTE_POST,
                data=json.dumps(dict(
                    usuario_origen_id=None,
                    usuario_destino="usuario1",
                    id_recurso= 3,
                    tipo_recurso="ALBUM"
                )),
                content_type='application/json'
            )
            self.assertEqual(
                result.data,
                b'"Error. El usuario destinatario o de origen no puede ser vacio"\n'
            )

    def test_tipo_recurso_vacio(self):
        with app.test_client() as client:
            result = client.post(
                ROUTE_POST,
                data=json.dumps(dict(
                    usuario_origen_id=2,
                    usuario_destino="usuario1",
                    id_recurso= 3,
                    tipo_recurso=None
                )),
                content_type='application/json'
            )
            self.assertEqual(
                result.data,
                b'"Error. El tipo de recurso no puede ser vacio"\n'
            )

    def test_id_recurso_vacio(self):
        with app.test_client() as client:
            result = client.post(
                ROUTE_POST,
                data=json.dumps(dict(
                    usuario_origen_id=2,
                    usuario_destino= "usuario1",
                    id_recurso= None,
                    tipo_recurso="ALBUM"
                )),
                content_type='application/json'
            )
            self.assertEqual(
                result.data,
                b'"Error. El id de recurso no puede ser vacio"\n'
            )

    def test_usuario_destinatario_numero(self):
        with app.test_client() as client:
            result = client.post(
                ROUTE_POST,
                data=json.dumps(dict(
                    usuario_origen_id=2,
                    usuario_destino=123456,
                    id_recurso= 3,
                    tipo_recurso="ALBUM"
                )),
                content_type='application/json'
            )
            self.assertEqual(
                result.data,
                b'"Error. El usuario destinatario debe ser un texto"\n'
            )

    def test_usuario_origen_texto(self):
        with app.test_client() as client:
            result = client.post(
                ROUTE_POST,
                data=json.dumps(dict(
                    usuario_origen_id="abc",
                    usuario_destino="usuario1,usuario2",
                    id_recurso= 3,
                    tipo_recurso="ALBUM"
                )),
                content_type='application/json'
            )
            self.assertEqual(
                result.data,
                b'"Error. El id de usuario origen debe ser un numero"\n'
            )

    def test_tipo_recurso_invalido(self):
        with app.test_client() as client:
            result = client.post(
                ROUTE_POST,
                data=json.dumps(dict(
                    usuario_origen_id=1,
                    usuario_destino="usuario1,usuario2",
                    id_recurso= 3,
                    tipo_recurso="ALBUM2"
                )),
                content_type='application/json'
            )
            self.assertEqual(
                result.data,
                b'"Error. El tipo de recurso debe ser ALBUM o CANCION"\n'
            )

if __name__ == '__main__':
    unittest.main()
