'''
This class uses for getting and store data from the Kusama Governance API https://www.kusamagovernance.com/
'''

import requests
import json

class KusamaGovernance:
    url = "https://www.kusamagovernance.com"
    account_dict = {}

    def __init__(self):
        pass


    def getAccountData(self, account_id):
        url = self.url + "/_dash-update-component"
        payload = json.dumps({
            "output": "..specific-account-data.data...delegation-data.data...account_input_warning.children..",
            "outputs": [
                {
                "id": "specific-account-data",
                "property": "data"
                },
                {
                "id": "delegation-data",
                "property": "data"
                },
                {
                "id": "account_input_warning",
                "property": "children"
                }
            ],
            "inputs": [
                {
                "id": "account_input",
                "property": "value",
                "value": account_id
                }
            ],
            "changedPropIds": [
                "account_input.value"
            ]
            })
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://www.kusamagovernance.com',
            'Referer': 'https://www.kusamagovernance.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'X-CSRFToken': 'undefined',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
            }
        self.account_dict[account_id] = json.loads(self.__send_request(url, "POST", payload, headers))
        return self.account_dict


    def __send_request(self, url, method, payload, headers):
        response = requests.request(method, url, headers=headers, data=payload)
        return response.text