from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Building, Room, Resident
from rest_framework.authtoken.models import Token
from unittest.mock import patch
from oauth2_provider.models import Application  # Add this import


class RoomViewSetTests(APITestCase):
    def setUp(self):
        # Create an admin user and obtain a token
        self.admin_user = User.objects.create_superuser(
            username="adminuser", password="adminpass"
        )
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Create a building for the room
        self.building = Building.objects.create(
            name="Test Building", address="123 Test St"
        )

    def test_create_room(self):
        # Define the room data
        room_data = {
            "building": self.building.id,  # Use the ID of the Building instance
            "room_number": "102",
            "capacity": 3,
        }

        # Make a POST request to create a room
        response = self.client.post("/api/rooms/", room_data, format="json")

        # Check that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the room was created in the database
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(Room.objects.get().room_number, "102")

    def test_get_room(self):
        # Create a room first
        room = Room.objects.create(
            building=self.building, room_number="103", capacity=2
        )

        # Make a GET request to retrieve the room
        response = self.client.get(f"/api/rooms/{room.id}/")

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the room data in the response
        self.assertEqual(response.data["room_number"], "103")
        self.assertEqual(response.data["capacity"], 2)

    def test_create_room_non_admin(self):
        # Create a non-admin user and obtain a token
        non_admin_user = User.objects.create_user(
            username="nonadminuser", password="nonadminpass"
        )
        non_admin_token = Token.objects.create(user=non_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + non_admin_token.key)

        # Define the room data
        room_data = {"building": self.building.id, "room_number": "104", "capacity": 4}

        # Attempt to create a room as a non-admin user
        response = self.client.post("/api/rooms/", room_data, format="json")

        # Check that the response status code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BuildingViewSetTests(APITestCase):
    def setUp(self):
        # Create an admin user and obtain a token
        self.admin_user = User.objects.create_superuser(
            username="adminuser", password="adminpass"
        )
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_building(self):
        # Define the building data
        building_data = {"name": "New Building", "address": "456 New St"}

        # Make a POST request to create a building
        response = self.client.post("/api/buildings/", building_data, format="json")

        # Check that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the building was created in the database
        self.assertEqual(Building.objects.count(), 1)
        self.assertEqual(Building.objects.get().name, "New Building")

    def test_get_building(self):
        # Create a building first
        building = Building.objects.create(
            name="Existing Building", address="789 Existing St"
        )

        # Make a GET request to retrieve the building
        response = self.client.get(f"/api/buildings/{building.id}/")

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the building data in the response
        self.assertEqual(response.data["name"], "Existing Building")
        self.assertEqual(response.data["address"], "789 Existing St")

    def test_create_building_non_admin(self):
        # Create a non-admin user and obtain a token
        non_admin_user = User.objects.create_user(
            username="nonadminuser", password="nonadminpass"
        )
        non_admin_token = Token.objects.create(user=non_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + non_admin_token.key)

        # Define the building data
        building_data = {
            "name": "Unauthorized Building",
            "address": "123 Unauthorized St",
        }

        # Attempt to create a building as a non-admin user
        response = self.client.post("/api/buildings/", building_data, format="json")

        # Check that the response status code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ResidentViewSetTests(APITestCase):
    def setUp(self):
        # Create an admin user and obtain a token
        self.admin_user = User.objects.create_superuser(
            username="adminuser", password="adminpass"
        )
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Create a building and room for the resident
        self.building = Building.objects.create(
            name="Test Building", address="123 Test St"
        )
        self.room = Room.objects.create(
            building=self.building, room_number="101", capacity=2
        )

    def test_create_resident(self):
        # Define the resident data
        resident_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "room": self.room.id,  # Use the ID of the Room instance
            "check_in_date": "2023-01-01",
            "check_out_date": "2023-12-31",
        }

        # Make a POST request to create a resident
        response = self.client.post("/api/residents/", resident_data, format="json")

        # Check that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the resident was created in the database
        self.assertEqual(Resident.objects.count(), 1)
        self.assertEqual(Resident.objects.get().first_name, "John")

    def test_get_resident(self):
        # Create a resident first
        resident = Resident.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            room=self.room,
            check_in_date="2023-01-01",
            check_out_date="2023-12-31",
        )

        # Make a GET request to retrieve the resident
        response = self.client.get(f"/api/residents/{resident.id}/")

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the resident data in the response
        self.assertEqual(response.data["first_name"], "Jane")
        self.assertEqual(response.data["last_name"], "Doe")

    def test_create_resident_non_admin(self):
        # Create a non-admin user and obtain a token
        non_admin_user = User.objects.create_user(
            username="nonadminuser", password="nonadminpass"
        )
        non_admin_token = Token.objects.create(user=non_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + non_admin_token.key)

        # Define the resident data
        resident_data = {
            "first_name": "Unauthorized",
            "last_name": "User",
            "email": "unauthorized@example.com",
            "room": self.room.id,
            "check_in_date": "2023-01-01",
            "check_out_date": "2023-12-31",
        }

        # Attempt to create a resident as a non-admin user
        response = self.client.post("/api/residents/", resident_data, format="json")

        # Check that the response status code is 403 (Forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class OAuth2IntegrationTests(APITestCase):
