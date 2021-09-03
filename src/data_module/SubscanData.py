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

    def __init__(self, address, url_extrinsics, url_transfers, url_rewards) -> None:
        self.address = address
        self.url_extrinsics = url_extrinsics
        self.url_transfers = url_transfers
        self.url_rewards = url_rewards

    def getAllData(self) -> None:
        self.getExtrinsics()
        self.getRewards()
        self.getTransactions()

    def getExtrinsics(self):
        data = self.__request_processor(self.url_extrinsics)
        self.data.append(data)
        return data

    def getTransactions(self):
        data = self.__request_processor(self.url_transfers)
        self.data.append(data)
        return data

    def getRewards(self):
        data = self.__request_processor(self.url_rewards)
        self.data.append(data)
        return data

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

    def store_all_operation_in_one_list(this):
        returned_data = []
        for blocks_of_data in this.data:
            for block_of_data in blocks_of_data:
                data = this.type_of_subscan_operation_picker(block_of_data)
                if (data):
                    for data_elemet in data:
                        returned_data.append(data_elemet)
        return returned_data

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
