from django.test import TestCase

class PostAdminTest(TestCase):
    def test_index(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_model_index(self):
        response = self.client.get('/hollow/post/')

        self.assertEqual(response.status_code, 200)