#     def setUp(self):
#         # Create a superuser (admin) for testing
#         self.admin_user = User.objects.create_superuser(
#             username="adminuser", password="adminpass", email="admin@example.com"
#         )

#         # Create a test OAuth2 client
#         self.client_app = Application.objects.create(
#             name="Test Client",
#             user=self.admin_user,
#             client_type=Application.CLIENT_CONFIDENTIAL,
#             authorization_grant_type=Application.GRANT_PASSWORD,
#             client_id="Fb4YtVmpbmOEtw829DjJCUgdXLEAvgN5GR98IYkU",  # Use a unique client ID
#             client_secret="pbkdf2_sha256$870000$YGbiM2uivSgGlNn4qLLEen$Mn2S1COOlTuo0Ydt0j6mwud8zi0pUDPCOpL+tK8ZbVw=",  # Use a unique client secret
#         )

#         self.client_id = self.client_app.client_id
#         self.client_secret = self.client_app.client_secret

#         # Create a building for the room
#         self.building = Building.objects.create(
#             name="Test Building", address="123 Test St"
#         )
#         self.room = Room.objects.create(
#             building=self.building, room_number="101", capacity=2
#         )

#     @patch("requests.post")  # Update this to the correct module path
#     def test_obtain_access_token(self, mock_post):
#         # Mock the response from the OAuth2 server
#         mock_post.return_value.status_code = 200
#         mock_post.return_value.json.return_value = {
#             "access_token": "mock_access_token",
#             "token_type": "Bearer",
#             "expires_in": 3600,
#         }

#         # Now call your method that requests the token
#         response = self.client.post(
#             "/o/token/",
#             {
#                 "grant_type": "password",
#                 "username": "adminuser",
#                 "password": "adminpass",
#                 "client_id": self.client_id,
#                 "client_secret": self.client_secret,
#             },
#         )

#         # Assert that the response is as expected
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(
#             "access_token", response.json()
#         )  # Use response.json() instead of response.data

#     def test_access_protected_resource_with_token(self):
#         # First, obtain an access token
#         token_response = self.client.post(
#             "/o/token/",
#             {
#                 "grant_type": "password",
#                 "username": "adminuser",
#                 "password": "adminpass",
#                 "client_id": self.client_id,
#                 "client_secret": self.client_secret,
#             },
#         )

#         access_token = token_response.json()[
#             "access_token"
#         ]  # Use token_response.json() instead of token_response.data

#         # Use the access token to access a protected resource
#         self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
#         response = self.client.get("/api/rooms/")  # Adjust the endpoint as necessary

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_access_protected_resource_without_token(self):
#         # Attempt to access a protected resource without an access token
#         response = self.client.get("/api/rooms/")  # Adjust the endpoint as necessary

#         # Check that the response status code is 401 (Unauthorized)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
