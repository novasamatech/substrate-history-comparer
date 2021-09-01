import requests
import json


class Networks:
    polka = ["polkadot", 10]
    kusama = ["kusama", 12]
    westend = ['westend', 12]


address = "13mAjFVjFDpfa42k2dLdSnUyrSzK8vAySsoudnxX2EKVtfaq"
current_network = Networks.polka
url = "https://api.subquery.network/sq/ef1rspb/fearless-wallet"
headers = {'Content-Type': 'application/json'}
with open('./history_query.json') as f:
  history_elements_query = json.load(f)


data = json.dumps(history_elements_query)

subquery_req = requests.request("POST", url, headers=headers,
                                    data=data)
history = json.loads(subquery_req.text)

subscan_url = "https://{}.api.subscan.io/api/scan/extrinsics".format(current_network[0])
subscan_data = '{"address": "%s","row": 100,"page": 0}' % (address)
subscan_req = requests.request("POST", subscan_url, headers=headers,
                                    data=subscan_data)

result = subscan_req.json()
print(result)