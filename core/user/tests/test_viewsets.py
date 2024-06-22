from rest_framework import status

from core.fixtures.user import user

class TestUserViewSet:

    endpoint = '/api/user/'

    def test_list(self, client, user):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_retrieve(self, client, user):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint + str(user.public_id) + '/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.public_id.hex

    def test_create(self, client, user):
        client.force_authenticate(user=user)
        response = client.post(self.endpoint)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update(self, client, user):
        client.force_authenticate(user=user)
        data = {
            'first_name': 'Guybrush'
        }
        response = client.patch(self.endpoint + str(user.public_id) + '/', data)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.first_name == 'Guybrush'

