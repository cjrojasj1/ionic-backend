from flaskr.tests import BaseTestClass
import unittest
import json
from flaskr.app import app

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
                content_type='application/json', follow_redirects=True
            )
            self.assertEqual(
                result.status_code,
                400
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
                content_type='application/json', follow_redirects=True
            )
            self.assertEqual(
                result.status_code,
                400
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
                content_type='application/json', follow_redirects=True
            )
            self.assertEqual(
                result.status_code,
                400
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
                content_type='application/json', follow_redirects=True
            )
            self.assertEqual(
                result.status_code,
                400
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
                content_type='application/json', follow_redirects=True
            )
            self.assertEqual(
                result.status_code,
                400
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
                content_type='application/json', follow_redirects=True
            )
            self.assertEqual(
                result.status_code,
                400
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
                content_type='application/json', follow_redirects=True
            )
            self.assertEqual(
                result.status_code,
                400
            )

if __name__ == '__main__':
    unittest.main()
