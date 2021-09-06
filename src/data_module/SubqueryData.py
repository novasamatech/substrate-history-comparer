import json
import requests

from .fixture import historyElement_by_id, historyElements_by_address, get_rewards


class SubqueryData:

    def __init__(self, url, address):
        self.address = address
        self.url = url
        self.history_elements = []

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

    def calculate_rewards(self, new_request=None):
        total_rewards = float()
        if (new_request):
            query = json.dumps(get_rewards(self.address))
            data = self.__send_request(self.url, query)
            iteration_data = json.loads(data.text)
            for element in iteration_data['data']['historyElements']['nodes']:
                total_rewards += float(element['reward']['amount'])
        else:
            for element in self.history_elements:
                try:
                    reward_amount = float(element['reward']['amount'])
                    if (element['reward']['isReward']):
                        total_rewards += reward_amount
                    else:
                        total_rewards -= reward_amount
                except:
                    continue
        return total_rewards

    def __send_request(self, url, data):
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'd5a1d1cffde69e7cbff6d9c0cf1cca6d'
        }
        return requests.request("POST", url, headers=headers,
                                data=data)
