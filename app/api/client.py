import requests
from app.config import Config
from app.logger import setup_logger

class RemnawaveAPIClient:
    def __init__(self):
        self.base_url = Config.REMNAWAVE_API_URL
        self.token = Config.REMNAWAVE_API_TOKEN
        self.logger = setup_logger()
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def get_users(self, size=25, start=0):
        response = requests.get(
            f'{self.base_url}/api/users',
            headers=self.headers,
            params={'size': size, 'start': start}
        )
        response.raise_for_status()
        return response.json()

    def get_user_by_username(self, username):
        response = requests.get(
            f'{self.base_url}/api/users/by-username/{username}',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def update_user(self, user_uuid, data):
        response = requests.patch(
            f'{self.base_url}/api/users',
            headers=self.headers,
            json={'uuid': user_uuid, **data}
        )
        response.raise_for_status()
        return response.json()

    def disable_user(self, user_uuid):
        response = requests.post(
            f'{self.base_url}/api/users/{user_uuid}/actions/disable',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def reset_traffic(self, user_uuid):
        response = requests.post(
            f'{self.base_url}/api/users/{user_uuid}/actions/reset-traffic',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_inbounds(self):
        response = requests.get(
            f'{self.base_url}/api/inbounds',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def add_inbound_to_users(self, inbound_uuid):
        response = requests.post(
            f'{self.base_url}/api/inbounds/bulk/add-to-users',
            headers=self.headers,
            json={'inboundUuid': inbound_uuid}
        )
        response.raise_for_status()
        return response.json()

    def add_inbound_to_nodes(self, inbound_uuid):
        response = requests.post(
            f'{self.base_url}/api/inbounds/bulk/add-to-nodes',
            headers=self.headers,
            json={'inboundUuid': inbound_uuid}
        )
        response.raise_for_status()
        return response.json()

    def get_system_stats(self):
        response = requests.get(
            f'{self.base_url}/api/system/stats',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_nodes_stats(self):
        response = requests.get(
            f'{self.base_url}/api/system/stats/nodes',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
