import requests
import json

class SophosAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.data_region = None
        self.id_type = None
        self.id = None

    def _save_to_json(self, data, filename):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def get_access_token(self):
        url_token = "https://id.sophos.com/api/v2/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "token"
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = requests.post(url_token, data=data, headers=headers)
            response.raise_for_status()
            self.access_token = response.json().get("access_token")
            print("Access Token retrieved successfully")
            self._save_to_json(response.json(), "access_token.json")
        except requests.exceptions.RequestException as e:
            print("Error retrieving Access Token:", e)
            exit()

    def get_whoami_info(self):
        url_whoami = "https://api.central.sophos.com/whoami/v1"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(url_whoami, headers=headers)
            response.raise_for_status()
            data = response.json()
            self.data_region = data.get("apiHosts", {}).get("dataRegion")
            self.id_type = data.get("idType")
            self.id = data.get("id")
            print(response.status_code, self.data_region, self.id_type, ":", self.id)
            self._save_to_json(response.json(), "whoami.json")
        except requests.exceptions.RequestException as e:
            print("Error retrieving Whoami information:", e)
            exit()

    def get_endpoints(self):
        if not self.access_token or not self.data_region or not self.id:
            print("Access token or Whoami information not available.")
            return
        url_endpoint = f"{self.data_region}/endpoint/v1/endpoints"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            f"X-{self.id_type}-ID": self.id
        }
        params = {"pageFromKey": "1"}
        try:
            response = requests.get(url_endpoint, headers=headers, params=params)
            print(response.status_code, response.json())
            self._save_to_json(response.json(), "endpoints.json")
        except requests.exceptions.RequestException as e:
            print("Error retrieving Endpoints:", e)
            exit()

if __name__ == "__main__":
    client_id = ""
    client_secret = ""

    sophos_api = SophosAPI(client_id, client_secret)
    sophos_api.get_access_token()
    sophos_api.get_whoami_info()
    sophos_api.get_endpoints()

