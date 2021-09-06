import json
import math

import requests


class SubscanData:

    def __init__(self, address, url_extrinsics, url_transfers, url_rewards) -> None:
        self.address = address
        self.url_extrinsics = url_extrinsics
        self.url_transfers = url_transfers
        self.url_rewards = url_rewards
        self.data = []
        self.transfer_count = int()
        self.extrinsic_count = int()
        self.reward_count = int()
        self.none_elements = int()

    def getAllData(self) -> None:
        self.getExtrinsics()
        self.getRewards()
        self.getTransfers()

    def getExtrinsics(self):
        data = self.__request_processor(self.url_extrinsics)
        self.data.append(data)
        for element in data:
            try:
                self.extrinsic_count = len(
                    self.type_of_subscan_operation_picker(element))
            except:
                pass
        return data

    def getTransfers(self):
        data = self.__request_processor(self.url_transfers)
        self.data.append(data)
        for element in data:
            try:
                self.transfer_count = len(
                    self.type_of_subscan_operation_picker(element))
            except:
                pass
        return data

    def getRewards(self):
        data = self.__request_processor(self.url_rewards)
        self.data.append(data)
        for element in data:
            try:
                self.reward_count = len(
                    self.type_of_subscan_operation_picker(element))
            except:
                pass
        return data

    def type_of_subscan_operation_picker(self, element):
        return_data = []
        try:
            return_data = element['data']['extrinsics']
        except:
            pass
        try:
            return_data = element['data']['list']
        except:
            pass
        try:
            return_data = element['data']['transfers']
        except:
            pass
        return return_data

    def store_all_operation_in_one_list(this):
        returned_data = []
        for blocks_of_data in this.data:
            for block_of_data in blocks_of_data:
                data = this.type_of_subscan_operation_picker(block_of_data)
                if (data):
                    for data_elemet in data:
                        returned_data.append(data_elemet)
        return returned_data

    def calculate_rewards(self):
        self.rewards_amount = float()
        for rewards in self.data[1]:
            try:
                for reward in rewards['data']['list']:
                    if reward['event_id'] == 'Reward':
                        self.rewards_amount += float(reward['amount'])
                    elif reward['event_id'] == 'Slash':
                        self.rewards_amount -= float(reward['amount'])
            except:
                return 0
        return self.rewards_amount

    def __send_request(self, url, data):
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'd5a1d1cffde69e7cbff6d9c0cf1cca6d'
        }
        return requests.request("POST", url, headers=headers,
                                data=data)

    def __request_processor(self, url):
        return_data = []
        first_response = self.__send_request(
            url, self.__payload_creator(self.address, 0)).json()
        count = int(first_response.get("data").get("count"))
        request_count = math.ceil(count/100)
        if count <= 100:
            return_data.append(first_response)
        else:
            for i in range(request_count):
                response = self.__send_request(
                    url, self.__payload_creator(self.address, i)).json()
                return_data.append(response)
        return return_data

    def __payload_creator(self, address, n) -> str:
        return json.dumps({
            "address": address,
            "row": 100,
            "page": n
        })
