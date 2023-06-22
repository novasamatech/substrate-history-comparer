import requests
import json
import math

from requests.models import requote_uri


class SubscanData:
    address = ""
    url_extrinsics = ""
    url_transfers = ""
    url_rewards = ""
    data = []

    def __init__(self, address=None, url_extrinsics=None, url_transfers=None, url_rewards=None, referenda_url=None) -> None:
        self.address = address
        self.url_extrinsics = url_extrinsics
        self.url_transfers = url_transfers
        self.url_rewards = url_rewards
        self.referenda_url = referenda_url

    def getAllData(self) -> None:
        self.getExtrinsics()
        self.getRewards()
        self.getTransactions()

    def getExtrinsics(self):
        payload = {"address": self.address}
        data = self.__request_processor(self.url_extrinsics, payload)
        self.data.append(data)
        return data

    def getTransactions(self):
        payload = {"address": self.address}
        data = self.__request_processor(self.url_transfers, payload)
        self.data.append(data)
        return data

    def getRewards(self):
        total_rewards = []
        payload = {"address": self.address}
        data = self.__request_processor(self.url_rewards, payload)
        for request in data:
            total_rewards = total_rewards + request.get('data').get('list')
        return total_rewards

    def type_of_subscan_operation_picker(self, element):
        try:
            return_data = element['data']['extrinsics']
        except:
            print('It is not extrinsics')
        try:
            return_data = element['data']['list']
        except:
            print('It is not list')
        try:
            return_data = element['data']['transfers']
        except:
            print('It is not transfer')
        return return_data

    def store_all_operation_in_one_list(self):
        returned_data = []
        for blocks_of_data in self.data:
            for block_of_data in blocks_of_data:
                data = self.type_of_subscan_operation_picker(block_of_data)
                if (data):
                    for data_elemet in data:
                        returned_data.append(data_elemet)
        return returned_data

    def get_referenda_list(self):
        referenda_list = []

        def merge_all_referenda(completed, active):
            return_array = []
            referendums = completed + active
            for referenda in referendums:
                return_array += referenda['data']['list']

            return return_array

        payload = {"status":"active","origin":"all"}
        active_referena = self.__request_processor(self.referenda_url, payload)
        payload['status'] = "completed"
        completed_referenda = self.__request_processor(self.referenda_url, payload)
        referenda_list = merge_all_referenda(active_referena, completed_referenda)
        referenda_dict = {}
        for referenda in referenda_list:
            referenda_dict[referenda['referendum_index']] = referenda

        self.all_referenda = referenda_dict

        return self.all_referenda

    def get_all_votes(self, referenda_dict: dict):
        total_votes = []

        for referenda_id, referenda in referenda_dict.items():
            votes = self.get_votes_for_referenda(referenda_id)
            total_votes += votes
            print(f"Referend {referenda_id} processed!")

        return total_votes

    def get_votes_for_referenda(self, referenda_id):
        referenda_votes = []
        payload = {"referendum_index": referenda_id}
        vote_list = self.__request_processor('https://kusama.webapi.subscan.io/api/scan/referenda/votes', payload)

        for votes in vote_list:
            referenda_votes += votes['data']['list']

        final_votes = self.__remove_recurring_votes(referenda_votes)

        self.all_referenda[referenda_id]['votes'] = final_votes

        return final_votes

    def __remove_recurring_votes(self, voters_list):
        account_dict = {}
        for voter in voters_list:
            account = voter['account']['address']
            voting_time = voter['voting_time']
            if account in account_dict:
                if voting_time > account_dict[account]['max_voting_time']:
                    account_dict[account]['max_voting_time'] = voting_time
            else:
                account_dict[account] = {'max_voting_time': voting_time, **voter}
        return list(account_dict.values())



    def __send_request(self, url, data):
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'd5a1d1cffde69e7cbff6d9c0cf1cca6d',
            'baggage': 'sentry-public_key=da3d374c00b64b6196b5d5861d4d1374,sentry-trace_id=fb6a06eb7a3c4ada9263c2451eadfba2,sentry-sample_rate=0.01',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        return requests.request("POST", url, headers=headers,
                                json=data)

    def __request_processor(self, url, payload):
        return_data = []
        first_response = self.__send_request(
            url, self.__payload_update(payload, 0)).json()
        count = int(first_response.get("data").get("count"))
        request_count = math.ceil(count/100)
        if count <= 100:
            return_data.append(first_response)
        else:
            for i in range(request_count):
                response = self.__send_request(
                    url, self.__payload_update(payload, i)).json()
                return_data.append(response)
        return return_data

    def __payload_update(self, payload, n) -> str:
        payload['page'] = n
        payload['row'] = 100
        return payload
