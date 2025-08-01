import requests
from http import HTTPStatus
from config.spacex_api import URL_BASE


class SpacexRequest:

    def __init__(self, base: str = URL_BASE):
        self.__base = base
    
    def get_launches(self) -> list[dict]:
        url = f"{self.__base}/launches"
        data = []

        try:
            response = requests.get(url)

            if (response.status_code == HTTPStatus.OK):
                data = response.json()

        except:
            print("Error obtaining launches")
        
        return data
