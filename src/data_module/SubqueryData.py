import requests
import json
from .fixture import historyElements_by_address, historyElement_by_id, referenda_by_id, referenda_all_account_votes


class SubqueryData:
    url = ""
    address = ""
    history_elements = []
    referenda_dict = {}
    account_votes_dictionary = {}

    def __init__(self, url, address=None):
        self.url = url
        self.address = address

    def getHistoryList(self):
        query = json.dumps(historyElements_by_address(self.address))
        data = self.__send_request(self.url, query)
        return json.loads(data.text)

    def getHistoryElement(self, id):
        query = json.dumps(historyElement_by_id(id))
        data = self.__send_request(self.url, query)
        return data.text

    def fetchHistory(self):
        history_list = self.getHistoryList()
        for element in history_list['data']['historyElements']['edges']:
            data = element['node']
            self.history_elements.append(data)

    def getReferendaList(self, referenda_id_array):
        for referenda_id in referenda_id_array:
            print(f"Getting referenda data for {referenda_id}...")
            self.referenda_dict[referenda_id] = self.getReferendaById(referenda_id)

        return self.referenda_dict

    def getReferendaById(self, referenda_id):
        query = json.dumps(referenda_by_id(referenda_id))
        data = self.__send_request(self.url, query)
        return json.loads(data.text)

    def getReferendaVotesForAddress(self, account_id):
        query = json.dumps(referenda_all_account_votes(account_id))
        data = self.__send_request(self.url, query)
        self.account_votes_dictionary[account_id] = json.loads(data.text)

        return json.loads(data.text)

    def __send_request(self, url, data):
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'd5a1d1cffde69e7cbff6d9c0cf1cca6d'
        }
        return requests.request("POST", url, headers=headers,
                                data=data)
