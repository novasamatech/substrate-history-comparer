'''
This module is responsible for getting data from the subsquare API
'''
import requests


class SubSquare:
    url = ""
    referenda_dict = {}

    def __init__(self, url):
        self.url = url

    def getReferendaList(self):
        url = self.url + "/_next/data/N8PtzlmYhHyOlEeMGBTTM/referenda.json?page=0"
        response = self.__send_request(url, "GET", None, None)
        for referenda in response.json()['pageProps']['posts']['items']:
            self.referenda_dict[referenda['referendumIndex']] = referenda
        return self.referenda_dict

    def getReferendaVoters(self, referenda_id):
        url = self.url + "/api/gov2/referendums/" + str(referenda_id) + "/vote-extrinsics"
        self.referenda_dict[referenda_id]['voters'] = self.__send_request(url, "GET", None, None).json()
        return self.referenda_dict

    def __send_request(self, url, method, payload, headers):
        response = requests.request(method, url, headers=headers, data=payload)
        return response