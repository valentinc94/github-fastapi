import requests


class UnableToGetUserData(Exception):
    pass


class UnableToUpdateUserData(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class GithubAPI:
    def __init__(self, token: str):
        self.api_url = "https://api.github.com"
        self.headers = {"Authorization": f"Bearer {token}"}

    def get_user_data(self) -> dict:
        url = f"{self.api_url}/user"
        response = requests.get(
            url,
            headers=self.headers,
        )
        if response.status_code == 401:
            raise InvalidCredentials()

        if response.status_code != 200:
            raise UnableToGetUserData(response.text)

        return response.json()

    def edit_user_data(self, data) -> dict:
        response = requests.patch(
            url=f"{self.api_url}/user",
            json=data,
            headers=self.headers,
        )

        if response.status_code == 401:
            raise InvalidCredentials(response.text)

        if response.status_code != 200:
            raise UnableToUpdateUserData(response.text)

        return response.json()
