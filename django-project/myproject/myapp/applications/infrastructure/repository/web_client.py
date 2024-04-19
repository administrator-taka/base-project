import time
import requests


class WebClient:
    @staticmethod
    def make_api_request(api_url, params):
        time.sleep(0.3)
        try:
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print("Error:", response.status_code)
                return None
        except Exception as e:
            print("Error:", str(e))
            return None
