import pytest
from rest_framework.test import APIClient

from apps.models import Blog, Question, Answer
from authentication.models import User


class TestBlog:
    @pytest.fixture
    def client(self):
        datas = [{
            'id': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'doe@gmail.com',
            'password': '1'
        }]
        user = User.objects.create_user(**datas[0])
        datas.append({
            'id': 2,
            'author': user,
            'title': 'Test',
            'content': 'Test',
            'tags': 'test',
        })
        Blog.objects.create(**datas[1])
        return APIClient()

    def login(self, client):
        data = {
            'email': 'doe@gmail.com',
            'password': '1'
        }
        response = client.post('/api/v1/login/', data, format='json')
        token = response.data.get('access')
        return {"Authorization": f"Bearer {token}"}

    @pytest.mark.django_db
    def test_blog_creat(self, client):
        data = {
            'title': 'Test',
            'content': 'Test',
            'tags': 'test',
        }
        response = client.post('/api/v1/blog-create', data, headers=self.login(client), format='json')
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data.get('title') == data.get('title'), 'Wrong title not found'

    @pytest.mark.django_db
    def test_blog_list(self, client):
        response = client.get('/api/v1/blogs', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert isinstance(response.data, list) == True, 'Bad response'

    @pytest.mark.django_db
    def test_blog_detail(self, client):
        response = client.get('/api/v1/blog-detail/2', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data.get('title') == 'Test', 'Wrong title not found'

    @pytest.mark.django_db
    def test_blog_update(self, client):
        data = {'tags': 'post'}
        response = client.patch('/api/v1/blog-update/2', data, headers=self.login(client), format='json')
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data.get('tags') == data.get('tags'), 'Wrong tags not found'

    @pytest.mark.django_db
    def test_blog_delete(self, client):
        response = client.delete('/api/v1/blog-delete/2', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'


class TestQuestion:
    @pytest.fixture
    def client(self):
        datas = [{
            'id': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'doe@gmail.com',
            'password': '1'
        }]
        user = User.objects.create_user(**datas[0])
        datas.append({
            'id': 2,
            'author': user,
            'title': 'Test',
            'content': 'Test',
        })
        Question.objects.create(**datas[1])
        return APIClient()

    def login(self, client):
        data = {
            'email': 'doe@gmail.com',
            'password': '1'
        }
        response = client.post('/api/v1/login/', data, format='json')
        token = response.data.get('access')
        return {"Authorization": f"Bearer {token}"}

    @pytest.mark.django_db
    def test_question_create(self, client):
        data = {
            'title': 'Test',
            'content': 'Test',
        }
        response = client.post('/api/v1/question-create', data, headers=self.login(client), format='json')
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data.get('title') == data.get('title'), 'Wrong title not found'

    @pytest.mark.django_db
    def test_question_list(self, client):
        response = client.get('/api/v1/questions', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert isinstance(response.data, list) == True, 'Bad response'

    @pytest.mark.django_db
    def test_question_detail(self, client):
        response = client.get('/api/v1/question-detail/2', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data.get('title') == 'Test', 'Wrong title not found'

    @pytest.mark.django_db
    def test_question_update(self, client):
        data = {'title': 'question1'}
        response = client.patch('/api/v1/question-update/2', data, headers=self.login(client), format='json')
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data.get('title') == data.get('title'), 'Wrong title not found'

    @pytest.mark.django_db
    def test_question_delete(self, client):
        response = client.delete('/api/v1/question-delete/2', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'


class TestAnswer:
    @pytest.fixture
    def client(self):
        datas = [{
            'id': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'doe@gmail.com',
            'password': '1'
        }]
        user = User.objects.create_user(**datas[0])
        datas.append({
            'id': 2,
            'author': user,
            'title': 'Test',
            'content': 'Test',
        })
        question = Question.objects.create(**datas[1])
        datas.append({
            'id': 2,
            'question': question,
            'content': 'Test',
            'author': user,
        })
        Answer.objects.create(**datas[2])
        return APIClient()

    def login(self, client):
        data = {
            'email': 'doe@gmail.com',
            'password': '1'
        }
        response = client.post('/api/v1/login/', data, format='json')
        token = response.data.get('access')
        return {"Authorization": f"Bearer {token}"}

    @pytest.mark.django_db
    def test_answer_create(self, client):
        data = {
            'question': 2,
            'content': 'Test',
        }
        response = client.post('/api/v1/answer-create', data, headers=self.login(client), format='json')
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data.get('title') == data.get('title'), 'Wrong title not found'

    @pytest.mark.django_db
    def test_answer_list(self, client):
        response = client.get('/api/v1/answers', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert isinstance(response.data, list) == True, 'Bad response'

    @pytest.mark.django_db
    def test_answer_detail(self, client):
        response = client.get('/api/v1/answer-detail/2', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data.get('question') == 2, 'Wrong title not found'

    @pytest.mark.django_db
    def test_answer_update(self, client):
        data = {'content': 'answer1'}
        response = client.patch('/api/v1/answer-update/2', data, headers=self.login(client), format='json')
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
        assert response.data.get('content') == data.get('content'), 'Wrong title not found'

    @pytest.mark.django_db
    def test_answer_delete(self, client):
        response = client.delete('/api/v1/answer-delete/2', headers=self.login(client))
        assert 200 <= response.status_code < 300, f'Bad request {response.data}'
