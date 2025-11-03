import pytest
from rest_framework.test import APIClient

from authentication.models import User, Follow


class TestUser:
    @pytest.fixture
    def client(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@gmail.com',
            'password': '1'
        }
        User.objects.create_user(**user_data)
        return APIClient()

    @pytest.mark.django_db
    def test_register(self, client):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johnson',
            'email': 'doe@gmail.com',
            'password': '1233g'
        }
        response = client.post('/api/v1/register/', data, format='json')
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data['message'] == 'Tasdiqlash kodi jo‘natildi', 'This not true massage'

    @pytest.mark.django_db
    def test_login(self, client):
        data = {
            'email': 'john@gmail.com',
            'password': '1'
        }
        response = client.post('/api/v1/login/', data, format='json')
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data.get('access'), 'Access token not found'


class TestFollowers:
    @pytest.fixture
    def client(self):
        data = [
            {
                'id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'johndoe',
                'email': 'doe@gmail.com',
                'password': '1'
            },
            {
                'id': 2,
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'doejohn',
                'email': 'john@gmail.com',
                'password': '1'
            },
            {
                'id': 3,
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'johnes',
                'email': 'johnson@gmail.com',
                'password': '1'
            }

        ]

        user1 = User.objects.create_user(**data[0])
        user2 = User.objects.create_user(**data[1])
        Follow.objects.create(follower=user1, following=user2)
        return APIClient()

    def login(self, client):
        data = {
            'email': 'john@gmail.com',
            'password': '1'
        }
        response = client.post('/api/v1/login/', data, format='json')
        token = response.data.get('access')
        return {"Authorization": f"Bearer {token}"}

    @pytest.mark.django_db
    def test_following(self, client):
        data = {'following': 1}
        response = client.post('/api/v1/following/', data, headers=self.login(client), format='json')
        assert 200 <= response.status_code < 302, f'Bad request {response.data}'
        assert response.data.get('following') == data.get('following'), 'Wrong following not found'

    @pytest.mark.django_db
    def test_followers_list(self, client):
        response = client.get('/api/v1/follows/list/', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert isinstance(response.data, list) == True, 'Bad response'

    @pytest.mark.django_db
    def test_delete_follower(self, client):
        response = client.delete('/api/v1/following/delete/2', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request'
