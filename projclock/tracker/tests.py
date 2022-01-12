from rest_framework.test import APITestCase
from rest_framework import response, status
from tracker.models import Project, ProjectActivity
from django.urls import reverse


class TestProjectHelper(APITestCase):
    """a class that contains helper method to be used by other classes"""

    def authenticate_admin(self):
        """
        a function to create a new user and authenticate it.
        
        """
        account_creation_data = {
            'username': 'admin',
            'password': 'admin',
            'email': 'admin@user.com',
            'is_staff': 1
        }
        login_data = {
            'email': 'admin@user.com',
            'password': 'admin'
        }
        self.client.post(reverse("register"), account_creation_data, format='json')
        response = self.client.post(reverse("login"), login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")
    

    def authenticate_user(self):
        """
        a function to create a new user and authenticate it.
        
        """
        account_creation_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@user.com',
            'is_staff': 0
        }
        login_data = {
            'email': 'test@user.com',
            'password': 'testpassword'
        }
        self.client.post(reverse("register"), account_creation_data, format='json')
        response = self.client.post(reverse("login"), login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

    def create_project(self, single=True):
        """
        method to create a project
        """
        if single:
            request_data = {
                'title': 'Test Project',
                'description': 'Test Project Description',
                'start_date': '2019-01-01',
                'technology': {
                    'technology': 'Python'
                },
                'members': [2]
            }
            project_response = self.client.post(reverse('add_project'), request_data, format='json')
            return project_response
        request_data = {
                'title': 'Test Project',
                'description': 'Test Project Description',
                'start_date': '2019-01-01',
                'technology': {
                    'technology': 'Python'
                },
                'members': [1, 2]
            }
        project_response = self.client.post(reverse('add_project'), request_data, format='json')
        return project_response

    def create_project_activity(self, member=True):
        """method to create activity object"""
        request_data = {
            'project': 1,
            'description': 'Test Project Activity',
            'user': 1,
            'start_time': '2019-01-01'
        }
        project_activity_response = self.client.post(reverse('add_activity'), request_data, format='json')
        return project_activity_response

# Create your tests here.
# class TestProjectUserCase(TestProjectHelper):
#     """
#     test case to test the project creation endpoints

#     """
#     def test_should_not_create_project_with_normal_user(self):
#         """
#         test case to test if the project creation endpoint will fail
#         if the user is not an admin.
#         """
#         self.authenticate_user()
#         project = self.create_project()
#         self.assertEqual(project.status_code, status.HTTP_403_FORBIDDEN)

    
#     def test_should_create_project_with_auth(self):
#         """
#         test case to test if the project creation endpoint will succeed
#         if the user is logged in.
#         """
#         previous_projects_count = Project.objects.all().count()
#         self.authenticate_admin()
#         response = self.create_project()
#         # print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertGreater(Project.objects.all().count(), previous_projects_count)
#         self.assertEqual(response.data['title'], 'Test Project')
#         self.assertEqual(response.data['description'], 'Test Project Description')
#         self.assertEqual(response.data['technology'], {'technology': 'Python'})
        

#     def test_retrives_all_projects_with_auth(self):
#         """
#         test case to test if the project retrival endpoint will succeed
#         if the user is logged in.
#         """
#         self.authenticate_admin()
#         response = self.client.get(reverse('list_projects'), format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         #self.assertIsInstance(response.data['result'], list)
#         response = self.create_project()
#         response = self.client.get(reverse('list_projects'), format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # self.assertIsInstance(response.data[0], list)
#         # print(response.data)

#     def test_retrive_one_project_with_auth(self):
#         """
#         with authendication, check if we can get a created project from the db
#         """
#         self.authenticate_admin()
#         response = self.create_project()
#         response = self.client.get(reverse('list_a_project', kwargs={'id': response.data['id']}), format='json')
#         response.data = dict(response.data[0])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         project = Project.objects.get(id=response.data['id'])
#         self.assertEqual(response.data['title'], 'Test Project')
#         self.assertEqual(response.data['description'], 'Test Project Description')
#         self.assertEqual(response.data['technology'], {'technology': 'Python'})

    
#     def test_update_one_project_with_auth(self):
#         """
#         with authentication, check if we can update a created project from the db
#         """
#         self.authenticate_admin()
#         response = self.create_project()
#         update_data = {
#             'title': 'Test Project Updated',
#             'description': 'Test Project Description Updated',
#             'end_date': '2019-01-01'
#         }
#         response = self.client.patch(reverse('update_project', kwargs={'pk': response.data['id']}), update_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         updated_response = Project.objects.get(id=response.data['id'])
#         print(updated_response)
#         self.assertEqual(updated_response.title, 'Test Project Updated')
#         self.assertEqual(updated_response.description, 'Test Project Description Updated')
#         self.assertEqual(updated_response.is_completed, True)

    
#     def test_delete_one_project_with_auth(self):
#         """check if with authentication, check if an admin can delete a created project from the db
#         """
#         self.authenticate_admin()
#         response = self.create_project()
#         response = self.client.delete(reverse('delete_project', kwargs={'pk': response.data['id']}), format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
class TestProjectActivityUserCase(TestProjectHelper):
    """
    test case to test the project activity endpoints

    """
    def test_should_not_create_project_activity_when_user_not_project_member(self):
        """
        test case to test if the project activity creation endpoint will fail
        if the user is not an admin.
        """
        self.authenticate_user()
        self.authenticate_admin()
        self.create_project()
        project_activity = self.create_project_activity()
        self.assertEqual(project_activity.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_project_activity_when_user_is_project_memeber(self):
        """test case to test if a user can create activities for project
        they are part of"""
        self.authenticate_user()
        self.authenticate_admin()
        self.create_project(single=False)
        self.authenticate_user()
        project_activity = self.create_project_activity()
        self.assertEqual(project_activity.status_code, status.HTTP_201_CREATED)
    
    def test_should_retrive_all_project_activities_when_user_is_activity_owner(self):
        """test case to test if a user can retrieve all activities for project they created"""
        self.authenticate_user()
        self.authenticate_admin()
        self.create_project(single=False)
        self.authenticate_user()
        self.create_project_activity()
        response = self.client.get(reverse('list_activities'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.data = dict(response.data[0])
        self.assertIsInstance(response.data, dict)

    def test_should_delete_activity_when_user_is_activity_owner(self):
        """test case to test if a user can delete activity they created"""
        self.authenticate_user()
        self.authenticate_admin()
        self.create_project(single=False)
        self.authenticate_user()
        response = self.create_project_activity()
        response = self.client.delete(reverse('list_update_delete_activity', kwargs={'pk': response.data['id']}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_should_update_activity_when_user_is_activity_owner(self):
        """test case to test if an activity ownwer can update activity"""
        self.authenticate_user()
        self.authenticate_admin()
        self.create_project(single=False)
        self.authenticate_user()
        response = self.create_project_activity()
        update_data = {
            'title': 'Test Project Activity Updated',
            'end_time'
        }