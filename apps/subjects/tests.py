"""Subjects app tests."""
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from apps.students.models import Student
from apps.teachers.models import Teacher
from apps.subjects.models import Subject, Registration
from rest_framework.test import APITestCase

class SubjectsAPITestCase(APITestCase):
    """Subjects API test case."""
    def setUp(self):
        """Configuración inicial antes de todas las pruebas."""
        # Datos iniciales
        # Crear un usuario para las pruebas
        self.user = User.objects.create_user(username='testuser', 
                                            password='password123')
        refresh = RefreshToken.for_user(self.user)
        self.token = refresh.access_token
        self.student = Student.objects.create(first_name='Test',
                                             last_name='Student',
                                             email='test.student@test.com',
                                             birth_date='1999-01-01')
        self.teacher = Teacher.objects.create(first_name='Test',
                                             last_name='Teacher',
                                             email='test.teacher@test.com')
        self.subject = Subject.objects.create(name='Test Subject',
                                             code='TS001',
                                             teacher=self.teacher)
        self.subject_2 = Subject.objects.create(name='Test Subject 2',
                                               code='TS002',
                                               teacher=self.teacher)
        self.subject_2.requirements.set([self.subject])
        self.subject_2.save()
        self.registration = Registration.objects.create(student=self.student,
                                                       subject=self.subject)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_subjects_registration(self):
        """Prueba registrar materias."""
        data = {
            "student": 1,
            "subjects": [1]
        }
        response = self.client.post('/api/registrations/multiple/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_subjects_registration(self):
        """Prueba listar materias inscritas."""
        response = self.client.get('/api/registrations/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_error_subjects_registration(self):
        """Prueba error al registrar materias."""
        data = {
            "student": 1,
            "subjects": [2]
        }
        response = self.client.post(f'/api/registrations/multiple/', data, format='json')
        self.assertEqual(response.status_code, 400)
