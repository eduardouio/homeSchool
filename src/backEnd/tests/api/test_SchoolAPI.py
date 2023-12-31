import pytest
from django.urls import reverse
from tests.api.BaseTest import BaseTest
from schools.models import School
from accounts.models import CustomUserModel as User


@pytest.mark.django_db
class TestSchoolCreateAPIView(BaseTest):

    @pytest.fixture
    def url(self):
        url = reverse('api:api-add-school')
        return url

    def test_create_school(self, client_logged, url):
        data = {
            "name": "Test",
            "address": "Test",
            "phone": "123456789",
            "id_owner": 2,
            "email": "gvc@d.com",
            "ami_code": "123456789",
            "state": "pichincha",
            "city": "quito",
        }
        response = client_logged.post(url, data=data)
        assert response.status_code == 201
        # comprobamos el registro en la base de datos
        school = School.objects.filter(
            name=data['name'],
            address=data['address']
        ).first()
        assert school is not None
        assert school.phone == data['phone']
        assert school.id_owner.pk == data['id_owner']
        assert school.address == data['address']
        assert school.email == data['email']
        assert school.ami_code == data['ami_code']

    def test_dont_logged_in_user(self, client_guest, url):
        data = {
            "name": "Test",
        }
        response = client_guest.post(url, data=data)
        assert response.status_code == 403

    def test_incomplete_data(self, url, client_logged):
        data = {
            "name": "Test",
        }
        response = client_logged.post(url, data=data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestDeleteSchoolAPIView(BaseTest):

    @pytest.fixture
    def url(self):
        url = reverse('api:api-delete-school', kwargs={'pk': 1})
        return url

    def test_delete_school(self, url, client_logged):
        user = User.objects.create_user(
            email='test@kjhgf.com',
            password='test',
            role='school'
        )
        school = School.objects.create(
            name="Test-delete",
            address="Test",
            phone="123456789",
            id_owner=user,
            email="gvc@d.com",
            ami_code="123456789",
            state="pichincha",
            city="quito"
        )
        url = url.replace('1', str(school.pk))
        response = client_logged.delete(url)
        assert response.status_code == 204
        # comprobamos el registro en la base de datos
        school_deleted = School.objects.filter(name='Test-delete').first()
        assert school_deleted is None

    def test_dont_logged_in_user(self, client_guest, url):
        response = client_guest.delete(url)
        assert response.status_code == 403

    def test_delete_school_not_found(self, url, client_logged):
        url = url.replace('1', '1000')
        response = client_logged.delete(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestListSchoolsAPIView(BaseTest):

    @pytest.fixture
    def url(self):
        url = reverse('api:api-schools-list')
        return url

    def test_not_authorized(self, client_guest, url):
        pass

    def test_list_schools(self, url, client_logged):
        response = client_logged.get(url)
        assert response.status_code == 200
        response = response.json()
        assert response['count'] > 1
        assert response['results']


@pytest.mark.django_db
class TestUpdateSchoolAPIView(BaseTest):

    @pytest.fixture
    def url(self):
        url = reverse('api:api-update-school', kwargs={'pk': 1})
        return url

    def test_update_school(self, url, client_logged):
        data = {
            "id_school": 1,
            "name": "Test-test",
            "address": "Test-test",
            "phone": "12345998087",
            "email": "gvc@d2.com",
            "ami_code": "1232456789",
            "state": "PICHINCHA",
            "city": "QUITO",
            "id_owner": 2,
        }
        response = client_logged.put(
            url,
            data=data,
            content_type='application/json'
        )
        assert response.status_code == 200
        # comprobamos el registro en la base de datos
        school = School.objects.get(pk=1)
        assert school.name == data['name']
        assert school.address == data['address']
        assert school.phone == data['phone']
        assert school.email == data['email']
        assert school.ami_code == data['ami_code']

    def test_dont_access_user(self, client_guest, url):
        data = {
            "id_school": 1,
        }
        response = client_guest.put(
            url, data=data, content_type='application/json'
        )
        assert response.status_code == 403

    def test_incomplete_data(self, client_guest, url):
        data = {
            "id_school": 1,
            "name": "Test-test"
        }
        response = client_guest.put(
            url, data=data, content_type='application/json'
        )
        assert response.status_code == 403


@pytest.mark.django_db
class TestSchoolDetailAPIView(BaseTest):

    @pytest.fixture
    def url(self):
        url = reverse('api:api-school-detail', kwargs={'pk': 1})
        return url

    def test_get_school(self, url, client_logged):
        response = client_logged.get(url)
        assert response.status_code == 200
        response = response.json()
    
