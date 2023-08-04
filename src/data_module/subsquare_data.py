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
        url = self.url + "/_next/data/Z6YaslKNwq0jhoSKCqoEZ/referenda.json"
        page_counter=0
        page_size = 0
        total_items = 0
        while page_size * page_counter <= total_items:
            page_counter+=1
            response = self.__send_request(url+f"?page={page_counter}", "GET", None, None)
            total_items = response['pageProps']['posts']['total']
            page_size = response['pageProps']['posts']['pageSize']
            for referenda in response['pageProps']['posts']['items']:
                self.referenda_dict[referenda['referendumIndex']] = referenda
        return self.referenda_dict

    def getReferendaVoters(self, referenda_id):
        url = self.url + "/api/gov2/referendums/" + str(referenda_id)
        self.referenda_dict[referenda_id]['voters'] = self.__send_request(url, "GET", None, None)
        return self.referenda_dict

    def __send_request(self, url, method, payload, headers):
        response = requests.request(method, url, headers=headers, data=payload).json()
        return response