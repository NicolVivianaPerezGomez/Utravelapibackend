from django.test import TestCase
from rest_framework.test import APIClient

from ..models import RutaTuristica


class RutaAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.list_url = '/api/utravel/rutas/'
		self.create_url = '/api/utravel/rutas/crear/'
		self.ruta1 = RutaTuristica.objects.create(
			rut_nombre='R1',
			rut_descripcion='desc1',
			rut_duracion='1h',
			rut_estado='1'
		)

	def test_list_returns_only_active(self):
		RutaTuristica.objects.create(
			rut_nombre='R_inactive',
			rut_descripcion='x',
			rut_duracion='1',
			rut_estado='0'
		)

		res = self.client.get(self.list_url)
		self.assertEqual(res.status_code, 200)

		data = res.json()
		names = [r['rut_nombre'] for r in data]
		self.assertIn('R1', names)
		self.assertNotIn('R_inactive', names)

	def test_create_and_unique_validation(self):
		payload = {'rut_nombre': 'R2', 'rut_descripcion': 'd2', 'rut_duracion': '2h'}
		res = self.client.post(self.create_url, payload, format='json')
		self.assertEqual(res.status_code, 201)

		res2 = self.client.post(self.create_url, payload, format='json')
		self.assertEqual(res2.status_code, 400)
		self.assertIn('rut_nombre', res2.json())

	def test_retrieve_update_delete_logic(self):
		res = self.client.get(f'/api/utravel/rutas/{self.ruta1.rut_id}/')
		self.assertEqual(res.status_code, 200)

		update_payload = {'rut_nombre': 'R1new', 'rut_descripcion': 'desc1 updated', 'rut_duracion': '2h'}
		res2 = self.client.put(f'/api/utravel/rutas/{self.ruta1.rut_id}/actualizar/', update_payload, format='json')
		self.assertEqual(res2.status_code, 200)
		self.ruta1.refresh_from_db()
		self.assertEqual(self.ruta1.rut_nombre, 'R1new')

		res3 = self.client.delete(f'/api/utravel/rutas/{self.ruta1.rut_id}/eliminar/')
		self.assertEqual(res3.status_code, 200)
		self.ruta1.refresh_from_db()
		self.assertEqual(self.ruta1.rut_estado, '0')

		res4 = self.client.get(self.list_url)
		names = [r['rut_nombre'] for r in res4.json()]
		self.assertNotIn('R1new', names)
