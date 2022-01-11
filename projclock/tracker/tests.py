from rest_framework.test import APITestCase
from rest_framework import status
from tracker.models import Project, ProjectActivity
from django.urls import reverse


# Create your tests here.
class TestTrackerUserCase(APITestCase):
    """
    test case to test the project creation endpoints

    """

    def authenticate(self):
        """
        a function to create a new user and authenticate it.
        
        """
        account_creation_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@user.com',
            'is_staff': 1
        }
        login_data = {
            'email': 'test@user.com',
            'password': 'testpassword'
        }
        self.client.post(reverse("register"), account_creation_data, format='json')
        response = self.client.post(reverse("login"), login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")


    def test_should_not_create_project_with_out_auth(self):
        """
        test case to test if the project creation endpoint will fail
        if the user is not logged in.
        """
        request_data = {
            'name': 'Test Project',
            'description': 'Test Project Description',
            'start_date': '2019-01-01',
            'technology': {
                'technology': 'Python'
            },
            'members': [1, 2]
        }
        project = self.client.post(reverse('add_project'), request_data, format='json')
        self.assertEqual(project.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_should_create_project_with_auth(self):
        """
        test case to test if the project creation endpoint will succeed
        if the user is logged in.
        """
        previous_projects_count = Project.objects.all().count()
        self.authenticate()
        request_data = {
            'title': 'Test Project',
            'description': 'Test Project Description',
            'start_date': '2019-01-01',
            'technology': {
                'technology': 'Python'
            },
            'members': [1]
        }
        response = self.client.post(reverse('add_project'), request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(Project.objects.all().count(), previous_projects_count)
        self.assertEqual(response.data['title'], 'Test Project')
        self.assertEqual(response.data['description'], 'Test Project Description')
        self.assertEqual(response.data['technology'], {'technology': 'Python'})
        

    def test_retrives_all_projects_with_auth(self):
        """
        test case to test if the project retrival endpoint will succeed
        if the user is logged in.
        """
        self.authenticate()
        response = self.client.get(reverse('list_projects'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertIsInstance(response.data['result'], list)
        print(response.data)
        
        request_data = {
            'name': 'Test Project',
            'description': 'Test Project Description',
            'start_date': '2019-01-01',
            'technology': {
                'technology': 'Python'
            },
            'members': [1, 2]
        }
        self.client.post(reverse('add_project'), request_data, format='json')
        response = self.client.get(reverse('list_projects'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIsInstance(response.data[0], list)
        print(response.data)