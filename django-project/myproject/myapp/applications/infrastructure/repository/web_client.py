import logging
import time

import requests


class WebClient:
    @staticmethod
    def make_api_request(api_url, params):
        time.sleep(0.3)
        try:
            # URLとパラメータをデバッグレベルのログに出力
            logging.debug("Request URL: %s", api_url)
            logging.debug("Request Parameters: %s", params)
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error("Error: %d", response.status_code)
                return None
        except Exception as e:
            logging.error("Error: %s", str(e))
            return None
