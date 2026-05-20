import requests

BASE_URL = "https://jsonplaceholder.typicode.com/users"


class ApiClient:

    @staticmethod
    def get_users():
        response = requests.get(BASE_URL)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_user(data):
        response = requests.post(BASE_URL, json=data)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def update_user(user_id, data):
        response = requests.put(f"{BASE_URL}/{user_id}", json=data)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def delete_user(user_id):
        response = requests.delete(f"{BASE_URL}/{user_id}")
        response.raise_for_status()
        return True