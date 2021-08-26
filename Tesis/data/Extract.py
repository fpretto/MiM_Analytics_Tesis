import pandas as pd
import requests  # this package is used for fetching data from API
import json


class Extract:

    def __init__(self, data_config):
        # loading our json file here to use it across different class methods
        self.data_sources = data_config
        self.api_football = self.data_sources['data_sources']['api']['api-football']
        self.csv_path = self.data_sources['data_sources']['csv']
        self.dict_countries = {'AR': 'Argentina', 'BO': 'Bolivia', 'BR': 'Brazil', 'CL': 'Chile', 'CO': 'Colombia',
                               'EC': 'Ecuador', 'PY': 'Paraguay', 'PE': 'Peru', 'UY': 'Uruguay', 'VE': 'Venezuela',
                               'MX': 'Mexico', 'ES': 'Spain', 'FR': 'France', 'IT': 'Italy', 'BE': 'Belgium',
                               'NL': 'Netherlands', 'GB': 'England', 'DE': 'Germany', 'PT': 'Portugal'}

    def getCSVData(self, csv_name, separator):
        # since we can use multiple CSV data files in future,
        # so will pass csv name as an argument to fetch the desired CSV data.
        df = pd.read_csv(self.csv_path["path"] + self.csv_path[csv_name], encoding="latin-1", sep=separator)
        return df

    def getAPIFootballData(self, endpoint, query=None):
        # since we have multiple API's (Pollution and Economy Data),
        # so we can get apt API link by passing in its name in function argument.

        if query == None:
            api_url = 'https://' + self.api_football['host'] + self.api_football['endpoints'][endpoint]
        else:
            api_url = 'https://' + self.api_football['host'] + self.api_football['endpoints'][endpoint] + query

        payload = {}
        headers = {'x-rapidapi-key': self.api_football['key'],
                   'x-rapidapi-host': self.api_football['host']
                   }

        response = requests.request("GET", api_url, headers=headers, data=payload).json()

        if len(response['errors']) > 1:
            raise Exception(f'El request {api_url} ha generado los siguientes errores: {response["errors"]}')
        else:
            return response

