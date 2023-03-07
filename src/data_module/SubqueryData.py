from collections import defaultdict
import requests
import json
import time

from .fixture import historyElements_by_address, historyElement_by_id, referenda_by_id, referenda_all_account_votes, small_data_referenda_by_id


class SubqueryData:
    url = ""
    address = ""
    history_elements = []
    referenda_dict = {}
    account_votes_dictionary = {}
    voter_dict = defaultdict(list)

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

    def fetch_referenda_data(self, referenda_id_array):
        self.getReferendaList(referenda_id_array)
        for referenda_id, referendum in self.referenda_dict.items():
            for voter in referendum['data']['castingVotings']['nodes']:
                self.voter_dict[voter['voter']].append(voter)

        return self.voter_dict

    def getReferendaList(self, referenda_id_array):
        for referenda_id in referenda_id_array:
            print(f"Getting referenda data for {referenda_id}...")
            self.referenda_dict[referenda_id] = self.getReferendaById(referenda_id)

        return self.referenda_dict

    def getReferendaById(self, referenda_id):
        # query = json.dumps(referenda_by_id(referenda_id))
        query = json.dumps(small_data_referenda_by_id(referenda_id))
        data = self.__send_request(self.url, query)
        return data

    def getReferendaVotesForAddress(self, account_id):
        query = json.dumps(referenda_all_account_votes(account_id))
        data = self.__send_request(self.url, query)
        self.account_votes_dictionary[account_id] = data

        return data

    def __send_request(self, url, data):
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'd5a1d1cffde69e7cbff6d9c0cf1cca6d'
        }
        response = requests.request("POST", url, headers=headers, data=data)
        response_data = json.loads(response.text)

        # Workaround to cover case when SubQuery return an "Unexpected error"
        if 'message' in response_data:
            time.sleep(5)
            return self.__send_request(url, data)

        return response_data
